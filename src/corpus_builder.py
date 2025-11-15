"""
corpus_builder.py

Build a one-opinion-per-document corpus (documents.parquet) from:
  - cases_master.parquet      (case metadata)
  - opinions.parquet          (contains `opinion_json` with {"unnest": {...}})
  - issues.parquet            (SCDB per-case; may have multiple rows per case)
  - votes.parquet             (per-justice rows)

Output columns (flat):
chunk_id, doc_id, opinion_id, case_id, cl_cluster_id, cl_url, case_name, date_filed, us_cite, sct_cite, led_cite, lexis_cite, type, opinion_text, term, decisionDirection, decisionType, majVotes, minVotes, majOpinWriter, majOpinAssigner, issue, issueArea, lawType, lawSupp, lawMinor, issues_json, votes_json
"""

import argparse
import json
import logging
import re
from typing import Any, Dict, List, Optional

import pandas as pd

# ================== CLI defaults ==================

DEF_CASES = "tables/cases_master.parquet"
DEF_OPIN  = "tables/opinions.parquet"
DEF_ISS   = "tables/issues.parquet"
DEF_VOTE  = "tables/votes.parquet"
DEF_OUT   = "tables/documents.parquet"


# ================== Utils ==================

def _coerce_num(x):
    """Coerce stringy numerics to numeric; leave NaN on failure."""
    if isinstance(x, str):
        x = x.strip()
    return pd.to_numeric(x, errors="coerce")

def _json(obj: Any) -> str:
    """Compact, stable JSON serialization."""
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"), sort_keys=False)

def _prefer_text(rec: Dict[str, Any]) -> str:
    """Pick best available text field; lightly strip HTML if needed."""
    for k in ("plain_text", "text", "opinion_text", "extracted_text"):
        v = rec.get(k)
        if isinstance(v, str) and v.strip():
            return v
    html = rec.get("html")
    if isinstance(html, str) and html.strip():
        return re.sub(r"<[^>]+>", " ", html)
    return ""


# ================== dataloaders/normalizers ==================

def load_cases(path: str) -> pd.DataFrame:
    """
    Load cases_master as-is, ensuring key dtypes and required columns exist.
    Expected columns:
      case_id, cl_cluster_id, cl_url, case_name, date_filed,
      us_cite, sct_cite, led_cite, lexis_cite,
      term, decisionDirection, decisionType,
      majVotes, minVotes, majOpinWriter, majOpinAssigner
    """
    df = pd.read_parquet(path).copy()
    # Keys normalized
    df["case_id"] = df["case_id"].apply(_coerce_num)
    df["cl_cluster_id"] = df["cl_cluster_id"].apply(_coerce_num)

    required = [
        "case_id", "cl_cluster_id", "cl_url", "case_name", "date_filed",
        "us_cite", "sct_cite", "led_cite", "lexis_cite",
        "term", "decisionDirection", "decisionType",
        "majVotes", "minVotes", "majOpinWriter", "majOpinAssigner",
    ]
    for c in required:
        if c not in df.columns:
            df[c] = None
    df = df[required]
    logging.info("cases_master: %d rows | sample: %s", len(df), df.head(1).to_dict("records"))
    return df


def explode_opinions(path: str) -> pd.DataFrame:
    """
    Explode opinions.opinion_json (with {"unnest": {...}}) to one row per opinion.
    Output columns: opinion_id, case_id, type, opinion_text, cl_cluster_id
    """
    op = pd.read_parquet(path).copy()
    op["case_id"] = op["case_id"].apply(_coerce_num)
    op["cl_cluster_id"] = op["cl_cluster_id"].apply(_coerce_num)

    def to_list(payload):
        if payload is None:
            return []
        if isinstance(payload, str):
            try:
                payload = json.loads(payload)
            except Exception:
                return []
        if isinstance(payload, dict) and "unnest" in payload:
            payload = payload["unnest"]
        if isinstance(payload, dict):
            return [payload]
        if isinstance(payload, list):
            return payload
        return []

    rows: List[Dict[str, Any]] = []
    for _, r in op.iterrows():
        base = {"case_id": r["case_id"], "cl_cluster_id": r["cl_cluster_id"]}
        items = to_list(r.get("opinion_json"))
        for rec in items:
            rows.append({
                **base,
                "opinion_id":   rec.get("opinion_id") or rec.get("id"),
                "type":         rec.get("type") or rec.get("opinion_type") or rec.get("type_id"),
                "opinion_text": _prefer_text(rec),
                "author_id":    rec.get("author_id"),
                "author_str":   rec.get("author_str"),
            })

    out = pd.DataFrame.from_records(rows)
    out = out.loc[out["opinion_id"].notna() & out["opinion_text"].astype(str).str.len().gt(0)].copy()
    out["opinion_id"] = pd.to_numeric(out["opinion_id"], errors="ignore")
    out["case_id"] = out["case_id"].apply(_coerce_num)
    out["cl_cluster_id"] = out["cl_cluster_id"].apply(_coerce_num)

    out = out[["opinion_id", "case_id", "opinion_text", "type", "cl_cluster_id"]]
    logging.info("opinions exploded: %d opinions | sample: %s", len(out), out.head(1).to_dict("records"))
    return out


def aggregate_issues(path: Optional[str]) -> pd.DataFrame:
    """
    Aggregate issues to one row per case.
    Input columns: case_id, issue, issueArea, lawType, lawSupp, lawMinor
    Output: case_id, issue, issueArea, lawType, lawSupp, lawMinor, issues_json
    """
    if not path:
        return pd.DataFrame(columns=["case_id", "issue", "issueArea", "lawType", "lawSupp", "lawMinor", "issues_json"])

    df = pd.read_parquet(path).copy()
    if df.empty:
        return pd.DataFrame(columns=["case_id", "issue", "issueArea", "lawType", "lawSupp", "lawMinor", "issues_json"])

    df["case_id"] = df["case_id"].apply(_coerce_num)
    for c in ("issue", "issueArea", "lawType", "lawSupp", "lawMinor"):
        if c not in df.columns:
            df[c] = None

    df["__rowdict__"] = df[["issue", "issueArea", "lawType", "lawSupp", "lawMinor"]].to_dict(orient="records")
    agg = (
        df.groupby("case_id", dropna=False, as_index=False)
          .agg(issues_json=("__rowdict__", lambda rows: _json(list(rows))))
    )

    prim = (
        df.sort_values(["case_id"])
          .groupby("case_id", as_index=False)
          .first()[["case_id", "issue", "issueArea", "lawType", "lawSupp", "lawMinor"]]
    )

    out = prim.merge(agg, on="case_id", how="left")
    logging.info("issues aggregated: %d rows | sample: %s", len(out), out.head(1).to_dict("records"))
    return out


def aggregate_votes(path: Optional[str]) -> pd.DataFrame:
    """
    Aggregate votes to one row per case with votes_json.
    Input columns: case_id, justiceName, vote, direction, majority
    Output: case_id, votes_json
    """
    if not path:
        return pd.DataFrame(columns=["case_id", "votes_json"])

    df = pd.read_parquet(path).copy()
    if df.empty:
        return pd.DataFrame(columns=["case_id", "votes_json"])

    df["case_id"] = df["case_id"].apply(_coerce_num)
    for c in ("justiceName", "vote", "direction", "majority"):
        if c not in df.columns:
            df[c] = None

    df["__rowdict__"] = df[["justiceName", "vote", "direction", "majority"]].to_dict(orient="records")
    agg = (
        df.groupby("case_id", dropna=False, as_index=False)
          .agg(votes_json=("__rowdict__", lambda rows: _json(list(rows))))
    )

    logging.info("votes aggregated: %d rows | sample: %s", len(agg), agg.head(1).to_dict("records"))
    return agg


# ================== Build helpers ==================

def build(cases: str, opinions: str, issues: Optional[str], votes: Optional[str]) -> pd.DataFrame:
    logging.info("Loading + normalizing...")
    cases_df = load_cases(cases)
    opinions_df = explode_opinions(opinions)
    issues_df = aggregate_issues(issues)
    votes_df  = aggregate_votes(votes)

    logging.info("Joining opinions → cases on case_id with explicit suffixes…")
    docs = opinions_df.merge(cases_df, on="case_id", how="left", suffixes=("_op", "_cm"))

    # Coalesce cl_cluster_id from _op (opinions) and _cm (cases)
    if "cl_cluster_id" not in docs.columns:
        have_op = "cl_cluster_id_op" in docs.columns
        have_cm = "cl_cluster_id_cm" in docs.columns
        if have_op and have_cm:
            docs["cl_cluster_id"] = docs["cl_cluster_id_op"].combine_first(docs["cl_cluster_id_cm"])
            docs.drop(columns=["cl_cluster_id_op", "cl_cluster_id_cm"], inplace=True)
        elif have_op:
            docs.rename(columns={"cl_cluster_id_op": "cl_cluster_id"}, inplace=True)
        elif have_cm:
            docs.rename(columns={"cl_cluster_id_cm": "cl_cluster_id"}, inplace=True)

    # Coverage after main join
    cov = docs["case_name"].notna().mean()
    logging.info("Coverage after case_id join (case_name notna): %.1f%%", 100 * cov)

    # Attach issues & votes on case_id
    logging.info("Joining issues & votes on case_id…")
    docs = docs.merge(issues_df, on="case_id", how="left").merge(votes_df, on="case_id", how="left")

    # IDs / final ordering
    docs["doc_id"] = docs["opinion_id"]
    docs["chunk_id"] = None

    wanted = [
        "chunk_id",
        "doc_id",
        "opinion_id",
        "case_id",
        "cl_cluster_id",
        "cl_url",
        "case_name",
        "date_filed",
        "us_cite",
        "sct_cite",
        "led_cite",
        "lexis_cite",
        "type",
        "opinion_text",
        "term",
        "decisionDirection",
        "decisionType",
        "majVotes",
        "minVotes",
        "majOpinWriter",
        "majOpinAssigner",
        "issue",
        "issueArea",
        "lawType",
        "lawSupp",
        "lawMinor",
        "issues_json",
        "votes_json",
    ]
    for c in wanted:
        if c not in docs.columns:
            docs[c] = None
    docs = docs[wanted]

    final_cov = docs["case_name"].notna().mean()
    logging.info("FINAL: %d documents | case_name coverage: %.1f%%", len(docs), 100 * final_cov)
    logging.info("cl_cluster_id coverage: %.1f%%", 100 * docs["cl_cluster_id"].notna().mean())
    logging.info("Sample row: %s", docs.head(1).to_dict("records"))
    return docs


# ================== CLI ==================

def main():
    ap = argparse.ArgumentParser(description="Build one-opinion-per-document corpus.")
    ap.add_argument("--cases", default=DEF_CASES, help="Path to cases_master.parquet")
    ap.add_argument("--opinions", default=DEF_OPIN, help="Path to opinions.parquet")
    ap.add_argument("--issues", default=DEF_ISS, help="Path to issues.parquet")
    ap.add_argument("--votes", default=DEF_VOTE, help="Path to votes.parquet")
    ap.add_argument("--out", default=DEF_OUT, help="Output path for documents.parquet")
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    docs = build(args.cases, args.opinions, args.issues, args.votes)

    logging.info("Writing %s …", args.out)
    docs.to_parquet(args.out, index=False)
    logging.info("Done.")

if __name__ == "__main__":
    main()