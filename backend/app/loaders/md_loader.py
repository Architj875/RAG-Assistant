import re

from app.loaders.base_loader import BaseLoader
from app.loaders.document_assembler import Block, assemble_documents

HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


class MarkdownLoader(BaseLoader):
    """
    Markdown headings are just '#' counts - the simplest structure
    signal of any format this pipeline handles, no inference needed
    at all. Table syntax and other markdown constructs are left as
    plain text blocks rather than re-parsed: markdown tables are
    already human/embedding-readable in their raw form, unlike a
    PDF's positionally-scattered table text, so there's nothing to
    reconstruct.
    """

    def load(self, file_path: str):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.read().splitlines()

        blocks = []
        position = 0
        buffer = []

        def flush_buffer():
            nonlocal buffer, position
            text = "\n".join(buffer).strip()
            buffer = []
            if text:
                blocks.append(Block(type="text", text=text, page=position))
                position += 1

        for line in lines:
            match = HEADING_PATTERN.match(line)
            if match:
                flush_buffer()
                level = len(match.group(1))
                heading_text = match.group(2).strip()
                blocks.append(
                    Block(type="heading", text=heading_text, level=level, page=position)
                )
                position += 1
                continue

            if line.strip() == "":
                flush_buffer()
                continue

            buffer.append(line)

        flush_buffer()

        return assemble_documents(blocks, source=file_path)