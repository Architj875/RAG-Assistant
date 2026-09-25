"use client";

import {
  useEffect,
  useRef,
  useState,
} from "react";

import { createPortal } from "react-dom";

import { FileText } from "lucide-react";

import { Source } from "@/types/api";

interface Props {
  source: Source;
}

interface PopupPosition {
  top: number;
  left: number;
}

export default function SourceCard({
  source,
}: Props) {
  const citationRef =
    useRef<HTMLButtonElement>(null);

  const [open, setOpen] =
    useState(false);

  const [position, setPosition] =
    useState<PopupPosition | null>(null);

  /**
   * Convert the backend page label into
   * a human-friendly UI label.
   *
   * Backend:
   *   "p. 31"
   *   "pp. 20-25"
   *
   * UI:
   *   "Page 31"
   *   "Pages 20-25"
   */
  const formatPageLabel = (
    pageLabel: string | null
  ): string => {
    if (!pageLabel) {
      return "Document source";
    }

    if (pageLabel.startsWith("pp. ")) {
      return `Pages ${pageLabel.slice(4)}`;
    }

    if (pageLabel.startsWith("p. ")) {
      return `Page ${pageLabel.slice(3)}`;
    }

    return pageLabel;
  };

  const updatePosition = () => {
    const element =
      citationRef.current;

    if (!element) {
      return;
    }

    const rect =
      element.getBoundingClientRect();

    const popupWidth = 270;

    let left =
      rect.left +
      rect.width / 2 -
      popupWidth / 2;

    const horizontalPadding = 12;

    left = Math.max(
      horizontalPadding,
      Math.min(
        left,
        window.innerWidth -
          popupWidth -
          horizontalPadding
      )
    );

    const top =
      rect.top - 8;

    setPosition({
      top,
      left,
    });
  };

  const handleClick = () => {
    updatePosition();

    setOpen(
      (previous) => !previous
    );
  };

  useEffect(() => {
    if (!open) {
      return;
    }

    const handleUpdate = () => {
      updatePosition();
    };

    window.addEventListener(
      "scroll",
      handleUpdate,
      true
    );

    window.addEventListener(
      "resize",
      handleUpdate
    );

    return () => {
      window.removeEventListener(
        "scroll",
        handleUpdate,
        true
      );

      window.removeEventListener(
        "resize",
        handleUpdate
      );
    };
  }, [open]);

  useEffect(() => {
    if (!open) {
      return;
    }

    const handleOutsideClick = (
      event: MouseEvent
    ) => {
      const target =
        event.target as Node;

      if (
        citationRef.current &&
        !citationRef.current.contains(
          target
        )
      ) {
        setOpen(false);
      }
    };

    document.addEventListener(
      "mousedown",
      handleOutsideClick
    );

    return () => {
      document.removeEventListener(
        "mousedown",
        handleOutsideClick
      );
    };
  }, [open]);

  return (
    <>
      {/* =====================================================
          CITATION BUTTON
      ====================================================== */}

      <button
        ref={citationRef}
        type="button"
        onClick={handleClick}
        aria-label={`View source ${source.citation_id}`}
        aria-expanded={open}
        className="
          inline-flex
          h-4.5
          min-w-4.5
          items-center
          justify-center

          rounded-[5px]

          border
          border-primary/20

          bg-primary/8

          px-1

          align-baseline

          cursor-pointer

          text-[9px]
          font-semibold
          leading-none
          text-primary

          -translate-y-px

          transition-all
          duration-200

          hover:border-primary/40
          hover:bg-primary/16
        "
      >
        {source.citation_id}
      </button>

      {/* =====================================================
          SOURCE POPUP
          Rendered into document.body so it is not clipped
          by the chat container.
      ====================================================== */}

      {open &&
        position &&
        typeof document !==
          "undefined" &&
        createPortal(
          <div
            className="
              pointer-events-none

              fixed

              z-9999

              w-67.5

              -translate-y-full

              rounded-xl

              border
              border-white/10

              bg-[#151715]

              px-3
              py-3

              text-left

              shadow-[0_14px_40px_rgba(0,0,0,0.50)]

              animate-in
              fade-in
              zoom-in-95
              duration-150
            "
            style={{
              top: position.top,
              left: position.left,
            }}
          >
            {/* =================================================
                ARROW
            ================================================== */}

            <span
              className="
                absolute

                -bottom-1

                left-1/2

                h-2
                w-2

                -translate-x-1/2

                rotate-45

                border-r
                border-b
                border-white/10

                bg-[#151715]
              "
            />

            {/* =================================================
                SOURCE INFORMATION
            ================================================== */}

            <div
              className="
                flex
                items-center
                gap-2.5
              "
            >
              {/* Icon */}

              <div
                className="
                  flex
                  h-8
                  w-8
                  shrink-0

                  items-center
                  justify-center

                  rounded-lg

                  border
                  border-primary/15

                  bg-primary/8
                "
              >
                <FileText
                  className="
                    h-4
                    w-4
                    text-primary
                  "
                />
              </div>

              {/* Source information */}

              <div
                className="
                  min-w-0
                  flex-1
                "
              >
                <div
                  className="
                    truncate

                    text-[11px]
                    font-medium
                    text-foreground
                  "
                >
                  {source.filename}
                </div>

                <div
                  className="
                    mt-0.5

                    text-[10px]
                    text-muted-foreground
                  "
                >
                  {formatPageLabel(
                    source.page_label
                  )}
                </div>
              </div>
            </div>

            {/* =================================================
                CITATION LABEL
            ================================================== */}

            <div
              className="
                mt-2.5

                border-t
                border-white/6

                pt-2

                text-[9px]
                uppercase
                tracking-[0.18em]

                text-muted-foreground
              "
            >
              Citation{" "}
              {source.citation_id}
            </div>
          </div>,
          document.body
        )}
    </>
  );
}