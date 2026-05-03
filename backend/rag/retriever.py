"""RAG retriever.

Queries the Chroma collection built by ingest.py and returns
RetrievedSource objects compatible with the RepairOutput schema.

Primary interface:
    retrieve(query, category=None, top_k=5) -> list[RetrievedSource]

The retriever is safe to call before ingest — it raises a clear
RuntimeError if the collection is empty so the caller can ingest first.
"""

from __future__ import annotations

from backend.rag.ingest import get_collection
from backend.schemas.repair_output import RetrievedSource


def retrieve(
    query: str,
    category: str | None = None,
    top_k: int = 5,
) -> list[RetrievedSource]:
    """
    Semantic search over the knowledge base.

    Args:
        query:    Natural-language symptom or repair question.
        category: Optional category slug to restrict results
                  (e.g. "robotics", "electronics", "household",
                   "emergency_equipment", "safety").
                  If None, searches all categories.
        top_k:    Maximum number of results to return.

    Returns:
        List of RetrievedSource objects sorted by relevance (best first).
        Returns empty list if collection is empty (not yet ingested).

    Raises:
        RuntimeError: If Chroma collection has never been ingested.
    """
    collection = get_collection()

    # Guard: collection must have documents
    count = collection.count()
    if count == 0:
        raise RuntimeError(
            "Knowledge base not ingested. "
            "Run: python -m backend.rag.ingest"
        )

    # Build where filter for category
    where: dict | None = None
    if category is not None:
        where = {"category": {"$eq": category}}

    results = collection.query(
        query_texts=[query],
        n_results=min(top_k, count),
        where=where,
        include=["documents", "metadatas", "distances"],
    )

    sources: list[RetrievedSource] = []

    if not results["ids"] or not results["ids"][0]:
        return sources

    ids       = results["ids"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]  # cosine distance: lower = more similar

    for _id, meta, dist in zip(ids, metadatas, distances):
        # Convert cosine distance (0–2) to similarity score (0–1)
        relevance = round(max(0.0, 1.0 - dist / 2.0), 4)

        sources.append(
            RetrievedSource(
                title=f"{meta.get('doc_title', 'Unknown')} — {meta.get('section_title', '')}",
                source=meta.get("source_path", _id),
                relevance_score=relevance,
            )
        )

    # Already sorted by distance (best first) from Chroma
    return sources


def retrieve_context(
    query: str,
    category: str | None = None,
    top_k: int = 5,
) -> str:
    """
    Like retrieve() but returns raw text chunks joined as a single string.

    Useful for stuffing context into an LLM prompt.

    Returns:
        Multi-section context string, or empty string if nothing found.
    """
    collection = get_collection()
    count = collection.count()
    if count == 0:
        return ""

    where: dict | None = None
    if category is not None:
        where = {"category": {"$eq": category}}

    results = collection.query(
        query_texts=[query],
        n_results=min(top_k, count),
        where=where,
        include=["documents", "metadatas"],
    )

    if not results["documents"] or not results["documents"][0]:
        return ""

    sections: list[str] = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        header = (
            f"[Source: {meta.get('doc_title', '?')} / "
            f"{meta.get('section_title', '?')} "
            f"({meta.get('category', '?')})]"
        )
        sections.append(f"{header}\n{doc}")

    return "\n\n---\n\n".join(sections)
