import hashlib
import re
from typing import Optional

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class TextChunker:

    # ============================================================
    # CONFIGURATION
    # ============================================================

    CHUNK_SIZE = 700
    CHUNK_OVERLAP = 120

    # Maximum number of words allowed for a structural heading.
    MAX_HEADING_WORDS = 14

    # Minimum amount of content expected after a heading.
    MIN_FOLLOWING_CONTENT_CHARS = 40

    # ============================================================
    # PUBLIC API
    # ============================================================

    @classmethod
    def recursive_chunk_documents(
        cls,
        documents: list[Document],
        chunk_size: int = CHUNK_SIZE,
        chunk_overlap: int = CHUNK_OVERLAP,
    ) -> list[Document]:

        final_chunks: list[Document] = []

        global_chunk_id = 0

        # --------------------------------------------------------
        # Process documents one by one.
        #
        # This preserves loader-provided metadata such as:
        #
        # source
        # page
        # page_label
        # total_pages
        # etc.
        # --------------------------------------------------------

        for document in documents:

            text = cls._clean_text(
                document.page_content
            )

            if not text:
                continue

            # ----------------------------------------------------
            # Normalize obvious PDF extraction artifacts.
            # ----------------------------------------------------

            text = cls._normalize_embedded_headings(
                text
            )

            # ----------------------------------------------------
            # Detect structural sections.
            #
            # If the loader already computed a heading for this
            # document (e.g. the PDF loader's `heading_path`,
            # built from real font-size/position signal), trust
            # it instead of re-guessing structure from flattened
            # text. Re-detecting on plain text has no font signal
            # to lean on, so it's strictly weaker than what the
            # loader already produced, and duplicating that work
            # risks reintroducing false-positive headings (e.g.
            # a wrapped sentence getting mistaken for a title).
            # ----------------------------------------------------

            heading_path = document.metadata.get(
                "heading_path"
            )

            if heading_path:

                sections = [
                    {
                        "title": heading_path,
                        "content": cls._strip_duplicate_heading_line(
                            text, heading_path
                        ),
                        "section_index": 0,
                    }
                ]

            else:

                sections = cls._detect_sections(
                    text
                )

                # ------------------------------------------------
                # If no reliable structure exists, treat the entire
                # document/page as one logical unit.
                # ------------------------------------------------

                if not sections:

                    sections = [
                        {
                            "title": "",
                            "content": text,
                            "section_index": 0,
                        }
                    ]

            # ====================================================
            # PROCESS SECTIONS
            # ====================================================

            for section in sections:

                section_title = section[
                    "title"
                ]

                section_content = section[
                    "content"
                ]

                section_index = section[
                    "section_index"
                ]

                if not section_content.strip():
                    continue

                # ------------------------------------------------
                # Expand abbreviations ("CL" -> "Casual Leave (CL)")
                # throughout the section content, not just once
                # wherever it's first defined. A chunk deep in a
                # long section may only ever say "CL" in its own
                # body text, giving a query naming "Casual Leave"
                # nothing to lexically/semantically match against
                # in that specific chunk.
                # ------------------------------------------------

                abbreviation_map = cls._extract_abbreviation_map(
                    heading_path or "",
                    section_content,
                )

                section_content = cls._expand_abbreviations(
                    section_content,
                    abbreviation_map,
                )

                # ------------------------------------------------
                # Split the RAW section content first, then
                # re-attach the section context ("Section: ...")
                # to EVERY resulting chunk individually.
                #
                # Prefixing once before splitting only protects
                # the first chunk of a section - any chunk further
                # into a long section (e.g. chunk 129 of a large
                # "Leave Policy" section) would otherwise contain
                # the actual rule text but none of the words from
                # its own heading, hurting both embedding
                # relevance and citation clarity for that chunk.
                # ------------------------------------------------

                chunks = cls._recursive_split(
                    section_content,
                    chunk_size,
                    chunk_overlap,
                )

                valid_chunks = []

                for chunk_text in chunks:

                    cleaned_chunk = (
                        cls._clean_chunk(
                            chunk_text
                        )
                    )

                    if not cleaned_chunk:
                        continue

                    # ------------------------------------------------
                    # Never create a vector containing only a heading.
                    # ------------------------------------------------

                    if cls._is_heading_only(
                        cleaned_chunk,
                        section_title,
                    ):
                        continue

                    chunk_with_context = (
                        cls._build_section_context(
                            section_title,
                            cleaned_chunk,
                        )
                    )

                    valid_chunks.append(
                        chunk_with_context
                    )

                section_chunk_count = len(
                    valid_chunks
                )

                # ====================================================
                # CREATE DOCUMENT OBJECTS
                # ====================================================

                for section_chunk_index, chunk_text in enumerate(
                    valid_chunks
                ):

                    metadata = dict(
                        document.metadata
                    )

                    # ------------------------------------------------
                    # Section metadata
                    # ------------------------------------------------

                    metadata[
                        "section_index"
                    ] = section_index

                    metadata[
                        "section_title"
                    ] = section_title

                    metadata[
                        "section_id"
                    ] = cls._build_section_id(
                        document,
                        section_index,
                        section_title,
                    )

                    location = cls._resolve_location(document.metadata)
                    metadata["location"] = location
                    metadata["location_kind"] = location.get("kind")
                    metadata["location_label"] = location.get("label")
                    metadata["location_start"] = location.get("start")
                    metadata["location_end"] = location.get("end")

                    if location.get("kind") == "page":
                        metadata["page"] = location.get("start")
                        metadata["page_label"] = location.get("label")
                    else:
                        metadata["page"] = None
                        metadata["page_label"] = None

                    # ------------------------------------------------
                    # Chunk metadata
                    # ------------------------------------------------

                    metadata[
                        "chunk_type"
                    ] = cls._detect_chunk_type(
                        chunk_text
                    )

                    metadata[
                        "section_chunk_index"
                    ] = section_chunk_index

                    metadata[
                        "section_chunk_count"
                    ] = section_chunk_count

                    metadata[
                        "chunk_id"
                    ] = global_chunk_id

                    # ------------------------------------------------
                    # chunk_id is sequential and SHIFTS any time the
                    # loader/chunker changes. A golden evaluation
                    # dataset built against chunk_id will silently go
                    # stale on the next pipeline change, scoring
                    # correct retrievals as misses.
                    #
                    # chunk_uid is a stable hash of source + heading +
                    # content, so a golden dataset can reference it
                    # instead and survive re-chunking.
                    # ------------------------------------------------

                    metadata["chunk_uid"] = cls._build_chunk_uid(
                        document.metadata.get("source", "unknown"),
                        section_title,
                        chunk_text,
                    )

                    final_chunks.append(
                        Document(
                            page_content=chunk_text,
                            metadata=metadata,
                        )
                    )

                    global_chunk_id += 1

        return final_chunks

    # ============================================================
    # ABBREVIATION EXPANSION
    # ============================================================

    ABBREVIATION_DEF_PATTERN = re.compile(
        r"\b([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+){0,4})\s*\(([A-Z]{2,6})\)"
    )

    @classmethod
    def _extract_abbreviation_map(
        cls,
        heading_path: str,
        content: str,
    ) -> dict:

        # --------------------------------------------------------
        # Find "Full Term (ABBR)" definitions in the heading path
        # and/or the section's own content, e.g. "Casual Leave (CL)".
        # The heading is checked first so it takes precedence if a
        # term is defined differently in multiple places.
        # --------------------------------------------------------

        mapping: dict = {}

        for source in (heading_path, content):

            if not source:
                continue

            for match in cls.ABBREVIATION_DEF_PATTERN.finditer(
                source
            ):

                full = match.group(1).strip()
                abbr = match.group(2).strip()

                if abbr not in mapping:
                    mapping[abbr] = full

        return mapping

    @classmethod
    def _expand_abbreviations(
        cls,
        content: str,
        abbreviation_map: dict,
    ) -> str:

        if not abbreviation_map:
            return content

        # --------------------------------------------------------
        # Replace standalone abbreviation mentions with
        # "Full Term (ABBR)", but skip occurrences already inside
        # parentheses (the original definition itself) or already
        # immediately followed by their own definition (don't turn
        # "Casual Leave (CL)" into "Casual Leave (CL) (CL)").
        # --------------------------------------------------------

        pattern = re.compile(
            r"(?<!\()\b("
            + "|".join(
                re.escape(abbr) for abbr in abbreviation_map
            )
            + r")\b(?!\s*\()"
        )

        def replace(match: re.Match) -> str:

            abbr = match.group(1)

            full = abbreviation_map.get(abbr)

            if not full:
                return abbr

            return f"{full} ({abbr})"

        return pattern.sub(replace, content)

    # ============================================================
    # DUPLICATE HEADING STRIPPING
    # ============================================================

    @staticmethod
    def _strip_duplicate_heading_line(
        text: str,
        heading_path: str,
    ) -> str:

        # ----------------------------------------------------
        # The PDF loader includes the heading's own text as the
        # first line of a section's content (it doesn't know the
        # chunker will re-add it via `Section: ...`). Drop it here
        # if present, comparing against the leaf of the heading
        # path, so we don't end up with "Section: Leave Policy"
        # followed immediately by a duplicate "Leave Policy" line.
        # ----------------------------------------------------

        leaf = heading_path.split(">")[-1].strip().lower()

        lines = text.splitlines()

        if lines and lines[0].strip().lower() == leaf:
            return "\n".join(lines[1:]).strip()

        return text

    # ============================================================
    # TEXT CLEANING
    # ============================================================

    @staticmethod
    def _clean_text(
        text: str,
    ) -> str:

        if not text:
            return ""

        # --------------------------------------------------------
        # Unicode whitespace
        # --------------------------------------------------------

        text = text.replace(
            "\u00a0",
            " ",
        )

        # --------------------------------------------------------
        # Normalize dash variants.
        # --------------------------------------------------------

        text = text.replace(
            "\u2013",
            "-",
        )

        text = text.replace(
            "\u2014",
            "-",
        )

        text = text.replace(
            "\u2212",
            "-",
        )

        # --------------------------------------------------------
        # Normalize common bullets.
        # --------------------------------------------------------

        text = text.replace(
            "\u25cf",
            "\u2022",
        )

        # --------------------------------------------------------
        # Normalize tabs.
        # --------------------------------------------------------

        text = text.replace(
            "\t",
            " ",
        )

        # --------------------------------------------------------
        # Normalize spaces.
        # --------------------------------------------------------

        text = re.sub(
            r"[ ]{2,}",
            " ",
            text,
        )

        # --------------------------------------------------------
        # Normalize line whitespace.
        # --------------------------------------------------------

        text = re.sub(
            r"[ \t]+\n",
            "\n",
            text,
        )

        text = re.sub(
            r"\n[ \t]+",
            "\n",
            text,
        )

        # --------------------------------------------------------
        # Avoid huge blank-line gaps.
        # --------------------------------------------------------

        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text,
        )

        return text.strip()

    # ============================================================
    # EMBEDDED HEADING NORMALIZATION
    # ============================================================

    @classmethod
    def _normalize_embedded_headings(
        cls,
        text: str,
    ) -> str:

        lines = text.splitlines()

        normalized_lines = []

        for line in lines:

            line = line.strip()

            if not line:
                normalized_lines.append("")
                continue

            separated = (
                cls._split_numbered_embedded_heading(
                    line
                )
            )

            if separated:

                heading, content = separated

                normalized_lines.append(
                    heading
                )

                if content:
                    normalized_lines.append(
                        content
                    )

                continue

            normalized_lines.append(
                line
            )

        return "\n".join(
            normalized_lines
        )

    # ============================================================
    # GENERIC EMBEDDED NUMBERED HEADING
    # ============================================================

    @classmethod
    def _split_numbered_embedded_heading(
        cls,
        line: str,
    ) -> Optional[tuple[str, str]]:

        match = re.match(
            r"^\s*(\d+(?:\.\d+)*\.?)\s+(.+?)\s*$",
            line,
        )

        if not match:
            return None

        number = match.group(1)

        remainder = match.group(2).strip()

        if (
            cls._looks_like_heading_line(
                remainder
            )
        ):
            return None

        boundary = cls._find_title_body_boundary(
            remainder
        )

        if boundary is None:
            return None

        title = remainder[
            :boundary
        ].strip()

        body = remainder[
            boundary:
        ].strip()

        if not title or not body:
            return None

        if not cls._looks_like_heading_line(
            title
        ):
            return None

        return (
            f"{number} {title}",
            body,
        )

    # ============================================================
    # GENERIC TITLE/BODY BOUNDARY
    # ============================================================

    @staticmethod
    def _find_title_body_boundary(
        text: str,
    ) -> Optional[int]:

        for index in range(1, len(text)):

            previous = text[
                index - 1
            ]

            current = text[
                index
            ]

            if (
                previous.islower()
                and current.isupper()
            ):

                candidate_title = (
                    text[:index].strip()
                )

                candidate_body = (
                    text[index:].strip()
                )

                if (
                    1
                    <= len(
                        candidate_title.split()
                    )
                    <= TextChunker.MAX_HEADING_WORDS
                ):

                    if (
                        len(candidate_body)
                        >= TextChunker.MIN_FOLLOWING_CONTENT_CHARS
                    ):

                        if not re.search(
                            r"[.!?]\s*$",
                            candidate_title,
                        ):

                            return index

        return None

    # ============================================================
    # SECTION DETECTION
    # ============================================================

    @classmethod
    def _detect_sections(
        cls,
        text: str,
    ) -> list[dict]:

        lines = [
            line.strip()
            for line in text.splitlines()
        ]

        lines = [
            line
            for line in lines
            if line
        ]

        if not lines:
            return []

        sections = []

        current_title = ""

        current_content = []

        section_index = 0

        for index, line in enumerate(
            lines
        ):

            is_heading = (
                cls._is_structural_heading(
                    lines,
                    index,
                )
            )

            if is_heading:

                if current_content:

                    content = "\n".join(
                        current_content
                    ).strip()

                    if content:

                        sections.append(
                            {
                                "title": current_title,
                                "content": content,
                                "section_index": section_index,
                            }
                        )

                        section_index += 1

                current_title = (
                    cls._clean_heading(
                        line
                    )
                )

                current_content = []

                continue

            current_content.append(
                line
            )

        if current_content:

            content = "\n".join(
                current_content
            ).strip()

            if content:

                sections.append(
                    {
                        "title": current_title,
                        "content": content,
                        "section_index": section_index,
                    }
                )

        has_headings = any(
            section["title"]
            for section in sections
        )

        if not has_headings:
            return []

        return sections

    # ============================================================
    # STRUCTURAL HEADING DETECTION
    # ============================================================

    @classmethod
    def _is_structural_heading(
        cls,
        lines: list[str],
        index: int,
    ) -> bool:

        line = lines[index].strip()

        if not line:
            return False

        if re.match(
            r"^#{1,6}\s+\S+",
            line,
        ):
            return True

        numbered = re.match(
            r"^\s*\d+(?:\.\d+)*\.?\s+(.+?)\s*$",
            line,
        )

        if numbered:

            title = numbered.group(1).strip()

            if (
                cls._looks_like_heading_line(
                    title
                )
                and cls._has_following_content(
                    lines,
                    index,
                )
            ):
                return True

        roman = re.match(
            r"^\s*[IVXLCDM]+\.?\s+(.+?)\s*$",
            line,
            re.IGNORECASE,
        )

        if roman:

            title = roman.group(1).strip()

            if (
                cls._looks_like_heading_line(
                    title
                )
                and cls._has_following_content(
                    lines,
                    index,
                )
            ):
                return True

        if (
            cls._is_short_line(line)
            and line.isupper()
            and any(
                char.isalpha()
                for char in line
            )
        ):

            if cls._has_following_content(
                lines,
                index,
            ):
                return True

        if cls._is_short_line(line):

            if cls._has_heading_context(
                lines,
                index,
            ):

                if cls._looks_like_heading_line(
                    line
                ):

                    next_line = cls._next_non_empty_line(
                        lines, index
                    )

                    if not cls._looks_like_continuation(
                        line, next_line
                    ):

                        return True

        return False

    # ============================================================
    # SENTENCE CONTINUATION GUARD
    # ============================================================

    @staticmethod
    def _next_non_empty_line(
        lines: list[str],
        index: int,
    ) -> str:

        for next_index in range(index + 1, len(lines)):

            candidate = lines[next_index].strip()

            if candidate:
                return candidate

        return ""

    @staticmethod
    def _looks_like_continuation(
        candidate_line: str,
        next_line: str,
    ) -> bool:

        candidate_line = candidate_line.strip()
        next_line = next_line.strip()

        if not candidate_line or not next_line:
            return False

        ends_open = not re.search(
            r"[.!?:]\s*$", candidate_line
        )

        next_starts_lowercase = bool(
            re.match(r"^[a-z]", next_line)
        )

        continuation_words = {
            "can", "will", "may", "shall", "must", "is", "are",
            "was", "were", "and", "or", "of", "to", "for",
        }

        next_first_word = (
            next_line.split(" ")[0].lower()
            if next_line
            else ""
        )

        return ends_open and (
            next_starts_lowercase
            or next_first_word in continuation_words
        )

    # ============================================================
    # HEADING LINE QUALITY
    # ============================================================

    @classmethod
    def _looks_like_heading_line(
        cls,
        line: str,
    ) -> bool:

        line = line.strip()

        if not line:
            return False

        words = line.split()

        if len(words) > cls.MAX_HEADING_WORDS:
            return False

        if re.search(
            r"[.!?]\s*$",
            line,
        ):
            return False

        if len(line) > 120:
            return False

        if not any(
            char.isalpha()
            for char in line
        ):
            return False

        alphanumeric = sum(
            char.isalnum()
            for char in line
        )

        if alphanumeric < 2:
            return False

        return True

    # ============================================================
    # SHORT LINE
    # ============================================================

    @classmethod
    def _is_short_line(
        cls,
        line: str,
    ) -> bool:

        return (
            len(line) <= 100
            and len(line.split())
            <= cls.MAX_HEADING_WORDS
        )

    # ============================================================
    # FOLLOWING CONTENT
    # ============================================================

    @staticmethod
    def _has_following_content(
        lines: list[str],
        index: int,
    ) -> bool:

        for next_index in range(
            index + 1,
            min(
                len(lines),
                index + 4,
            ),
        ):

            next_line = (
                lines[next_index].strip()
            )

            if not next_line:
                continue

            if re.match(
                r"^#{1,6}\s+",
                next_line,
            ):
                return False

            if len(next_line) >= 40:
                return True

            if len(next_line.split()) >= 5:
                return True

            return False

        return False

    # ============================================================
    # HEADING CONTEXT
    # ============================================================

    @classmethod
    def _has_heading_context(
        cls,
        lines: list[str],
        index: int,
    ) -> bool:

        if not cls._has_following_content(
            lines,
            index,
        ):
            return False

        for next_index in range(
            index + 1,
            min(
                len(lines),
                index + 4,
            ),
        ):

            next_line = (
                lines[next_index].strip()
            )

            if not next_line:
                continue

            if len(next_line) >= 80:
                return True

            if len(next_line.split()) >= 10:
                return True

            break

        return False

    # ============================================================
    # BUILD SECTION CONTEXT
    # ============================================================

    @staticmethod
    def _build_section_context(
        section_title: str,
        content: str,
    ) -> str:

        content = content.strip()

        if not section_title:
            return content

        return (
            f"Section: {section_title}\n\n"
            f"{content}"
        )

    # ============================================================
    # RECURSIVE SPLITTING
    # ============================================================

    @staticmethod
    def _recursive_split(
        text: str,
        chunk_size: int,
        chunk_overlap: int,
    ) -> list[str]:

        splitter = (
            RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                separators=[
                    "\n\n",
                    "\n",
                    "\u2022 ",
                    "\u25cf ",
                    "- ",
                    ". ",
                    "? ",
                    "! ",
                    "; ",
                    ", ",
                    " ",
                    "",
                ],
                keep_separator=True,
            )
        )

        return splitter.split_text(
            text
        )

    # ============================================================
    # CHUNK CLEANUP
    # ============================================================

    @staticmethod
    def _clean_chunk(
        text: str,
    ) -> str:

        text = text.strip()

        text = re.sub(
            r"^[\s.,;:\-]+",
            "",
            text,
        )

        if not re.search(
            r"[A-Za-z0-9]",
            text,
        ):
            return ""

        return text.strip()

    # ============================================================
    # HEADING-ONLY CHUNK CHECK
    # ============================================================

    @staticmethod
    def _is_heading_only(
        chunk: str,
        section_title: str,
    ) -> bool:

        if not section_title:
            return False

        normalized_chunk = (
            chunk.strip()
            .lower()
        )

        normalized_title = (
            section_title.strip()
            .lower()
        )

        if normalized_chunk == normalized_title:
            return True

        if normalized_chunk in (
            f"section: {normalized_title}",
            f"section:{normalized_title}",
        ):
            return True

        return False

    # ============================================================
    # CHUNK TYPE
    # ============================================================

    @staticmethod
    def _detect_chunk_type(
        text: str,
    ) -> str:

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        if not lines:
            return "text"

        table_signals = 0

        for line in lines:

            if "|" in line:
                table_signals += 1

            elif "\t" in line:
                table_signals += 1

            elif re.search(
                r"\s{3,}",
                line,
            ):
                table_signals += 1

        if (
            len(lines) >= 2
            and table_signals
            >= max(
                2,
                len(lines) // 2,
            )
        ):
            return "table"

        list_lines = sum(
            1
            for line in lines
            if re.match(
                r"^(?:[-*\u2022\u25cf]|\d+[.)])\s+",
                line,
            )
        )

        if (
            len(lines) >= 2
            and list_lines
            >= len(lines) // 2
        ):
            return "list"

        return "text"

    # ============================================================
    # SECTION ID
    # ============================================================

    # ============================================================
    # STABLE CHUNK IDENTIFIER
    # ============================================================

    @staticmethod
    def _build_chunk_uid(
        source: str,
        section_title: str,
        chunk_text: str,
    ) -> str:

        fingerprint = f"{source}|{section_title}|{chunk_text}"

        return hashlib.sha1(
            fingerprint.encode("utf-8")
        ).hexdigest()[:16]

    @classmethod
    def _build_section_id(
        cls,
        document: Document,
        section_index: int,
        section_title: str,
    ) -> str:

        source = document.metadata.get(
            "source",
            "unknown",
        )

        page = cls._resolve_page_label(
            document.metadata
        )

        title = (
            cls._normalize_identifier(
                section_title
            )
        )

        if not title:
            title = "untitled"

        return (
            f"{source}"
            f":page-{page}"
            f":section-{section_index}"
            f":{title}"
        )

    # ============================================================
    # PAGE LABEL RESOLUTION
    # ============================================================

    @staticmethod
    def _resolve_location(metadata: dict) -> dict:
        """
        Returns a normalized generic location dict:
        {
            "kind": "page" | "row" | "line" | "section" | "element" | "document",
            "start": ...,
            "end": ...,
            "label": ...
        }
        """
        location = metadata.get("location")

        if isinstance(location, dict):
            kind = location.get("kind") or "document"
            start = location.get("start")
            end = location.get("end")
            label = location.get("label")

            if label:
                return {
                    "kind": kind,
                    "start": start,
                    "end": end,
                    "label": label,
                }

            if kind == "page":
                if start == end:
                    return {
                        "kind": "page",
                        "start": start,
                        "end": end,
                        "label": f"p. {start}",
                    }
                return {
                    "kind": "page",
                    "start": start,
                    "end": end,
                    "label": f"pp. {start}-{end}",
                }

            if kind == "row":
                if start == end:
                    return {
                        "kind": "row",
                        "start": start,
                        "end": end,
                        "label": f"Row {start}",
                    }
                return {
                    "kind": "row",
                    "start": start,
                    "end": end,
                    "label": f"Rows {start}-{end}",
                }

            if kind == "line":
                if start == end:
                    return {
                        "kind": "line",
                        "start": start,
                        "end": end,
                        "label": f"Line {start}",
                    }
                return {
                    "kind": "line",
                    "start": start,
                    "end": end,
                    "label": f"Lines {start}-{end}",
                }

            if kind == "section":
                return {
                    "kind": "section",
                    "start": start,
                    "end": end,
                    "label": f"Section: {start}",
                }

            if kind == "element":
                return {
                    "kind": "element",
                    "start": start,
                    "end": end,
                    "label": f"Element: {start}",
                }

            return {
                "kind": "document",
                "start": None,
                "end": None,
                "label": "Document",
            }

        page = metadata.get("page")
        if page is not None:
            return {
                "kind": "page",
                "start": page,
                "end": page,
                "label": f"p. {page}",
            }

        page_start = metadata.get("page_start")
        page_end = metadata.get("page_end")

        if page_start is not None:
            end = page_end if page_end is not None else page_start

            if page_start == end:
                return {
                    "kind": "page",
                    "start": page_start,
                    "end": end,
                    "label": f"p. {page_start}",
                }

            return {
                "kind": "page",
                "start": page_start,
                "end": end,
                "label": f"pp. {page_start}-{end}",
            }

        return {
            "kind": "document",
            "start": None,
            "end": None,
            "label": "Document",
        }

    @staticmethod
    def _resolve_page_label(
        metadata: dict,
    ) -> str:

        if isinstance(metadata.get("location"), dict):
            location = metadata["location"]
            label = location.get("label")
            if label:
                return str(label)

            kind = location.get("kind")
            start = location.get("start")
            end = location.get("end")

            if kind == "page":
                if start == end:
                    return str(start)
                return f"{start}-{end}"

            if kind == "row":
                if start == end:
                    return str(start)
                return f"{start}-{end}"

            if kind == "line":
                if start == end:
                    return str(start)
                return f"{start}-{end}"

            if kind == "section":
                return str(start)

            if kind == "element":
                return str(start)

        if "page" in metadata and metadata["page"] is not None:
            return str(metadata["page"])

        page_start = metadata.get("page_start")
        page_end = metadata.get("page_end")

        if page_start is not None and page_end is not None:
            if page_start == page_end:
                return str(page_start)
            return f"{page_start}-{page_end}"

        return "unknown"

    # ============================================================
    # IDENTIFIER NORMALIZATION
    # ============================================================

    @staticmethod
    def _normalize_identifier(
        text: str,
    ) -> str:

        if not text:
            return ""

        text = text.lower()

        text = re.sub(
            r"[^a-z0-9]+",
            "-",
            text,
        )

        text = re.sub(
            r"-+",
            "-",
            text,
        )

        return text.strip("-")

    # ============================================================
    # HEADING CLEANUP
    # ============================================================

    @staticmethod
    def _clean_heading(
        line: str,
    ) -> str:

        line = line.strip()

        line = re.sub(
            r"^#{1,6}\s*",
            "",
            line,
        )

        line = re.sub(
            r"\s+",
            " ",
            line,
        )

        return line.strip()