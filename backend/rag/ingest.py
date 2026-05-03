"""RAG ingest pipeline.

Reads all 37 knowledge base markdown documents, splits them into
section-level chunks (each ## heading = one chunk), embeds with
ChromaDB's default offline model (all-MiniLM-L6-v2, 384-dim),
and upserts into a persistent local Chroma collection.

Chunking strategy:
  - Each ## section in a KB doc = one chunk
  - Chunk text = "## {section_title}\\n{body}"
  - Metadata stored: category, doc_title, section_title, source_path

Run directly to (re-)ingest:
    python -m backend.rag.ingest
"""

import os
import re
from pathlib import Path

# Suppress ChromaDB telemetry noise (capture() signature bug in 0.6.x)
os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")
import logging as _logging
_logging.getLogger("chromadb.telemetry").setLevel(_logging.CRITICAL)

import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

# ── Paths ─────────────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).parent.parent.parent
KB_DIR = PROJECT_ROOT / "knowledge_base"
CHROMA_DIR = PROJECT_ROOT / "backend" / "data" / "chroma"

COLLECTION_NAME = "fieldfix_kb"

# ── Chroma client (singleton-safe, called from retriever too) ─────────────────

def get_collection() -> chromadb.Collection:
    """Return (or create) the persistent Chroma collection."""
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR),
        settings=Settings(anonymized_telemetry=False),
    )
    ef = DefaultEmbeddingFunction()
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=ef,
        metadata={"hnsw:space": "cosine"},
    )


# ── Chunking ──────────────────────────────────────────────────────────────────

def _slugify(text: str) -> str:
    """Convert a string to a safe ID component."""
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def _chunk_document(path: Path, category: str) -> list[dict]:
    """
    Split a markdown KB document into section-level chunks.

    Returns list of dicts:
        {
            "id":       str   — unique chunk ID
            "text":     str   — chunk content (section header + body)
            "metadata": dict  — category, doc_title, section_title, source_path
        }
    """
    raw = path.read_text(encoding="utf-8").strip()
    doc_title = path.stem.replace("_", " ").title()

    # Split on level-2 headings (## ...) — keep the heading with its body
    # First item before any ## heading is the doc-level title block
    parts = re.split(r"(?=^## )", raw, flags=re.MULTILINE)

    chunks: list[dict] = []
    for part in parts:
        part = part.strip()
        if not part:
            continue

        # Extract section title
        first_line = part.splitlines()[0]
        if first_line.startswith("## "):
            section_title = first_line[3:].strip()
        elif first_line.startswith("# "):
            # Top-level doc title block — skip, context is in metadata
            continue
        else:
            section_title = "Overview"

        # Build chunk ID: category__doc__section (all slugified)
        chunk_id = f"{_slugify(category)}__{_slugify(path.stem)}__{_slugify(section_title)}"

        chunks.append({
            "id": chunk_id,
            "text": part,
            "metadata": {
                "category": category,
                "doc_title": doc_title,
                "section_title": section_title,
                "source_path": str(path.relative_to(PROJECT_ROOT)),
            },
        })

    return chunks


# ── Ingest ────────────────────────────────────────────────────────────────────

def ingest_all(verbose: bool = True) -> int:
    """
    Ingest all knowledge base documents into Chroma.

    Idempotent — uses upsert, safe to re-run after KB updates.

    Returns:
        Total number of chunks upserted.
    """
    collection = get_collection()

    all_ids: list[str] = []
    all_texts: list[str] = []
    all_metadatas: list[dict] = []

    md_files = sorted(KB_DIR.rglob("*.md"))
    if not md_files:
        raise FileNotFoundError(f"No .md files found under {KB_DIR}")

    doc_count = 0
    for md_path in md_files:
        # category = immediate parent directory name
        category = md_path.parent.name
        chunks = _chunk_document(md_path, category)
        if not chunks:
            continue
        doc_count += 1
        for chunk in chunks:
            all_ids.append(chunk["id"])
            all_texts.append(chunk["text"])
            all_metadatas.append(chunk["metadata"])

    # Batch upsert (Chroma handles duplicates via ID)
    # Process in batches of 100 to avoid memory spikes
    BATCH = 100
    for i in range(0, len(all_ids), BATCH):
        collection.upsert(
            ids=all_ids[i : i + BATCH],
            documents=all_texts[i : i + BATCH],
            metadatas=all_metadatas[i : i + BATCH],
        )
        if verbose:
            end = min(i + BATCH, len(all_ids))
            print(f"  upserted chunks {i + 1}–{end} / {len(all_ids)}")

    if verbose:
        print(f"\nIngested {doc_count} documents → {len(all_ids)} chunks")
        print(f"Chroma collection '{COLLECTION_NAME}' at {CHROMA_DIR}")

    return len(all_ids)


# ── CLI entrypoint ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"FieldFix AI — Knowledge Base Ingest")
    print(f"KB dir   : {KB_DIR}")
    print(f"Chroma   : {CHROMA_DIR}")
    print()
    total = ingest_all(verbose=True)
    print(f"\nDone. {total} chunks ready for retrieval.")
