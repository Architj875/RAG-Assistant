from app.loaders.base_loader import BaseLoader
from app.loaders.document_assembler import Block, assemble_documents


class TXTLoader(BaseLoader):
    """
    Plain text has no structural signal at all - no font size, no
    style names, no tags, no '#' markers. This loader honestly
    reflects that: it emits paragraph-level text Blocks with no
    headings, which means assemble_documents() produces a single
    Document per file with an empty heading_path. That's not a gap -
    it's the correct handoff. The chunker already has its own
    text-based heading heuristics (_detect_sections) specifically
    for sources like this one that arrive with no known structure.
    """

    def load(self, file_path: str):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]

        blocks = [
            Block(type="text", text=p, page=i) for i, p in enumerate(paragraphs)
        ]

        return assemble_documents(blocks, source=file_path)