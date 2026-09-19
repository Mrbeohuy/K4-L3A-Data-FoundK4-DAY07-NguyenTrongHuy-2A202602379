from typing import Callable

from .store import EmbeddingStore


class KnowledgeBaseAgent:
    """
    An agent that answers questions using a vector knowledge base.

    Retrieval-augmented generation (RAG) pattern:
        1. Retrieve top-k relevant chunks from the store.
        2. Build a prompt with the chunks as context.
        3. Call the LLM to generate an answer.
    """

    def __init__(self, store: EmbeddingStore, llm_fn: Callable[[str], str]) -> None:
        self.store = store
        self.llm_fn = llm_fn

    def answer(self, question: str, top_k: int = 3) -> str:
        if self.store.get_collection_size() == 0:
            return "Không tìm thấy thông tin trong cơ sở tri thức."

        results = self.store.search(question, top_k=top_k)
        if not results:
            return "Không tìm thấy thông tin phù hợp trong cơ sở tri thức."

        context_blocks = []
        for index, result in enumerate(results, start=1):
            metadata = result.get("metadata", {})
            source = (
                metadata.get("source")
                or metadata.get("file_path")
                or metadata.get("file")
                or metadata.get("doc_id")
                or metadata.get("title")
                or result.get("id")
                or "unknown"
            )
            context_blocks.append(
                f"[{index}] Source: {source}\n"
                f"Content: {result.get('content', '')}"
            )

        prompt = (
            "You are a retrieval-augmented assistant. Answer the question using only "
            "the numbered context below. Cite the context numbers you used, such as "
            "[1] or [2]. If the context does not contain enough information, say that "
            "the answer was not found in the provided context. Do not invent facts.\n\n"
            f"Question: {question}\n\n"
            "Context:\n"
            + "\n\n".join(context_blocks)
            + "\n\nAnswer:"
        )
        return self.llm_fn(prompt)
