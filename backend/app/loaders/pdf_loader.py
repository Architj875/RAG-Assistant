import re
import statistics
from collections import defaultdict

import fitz
import pdfplumber

from langchain_core.documents import Document

from app.loaders.base_loader import BaseLoader


class PDFLoader(BaseLoader):
    """
    Layout-aware PDF loader for RAG ingestion.

    Pipeline:
      1. Extract text spans with font size / bold / position via PyMuPDF
         (get_text("dict"), NOT get_text("text") — plain text mode throws
         away the layout signal this whole pipeline depends on).
      2. Detect repeating header/footer zones by POSITION on the page
         (top/bottom N%), not exact string match — this catches boilerplate
         even when it varies slightly page to page (page numbers, dates).
      3. Extract tables separately via pdfplumber and exclude their regions
         from the text flow, so table cells never get scored as headings.
      4. Detect headings using font-size-relative-to-body-text scoring,
         with a sentence-continuation guard so wrapped sentences
         ("Deliberate abuse of Sick" + "Leave can lead to...") are never
         flagged as headings.
      5. Group content under detected headings and emit one Document per
         section (with page range + heading path in metadata) instead of
         one Document per page, so chunks carry real structure.
    """

    HEADER_ZONE_PCT = 0.08
    FOOTER_ZONE_PCT = 0.08
    BOILERPLATE_PAGE_RATIO = 0.5
    HEADING_SIZE_RATIO = 1.15  # heading font must be >= 1.15x body font size
    MAX_HEADING_LEN = 120

    TOC_TITLE_PATTERN = re.compile(
        r"^(table of contents|contents|index|list of contents)$", re.IGNORECASE
    )
    # matches lines ending in a page-number reference, with or without dot leaders
    # e.g. "Leave Policy ..... 12", "Leave Policy   12", "Leave Policy12"
    TOC_ENTRY_PATTERN = re.compile(r"[.\s]{0,}\d{1,4}\s*$")
    TOC_MIN_ENTRY_RATIO = 0.4  # fraction of a page's lines that must look like entries
    DROP_TABLE_OF_CONTENTS = True

    def load(self, file_path: str):
        doc = fitz.open(file_path)
        try:
            spans = self._extract_spans(doc)

            table_bboxes_by_page = self._extract_table_bboxes(file_path)
            spans = self._exclude_table_spans(spans, table_bboxes_by_page)

            boilerplate_zones = self._find_boilerplate_zones(spans, doc.page_count)
            spans = [s for s in spans if s["zone"] not in boilerplate_zones]

            if self.DROP_TABLE_OF_CONTENTS:
                toc_pages = self._find_toc_pages(spans)
                spans = [s for s in spans if s["page"] not in toc_pages]

            body_size = self._estimate_body_font_size(spans)
            spans = self._tag_headings(spans, body_size)

            tables_text_by_page = self._render_tables_text(file_path, table_bboxes_by_page)

            documents = self._build_documents(
                file_path, spans, tables_text_by_page, doc.page_count
            )
        finally:
            doc.close()

        return documents

    # ---------- extraction ----------

    # run-in heading detection: a bold prefix on a line, followed by
    # non-bold prose on the SAME line - common in legal/policy documents
    # where the sub-heading isn't its own paragraph/line, just a bolded
    # lead-in ("Attendance and Punctuality The Company expects...").
    # Font-size-only detection can never see these, since the heading
    # and the paragraph after it are literally one PyMuPDF "line".
    RUN_IN_MIN_BODY_CHARS = 40
    RUN_IN_MAX_HEADING_WORDS = 10

    def _extract_spans(self, doc):
        spans = []
        for page_index in range(len(doc)):
            page = doc[page_index]
            page_height = page.rect.height
            page_dict = page.get_text("dict")

            for block in page_dict.get("blocks", []):
                if block.get("type") != 0:  # 0 = text block, skip images
                    continue
                for line in block.get("lines", []):
                    line_spans = line.get("spans", [])
                    if not line_spans:
                        continue

                    bbox = line["bbox"]
                    zone = self._classify_zone(bbox, page_height)

                    run_in = self._split_run_in_heading(line_spans)

                    if run_in and zone == "body":
                        heading_text, body_text, heading_size, heading_bold = run_in

                        spans.append(
                            {
                                "text": heading_text,
                                "size": heading_size,
                                "bold": heading_bold,
                                "page": page_index,
                                "bbox": bbox,
                                "zone": zone,
                                "forced_heading": True,
                            }
                        )

                        if body_text:
                            spans.append(
                                {
                                    "text": body_text,
                                    "size": round(
                                        max(s["size"] for s in line_spans), 1
                                    ),
                                    "bold": False,
                                    "page": page_index,
                                    "bbox": bbox,
                                    "zone": zone,
                                    "forced_heading": False,
                                }
                            )
                        continue

                    text = "".join(s["text"] for s in line_spans).strip()
                    if not text:
                        continue

                    size = round(max(s["size"] for s in line_spans), 1)
                    bold = any(bool(s["flags"] & 2 ** 4) for s in line_spans)

                    spans.append(
                        {
                            "text": text,
                            "size": size,
                            "bold": bold,
                            "page": page_index,
                            "bbox": bbox,
                            "zone": zone,
                            "forced_heading": False,
                        }
                    )
        return spans

    @classmethod
    def _split_run_in_heading(cls, line_spans):
        """
        Detect a bold lead-in phrase followed by non-bold prose on the
        SAME line, and split them into (heading_text, body_text,
        heading_font_size, heading_bold). Returns None if the line
        doesn't match this pattern.
        """
        if len(line_spans) < 2:
            return None

        is_bold = lambda s: bool(s["flags"] & 2 ** 4)

        # find the run of leading bold spans
        prefix_end = 0
        while prefix_end < len(line_spans) and is_bold(line_spans[prefix_end]):
            prefix_end += 1

        if prefix_end == 0 or prefix_end == len(line_spans):
            return None  # no bold prefix, or the WHOLE line is bold

        heading_text = "".join(
            s["text"] for s in line_spans[:prefix_end]
        ).strip()
        body_text = "".join(
            s["text"] for s in line_spans[prefix_end:]
        ).strip()

        if not heading_text or not body_text:
            return None

        # heading candidate must look like a title, not a sentence
        # fragment: short, no trailing sentence punctuation, and the
        # body that follows must be substantial prose (rules out a
        # merely-emphasised word or two inside a normal sentence).
        if len(heading_text.split()) > cls.RUN_IN_MAX_HEADING_WORDS:
            return None
        if re.search(r"[.!?:,]\s*$", heading_text):
            return None
        if len(body_text) < cls.RUN_IN_MIN_BODY_CHARS:
            return None
        if not re.match(r"^[A-Z]", heading_text):
            return None
        # the body continuation should read like the start of a new
        # sentence (capitalised), not a grammatical continuation of
        # the heading phrase itself.
        if not re.match(r"^[A-Z]", body_text):
            return None

        heading_size = round(
            max(s["size"] for s in line_spans[:prefix_end]), 1
        )

        return heading_text, body_text, heading_size, True

    def _classify_zone(self, bbox, page_height):
        y0, y1 = bbox[1], bbox[3]
        if y1 < page_height * self.HEADER_ZONE_PCT:
            return "header"
        if y0 > page_height * (1 - self.FOOTER_ZONE_PCT):
            return "footer"
        return "body"

    # ---------- tables ----------

    def _extract_table_bboxes(self, file_path):
        """Return {page_index: [bbox, ...]} for detected tables (pdfplumber coords)."""
        bboxes_by_page = defaultdict(list)
        with pdfplumber.open(file_path) as pdf:
            for page_index, page in enumerate(pdf.pages):
                try:
                    found = page.find_tables()
                except Exception:
                    found = []
                for t in found:
                    bboxes_by_page[page_index].append(t.bbox)
        return bboxes_by_page

    def _render_tables_text(self, file_path, table_bboxes_by_page):
        """Return {page_index: [markdown_table_str, ...]}."""
        tables_by_page = defaultdict(list)
        with pdfplumber.open(file_path) as pdf:
            for page_index, page in enumerate(pdf.pages):
                if page_index not in table_bboxes_by_page:
                    continue
                try:
                    extracted = page.extract_tables()
                except Exception:
                    extracted = []
                for table in extracted:
                    md = self._table_to_markdown(table)
                    if md:
                        tables_by_page[page_index].append(md)
        return tables_by_page

    @staticmethod
    def _table_to_markdown(table):
        rows = [[(cell or "").strip() for cell in row] for row in table if row]
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

    def _exclude_table_spans(self, spans, table_bboxes_by_page):
        """Drop text spans whose center point falls inside a detected table bbox."""

        def inside(bbox, table_bbox):
            cx = (bbox[0] + bbox[2]) / 2
            cy = (bbox[1] + bbox[3]) / 2
            x0, top, x1, bottom = table_bbox
            return x0 <= cx <= x1 and top <= cy <= bottom

        cleaned = []
        for s in spans:
            page_tables = table_bboxes_by_page.get(s["page"], [])
            if any(inside(s["bbox"], tb) for tb in page_tables):
                continue
            cleaned.append(s)
        return cleaned

    # ---------- boilerplate (header/footer) ----------

    def _find_boilerplate_zones(self, spans, page_count):
        """
        A zone (header/footer) is boilerplate if it has text on a large
        fraction of pages — regardless of whether the text is identical
        across pages (page numbers / dates vary but the zone is still
        structurally a header or footer).
        """
        pages_hit = defaultdict(set)
        for s in spans:
            if s["zone"] in ("header", "footer"):
                pages_hit[s["zone"]].add(s["page"])

        boilerplate_zones = set()
        for zone, pages in pages_hit.items():
            if len(pages) >= page_count * self.BOILERPLATE_PAGE_RATIO:
                boilerplate_zones.add(zone)
        return boilerplate_zones

    # ---------- table of contents ----------

    def _find_toc_pages(self, spans):
        """
        Identify pages that belong to a Table of Contents so they can be
        dropped before heading tagging. ToC entries are frequently styled
        with the same font size as real headings, which is what causes
        them to get pushed onto the heading stack ("Table of Contents >
        Leave Policy") if not caught here.

        Strategy: find a page containing a "Table of Contents" / "Contents"
        title, then walk forward while each subsequent page is still mostly
        made of entry-like lines (short lines ending in a page number,
        typically with dot leaders). Stop at the first page that looks like
        real prose instead.
        """
        by_page = defaultdict(list)
        for s in spans:
            if s["zone"] == "body":
                by_page[s["page"]].append(s["text"])

        toc_start_pages = sorted(
            page
            for page, texts in by_page.items()
            if any(self.TOC_TITLE_PATTERN.match(t.strip()) for t in texts)
        )

        toc_pages = set()
        for start_page in toc_start_pages:
            page = start_page
            while page in by_page:
                texts = by_page[page]
                if not texts:
                    break
                is_title_page = page == start_page
                entry_like = sum(1 for t in texts if self.TOC_ENTRY_PATTERN.search(t))
                ratio = entry_like / len(texts)

                if is_title_page or ratio >= self.TOC_MIN_ENTRY_RATIO:
                    toc_pages.add(page)
                    page += 1
                else:
                    break

        return toc_pages

    # ---------- heading detection ----------

    def _estimate_body_font_size(self, spans):
        body_spans = [s for s in spans if s["zone"] == "body"]
        if not body_spans:
            return 10.0
        sizes = [s["size"] for s in body_spans]
        try:
            return statistics.mode(sizes)
        except statistics.StatisticsError:
            return sorted(sizes)[len(sizes) // 2]

    def _tag_headings(self, spans, body_size):
        body_spans = [s for s in spans if s["zone"] == "body"]

        for i, s in enumerate(body_spans):
            s["is_heading"] = False

            if s.get("forced_heading"):
                next_text = body_spans[i + 1]["text"] if i + 1 < len(body_spans) else ""
                if self._looks_like_continuation(s["text"], next_text):
                    continue
                s["is_heading"] = True
                s["heading_level"] = self._heading_level(s["size"], body_size)
                continue

            size_ok = s["size"] >= body_size * self.HEADING_SIZE_RATIO
            short_enough = len(s["text"]) <= self.MAX_HEADING_LEN
            not_lowercase_start = not re.match(r"^[a-z]", s["text"])

            if not (size_ok and short_enough and not_lowercase_start):
                continue

            next_text = body_spans[i + 1]["text"] if i + 1 < len(body_spans) else ""
            if self._looks_like_continuation(s["text"], next_text):
                continue

            s["is_heading"] = True
            s["heading_level"] = self._heading_level(s["size"], body_size)

        return body_spans

    @staticmethod
    def _looks_like_continuation(candidate_line, next_line):
        candidate_line = candidate_line.strip()
        next_line = next_line.strip()
        if not candidate_line or not next_line:
            return False

        ends_open = not re.search(r"[.!?:]\s*$", candidate_line)
        next_starts_lowercase = bool(re.match(r"^[a-z]", next_line))

        continuation_words = {
            "can", "will", "may", "shall", "must", "is", "are", "was",
            "were", "and", "or", "of", "to", "for", "the", "a", "an",
            "with", "by", "in", "on", "at", "as", "if", "when", "that",
            "which", "who", "not",
        }
        next_first_word = next_line.split(" ")[0].lower() if next_line else ""

        return ends_open and (next_starts_lowercase or next_first_word in continuation_words)

    @staticmethod
    def _heading_level(size, body_size):
        ratio = size / body_size if body_size else 1
        if ratio >= 1.6:
            return 1
        if ratio >= 1.35:
            return 2
        return 3

    # ---------- document assembly ----------

    def _build_documents(self, file_path, spans, tables_text_by_page, page_count):
        documents = []
        heading_stack = []  # [(level, text), ...] building the heading path
        current_heading_path = ""
        current_lines = []
        current_start_page = 0
        seen_tables = set()

        def flush(end_page):
            if not current_lines:
                return
            content = "\n".join(current_lines).strip()
            if not content:
                return
            documents.append(
                Document(
                    page_content=content,
                    metadata={
                        "source": file_path,
                        "page_start": current_start_page,
                        "page_end": end_page,
                        "heading_path": current_heading_path,
                    },
                )
            )

        last_page = 0
        for s in spans:
            page = s["page"]

            # emit any tables on pages we're passing through
            for p in range(last_page, page + 1):
                for t_idx, table_md in enumerate(tables_text_by_page.get(p, [])):
                    key = (p, t_idx)
                    if key in seen_tables:
                        continue
                    seen_tables.add(key)
                    current_lines.append(f"\n[Table on page {p + 1}]\n{table_md}\n")
            last_page = page

            if s["is_heading"]:
                flush(end_page=page)
                current_lines = []
                current_start_page = page

                level = s["heading_level"]
                heading_stack = [h for h in heading_stack if h[0] < level]
                heading_stack.append((level, s["text"]))
                current_heading_path = " > ".join(h[1] for h in heading_stack)

                current_lines.append(s["text"])
            else:
                if not current_lines:
                    current_start_page = page
                current_lines.append(s["text"])

        for p in range(last_page, page_count):
            for t_idx, table_md in enumerate(tables_text_by_page.get(p, [])):
                key = (p, t_idx)
                if key in seen_tables:
                    continue
                seen_tables.add(key)
                current_lines.append(f"\n[Table on page {p + 1}]\n{table_md}\n")

        flush(end_page=page_count - 1)

        return documents