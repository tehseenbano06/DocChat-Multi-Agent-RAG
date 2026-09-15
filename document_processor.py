from pathlib import Path
import hashlib
import pickle

from docling.document_converter import DocumentConverter
from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter

from config import settings

SUPPORTED = {".pdf", ".docx", ".txt", ".md"}

class DocumentProcessor:
    def __init__(self):
        self.converter = DocumentConverter()
        self.splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "Header 1"),
                ("##", "Header 2"),
                ("###", "Header 3"),
            ],
            strip_headers=False,
        )

    def _cache_path(self, digest):
        return Path("data") / "cache" / f"{digest}.pkl"

    def process(self, files):
        if not files:
            raise ValueError("Upload at least one PDF, DOCX, TXT, or Markdown file.")

        total = sum(Path(f.name).stat().st_size for f in files)
        if total > settings.max_total_size_bytes:
            raise ValueError(f"Files exceed {settings.max_total_size_mb} MB.")

        Path("data/cache").mkdir(parents=True, exist_ok=True)
        output = []
        seen = set()

        for f in files:
            path = Path(f.name)
            if path.suffix.lower() not in SUPPORTED:
                continue

            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            cache = self._cache_path(digest)

            if cache.exists():
                chunks = pickle.loads(cache.read_bytes())
            else:
                if path.suffix.lower() in {".txt", ".md"}:
                    markdown = path.read_text(encoding="utf-8", errors="ignore")
                else:
                    markdown = (
                        self.converter.convert(path)
                        .document.export_to_markdown()
                    )

                chunks = self.splitter.split_text(markdown)
                for c in chunks:
                    c.metadata.update({
                        "source": path.name,
                        "file_type": path.suffix.lower(),
                    })
                cache.write_bytes(pickle.dumps(chunks))

            for c in chunks:
                key = hashlib.sha256(c.page_content.encode()).hexdigest()
                if key not in seen and c.page_content.strip():
                    seen.add(key)
                    output.append(c)

        if not output:
            raise ValueError("No readable text was extracted.")
        return output
