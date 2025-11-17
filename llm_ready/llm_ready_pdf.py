"""
llm_ready_pdf.py

Convert PDFs to LLM-ready text using 'marker' library: 
    - split into size-bounded chunks, 
    - export JSONL/Parquet so PDFs can be searched/embedded alongside other sources.
"""

import argparse, pathlib, json, re, os
from datetime import datetime
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered

import pandas as pd

def list_inputs(inp: str):
    p = pathlib.Path(inp)
    if p.is_file():
        return [str(p)]
    if p.is_dir():
        exts = [".pdf"]  # extend if you want: ".docx",".pptx",...
        return [str(x) for x in sorted(p.rglob("*")) if x.suffix.lower() in exts]
    from glob import glob
    return sorted(glob(inp))

def chunk(md: str, max_chars=1600):
    parts = re.split(r"\n(?=#+\s)", md) if "#" in md else md.split("\n\n")
    out, buf = [], ""
    for part in parts:
        if len(buf) + len(part) <= max_chars:
            buf += ("\n" if buf else "") + part
        else:
            if buf.strip(): out.append(buf.strip())
            buf = part
    if buf.strip(): out.append(buf.strip())
    return out

def to_jsonl(md_text: str, jsonl_path: pathlib.Path, source: str, max_chars=1600):
    jsonl_path.parent.mkdir(parents=True, exist_ok=True)
    chunks = chunk(md_text, max_chars)
    with jsonl_path.open("w", encoding="utf-8") as f:
        for i, t in enumerate(chunks, 1):
            f.write(json.dumps({
                "id": f"{pathlib.Path(source).stem}-{i}",
                "source": source,
                "created_at": datetime.utcnow().isoformat() + "Z",
                "text": t
            }, ensure_ascii=False) + "\n")
    return len(chunks)

def to_parquet(md_text: str, pq_path: pathlib.Path, source: str, mode="chunks", chunk_size=1600):
    pq_path.parent.mkdir(parents=True, exist_ok=True)
    if mode == "single":
        df = pd.DataFrame([{
            "id": pathlib.Path(source).stem,
            "source": source,
            "created_at": datetime.utcnow().isoformat() + "Z",
            "text": md_text
        }])
    else:
        parts = chunk(md_text, chunk_size)
        df = pd.DataFrame([{
            "id": f"{pathlib.Path(source).stem}-{i}",
            "source": source,
            "created_at": datetime.utcnow().isoformat() + "Z",
            "text": t
        } for i, t in enumerate(parts, 1)])
    df.to_parquet(pq_path, index=False)
    return len(df)

# ================== CLI ==================

def main():
    ap = argparse.ArgumentParser(description="Convert PDFs to Markdown with Marker (+ optional JSONL/Parquet).")
    ap.add_argument("--input", required=True, help="file / folder / glob")
    ap.add_argument("--out", required=True, help="output directory")

    ap.add_argument("--device", default="auto", help="auto|cpu|cuda|mps (Marker reads TORCH_DEVICE)")
    ap.add_argument("--images", action="store_true", help="attempt to save extracted images next to Markdown")

    ap.add_argument("--jsonl", type=int, default=0, help="write chunks.jsonl with this max chars per chunk")
    ap.add_argument("--parquet", choices=["single","chunks"], help="write Parquet (single row or per chunk)")
    ap.add_argument("--chunk", type=int, default=1600, help="chunk size for JSONL/Parquet chunks")
    args = ap.parse_args()

    if args.device and args.device.lower() != "auto":
        os.environ["TORCH_DEVICE"] = args.device.lower()

    out_root = pathlib.Path(args.out); out_root.mkdir(parents=True, exist_ok=True)
    files = list_inputs(args.input)
    if not files:
        raise SystemExit("No inputs found.")

    converter = PdfConverter(artifact_dict=create_model_dict())

    for f in files:
        src = pathlib.Path(f)
        out_dir = out_root / src.stem
        out_dir.mkdir(parents=True, exist_ok=True)

        # --- Marker conversion (new API) ---
        rendered = converter(str(src))
        # NOTE: text_from_rendered returns (markdown_str, metadata_dict, images_info)
        # Some Marker versions save images during rendering; others return info only.
        # We call it plainly and then handle images list if present.
        md_text, meta, images = text_from_rendered(rendered)

        (out_dir / f"{src.stem}.md").write_text(md_text, encoding="utf-8")
        (out_dir / f"{src.stem}.meta.json").write_text(
            json.dumps({"source": str(src), "marker_meta": meta}, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

        if args.images and images:
            img_dir = out_dir / "images"
            img_dir.mkdir(exist_ok=True)
            for i, im in enumerate(images, 1):
                path = None
                if isinstance(im, (str, pathlib.Path)):
                    path = pathlib.Path(im)
                    # If it's already a saved path, just copy next to output (optional)
                    # Skipping copy to keep it minimal.
                elif isinstance(im, dict):
                    name = im.get("name") or f"img_{i}.png"
                    if "bytes" in im and isinstance(im["bytes"], (bytes, bytearray)):
                        (img_dir / name).write_bytes(im["bytes"])
                    elif "image" in im:
                        try:
                            im["image"].save(img_dir / name)
                        except Exception:
                            pass
                # else: unknown structure → skip silently

        # Optional RAG formats
        if args.jsonl > 0:
            n = to_jsonl(md_text, out_dir / f"{src.stem}.chunks.jsonl", str(src), args.jsonl)
            print(f"[OK] {src.name}: markdown + JSONL (chunks={n})")
        if args.parquet:
            pq = out_dir / (f"{src.stem}.parquet" if args.parquet == "single" else f"{src.stem}.chunks.parquet")
            n = to_parquet(md_text, pq, str(src), mode=args.parquet, chunk_size=args.chunk)
            print(f"[OK] {src.name}: markdown + Parquet rows={n}")
        if not args.jsonl and not args.parquet:
            print(f"[OK] {src.name}: markdown only → {out_dir}")

if __name__ == "__main__":
    main()
