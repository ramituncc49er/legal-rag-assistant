"""
ingest.py
"""

from __future__ import annotations
from typing import Iterable, Dict, Any, Optional
import os
import pathlib, time, json
import pandas as pd
from dataclasses import dataclass
from datasets import load_dataset, DownloadConfig
from itertools import islice
from abc import ABC, abstractmethod

from huggingface_hub import snapshot_download
import pyarrow as pa                         
import pyarrow.parquet as pq

@dataclass
class IngestConfig:
    out_dir: str
    limit: Optional[int] = None  # stop after N raw rows
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    streaming: bool = True
    chunk_size: int = 5000
    tmp_dir: Optional[str] = None
    token: Optional[str] = None

class BaseIngestor(ABC):
    """Abstract ETL skeleton. Concrete classes implement extract() and transform_row()."""

    def __init__(self, cfg: IngestConfig):
        self.cfg = cfg
        self.out = pathlib.Path(cfg.out_dir)
        self.out.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def extract(self) -> Iterable[Dict[str, Any]]:
        """Yield raw records (dicts)."""
        ...

    @abstractmethod
    def transform_row(self, row: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Map a raw record to your canonical schema. Return None to skip."""
        ...

    def validate_row(self, row: Dict[str, Any]) -> bool:
        """Optional shape/type checks."""
        return True

    def persist_batch(self, batch: list[Dict[str, Any]], name: str) -> None:
        """Default: write JSONL; swap with Parquet if you prefer."""
        path = self.out / f"{name}.jsonl"
        with path.open("a", encoding="utf-8") as f:
            for r in batch:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    
    def run_collect(self) -> pd.DataFrame:
        """Extract → transform → validate in memory; return a pandas DataFrame."""
        rows = []
        n_raw = 0
        for n_raw, raw in enumerate(self.extract(), start=1):
            tr = self.transform_row(raw)
            if tr is None:
                continue
            if self.validate_row(tr):
                rows.append(tr)
            if self.cfg.limit and n_raw >= self.cfg.limit:
                break
        return pd.DataFrame(rows)

    def run_to_parquet(
        self,
        out_parquet: str,
        select_cols: Optional[List[str]] = None,
        opinion_sink: Optional[str] = None,  # optional second Parquet for exploded opinions
    ) -> Dict[str, int]:
        """
        Stream records, transform, and write to Parquet in small batches.
        If opinion_sink is provided and transform_row returns an 'opinions' list,
        it writes a flattened opinions parquet alongside (columns: cl_cluster_id + opinion fields).
        """
        os.makedirs(os.path.dirname(out_parquet), exist_ok=True)
        main_writer = None
        opin_writer = None
        main_count = opin_count = 0
        batch: List[Dict[str, Any]] = []
        opin_batch: List[Dict[str, Any]] = []
        n_raw = 0

        def df_to_table(df: pd.DataFrame) -> pa.Table:
            return pa.Table.from_pandas(df, preserve_index=False)

        for n_raw, raw in enumerate(self.extract(), start=1):
            tr = self.transform_row(raw)
            if tr is None or not self.validate_row(tr):
                continue

            # Only remove opinions when we actually have an opinion_sink.
            # Otherwise, KEEP opinions embedded in the main record.
            opinions = None
            if opinion_sink:
                opinions = tr.pop("opinions", None)  # (UPDATED)

            # If select_cols is provided and we are keeping opinions in main,
            # ensure 'opinions' isn't accidentally dropped.
            if select_cols is not None: 
                cols = list(select_cols)
                if not opinion_sink and "opinions" in tr and "opinions" not in cols:
                    cols.append("opinions")
                tr = {k: tr.get(k) for k in cols}

            batch.append(tr)

            # Only build the opinions side-batch if an opinion_sink is requested.
            if opinion_sink and isinstance(opinions, list):
                clid = tr.get("cl_cluster_id")
                for op in opinions:
                    opd = op if isinstance(op, dict) else {}
                    ob = {"cl_cluster_id": clid, **opd}
                    opin_batch.append(ob)

            # flush when batch is big enough
            if len(batch) >= self.cfg.chunk_size:
                df = pd.DataFrame(batch); batch.clear()
                tbl = df_to_table(df)
                if main_writer is None:
                    main_writer = pq.ParquetWriter(out_parquet, tbl.schema)
                main_writer.write_table(tbl)
                main_count += len(df)

            if opinion_sink and len(opin_batch) >= self.cfg.chunk_size:
                odf = pd.DataFrame(opin_batch); opin_batch.clear()
                otbl = df_to_table(odf)
                if opin_writer is None:
                    opin_writer = pq.ParquetWriter(opinion_sink, otbl.schema)
                opin_writer.write_table(otbl)
                opin_count += len(odf)

            if self.cfg.limit and n_raw >= self.cfg.limit:
                break

        # final flush
        if batch:
            df = pd.DataFrame(batch)
            tbl = df_to_table(df)
            if main_writer is None:
                main_writer = pq.ParquetWriter(out_parquet, tbl.schema)
            main_writer.write_table(tbl)
            main_count += len(df)
        if opinion_sink and opin_batch:
            odf = pd.DataFrame(opin_batch)
            otbl = df_to_table(odf)
            if opin_writer is None:
                opin_writer = pq.ParquetWriter(opinion_sink, otbl.schema)
            opin_writer.write_table(otbl)
            opin_count += len(odf)

        if main_writer: main_writer.close()
        if opin_writer: opin_writer.close()
        return {"raw": n_raw, "main_rows": main_count, "opinion_rows": opin_count}

class ColdCasesHFIngestor(BaseIngestor):
    def _ensure_local_repo(self) -> str:
        target = os.path.join(os.environ.get("HF_HOME", os.path.expanduser("~/.cache/hf")), "cold_cases_local")
        os.makedirs(target, exist_ok=True)
        snapshot_download(
            repo_id="harvard-lil/cold-cases",
            repo_type="dataset",
            local_dir=target,
            local_dir_use_symlinks=False,
            ignore_patterns=None,
        )
        return target

    def extract(self) -> Iterable[Dict[str, Any]]:
        local_path = self._ensure_local_repo()
        ds = load_dataset(
            path=local_path,
            split="train",
            streaming=True,
            download_config=DownloadConfig(max_retries=8, use_etag=True)
        )
        for row in ds:
            yield row
               
    def transform_row(self, row: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        
        cl_cluster_id = row.get("id")
        cl_slug = row.get("slug") or ""
        cl_url = f"https://www.courtlistener.com/opinion/{cl_cluster_id}/{cl_slug}"
        
        ## Extract citations                        
        us = sct = led = lexis = None
        for c in (row.get("citations") or []):
            c_str = (c or "").strip()
            if not c_str:
                continue
            c_low = c_str.lower()
            
            if ("u.s." in c_low) and ("s. ct" not in c_low) and ("lexis" not in c_low):  ## Check for '1886 U.S. LEXIS 2006'
                us = us or c_str  ## if citations = ["119 U.S. 407", "120 U.S. 500"], without 'or' we lose the 1st one
            elif "s. ct" in c_low:
                sct = sct or c_str
            elif "l. ed" in c_low:
                led = led or c_str
            elif "lexis" in c_low:
                lexis = lexis or c_str
        
        return {
            "source": "courtlistener_hf",
            "cl_cluster_id": cl_cluster_id,
            "cl_url": cl_url,
            "case_name": row.get("case_name") or row.get("case_name_short"),
            "date_filed": row.get("date_filed"),
            #"court_full_name": row.get("court_full_name"),
            "us_cite": us, 
            "sct_cite": sct, 
            "led_cite": led,
            "lexis_cite": lexis,
            #"docket_numbers": [d.get("number") for d in (row.get("dockets") or []) if d.get("number")],
            "opinions": row.get("opinions") or []
        }
                         
class SCDBCaseCiteIngestor(BaseIngestor):
    def __init__(self, cfg: IngestConfig, csv_path: str, chunksize: int = 100_000):
        super().__init__(cfg)
        self.csv_path = csv_path
        self.chunksize = chunksize

    def extract(self) -> Iterable[Dict[str, Any]]:
        for chunk in pd.read_csv(self.csv_path, dtype=str, chunksize=self.chunksize):
            chunk = chunk.rename(columns=lambda c: c.strip().replace(" ", ""))
            for _, r in chunk.iterrows():
                yield r.to_dict()

    def transform_row(self, r: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return {
            "source": "scdb_merged_case_cite",
            "usCite": r.get("usCite"),
            "sctCite": r.get("sctCite"),
            "ledCite": r.get("ledCite"),
            "lexisCite": r.get("lexisCite"),
            "caseName": r.get("caseName"),
            "term": r.get("term"),
            "decisionDirection": r.get("decisionDirection"),
            "decisionType": r.get("decisionType"),
            "majVotes": r.get("majVotes"),
            "minVotes": r.get("minVotes"),
            "majOpinionWriter": r.get("majOpinionWriter"),
            "majOpinionAssigner": r.get("majOpinionAssigner"),
        }

class SCDBIssueProvisionIngestor(BaseIngestor):
    def __init__(self, cfg: IngestConfig, csv_path: str, chunksize: int = 100_000):
        super().__init__(cfg); self.csv_path = csv_path; self.chunksize = chunksize

    def extract(self) -> Iterable[Dict[str, Any]]:
        for chunk in pd.read_csv(self.csv_path, dtype=str, chunksize=self.chunksize):
            chunk = chunk.rename(columns=lambda c: c.strip().replace(" ", ""))
            for _, r in chunk.iterrows():
                yield r.to_dict()

    def transform_row(self, r: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return {
            "source": "scdb_case_issue",
            "usCite": r.get("usCite"),
            "sctCite": r.get("sctCite"),
            "ledCite": r.get("ledCite"),
            "lexisCite": r.get("lexisCite"),
            "issue": r.get("issue"),
            "issueArea": r.get("issueArea"),
            "lawType": r.get("lawType"),
            "lawSupp": r.get("lawSupp"),
            "lawMinor": r.get("lawMinor"),
            "authorityDecision1": r.get("authorityDecision1"),
            "authorityDecision2": r.get("authorityDecision2"),
        }

class SCDBJusticeCiteIngestor(BaseIngestor):
    def __init__(self, cfg: IngestConfig, csv_path: str, chunksize: int = 100_000):
        super().__init__(cfg); self.csv_path = csv_path; self.chunksize = chunksize

    def extract(self) -> Iterable[Dict[str, Any]]:
        for chunk in pd.read_csv(self.csv_path, dtype=str, chunksize=self.chunksize):
            chunk = chunk.rename(columns=lambda c: c.strip().replace(" ", ""))
            for _, r in chunk.iterrows():
                yield r.to_dict()

    def transform_row(self, r: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return {
            "source": "scdb_merged_justice_cite",
            "usCite": r.get("usCite"),
            "sctCite": r.get("sctCite"),
            "ledCite": r.get("ledCite"),
            "lexisCite": r.get("lexisCite"),
            "justice": r.get("justice"),
            "justiceName": r.get("justiceName"),
            "vote": r.get("vote"),
            "opinion": r.get("opinion"),
            "direction": r.get("direction"),
        }
                