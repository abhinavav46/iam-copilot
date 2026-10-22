"""Small BM25 retriever over the Markdown files in /knowledge (RAG without heavy deps)."""
import math
import re
from collections import Counter
from pathlib import Path

STOP = set("a an the is are was of to in on for and or what how why do does i me my can with it be as at by from this that".split())


def tok(text: str):
    return [w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP and len(w) > 1]


class KB:
    def __init__(self, folder):
        self.docs = []  # (title, body, source)
        for f in sorted(Path(folder).glob("*.md")):
            for sec in re.split(r"\n(?=## )", f.read_text(encoding="utf-8")):
                sec = sec.strip()
                if sec.startswith("## "):
                    title, _, body = sec.partition("\n")
                    self.docs.append((title[3:].strip(), body.strip(), f.stem))
        self.tokens = [tok(f"{t} {t} {b}") for t, b, _ in self.docs]
        self.df = Counter(w for ts in self.tokens for w in set(ts))
        self.avg = sum(map(len, self.tokens)) / max(1, len(self.tokens))

    def search(self, query: str, k: int = 3):
        qt, n, scored = tok(query), len(self.docs), []
        for i, ts in enumerate(self.tokens):
            c, s = Counter(ts), 0.0
            for w in qt:
                if w in c:
                    idf = math.log(1 + (n - self.df[w] + 0.5) / (self.df[w] + 0.5))
                    s += idf * c[w] * 2.2 / (c[w] + 1.2 * (0.25 + 0.75 * len(ts) / self.avg))
            if s > 0:
                scored.append((s, i))
        scored.sort(reverse=True)
        return [{"title": self.docs[i][0], "text": self.docs[i][1], "source": self.docs[i][2], "score": round(s, 2)}
                for s, i in scored[:k]]
