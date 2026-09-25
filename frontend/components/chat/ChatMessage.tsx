"use client";

import {
  useEffect,
  useRef,
  useState,
} from "react";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import {
  Bot,
  User,
  FileText,
  X,
} from "lucide-react";

import { createPortal } from "react-dom";

import {
  ChatMessage as ChatMessageType,
} from "@/types/api";

interface Props {
  message: ChatMessageType;
}

interface CitationPosition {
  top: number;
  left: number;
  openBelow: boolean;
}

export default function ChatMessage({
  message,
}: Props) {

  const isUser =
    message.role === "user";

  const [
    activeCitation,
    setActiveCitation,
  ] = useState<number | null>(null);

  const [
    citationPosition,
    setCitationPosition,
  ] = useState<CitationPosition | null>(
    null
  );

  const activeButtonRef =
    useRef<HTMLButtonElement | null>(
      null
    );

  const popupRef =
    useRef<HTMLDivElement | null>(
      null
    );

  // ============================================================
  // CITATION-AWARE CONTENT
  // ============================================================

  function renderContent(
    content: string
  ) {

    if (
      isUser ||
      !message.sources ||
      message.sources.length === 0
    ) {
      return content;
    }

    return content.replace(
      /\[(\d+)\]/g,
      (
        match,
        citationNumber
      ) => {

        const citationId =
          Number(citationNumber);

        const source =
          message.sources?.find(
            (item) =>
              item.citation_id ===
              citationId
          );

        if (!source) {
          return match;
        }

        return `[${citationId}](#citation-${citationId})`;
      }
    );
  }

  // ============================================================
  // CALCULATE POPUP POSITION
  // ============================================================

  function calculateCitationPosition(
    button: HTMLButtonElement
  ) {

    const rect =
      button.getBoundingClientRect();

    const popupWidth = 280;

    const horizontalPadding = 12;

    const estimatedPopupHeight = 120;

    let left =
      rect.left +
      rect.width / 2 -
      popupWidth / 2;

    // ----------------------------------------------------------
    // Keep popup inside viewport horizontally
    // ----------------------------------------------------------

    left = Math.max(
      horizontalPadding,
      Math.min(
        left,
        window.innerWidth -
          popupWidth -
          horizontalPadding
      )
    );

    // ----------------------------------------------------------
    // Decide whether popup opens above or below
    // ----------------------------------------------------------

    const hasRoomAbove =
      rect.top >
      estimatedPopupHeight +
        horizontalPadding;

    const openBelow =
      !hasRoomAbove;

    const top = openBelow
      ? rect.bottom + 8
      : rect.top - 8;

    setCitationPosition({
      top,
      left,
      openBelow,
    });
  }

  // ============================================================
  // CITATION CLICK
  // ============================================================

  function handleCitationClick(
    citationId: number,
    button: HTMLButtonElement
  ) {

    // ----------------------------------------------------------
    // Clicking the currently open citation closes it.
    // ----------------------------------------------------------

    if (
      activeCitation === citationId &&
      activeButtonRef.current === button
    ) {

      setActiveCitation(null);

      setCitationPosition(null);

      activeButtonRef.current = null;

      return;
    }

    // ----------------------------------------------------------
    // Store the EXACT button that was clicked.
    //
    // This is important because multiple [1], [2], etc.
    // citations can exist in the same answer.
    // ----------------------------------------------------------

    activeButtonRef.current =
      button;

    calculateCitationPosition(
      button
    );

    setActiveCitation(
      citationId
    );
  }

  // ============================================================
  // KEEP POPUP POSITIONED
  // ============================================================

  useEffect(() => {

    if (
      activeCitation === null ||
      !activeButtonRef.current
    ) {
      return;
    }

    const handlePositionUpdate =
      () => {

        const button =
          activeButtonRef.current;

        if (!button) {
          return;
        }

        calculateCitationPosition(
          button
        );
      };

    window.addEventListener(
      "resize",
      handlePositionUpdate
    );

    window.addEventListener(
      "scroll",
      handlePositionUpdate,
      true
    );

    return () => {

      window.removeEventListener(
        "resize",
        handlePositionUpdate
      );

      window.removeEventListener(
        "scroll",
        handlePositionUpdate,
        true
      );
    };

  }, [activeCitation]);

  // ============================================================
  // CLOSE WHEN CLICKING OUTSIDE
  // ============================================================

  useEffect(() => {

    if (
      activeCitation === null
    ) {
      return;
    }

    function handleOutsideClick(
      event: MouseEvent
    ) {

      const target =
        event.target as Node;

      const clickedCitation =
        activeButtonRef.current?.contains(
          target
        );

      const clickedPopup =
        popupRef.current?.contains(
          target
        );

      if (
        clickedCitation ||
        clickedPopup
      ) {
        return;
      }

      setActiveCitation(null);

      setCitationPosition(null);

      activeButtonRef.current =
        null;
    }

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

  }, [activeCitation]);

  // ============================================================
  // INLINE CITATION
  // ============================================================

  function renderLink({
    href,
    children,
  }: {
    href?: string;
    children?: React.ReactNode;
  }) {

    if (
      href?.startsWith(
        "#citation-"
      )
    ) {

      const citationId =
        Number(
          href.replace(
            "#citation-",
            ""
          )
        );

      const source =
        message.sources?.find(
          (item) =>
            item.citation_id ===
            citationId
        );

      if (source) {

        return (
          <button
            type="button"
            onClick={(event) =>
              handleCitationClick(
                citationId,
                event.currentTarget
              )
            }
            className="
              mx-0.5
              inline-flex
              h-[19px]
              min-w-[19px]
              items-center
              justify-center
              rounded-md
              border
              border-white/[0.10]
              bg-white/[0.05]
              px-1
              align-baseline
              cursor-pointer
              text-[10px]
              font-semibold
              leading-none
              text-muted-foreground
              transition-all
              duration-200
              hover:border-primary/30
              hover:bg-primary/10
              hover:text-primary
            "
            aria-label={`View citation ${citationId}`}
          >
            {citationId}
          </button>
        );
      }
    }

    return (
      <a
        href={href}
        className="
          text-primary
          no-underline
          hover:underline
        "
      >
        {children}
      </a>
    );
  }

  // ============================================================
  // ACTIVE SOURCE
  // ============================================================

  const activeSource =
    message.sources?.find(
      (source) =>
        source.citation_id ===
        activeCitation
    );

  // ============================================================
  // RENDER
  // ============================================================

  return (
    <div
      className={`flex gap-3 ${
        isUser
          ? "justify-end"
          : "justify-start"
      }`}
    >

      {/* ======================================================
          ASSISTANT AVATAR
      ======================================================= */}

      {!isUser && (
        <div
          className="
            flex
            h-9
            w-9
            shrink-0
            items-center
            justify-center
            rounded-xl
            border
            border-primary/20
            bg-primary/10
            shadow-[0_0_18px_rgba(34,197,94,0.08)]
          "
        >
          <Bot
            className="
              h-4
              w-4
              text-primary
            "
          />
        </div>
      )}

      {/* ======================================================
          MESSAGE CONTAINER
      ======================================================= */}

      <div
        className={`min-w-0 max-w-[80%] ${
          isUser
            ? `
              rounded-2xl
              rounded-br-md
              border
              border-primary/15
              bg-primary/[0.08]
              px-5
              py-4
            `
            : `
              rounded-2xl
              border
              border-white/[0.06]
              bg-white/[0.025]
              px-5
              py-4
            `
        }`}
      >

        {/* ====================================================
            MARKDOWN MESSAGE
        ===================================================== */}

        <div
          className="
            prose
            prose-invert
            max-w-none
            text-sm
            leading-7
            prose-headings:font-semibold
            prose-headings:text-foreground
            prose-p:text-foreground
            prose-p:my-2
            prose-strong:text-foreground
            prose-li:text-foreground
            prose-li:my-1
            prose-a:text-primary
            prose-a:no-underline
            hover:prose-a:underline
            prose-code:text-primary
            prose-pre:overflow-x-auto
            prose-pre:border
            prose-pre:border-white/10
            prose-pre:bg-black/30
            prose-pre:rounded-xl
            prose-blockquote:border-primary/30
            prose-blockquote:text-muted-foreground
          "
        >
          <ReactMarkdown
            remarkPlugins={[
              remarkGfm,
            ]}
            components={{
              a: renderLink,
            }}
          >
            {renderContent(
              message.content
            )}
          </ReactMarkdown>
        </div>
      </div>

      {/* ======================================================
          CITATION POPUP
          Rendered into document.body so it is independent
          of the Markdown layout.
      ======================================================= */}

      {!isUser &&
        activeSource &&
        citationPosition &&
        typeof document !==
          "undefined" &&
        createPortal(
          <div
            ref={popupRef}
            className="
              fixed
              z-[9999]
              w-[280px]
              rounded-xl
              border
              border-white/[0.10]
              bg-[#151715]
              px-3
              py-3
              text-left
              shadow-[0_14px_40px_rgba(0,0,0,0.50)]
              backdrop-blur-xl
            "
            style={{
              top:
                citationPosition.top,
              left:
                citationPosition.left,
              transform:
                citationPosition.openBelow
                  ? "translateY(0)"
                  : "translateY(-100%)",
            }}
          >

            {/* =================================================
                ARROW
            ================================================== */}

            <span
              className="
                absolute
                left-1/2
                h-2
                w-2
                -translate-x-1/2
                rotate-45
                border-white/[0.10]
                bg-[#151715]
              "
              style={{
                top:
                  citationPosition.openBelow
                    ? "-4px"
                    : "auto",

                bottom:
                  citationPosition.openBelow
                    ? "auto"
                    : "-4px",

                borderLeftWidth:
                  "1px",

                borderTopWidth:
                  citationPosition.openBelow
                    ? "1px"
                    : "0px",

                borderRightWidth:
                  citationPosition.openBelow
                    ? "0px"
                    : "1px",

                borderBottomWidth:
                  citationPosition.openBelow
                    ? "0px"
                    : "1px",
              }}
            />

            {/* =================================================
                SOURCE HEADER
            ================================================== */}

            <div className="flex items-center gap-2.5">

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
                  bg-primary/[0.08]
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

              <div className="min-w-0 flex-1">

                <div
                  className="
                    truncate
                    text-[11px]
                    font-medium
                    text-foreground
                  "
                >
                  {activeSource.filename}
                </div>

                <div
                  className="
                    mt-0.5
                    text-[10px]
                    text-muted-foreground
                  "
                >
                  {activeSource.page_label !== null &&
                  activeSource.page_label !== undefined
                    ? activeSource.page_label.startsWith("pp. ")
                      ? `Pages ${activeSource.page_label.slice(4)}`
                      : activeSource.page_label.startsWith("p. ")
                        ? `Page ${activeSource.page_label.slice(3)}`
                        : activeSource.page_label
                    : activeSource.page !== null &&
                      activeSource.page !== undefined
                      ? `Page ${activeSource.page + 1}`
                      : "Document source"}
                </div>

              </div>

              <button
                type="button"
                onClick={() => {
                  setActiveCitation(
                    null
                  );

                  setCitationPosition(
                    null
                  );

                  activeButtonRef.current =
                    null;
                }}
                className="
                  flex
                  h-6
                  w-6
                  shrink-0
                  items-center
                  justify-center
                  rounded-md
                  text-muted-foreground
                  transition
                  hover:bg-white/[0.06]
                  hover:text-foreground
                "
                aria-label="Close citation"
              >
                <X
                  className="
                    h-3.5
                    w-3.5
                  "
                />
              </button>

            </div>

            {/* =================================================
                CITATION LABEL
            ================================================== */}

            <div
              className="
                mt-2.5
                border-t
                border-white/[0.06]
                pt-2
              "
            >
              <span
                className="
                  text-[9px]
                  uppercase
                  tracking-[0.18em]
                  text-muted-foreground
                "
              >
                Citation{" "}
                {activeSource.citation_id}
              </span>
            </div>

          </div>,
          document.body
        )}

      {/* ======================================================
          USER AVATAR
      ======================================================= */}

      {isUser && (
        <div
          className="
            flex
            h-9
            w-9
            shrink-0
            items-center
            justify-center
            rounded-xl
            border
            border-white/10
            bg-white/[0.04]
          "
        >
          <User
            className="
              h-4
              w-4
              text-muted-foreground
            "
          />
        </div>
      )}

    </div>
  );
}