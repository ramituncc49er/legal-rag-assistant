"""
data_pipeline.py

Orchestrate the end-to-end table build: load SCDB CSVs and CL/other sources, standardize column names, write cleaned Parquet tables.
"""

import os
from typing import Optional, Dict, Any
import pandas as pd
import duckdb
import pyarrow as pa
import pyarrow.parquet as pq  

from ingest import IngestConfig, ColdCasesHFIngestor, SCDBCaseCiteIngestor, SCDBIssueProvisionIngestor, SCDBJusticeCiteIngestor                 

TMPDIR = os.getenv("TMPDIR")
if TMPDIR:
    os.environ.setdefault("HF_HOME", os.path.join(TMPDIR, "hf"))
    os.environ.setdefault("HF_DATASETS_CACHE", os.path.join(TMPDIR, "hf", "datasets"))
    os.environ.setdefault("HF_HUB_CACHE", os.path.join(TMPDIR, "hf", "hub"))
    os.makedirs(os.environ["HF_DATASETS_CACHE"], exist_ok=True)
    os.makedirs(os.environ["HF_HUB_CACHE"], exist_ok=True)

def _read_scdb_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, dtype=str, low_memory=False)
    df = df.rename(columns=lambda c: c.strip().replace(" ", ""))
    return df

def _ensure_cols(df: pd.DataFrame, cols):
    for c in cols:
        if c not in df.columns:
            df[c] = pd.Series([None] * len(df))
    return df

def _to_parquet(df: pd.DataFrame, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_parquet(path, index=False)

def build_legal_tables(
    cfg: IngestConfig,
    scdb_case_cite_path: str,
    scdb_case_issue_path: str,
    scdb_justice_path: str,
    out_dir: Optional[str] = "tables",
    persist: bool = True,
) -> Dict[str, pd.DataFrame]:
    os.makedirs(out_dir, exist_ok=True)

    # ================== CourtListener → Parquet (stream/batched) ==================
    cl_parquet = os.path.join(out_dir, "cl_cases.parquet")
    cl_ing = ColdCasesHFIngestor(cfg)

    select_cols = ["cl_cluster_id","case_name","date_filed","us_cite","sct_cite","led_cite","lexis_cite","cl_url","opinions"]
    stats = cl_ing.run_to_parquet(cl_parquet, select_cols=select_cols, opinion_sink=None)
    print(stats)

    # ================== DuckDB joins (out-of-core, RAM friendly) ==================
    con = duckdb.connect()
    con.execute(f"CREATE TABLE cl AS SELECT * FROM '{cl_parquet}';")

    # Normalizing strings for both CL and SCDB to force harmonization. 'r"""..."""' is used to indicated regex execution
    con.execute(r"""
    CREATE OR REPLACE MACRO canon(s) AS
        LOWER(
          REGEXP_REPLACE(
            REGEXP_REPLACE(NULLIF(TRIM(s), ''), '\\s+', ' '),
            '\\.', ''
          )
        );
    """)

    # Load SCDB Case-Cite CSV with just needed columns
    scdb_case_cite_cols = ["usCite","sctCite","ledCite","lexisCite","term","decisionDirection","decisionType","majVotes","minVotes","majOpinWriter","majOpinAssigner"]
    con.execute(f"""
    CREATE TABLE scdb_case_cite AS
    SELECT {", ".join(scdb_case_cite_cols)}
    FROM read_csv_auto('{scdb_case_cite_path}', SAMPLE_SIZE=-1, IGNORE_ERRORS=TRUE);
    """)

    con.execute("""ALTER TABLE cl ADD COLUMN join_key_lexis TEXT;""")
    con.execute("""UPDATE cl SET join_key_lexis = canon(lexis_cite);""")

    con.execute("""ALTER TABLE scdb_case_cite ADD COLUMN join_key_lexis TEXT;""")
    con.execute("""UPDATE scdb_case_cite SET join_key_lexis = canon(lexisCite);""")

    # ================== CASES_MASTER ==================
    con.execute("""
    CREATE TABLE cases_master AS
    SELECT
        ROW_NUMBER() OVER () AS case_id,
        cl.cl_cluster_id,
        cl.case_name,
        cl.date_filed,
        cl.us_cite,
        cl.sct_cite,
        cl.led_cite,
        cl.lexis_cite,
        cl.cl_url,
        cl.join_key_lexis,                 -- (UPDATED) carry LEXIS key for downstream joins
        s.term,
        s.decisionDirection,
        s.decisionType,
        s.majVotes,
        s.minVotes,
        s.majOpinWriter,
        s.majOpinAssigner
    FROM cl AS cl
    JOIN scdb_case_cite AS s                -- (UPDATED) INNER JOIN
      ON cl.join_key_lexis IS NOT NULL
     AND cl.join_key_lexis = s.join_key_lexis;
    """)

    cases_master_parquet = os.path.join(out_dir, "cases_master.parquet")
    con.execute(f"COPY cases_master TO '{cases_master_parquet}' (FORMAT PARQUET);")

    # ================== OPINIONS (for matched cases only) ==================
    con.execute("""  -- (UPDATED)
    CREATE TABLE cl_matched AS
    SELECT cl.*
    FROM cl
    JOIN cases_master cm ON cl.cl_cluster_id = cm.cl_cluster_id;
    """)

    con.execute("""  -- (UPDATED)
    CREATE TABLE opinions AS
    SELECT
        cm.case_id,
        cm.cl_cluster_id,
        -- explode the list of opinions; to_json() keeps the full payload even if schema varies
        to_json(opinion) AS opinion_json
    FROM cl_matched c
    JOIN cases_master cm USING (cl_cluster_id)
    , UNNEST(c.opinions) AS opinion;
    """)

    opin_parquet = os.path.join(out_dir, "opinions.parquet")
    con.execute(f"COPY opinions TO '{opin_parquet}' (FORMAT PARQUET);")

    # ================== ISSUES ==================
    scdb_case_issue_cols = ["usCite","sctCite","ledCite","lexisCite","issue","issueArea","lawType","lawSupp","lawMinor","authorityDecision1","authorityDecision2"]
    con.execute(f"""
    CREATE TABLE scdb_case_issue AS
    SELECT {", ".join(scdb_case_issue_cols)}
    FROM read_csv_auto('{scdb_case_issue_path}', SAMPLE_SIZE=-1, IGNORE_ERRORS=TRUE);
    """)
    con.execute("""ALTER TABLE scdb_case_issue ADD COLUMN join_key_lexis TEXT;""")
    con.execute("""UPDATE scdb_case_issue SET join_key_lexis = canon(lexisCite);""")

    con.execute("""  -- (UPDATED)
    CREATE TABLE issues AS
    SELECT
        cm.case_id,
        cm.cl_cluster_id,
        cm.join_key_lexis,
        i.usCite,
        i.sctCite,
        i.ledCite,
        i.lexisCite,
        i.issue,
        i.issueArea,
        i.lawType,
        i.lawSupp,
        i.lawMinor,
        i.authorityDecision1,
        i.authorityDecision2
    FROM cases_master AS cm
    LEFT JOIN scdb_case_issue AS i
      ON cm.join_key_lexis = i.join_key_lexis;
    """)

    issues_parquet = os.path.join(out_dir, "issues.parquet")
    con.execute(f"COPY issues TO '{issues_parquet}' (FORMAT PARQUET);")

    # ================== VOTES ==================
    scdb_justice_cols = ["usCite","sctCite","ledCite","lexisCite","justiceName","vote","direction","majority"]
    con.execute(f"""
    CREATE TABLE scdb_justice AS
    SELECT {", ".join(scdb_justice_cols)} 
    FROM read_csv_auto('{scdb_justice_path}', SAMPLE_SIZE=-1, IGNORE_ERRORS=TRUE);
    """)

    con.execute("""ALTER TABLE scdb_justice ADD COLUMN join_key_lexis TEXT;""")
    con.execute("""UPDATE scdb_justice SET join_key_lexis = canon(lexisCite);""")

    con.execute("""  -- (UPDATED)
    CREATE TABLE votes AS
    SELECT
        cm.case_id,
        cm.cl_cluster_id,
        cm.join_key_lexis,
        j.usCite,
        j.sctCite,
        j.ledCite,
        j.lexisCite,
        j.justiceName,
        j.vote,
        j.direction,
        j.majority
    FROM cases_master AS cm
    LEFT JOIN scdb_justice AS j
      ON cm.join_key_lexis = j.join_key_lexis;
    """)

    votes_parquet = os.path.join(out_dir, "votes.parquet")
    con.execute(f"COPY votes TO '{votes_parquet}' (FORMAT PARQUET);")

    con.close()

    # ================== (Optional) opinions ← join case_id by cl_cluster_id ==================
    cases_master = pd.read_parquet(cases_master_parquet)
    issues = pd.read_parquet(issues_parquet)
    votes = pd.read_parquet(votes_parquet)
    opinions = pd.read_parquet(opin_parquet)

    if persist:
        pass

    return {
        "cases_master": cases_master,
        "opinions": opinions,
        "issues": issues,
        "votes": votes,
    }

if __name__ == "__main__":
    cfg = IngestConfig(
        out_dir="./ingest",
        limit=None,
        streaming=True,
        chunk_size=50_000,
    )

    tables = build_legal_tables(
        cfg,
        scdb_case_cite_path="./SCDB_2025_01_caseCentered_Citation.csv",
        scdb_case_issue_path="./SCDB_2025_01_caseCentered_LegalProvision.csv",
        scdb_justice_path="./SCDB_2025_01_justiceCentered_Citation.csv",
        out_dir="tables",
        persist=True,
    )

    for k, v in tables.items():
        print(k, getattr(v, "shape", getattr(v, "__len__", lambda: "?")()))
