"""Tests for RAG retriever."""

import pytest
from backend.rag.retriever import retrieve, retrieve_context
from backend.schemas.repair_output import RetrievedSource


def test_retrieve_returns_list():
    results = retrieve("servo buzzing", category="robotics", top_k=3)
    assert isinstance(results, list)
    assert len(results) <= 3


def test_retrieve_returns_retrieved_source_objects():
    results = retrieve("raspberry pi not booting", category="electronics", top_k=2)
    for r in results:
        assert isinstance(r, RetrievedSource)
        assert isinstance(r.title, str)
        assert isinstance(r.source, str)
        assert 0.0 <= r.relevance_score <= 1.0


def test_retrieve_relevance_sorted_best_first():
    results = retrieve("door hinge squeaking", category="household", top_k=5)
    scores = [r.relevance_score for r in results]
    assert scores == sorted(scores, reverse=True)


def test_retrieve_category_filter_respected():
    """Results for robotics query + robotics filter should be robotics docs."""
    results = retrieve("stepper motor stalling", category="robotics", top_k=3)
    for r in results:
        assert "robotics" in r.source.lower() or "motor" in r.title.lower()


def test_retrieve_no_category_returns_results():
    results = retrieve("battery overheating", top_k=3)
    assert len(results) >= 1


def test_retrieve_context_returns_string():
    ctx = retrieve_context("servo buzzing", category="robotics", top_k=2)
    assert isinstance(ctx, str)
    assert len(ctx) > 0


def test_retrieve_context_contains_source_header():
    ctx = retrieve_context("smoke detector chirping", category="emergency_equipment", top_k=1)
    assert "[Source:" in ctx


@pytest.mark.parametrize("category", [
    "robotics", "electronics", "emergency_equipment", "household", "safety"
])
def test_retrieve_works_for_all_categories(category):
    results = retrieve("common problem", category=category, top_k=2)
    assert isinstance(results, list)
