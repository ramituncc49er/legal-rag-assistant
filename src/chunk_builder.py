"""
chunk_builder.py

Turn raw opinion texts and metadata into retrieval-friendly chunks: 
    - clean/normalize text, 
    - strip boilerplate, 
    - detect citations,
    - slice into overlap-aware chunks, 
    - write a Parquet/JSONL with per-chunk fields (ids, spans, stats).
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, date
import math
import uuid
import tiktoken
import pandas as pd
import numpy as np
import re
import argparse, os, json
import unicodedata  # <-- NFKC

# ================== JSON helper ==================
def _json_default(o):
    # datetime/date → ISO 8601
    if isinstance(o, (datetime, date)):
        return o.isoformat()

    try:
        if isinstance(o, pd.Timestamp):
            return o.isoformat()
        if isinstance(o, pd.Timedelta):
            return str(o)
    except Exception:
        pass

    try:
        import numpy as np
        if isinstance(o, np.integer):
            return int(o)
        if isinstance(o, np.floating):
            val = float(o)
            if math.isnan(val) or math.isinf(val):
                return None
            return val
        if isinstance(o, np.ndarray):
            return o.tolist()
    except Exception:
        pass

    # UUID
    if isinstance(o, uuid.UUID):
        return str(o)

    return str(o)

def _sanitize_for_json(obj):
    """Recursively convert NaN/Inf to None and normalize pandas/numpy types."""
    if isinstance(obj, dict):
        return {k: _sanitize_for_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_sanitize_for_json(v) for v in obj]
    if obj is None:
        return None

    # floats (native)
    if isinstance(obj, float):
        return None if (math.isnan(obj) or math.isinf(obj)) else obj

    # numpy scalars / arrays
    if np is not None:
        if isinstance(obj, np.floating):
            val = float(obj)
            return None if (math.isnan(val) or math.isinf(val)) else val
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.ndarray):
            return [_sanitize_for_json(v) for v in obj.tolist()]

    # pandas timestamp/NaT/timedelta
    if isinstance(obj, pd.Timestamp):
        return obj.isoformat()
    if obj is pd.NaT:
        return None
    if isinstance(obj, pd.Timedelta):
        return str(obj)

    # datetime/date
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()

    # leave everything else as-is (str, int, bool, etc.)
    return obj


# ================== Tokenizer (fixed to cl100k_base) ==================
def _get_tokenizer():
    enc = tiktoken.get_encoding("cl100k_base")

    def _tokcount(s: str) -> int:
        return len(enc.encode(s))

    def _truncate_to_tokens(s: str, max_tokens: int) -> str:
        ids = enc.encode(s)
        return s if len(ids) <= max_tokens else enc.decode(ids[:max_tokens])

    return _tokcount, _truncate_to_tokens, "cl100k_base"


# ================== Helpers ==================
_para_split_re = re.compile(r"(?:\n\s*\n)+", re.MULTILINE)
_sent_split_re = re.compile(r"(?<=[\.!?])\s+(?=[A-Z0-9“\"'])")

# robust citation patterns (allow optional space in "U. S.")
CITATION_PATTERNS = [
    r"\b\d+\s+U\.?\s*S\.?\s+\d+\b",              # U.S. or U. S.
    r"\b\d+\s+S\.?\s*Ct\.?\s+\d+\b",             # S. Ct.
    r"\b\d+\s+L\.?\s*Ed\.?(?:\s*2d)?\s+\d+\b",   # L. Ed. / L. Ed. 2d
    r"\b\d{4}\s+U\.?\s*S\.?\s+LEXIS\s+\d+\b",    # 1971 U. S. LEXIS 100
]
citation_res = [re.compile(p) for p in CITATION_PATTERNS]

# reporter star-page markers like "*714" possibly without space after
_STARLEAD_RE = re.compile(r"^\*\s*(\d+)\s*")

def split_paragraphs(text_raw: str) -> List[str]:
    return [p.strip() for p in _para_split_re.split(text_raw) if p.strip()]

def split_sentences(p: str) -> List[str]:
    pieces = _sent_split_re.split(p.strip())
    return [s.strip() for s in pieces if s.strip()]

def normalize_whitespace(s: str) -> str:
    s = re.sub(r"[ \t]+", " ", s)
    s = s.replace("\u00A0", " ")
    return s.strip()

def normalize_nfkc_and_ws(s: str) -> str:
    # NFKC first, then whitespace collapse
    s = unicodedata.normalize("NFKC", s)
    return normalize_whitespace(s)

def strip_starpage_keep_number(s: str) -> Tuple[str, Optional[int]]:
    """
    If paragraph starts with a reporter star page like '*714', strip it for model text
    but return the page number to keep in metadata.
    """
    m = _STARLEAD_RE.match(s)
    if not m:
        return s, None
    page = None
    try:
        page = int(m.group(1))
    except Exception:
        page = None
    stripped = s[m.end():]
    return stripped.lstrip(), page

def has_citation(text: str) -> Tuple[bool, List[str]]:
    kinds = [label for rx, label in zip(citation_res, ["U.S.", "S. Ct.", "L. Ed.", "LEXIS"]) if rx.search(text)]
    return (len(kinds) > 0, kinds)

def find_char_span(haystack: str, needle: str, start_at: int) -> Tuple[int, int]:
    idx = haystack.find(needle, start_at)
    if idx >= 0:
        return idx, idx + len(needle)
    n_clean = normalize_whitespace(needle)
    hs_clean = normalize_whitespace(haystack[start_at:])
    idx2 = hs_clean.find(n_clean)
    if idx2 >= 0:
        return start_at + idx2, start_at + idx2 + len(n_clean)
    return -1, -1


# ================== Options / Record ==================
@dataclass
class ChunkOptions:
    max_tokens: int = 900
    overlap_tokens: int = 180
    max_paragraphs_per_chunk: int = 12
    sentence_split_threshold: int = 1300
    max_chunk_chars: int = 8000
    attach_footnotes: bool = True

@dataclass
class ChunkRecord:
    chunk_id: str
    doc_id: Optional[int]
    opinion_id: Optional[int]
    case_id: Optional[int]
    cl_cluster_id: Optional[int]
    case_name: Optional[str]
    type: Optional[str]
    para_indices: List[int]
    core_start_char: int
    core_end_char: int
    text_clean: str
    text_raw: str
    has_citation: bool
    citation_kinds: List[str]
    roles_present: List[str] = field(default_factory=list)
    prev_chunk_id: Optional[str] = None
    next_chunk_id: Optional[str] = None
    overlap_tokens_from_prev: int = 0
    reporter_pages: List[int] = field(default_factory=list)  # <-- NEW
    issues: List[Dict[str, Any]] = field(default_factory=list)  # <-- hydrated
    votes: List[Dict[str, Any]] = field(default_factory=list)   # <-- hydrated
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


# ================== ChunkBuilder ==================
class ChunkBuilder:
    def __init__(self, options: Optional[ChunkOptions] = None):
        self.options = options or ChunkOptions()
        self.tokcount, self.truncate_to_tokens, self.tokenizer_name = _get_tokenizer()

    def _maybe_sentence_split(self, p: str) -> List[str]:
        # NOTE: split uses raw paragraph text; normalization happens later for model text
        if self.tokcount(p) <= self.options.sentence_split_threshold:
            return [p]
        return split_sentences(p)

    def _clean_for_model(self, s: str) -> Tuple[str, Optional[int]]:
        """
        Returns: (text_for_model, reporter_page_if_any)
        - Strips leading star-page like '*714'
        - Applies NFKC and whitespace normalization
        """
        s2, page = strip_starpage_keep_number(s)
        s2 = normalize_nfkc_and_ws(s2)
        return s2, page

    def _truncate_to_sentence_boundary(self, s: str, max_tokens: int) -> str:
        t = self.truncate_to_tokens(s, max_tokens)
        m = list(re.finditer(r"[\.!?](?=\s|$)", t))
        if m:
            return t[: m[-1].end()].rstrip()
        return t

    def _make_overlap_prefix(self, prev_text_clean: str, overlap_tokens: int) -> str:
        if overlap_tokens <= 0:
            return ""
        tok_len = self.tokcount(prev_text_clean)
        if tok_len <= overlap_tokens:
            return prev_text_clean
        truncated = self.truncate_to_tokens(prev_text_clean, tok_len)
        ratio = overlap_tokens / max(tok_len, 1)
        cut_chars = max(0, int(len(truncated) * (1 - ratio)))
        overlap = truncated[cut_chars:].lstrip()
        m = re.search(r"(?<=[\.!?])\s", overlap)
        if m and m.start() > 10:
            overlap = overlap[m.start():].lstrip()
        return overlap

    def _flush_chunk(self,
                     acc_texts,
                     acc_raw_texts,
                     acc_para_indices,
                     acc_reporter_pages,
                     full_text,
                     meta,
                     prev_chunk,
                     out_chunks):
        text_clean = "\n\n".join([t for t in acc_texts if t.strip()])
        text_raw = "\n\n".join([t for t in acc_raw_texts if t.strip()])

        overlap_tokens_from_prev = 0

        core_pairs = [(idx, raw.strip()) for idx, raw in zip(acc_para_indices, acc_raw_texts) if idx >= 0]
        core_indices = [idx for idx, _ in core_pairs]

        core_start_char = -1
        core_end_char = -1
        if core_pairs:
            try:
                first_raw = core_pairs[0][1]
                last_raw = core_pairs[-1][1]
                s, e = find_char_span(full_text, first_raw, 0)
                core_start_char, core_end_char = s, e
                s2, e2 = find_char_span(full_text, last_raw, core_end_char if core_end_char >= 0 else 0)
                if e2 > 0:
                    core_end_char = e2
            except Exception:
                pass

        has_cit, kinds = has_citation(text_raw)

        if len(text_clean) > self.options.max_chunk_chars:
            text_clean = text_clean[: self.options.max_chunk_chars]
        if len(text_raw) > self.options.max_chunk_chars:
            text_raw = text_raw[: self.options.max_chunk_chars]

        if acc_para_indices and acc_para_indices[0] == -1:
            overlap_tokens_from_prev = self.tokcount(acc_texts[0])

        base = f"{meta.get('case_id', 'x')}-{meta.get('opinion_id', 'x')}"
        chunk_id = f"{base}-{str(uuid.uuid4())[:8]}"

        # JSON hydration (issues_json, votes_json) from metadata
        def _parse_list_json(s):
            if s is None or not isinstance(s, str) or not s.strip():
                return []
            try:
                val = json.loads(s)
                return val if isinstance(val, list) else [val]
            except Exception:
                return []

        hydrated_issues = meta.get("issues", [])
        hydrated_votes  = meta.get("votes", [])

        # de-duplicate and sort reporter pages
        rep_pages = sorted({p for p in acc_reporter_pages if isinstance(p, int)})

        rec_dict: Dict[str, Any] = {
            "chunk_id": chunk_id,
            "doc_id": meta.get("doc_id"),
            "opinion_id": meta.get("opinion_id"),
            "case_id": meta.get("case_id"),
            "cl_cluster_id": meta.get("cl_cluster_id"),
            "case_name": meta.get("case_name"),
            "type": meta.get("type"),
            "para_indices": core_indices,
            "core_start_char": core_start_char,
            "core_end_char": core_end_char,
            "text_clean": text_clean,     # NFKC + no star-pages
            "text_raw": text_raw,         # exact source text (star-pages intact)
            "has_citation": has_cit,
            "citation_kinds": kinds,
            "roles_present": [],
            "prev_chunk_id": None,
            "next_chunk_id": None,
            "overlap_tokens_from_prev": overlap_tokens_from_prev,
            "reporter_pages": rep_pages,  # NEW
            "issues": hydrated_issues,    # NEW (hydrated copies)
            "votes": hydrated_votes,      # NEW (hydrated copies)
            "created_at": datetime.utcnow().isoformat() + "Z",
        }
        # passthrough any extra metadata (SCDB, etc.)
        for k, v in meta.items():
            if k not in rec_dict:
                rec_dict[k] = v

        out_chunks.append(rec_dict)
        return rec_dict

    def _pack(self, paragraphs: List[str], full_text: str, meta: Dict[str, Any]) -> List[dict]:
        chunks: List[Dict[str, Any]] = []
        acc_texts: List[str] = []
        acc_raw_texts: List[str] = []
        acc_para_indices: List[int] = []
        acc_reporter_pages: List[Optional[int]] = []  # NEW
        prev_chunk: Optional[Dict[str, Any]] = None

        for i, p in enumerate(paragraphs):
            for part in self._maybe_sentence_split(p):
                # model text (clean) vs raw text
                clean_part, page = self._clean_for_model(part)
                candidate_texts = acc_texts + [clean_part]
                candidate_text_clean = "\n\n".join(candidate_texts)

                too_many_tokens = self.tokcount(candidate_text_clean) > self.options.max_tokens
                too_many_paras = len(candidate_texts) > self.options.max_paragraphs_per_chunk

                if too_many_tokens or too_many_paras:
                    if acc_texts:
                        prev_chunk = self._flush_chunk(acc_texts, acc_raw_texts, acc_para_indices,
                                                       acc_reporter_pages, full_text, meta, prev_chunk, chunks)
                        acc_texts, acc_raw_texts, acc_para_indices, acc_reporter_pages = [], [], [], []
                        if prev_chunk and self.options.overlap_tokens > 0:
                            overlap_prefix = self._make_overlap_prefix(prev_chunk["text_clean"], self.options.overlap_tokens)
                            if overlap_prefix:
                                acc_texts.append(overlap_prefix)
                                acc_raw_texts.append(overlap_prefix)  # note: overlap is synthetic; ok to mirror
                                acc_para_indices.append(-1)
                                acc_reporter_pages.append(None)

                    if not acc_texts:
                        trimmed = self._truncate_to_sentence_boundary(clean_part, self.options.max_tokens)
                        acc_texts.append(trimmed)
                        acc_raw_texts.append(part)  # keep exact raw
                        acc_para_indices.append(i)
                        acc_reporter_pages.append(page)
                        prev_chunk = self._flush_chunk(acc_texts, acc_raw_texts, acc_para_indices,
                                                       acc_reporter_pages, full_text, meta, prev_chunk, chunks)
                        acc_texts, acc_raw_texts, acc_para_indices, acc_reporter_pages = [], [], [], []
                        if prev_chunk and self.options.overlap_tokens > 0:
                            overlap_prefix = self._make_overlap_prefix(prev_chunk["text_clean"], self.options.overlap_tokens)
                            if overlap_prefix:
                                acc_texts.append(overlap_prefix)
                                acc_raw_texts.append(overlap_prefix)
                                acc_para_indices.append(-1)
                                acc_reporter_pages.append(None)
                else:
                    acc_texts.append(clean_part)
                    acc_raw_texts.append(part)
                    acc_para_indices.append(i)
                    acc_reporter_pages.append(page)

        if acc_texts:
            self._flush_chunk(acc_texts, acc_raw_texts, acc_para_indices,
                              acc_reporter_pages, full_text, meta, prev_chunk, chunks)

        for k in range(len(chunks) - 1):
            chunks[k]["next_chunk_id"] = chunks[k + 1]["chunk_id"]
            chunks[k + 1]["prev_chunk_id"] = chunks[k]["chunk_id"]

        return chunks

    def _attach_footnotes(self, paragraphs: List[str]) -> List[str]:
        out_p = []
        i = 0
        while i < len(paragraphs):
            p = paragraphs[i]
            combined = p
            if re.search(r"\[\d+\]\s*$", p) and i + 1 < len(paragraphs):
                next_p = paragraphs[i + 1]
                if self.tokcount(next_p) < 120:
                    combined = p + "\n\n" + next_p
                    i += 1
            out_p.append(combined)
            i += 1
        return out_p

    def build(self, text_raw: str, meta: Dict[str, Any]) -> List[Dict[str, Any]]:
        # NOTE: do not mutate text_raw (provenance). Cleaning happens for model text only.
        paragraphs = split_paragraphs(text_raw)
        if self.options.attach_footnotes:
            paragraphs = self._attach_footnotes(paragraphs)
        return self._pack(paragraphs, text_raw, meta)


# ================== Helpers ==================
def build_chunks_for_opinion(text_raw: str, meta: Dict[str, Any], **options) -> List[Dict[str, Any]]:
    opts = ChunkOptions(**options) if options else ChunkOptions()
    return ChunkBuilder(opts).build(text_raw, meta)

def quick_eval_variants(text_raw: str, meta: Dict[str, Any], variants: List[Dict[str, Any]]):
    results = {}
    for v in variants:
        name = v.get("name") or f"v{len(results)+1}"
        opts = ChunkOptions(**{k: v[k] for k in v if k != "name"})
        b = ChunkBuilder(opts)
        chunks = b.build(text_raw, meta)
        toks = [b.tokcount(c["text_clean"]) for c in chunks]
        if toks:
            toks_sorted = sorted(toks)
            p95 = toks_sorted[int(0.95 * (len(toks_sorted) - 1))]
            results[name] = {
                "n_chunks": len(chunks),
                "avg_tokens": sum(toks) / len(toks),
                "p95_tokens": p95,
                "tokenizer": b.tokenizer_name,
                "max_tokens": opts.max_tokens,
                "overlap_tokens": opts.overlap_tokens,
            }
        else:
            results[name] = {"n_chunks": 0, "avg_tokens": 0, "p95_tokens": 0}
    return results


# ================== CLI ==================
def main() -> int:

    ap = argparse.ArgumentParser(description="Build RAG chunks.")
    ap.add_argument("--docs", required=True, help="Path to documents.parquet")
    ap.add_argument("--out", required=True,
                    help="Output directory or file path. The program will always write <dir>/chunk.json")
    ap.add_argument("--row-index", type=int, default=None,
                    help="Single row index to process (overrides start/num).")
    ap.add_argument("--start-index", type=int, default=0, help="Start index for range processing.")
    ap.add_argument("--num-records", type=int, default=1,
                    help="How many records from start-index. Use -1 for all from start.")

    ap.add_argument("--text-cols", default="opinion_text,text,full_text",
                    help="Comma-separated candidate text columns to try in order.")
    ap.add_argument("--max-tokens", type=int, default=900)
    ap.add_argument("--overlap-tokens", type=int, default=180)
    ap.add_argument("--sentence-split-threshold", type=int, default=1300)
    ap.add_argument("--attach-footnotes", dest="attach_footnotes", action="store_true", default=True)
    ap.add_argument("--no-attach-footnotes", dest="attach_footnotes", action="store_false")
    ap.add_argument("--max-paragraphs-per-chunk", type=int, default=12)
    ap.add_argument("--max-chunk-chars", type=int, default=8000)

    args = ap.parse_args()

    # Load corpus
    df = pd.read_parquet(args.docs)
    n = len(df)
    if n == 0:
        raise ValueError("No rows found in --docs")

    # SLICING LOGIC
    if args.row_index is not None:
        if not (0 <= args.row_index < n):
            raise IndexError(f"row_index {args.row_index} out of range (len={n})")
        df_slice = df.iloc[[args.row_index]]  # keep as DataFrame slice
    else:
        start = max(0, args.start_index)
        end = n if args.num_records == -1 else min(n, start + max(0, args.num_records))
        if not (0 <= start < n) or not (0 < end <= n) or start >= end:
            raise IndexError(f"Selection empty/invalid: start={start}, end={end}, len={n}")
        df_slice = df.iloc[start:end]

    text_cols = [c.strip() for c in args.text_cols.split(",") if c.strip()]

    # Build all chunks (merged mode only)
    all_chunks: List[Dict[str, Any]] = []
    for idx, row in df_slice.iterrows():
        row_dict = row.to_dict()
        text_raw = ""
        for c in text_cols:
            v = row_dict.get(c)
            if isinstance(v, str) and v.strip():
                text_raw = v
                break
        if not text_raw:
            print(f"Skipping row {idx}: no text in columns {text_cols}")
            continue

        meta = {k: v for k, v in row_dict.items() if k not in text_cols}

        def _parse_list_json(s):
            if not isinstance(s, str) or not s.strip():
                return []
            try:
                v = json.loads(s)
                return v if isinstance(v, list) else [v]
            except Exception:
                return []

        meta["issues"] = _parse_list_json(row_dict.get("issues_json"))
        meta["votes"]  = _parse_list_json(row_dict.get("votes_json"))

        meta.pop("issues_json", None)
        meta.pop("votes_json", None)

        chunks = build_chunks_for_opinion(
            text_raw,
            meta,
            max_tokens=args.max_tokens,
            overlap_tokens=args.overlap_tokens,
            sentence_split_threshold=args.sentence_split_threshold,
            attach_footnotes=args.attach_footnotes,
            max_paragraphs_per_chunk=args.max_paragraphs_per_chunk,
            max_chunk_chars=args.max_chunk_chars,
        )
        all_chunks.extend(chunks)
        if (len(all_chunks) % 2000) == 0:
            print(f"Accumulated {len(all_chunks)} chunks...")

    out_path = args.out
    out_dir = out_path if os.path.isdir(out_path) or out_path.endswith(("/", "\\")) else os.path.dirname(out_path)
    if not out_dir:
        out_dir = "."
    os.makedirs(out_dir, exist_ok=True)
    final_json = os.path.join(out_dir, "chunk.json")

    with open(final_json, "w", encoding="utf-8") as f:
        safe = _sanitize_for_json(all_chunks)
        json.dump(
            safe,
            f,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )

    print(f"Saved {len(all_chunks)} chunks -> {final_json}")
    print(f"Done. Rows processed: {len(df_slice)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())