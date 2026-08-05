"""The example/doc retrieval index (Custom_Widgets/mcp/retrieval.py) must surface
the right recipe for a query and must NOT leak the internal design docs."""
import os

from Custom_Widgets.mcp import retrieval as r

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _top_paths(query, k=3):
    return [h["path"] for h in r.search(query, k=k, project_dir=_ROOT)]


def test_query_finds_the_matching_example():
    assert any("QCustomBadge" in p for p in _top_paths("badge with a count"))
    assert any("QCustomDataTable" in p for p in _top_paths("data table sorting"))
    assert any("QCustomCommandPalette" in p
               for p in _top_paths("command palette search"))


def test_camelcase_query_matches_code_identifiers():
    # 'QCustomStepper' should be reachable via plain-word tokens
    hits = _top_paths("stepper wizard steps", k=5)
    assert any("Stepper" in p for p in hits)


def test_internal_design_docs_are_not_indexed():
    idx = r._index(_ROOT, "")
    assert idx.docs, "corpus should not be empty"
    assert not any("docs/design" in d["path"] for d in idx.docs)
    assert not any(d["path"].startswith("docs/design") for d in idx.docs)


def test_results_are_well_formed_and_ranked():
    hits = r.search("dark light theme toggle", k=4, project_dir=_ROOT)
    assert hits, "expected matches"
    scores = [h["score"] for h in hits]
    assert scores == sorted(scores, reverse=True)   # descending
    for h in hits:
        assert set(h) >= {"path", "kind", "title", "line", "score", "excerpt"}
        assert h["kind"] in ("example", "doc")
        assert h["score"] > 0


def test_no_match_returns_empty():
    # a single gibberish token that doesn't split into any real subword
    assert r.search("qwerplkjhgfdsazxcvbnm", project_dir=_ROOT) == []


def test_full_inlines_text():
    hits = r.search("badge count", k=1, project_dir=_ROOT, full=True)
    assert hits and "text" in hits[0] and hits[0]["text"]
