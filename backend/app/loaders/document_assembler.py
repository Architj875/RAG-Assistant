"""
Shared contract between format-specific loaders and the generic chunker.

Every loader (PDF, DOCX, HTML, TXT, Markdown, ...) is responsible for one
thing only: turning its source format into a flat, ordered list of Block
objects. Nothing downstream of that - section assembly, chunking,
abbreviation handling, context re-attachment - ever needs to know what
format the content came from.

This is the piece that makes the pipeline format-agnostic in practice,
not just in principle: a new loader only has to implement "what is a
heading, at what level, on what page/position" for its own format and
hand back Blocks. Everything else (grouping into sections, building
heading_path, producing chunker-ready Documents) is written once, here,
and is identical for a PDF, a Word doc, or an HTML page.
"""

from dataclasses import dataclass

from langchain_core.documents import Document


def table_to_markdown(rows: list) -> str:
    """
    Render a table (list of rows, each a list of cell strings) as
    markdown. Shared by any loader that extracts real tables (PDF via
    pdfplumber, DOCX via python-docx, HTML via <table> tags) so table
    rendering is identical regardless of source format.
    """
    rows = [[(cell or "").strip() for cell in row] for row in rows if row]
    if not rows:
        return ""
    header, *body = rows
    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(["---"] * len(header)) + " |",
    ]
    for row in body:
        row = row + [""] * (len(header) - len(row))
        lines.append("| " + " | ".join(row[: len(header)]) + " |")
    return "\n".join(lines)


@dataclass
class Block:
    """
    One structural unit of a document, in reading order.

    type: "heading" | "text" | "table"
    text: the block's content (for a table, pre-rendered as markdown)
    level: heading level (1 = top-level), meaningless for non-headings
    page: a 0-indexed page/position marker. Formats with real pages
          (PDF, DOCX) use the actual page number; formats without one
          (HTML, TXT, Markdown) can use a running section/paragraph
          counter - assemble_documents only needs it to detect where
          one span of content ends and the next begins.
    """

    type: str
    text: str
    level: int = 0
    page: int = 0


def assemble_documents(blocks: list[Block], source: str) -> list[Document]:
    """
    Generic block-to-section assembler.

    Walks an ordered Block list and groups content under detected
    headings into one Document per section - each carrying a
    heading_path built purely from the sequence of heading levels it
    saw, with no knowledge of where those blocks came from. Any loader
    that can express its content as Blocks gets identical section
    assembly, heading-path construction, and chunker-ready metadata
    for free.
    """
    documents: list[Document] = []
    heading_stack: list[tuple[int, str]] = []
    current_heading_path = ""
    current_lines: list[str] = []
    current_start_page = 0
    last_page = 0

    def flush(end_page: int):
        if not current_lines:
            return
        content = "\n".join(current_lines).strip()
        if not content:
            return
        documents.append(
            Document(
                page_content=content,
                metadata={
                    "source": source,
                    "page_start": current_start_page,
                    "page_end": end_page,
                    "heading_path": current_heading_path,
                },
            )
        )

    for b in blocks:
        last_page = b.page

        if b.type == "heading":
            flush(end_page=b.page)
            current_lines = []
            current_start_page = b.page

            heading_stack = [h for h in heading_stack if h[0] < b.level]
            heading_stack.append((b.level, b.text))
            current_heading_path = " > ".join(h[1] for h in heading_stack)

            current_lines.append(b.text)
        else:
            if not current_lines:
                current_start_page = b.page
            current_lines.append(b.text)

    flush(end_page=last_page)

    return documents