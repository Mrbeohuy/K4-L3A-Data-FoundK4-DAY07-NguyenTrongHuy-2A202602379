"""Benchmark retrieval trên corpus nhóm — dùng chung cho cả 3 thành viên.

Mỗi người CHỈ đổi dòng `CHUNKER = ...` sang chiến lược của mình; mọi thứ khác
(corpus, 5 câu hỏi, embedder, cách chấm) giữ nguyên để so sánh công bằng.

    python bench.py                       # chạy với CHUNKER bên dưới
    python bench.py > ket_qua_benchmark.txt
    python bench.py --strategy fixed      # ghi đè tạm để so sánh: fixed | sentence | recursive

Embedder đọc từ .env (EMBEDDING_PROVIDER=local|openai|gemini|mock), giống main.py.
Chấm 2 mức cho mỗi câu (theo docs/SCORING.md + lab doc mục 7):
  - Mức 1 (doc):   doc_id gold có trong top-3 không (cách chấm "ngây thơ", dễ thổi phồng).
  - Mức 2 (chunk): chunk trong top-3 có thực sự chứa `needle` (chuỗi đáp án) không.
  Điểm: 2 nếu top-1 chứa đáp án, 1 nếu đáp án chỉ ở top-2/3, 0 nếu không có trong top-3.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

from src import Document, EmbeddingStore, FixedSizeChunker, HeadingSectionChunker, RecursiveChunker, SentenceChunker

DATA_DIR = Path("data/thu-vien")
TOP_K = 3

# ─── DÒNG DUY NHẤT MỖI THÀNH VIÊN ĐƯỢC ĐỔI ─────────────────────────────────────
CHUNKER = HeadingSectionChunker(max_chunk_size=500)      # R3 · Heading (custom)
# CHUNKER = FixedSizeChunker(chunk_size=500, overlap=100)  # R1 · Fixed-size
# CHUNKER = RecursiveChunker(chunk_size=400)  # R2 · Recursive (đã thử 300/400/500/800 × 3 bộ separator)
# ────────────────────────────────────────────────────────────────────────────────

BASELINES = {
    "fixed": lambda: FixedSizeChunker(chunk_size=500, overlap=100),
    "sentence": lambda: SentenceChunker(max_sentences_per_chunk=3),
    "recursive": lambda: RecursiveChunker(chunk_size=500),
}

# 5 câu hỏi chung của nhóm. gold_answer trích nguyên văn từ corpus; needle là chuỗi
# con bắt buộc có trong chunk truy xuất được thì mới tính là "chứa đáp án".
QUERIES = [
    {
        "id": 1,
        "type": "bẫy audience (cần filter)",
        "query": "Ở Thư viện Đại học Ngoại thương được mượn về nhà tối đa bao nhiêu tài liệu và trong bao lâu?",
        "gold_answer": "03 tài liệu/30 ngày (Một lần gia hạn thêm 15 ngày tính từ ngày thực hiện lệnh gia hạn) đối với sách tham khảo",
        "gold_doc": "ftu-library-borrowing-student",
        "needle": "03 tài liệu/30 ngày",
        "filter": {"audience": "student"},
    },
    {
        "id": 2,
        "type": "tra con số",
        "query": "Chỉ số trùng lặp tối đa cho khóa luận tốt nghiệp khi tra soát trên Turnitin là bao nhiêu?",
        "gold_answer": "Khóa luận tốt nghiệp: 25%",
        "gold_doc": "library-similarity-check",
        "needle": "Khóa luận tốt nghiệp | 25%",
        "filter": None,
    },
    {
        "id": 3,
        "type": "quy trình / thời hạn",
        "query": "Sau khi người học nộp biên bản tra soát, thư viện trả kết quả trong bao lâu và ở đâu?",
        "gold_answer": "Trả kết quả tra soát tại K214 (Nhà K – ĐH Ngoại thương), chậm nhất trong vòng 02 ngày làm việc kể từ ngày người học nộp biên bản",
        "gold_doc": "library-similarity-check",
        "needle": "02 ngày làm việc kể từ ngày người học nộp biên bản",
        "filter": None,
    },
    {
        "id": 4,
        "type": "tra cứu giờ phục vụ",
        "query": "Thư viện Học viện Ngoại giao mở cửa vào Thứ Bảy từ mấy giờ đến mấy giờ?",
        "gold_answer": "Thứ Bảy: Từ 9:00 đến 18:00 (thông tầm không nghỉ giữa giờ); thư viện dừng phục vụ bạn đọc 15 phút trước giờ đóng cửa",
        "gold_doc": "dav-library-rules",
        "needle": "Thứ Bảy: Từ 9:00 đến 18:00",
        "filter": None,
    },
    {
        "id": 5,
        "type": "điều kiện vi phạm",
        "query": "Mượn tài liệu về nhà trả trễ hạn bao nhiêu lần trong một năm học thì bị coi là hành vi nghiêm cấm?",
        "gold_answer": "Mượn tài liệu về nhà quá hạn trên 03 lần/năm học",
        "gold_doc": "ftu-library-general-regulations",
        "needle": "quá hạn trên 03 lần/năm học",
        "filter": None,
    },
]


def load_embedder():
    """Chọn embedder theo .env; thiếu thư viện/API key thì quay về mock (giống main.py)."""
    from src.embeddings import GeminiEmbedder, LocalEmbedder, OpenAIEmbedder, _mock_embed

    load_dotenv(override=False)
    provider = os.getenv("EMBEDDING_PROVIDER", "mock").strip().lower()
    factories = {"local": LocalEmbedder, "openai": OpenAIEmbedder, "gemini": GeminiEmbedder}
    embedder = _mock_embed
    if provider in factories:
        try:
            embedder = factories[provider]()
        except Exception as error:  # noqa: BLE001 - fallback is intentional
            print(f"[warn] Không khởi tạo được embedder '{provider}' ({error}); dùng mock.", file=sys.stderr)
    name = getattr(embedder, "_backend_name", embedder.__class__.__name__)
    # Cache theo nội dung: chạy lại A/B không phải embed lại (và không tốn tiền API).
    return lru_cache(maxsize=None)(embedder), name


def parse_markdown(path: Path) -> tuple[dict, str]:
    """Tách YAML front matter (metadata) và phần thân (content) của một file .md."""
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not match:
        return {}, text
    metadata = {}
    for key, value in re.findall(r"^(\w+):\s*(.+)$", match.group(1), re.M):
        value = re.sub(r"\s+#.*$", "", value).strip().strip('"').strip("'")
        metadata[key] = value
    return metadata, match.group(2)


def build_documents(chunker) -> list[Document]:
    docs = []
    for path in sorted(DATA_DIR.glob("*.md")):
        metadata, body = parse_markdown(path)
        doc_id = metadata.get("doc_id", path.stem)
        for index, chunk in enumerate(chunker.chunk(body)):
            docs.append(
                Document(
                    id=f"{doc_id}#{index}",
                    content=chunk,
                    metadata={**metadata, "doc_id": doc_id, "chunk_index": index},
                )
            )
    return docs


def score_results(results: list[dict], query: dict) -> dict:
    doc_ids = [r["metadata"]["doc_id"] for r in results]
    has_answer = [query["needle"] in r["content"] for r in results]
    doc_rank = doc_ids.index(query["gold_doc"]) + 1 if query["gold_doc"] in doc_ids else None
    chunk_rank = has_answer.index(True) + 1 if any(has_answer) else None

    def points(rank):
        return 0 if rank is None else (2 if rank == 1 else 1)

    return {"doc_rank": doc_rank, "chunk_rank": chunk_rank, "doc_points": points(doc_rank), "chunk_points": points(chunk_rank), "has_answer": has_answer}


def print_results(results: list[dict], has_answer: list[bool], gold_doc: str) -> None:
    for rank, (r, ok) in enumerate(zip(results, has_answer), start=1):
        meta = r["metadata"]
        marks = ("✔ đáp án" if ok else "✘       ") + (" · gold doc" if meta["doc_id"] == gold_doc else "")
        preview = " ".join(r["content"].split())[:110]
        print(f"   {rank}. score={r['score']:.3f}  {r['id']:<38} audience={meta.get('audience', '?'):<8} [{marks}]")
        print(f"      {preview}…")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--strategy", choices=sorted(BASELINES), help="ghi đè CHUNKER để so sánh baseline")
    args = parser.parse_args()

    chunker = BASELINES[args.strategy]() if args.strategy else CHUNKER
    embedder, embedder_name = load_embedder()
    docs = build_documents(chunker)
    store = EmbeddingStore(collection_name="bench", embedding_fn=embedder)
    store.add_documents(docs)

    lengths = [len(d.content) for d in docs]
    print("=" * 100)
    print(f"Chiến lược : {chunker.__class__.__name__} {vars(chunker)}")
    print(f"Embedder   : {embedder_name}")
    print(f"Corpus     : {DATA_DIR} — {len({d.metadata['doc_id'] for d in docs})} tài liệu, "
          f"{store.get_collection_size()} chunk (dài TB {sum(lengths) / len(lengths):.0f}, min {min(lengths)}, max {max(lengths)})")
    if embedder_name.startswith("mock"):
        print("[CẢNH BÁO] Đang dùng MockEmbedder — điểm số là nhiễu, không phản ánh ngữ nghĩa.")
    print("=" * 100)

    summary = []
    for q in QUERIES:
        results = store.search_with_filter(q["query"], top_k=TOP_K, metadata_filter=q["filter"])
        s = score_results(results, q)
        summary.append((q, s))
        print(f"\nQ{q['id']} [{q['type']}] {q['query']}")
        print(f"   filter={q['filter']}  gold_doc={q['gold_doc']}  needle=\"{q['needle']}\"")
        print(f"   gold: {q['gold_answer']}")
        print_results(results, s["has_answer"], q["gold_doc"])
        print(f"   → Mức 1 (doc): {s['doc_points']}đ (hạng {s['doc_rank']})   Mức 2 (chunk chứa đáp án): {s['chunk_points']}đ (hạng {s['chunk_rank']})")

        if q["filter"]:
            unfiltered = store.search(q["query"], top_k=TOP_K)
            su = score_results(unfiltered, q)
            wrong = [r["id"] for r in unfiltered if any(r["metadata"].get(k) != v for k, v in q["filter"].items())]
            print(f"\n   [A/B] Cùng câu hỏi, KHÔNG filter:")
            print_results(unfiltered, su["has_answer"], q["gold_doc"])
            print(f"   → Mức 2 không filter: {su['chunk_points']}đ (hạng {su['chunk_rank']}) — "
                  f"{len(wrong)}/{len(unfiltered)} chunk sai đối tượng lọt top-{TOP_K}: {wrong or 'không có'}")
            if [r["id"] for r in unfiltered] == [r["id"] for r in results]:
                print("   [!] Kết quả có/không filter giống hệt nhau — câu hỏi này chưa thực sự cần filter.")

    print("\n" + "=" * 100)
    print(f"{'#':<3}{'Loại câu hỏi':<28}{'Mức 1 (doc)':>12}{'Mức 2 (chunk)':>15}")
    for q, s in summary:
        print(f"Q{q['id']:<2}{q['type']:<28}{s['doc_points']:>10}đ {s['chunk_points']:>13}đ")
    doc_total = sum(s["doc_points"] for _, s in summary)
    chunk_total = sum(s["chunk_points"] for _, s in summary)
    in_top = sum(s["chunk_rank"] is not None for _, s in summary)
    print(f"{'TỔNG':<31}{doc_total:>8}/10 {chunk_total:>11}/10")
    print(f"Câu có chunk chứa đáp án trong top-{TOP_K}: {in_top}/{len(QUERIES)}   "
          f"(chênh lệch Mức 1 − Mức 2 = {doc_total - chunk_total} điểm bị 'thổi phồng' nếu chỉ chấm theo doc_id)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
