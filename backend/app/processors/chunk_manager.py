from pathlib import Path
import json

from langchain_core.documents import Document

from app.processors.cleaner import TextCleaner
from app.processors.chunker import TextChunker
from app.utils.logger import logger


class ChunkManager:
    """
    Coordinates document cleaning and chunking.

    The ChunkManager is responsible for:
    1. Cleaning loaded documents.
    2. Creating chunks using TextChunker.
    3. Writing a complete chunk dump for evaluation/debugging.
    4. Logging representative chunk information.
    """

    # ============================================================
    # CONFIGURATION
    # ============================================================

    SAMPLE_CHUNK_COUNT = 8

    SAMPLE_CONTENT_LENGTH = 1000

    # ============================================================
    # CHUNK DUMP PATH
    # ============================================================

    @staticmethod
    def _get_chunk_dump_path() -> Path:
        """
        Returns the absolute path to:

            backend/data/uploads/chunks_dump.json

        This avoids problems caused by the directory from which
        the FastAPI server is started.
        """

        backend_dir = (
            Path(__file__)
            .resolve()
            .parents[2]
        )

        data_dir = backend_dir / "data"

        data_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        return data_dir / "chunks_dump.json"

    # ============================================================
    # PUBLIC API
    # ============================================================

    @classmethod
    def process_documents(
        cls,
        documents: list[Document],
        chunk_size: int = 700,
        chunk_overlap: int = 120,
    ) -> list[Document]:

        # ========================================================
        # 1. CLEAN DOCUMENTS
        # ========================================================

        logger.info(
            "========== DOCUMENT CLEANING =========="
        )

        logger.info(
            "Documents received for cleaning: %d",
            len(documents),
        )

        cleaned_documents = (
            TextCleaner.clean_documents(
                documents
            )
        )

        logger.info(
            "Documents after cleaning: %d",
            len(cleaned_documents),
        )

        logger.info(
            "========== END DOCUMENT CLEANING =========="
        )

        # ========================================================
        # 2. CHUNK DOCUMENTS
        # ========================================================

        logger.info(
            "========== DOCUMENT CHUNKING =========="
        )

        logger.info(
            "Chunk size: %d",
            chunk_size,
        )

        logger.info(
            "Chunk overlap: %d",
            chunk_overlap,
        )

        chunks = (
            TextChunker.recursive_chunk_documents(
                cleaned_documents,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )
        )

        logger.info(
            "Generated %d chunks",
            len(chunks),
        )

        logger.info(
            "========== END DOCUMENT CHUNKING =========="
        )

        # ========================================================
        # 3. WRITE COMPLETE CHUNK DUMP
        # ========================================================

        cls._write_chunk_dump(
            chunks
        )

        # ========================================================
        # 4. CHUNK SAMPLES
        # ========================================================

        cls._log_chunk_samples(
            chunks
        )

        return chunks

    # ============================================================
    # COMPLETE CHUNK DUMP
    # ============================================================

    @classmethod
    def _write_chunk_dump(
        cls,
        chunks: list[Document],
    ) -> None:
        """
        Writes every generated chunk and its metadata to:

            backend/data/uploads/chunks_dump.json

        This is intended for debugging and retrieval evaluation.
        """

        logger.info(
            "========== WRITING FULL CHUNK DUMP =========="
        )

        dump = []

        for index, chunk in enumerate(chunks):

            metadata = chunk.metadata

            dump.append(
                {
                    # ------------------------------------------------
                    # Position in generated chunk list
                    # ------------------------------------------------

                    "index": index,

                    # ------------------------------------------------
                    # Chunk identity
                    # ------------------------------------------------

                    "chunk_id": metadata.get(
                        "chunk_id"
                    ),

                    # ------------------------------------------------
                    # Document information
                    # ------------------------------------------------

                    "source": metadata.get(
                        "source"
                    ),

                    # ------------------------------------------------
                    # Page information
                    # ------------------------------------------------

                    "page": metadata.get(
                        "page"
                    ),

                    "page_label": metadata.get(
                        "page_label"
                    ),

                    # ------------------------------------------------
                    # Section information
                    # ------------------------------------------------

                    "section_index": metadata.get(
                        "section_index"
                    ),

                    "section_title": metadata.get(
                        "section_title"
                    ),

                    "section_id": metadata.get(
                        "section_id"
                    ),

                    # ------------------------------------------------
                    # Chunk classification
                    # ------------------------------------------------

                    "chunk_type": metadata.get(
                        "chunk_type"
                    ),

                    # ------------------------------------------------
                    # Section chunk position
                    # ------------------------------------------------

                    "section_chunk_index": metadata.get(
                        "section_chunk_index"
                    ),

                    "section_chunk_count": metadata.get(
                        "section_chunk_count"
                    ),

                    # ------------------------------------------------
                    # Actual chunk text
                    # ------------------------------------------------

                    "content": chunk.page_content,
                }
            )

        dump_path = (
            cls._get_chunk_dump_path()
        )

        try:

            with dump_path.open(
                "w",
                encoding="utf-8",
            ) as file:

                json.dump(
                    dump,
                    file,
                    ensure_ascii=False,
                    indent=2,
                )

            logger.info(
                "Full chunk dump written successfully."
            )

            logger.info(
                "Chunk dump path: %s",
                dump_path,
            )

            logger.info(
                "Chunks written to dump: %d",
                len(dump),
            )

        except Exception:

            logger.exception(
                "Failed to write full chunk dump."
            )

        logger.info(
            "========== END FULL CHUNK DUMP =========="
        )

    # ============================================================
    # CHUNK SAMPLE LOGGING
    # ============================================================

    @classmethod
    def _log_chunk_samples(
        cls,
        chunks: list[Document],
    ) -> None:

        logger.info(
            "========== CHUNK SAMPLES =========="
        )

        if not chunks:

            logger.warning(
                "No chunks were generated."
            )

            logger.info(
                "========== END CHUNK SAMPLES =========="
            )

            return

        sample_count = min(
            cls.SAMPLE_CHUNK_COUNT,
            len(chunks),
        )

        for index in range(
            sample_count
        ):

            chunk = chunks[index]

            metadata = chunk.metadata

            source = metadata.get(
                "source",
                "Unknown",
            )

            page = metadata.get(
                "page",
                "Unknown",
            )

            page_label = metadata.get(
                "page_label",
                "Unknown",
            )

            section_index = metadata.get(
                "section_index",
                "Unknown",
            )

            section_title = metadata.get(
                "section_title",
                "",
            )

            section_id = metadata.get(
                "section_id",
                "Unknown",
            )

            chunk_type = metadata.get(
                "chunk_type",
                "Unknown",
            )

            chunk_id = metadata.get(
                "chunk_id",
                "Unknown",
            )

            section_chunk_index = metadata.get(
                "section_chunk_index",
                "Unknown",
            )

            section_chunk_count = metadata.get(
                "section_chunk_count",
                "Unknown",
            )

            content = (
                chunk.page_content
                .strip()
            )

            if len(content) > cls.SAMPLE_CONTENT_LENGTH:

                content = (
                    content[
                        :cls.SAMPLE_CONTENT_LENGTH
                    ]
                    + "..."
                )

            logger.info(
                "\n"
                "------------------------------------------------------------\n"
                "CHUNK SAMPLE %d\n"
                "------------------------------------------------------------\n"
                "Chunk ID: %s\n"
                "Source: %s\n"
                "Page Index: %s\n"
                "Page Label: %s\n"
                "Section Index: %s\n"
                "Section Title: %s\n"
                "Section ID: %s\n"
                "Chunk Type: %s\n"
                "Section Chunk: %s / %s\n"
                "Content:\n%s\n"
                "------------------------------------------------------------",

                index + 1,

                chunk_id,

                source,

                page,

                page_label,

                section_index,

                (
                    section_title
                    if section_title
                    else "None"
                ),

                section_id,

                chunk_type,

                (
                    section_chunk_index + 1
                    if isinstance(
                        section_chunk_index,
                        int,
                    )
                    else section_chunk_index
                ),

                section_chunk_count,

                content,
            )

        logger.info(
            "========== END CHUNK SAMPLES =========="
        )

    # ============================================================
    # FIRST CHUNK
    # ============================================================

    @classmethod
    def log_first_chunk(
        cls,
        chunks: list[Document],
    ) -> None:

        logger.info(
            "========== FIRST CHUNK =========="
        )

        if not chunks:

            logger.warning(
                "No chunks available."
            )

            logger.info(
                "========== END FIRST CHUNK =========="
            )

            return

        chunk = chunks[0]

        logger.info(
            "%s",
            chunk.page_content,
        )

        logger.info(
            "Metadata: %s",
            chunk.metadata,
        )

        logger.info(
            "========== END FIRST CHUNK =========="
        )