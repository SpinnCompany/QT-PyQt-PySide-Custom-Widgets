########################################################################
## CUSTOM WIDGETS — EXAMPLE / DOC RETRIEVAL (dependency-free BM25)
##
## Grounds an agent in real task->code recipes instead of training memory: a
## lexical BM25 index over the bundled example projects + the user-facing repo
## docs (README, AGENTS.md) and, optionally, an external docs tree pointed at by
## CUSTOM_WIDGETS_DOCS_DIR (e.g. the Docusaurus site). No embeddings, no vector
## store, no new dependency — the corpus is small and BM25 over it is instant.
##
## The internal docs/design/* tree is deliberately NOT indexed (design notes and
## commercial material are not user recipes).
########################################################################
import functools
import math
import os
import re

_SKIP_DIRS = {"__pycache__", "generated-files", "build", ".venv", ".git",
              "node_modules", "src", "Qss", ".pytest_cache"}
_MAX_BYTES = 40000                 # cap a single file's contribution
_K1 = 1.5
_B = 0.75

_CAMEL = re.compile(r"[A-Z]+(?![a-z])|[A-Z][a-z]*|[a-z0-9]+")
_WORD = re.compile(r"[A-Za-z0-9]+")


def _tokenize(text):
    """Lowercase alphanumeric tokens, PLUS camelCase/identifier subwords so a
    query like 'badge count' matches `QCustomBadge`/`setCount` in code."""
    out = []
    for raw in _WORD.findall(text):
        low = raw.lower()
        out.append(low)
        parts = _CAMEL.findall(raw)
        if len(parts) > 1:
            out.extend(p.lower() for p in parts)
    return out


def _read(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read(_MAX_BYTES)
    except OSError:
        return ""


def _split_markdown(text):
    """(title, start_line, body) per heading section; preamble title=None."""
    lines = text.splitlines()
    sections, title, start, buf = [], None, 1, []
    for i, line in enumerate(lines):
        if line.lstrip().startswith("#"):
            if any(s.strip() for s in buf):
                sections.append((title, start, "\n".join(buf)))
            title, start, buf = line.strip("# ").strip(), i + 1, [line]
        else:
            buf.append(line)
    if any(s.strip() for s in buf):
        sections.append((title, start, "\n".join(buf)))
    return sections or [(None, 1, text)]


def _iter_sources(project_dir, docs_dir):
    """Yield (kind, path) for every indexable source."""
    examples = os.path.join(project_dir, "examples")
    if os.path.isdir(examples):
        for root, dirs, files in os.walk(examples):
            dirs[:] = [d for d in dirs if d not in _SKIP_DIRS]
            for name in files:
                if name.endswith(".py") and not name.startswith("ui_"):
                    yield "example", os.path.join(root, name)
                elif name.endswith((".md", ".mdx")):
                    yield "doc", os.path.join(root, name)
    for name in ("README.md", "AGENTS.md"):
        path = os.path.join(project_dir, name)
        if os.path.isfile(path):
            yield "doc", path
    if docs_dir and os.path.isdir(docs_dir):
        for root, dirs, files in os.walk(docs_dir):
            dirs[:] = [d for d in dirs if d not in _SKIP_DIRS]
            for name in files:
                if name.endswith((".md", ".mdx")):
                    yield "doc", os.path.join(root, name)


def _build_docs(project_dir, docs_dir):
    """Chunk sources into retrievable documents. Example .py -> one doc each;
    markdown -> one doc per heading section."""
    docs = []
    for kind, path in _iter_sources(project_dir, docs_dir):
        text = _read(path)
        if not text.strip():
            continue
        rel = os.path.relpath(path, project_dir)
        if kind == "doc" and path.endswith((".md", ".mdx")):
            for title, start, body in _split_markdown(text):
                docs.append({"kind": kind, "path": rel, "title": title,
                             "start": start, "text": body,
                             "tokens": _tokenize((title or "") + "\n" + body)})
        else:
            head = next((ln.strip("# ").strip() for ln in text.splitlines()
                         if ln.strip() and not ln.lstrip().startswith(("#!", "import",
                         "from"))), rel)
            docs.append({"kind": kind, "path": rel, "title": head, "start": 1,
                         "text": text, "tokens": _tokenize(rel + "\n" + text)})
    return docs


class _Index(object):
    def __init__(self, docs):
        self.docs = docs
        self.df = {}
        self.tf = []
        self.len = []
        for doc in docs:
            counts = {}
            for tok in doc["tokens"]:
                counts[tok] = counts.get(tok, 0) + 1
            self.tf.append(counts)
            self.len.append(max(1, len(doc["tokens"])))
            for tok in counts:
                self.df[tok] = self.df.get(tok, 0) + 1
        n = len(docs) or 1
        self.avgdl = sum(self.len) / n
        # BM25+ idf (always positive, safe on tiny corpora)
        self.idf = {t: math.log(1 + (n - df + 0.5) / (df + 0.5))
                    for t, df in self.df.items()}

    def score(self, q_tokens, i):
        tf, dl, s = self.tf[i], self.len[i], 0.0
        for tok in q_tokens:
            f = tf.get(tok)
            if not f:
                continue
            denom = f + _K1 * (1 - _B + _B * dl / self.avgdl)
            s += self.idf.get(tok, 0.0) * (f * (_K1 + 1)) / denom
        return s


@functools.lru_cache(maxsize=8)
def _index(project_dir, docs_dir):
    return _Index(_build_docs(project_dir, docs_dir))


def _excerpt(doc, q_tokens, width=4):
    """A window around the line with the most query-term hits."""
    lines = doc["text"].splitlines()
    if not lines:
        return ""
    qset = set(q_tokens)
    best_i, best_hits = 0, -1
    for i, line in enumerate(lines):
        hits = sum(1 for t in _tokenize(line) if t in qset)
        if hits > best_hits:
            best_i, best_hits = i, hits
    lo, hi = max(0, best_i - 1), min(len(lines), best_i + width)
    snippet = "\n".join(lines[lo:hi]).strip()
    return snippet[:600]


def search(query, k=5, project_dir=None, docs_dir=None, full=False):
    """Top-k example/doc chunks for a natural-language or keyword query.
    Returns a list of {path, kind, title, line, score, excerpt[, text]}."""
    project_dir = project_dir or os.getcwd()
    docs_dir = docs_dir or os.environ.get("CUSTOM_WIDGETS_DOCS_DIR") or ""
    idx = _index(os.path.abspath(project_dir), os.path.abspath(docs_dir) if docs_dir else "")
    q_tokens = _tokenize(query)
    scored = [(idx.score(q_tokens, i), i) for i in range(len(idx.docs))]
    scored = [(s, i) for s, i in scored if s > 0]
    scored.sort(key=lambda x: x[0], reverse=True)
    results = []
    for s, i in scored[:k]:
        doc = idx.docs[i]
        item = {"path": doc["path"], "kind": doc["kind"], "title": doc["title"],
                "line": doc["start"], "score": round(s, 3),
                "excerpt": _excerpt(doc, q_tokens)}
        if full:
            item["text"] = doc["text"]
        results.append(item)
    return results
