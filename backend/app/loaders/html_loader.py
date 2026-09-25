from bs4 import BeautifulSoup

from app.loaders.base_loader import BaseLoader
from app.loaders.document_assembler import Block, assemble_documents, table_to_markdown

HEADING_TAGS = {f"h{n}": n for n in range(1, 7)}
TEXT_TAGS = {"p", "li", "blockquote", "pre"}


class HTMLLoader(BaseLoader):
    """
    HTML has explicit heading tags (h1-h6), so - like DOCX - there's
    no layout inference needed: the tag name directly gives the
    heading level. This walks the parsed tree in document order and
    hands off Blocks the same way every other loader does.
    """

    def load(self, file_path: str):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            soup = BeautifulSoup(f.read(), "html.parser")

        body = soup.body or soup

        blocks = []
        position = 0

        for tag in body.find_all(list(HEADING_TAGS) + list(TEXT_TAGS) + ["table"]):
            # skip tags nested inside a table or another block we've
            # already captured (e.g. a <p> inside a <li>) to avoid
            # duplicating content
            if tag.find_parent("table") is not None:
                continue

            if tag.name in HEADING_TAGS:
                text = tag.get_text(strip=True)
                if text:
                    blocks.append(
                        Block(
                            type="heading",
                            text=text,
                            level=HEADING_TAGS[tag.name],
                            page=position,
                        )
                    )
                    position += 1

            elif tag.name == "table":
                rows = [
                    [cell.get_text(strip=True) for cell in row.find_all(["th", "td"])]
                    for row in tag.find_all("tr")
                ]
                md = table_to_markdown(rows)
                if md:
                    blocks.append(Block(type="table", text=f"\n{md}\n", page=position))
                    position += 1

            else:
                text = tag.get_text(strip=True)
                if text:
                    blocks.append(Block(type="text", text=text, page=position))
                    position += 1

        return assemble_documents(blocks, source=file_path)