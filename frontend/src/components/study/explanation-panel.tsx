"use client";

import { useEffect, useRef } from "react";
import { motion } from "framer-motion";
import { useTranslations } from "next-intl";
import { ArrowRight, Lightbulb, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Markdown } from "@/components/ui/markdown";
import { useTutorStream } from "@/components/tutor/use-tutor-stream";
import { useStudySessionStore } from "@/lib/stores/study-session";
import { getLocaleFromCookie } from "@/lib/api-client";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "/api";

interface Props {
  sessionId: string;
  onExplanationDone: () => void;
}

export function ExplanationPanel({ sessionId, onExplanationDone }: Props) {
  const t = useTranslations("study");
  const bodyRef = useRef<HTMLDivElement>(null);

  const explanation = useStudySessionStore((s) => s.explanation);
  const setExplanation = useStudySessionStore((s) => s.setExplanation);
  const completeExplanation = useStudySessionStore((s) => s.completeExplanation);
  const explanationComplete = useStudySessionStore((s) => s.explanationComplete);

  // Do NOT auto-advance to practice on `done` — the student needs time to
  // actually read the explanation. We mark the stream complete and render a
  // "Continue to practice" button; `onExplanationDone` fires only when the
  // student clicks it. (The backend has already flipped phase → practice in
  // the DB during the atomic explain→practice transition, so state is
  // consistent either way.)
  const stream = useTutorStream({
    onEvent: (event, data) => {
      if (event === "done") {
        try {
          const parsed = JSON.parse(data) as { content?: string };
          if (parsed.content) setExplanation(parsed.content, false);
        } catch {
          /* ignore */
        }
        completeExplanation();
        return true;
      }
      if (event === "error") {
        completeExplanation();
        return true;
      }
    },
  });

  // Mirror stream buffer into the store so the panel survives a re-render
  // and so /practice can proceed even if this component unmounts early.
  useEffect(() => {
    if (stream.streaming) {
      setExplanation(stream.buffer, true);
    }
  }, [stream.buffer, stream.streaming, setExplanation]);

  // Trigger the SSE stream. No mount-dedup ref: in React 18 StrictMode dev,
  // the previous pattern set the ref on mount-1 then was aborted by the
  // cleanup, leaving mount-2 to short-circuit and never restart the stream
  // (panel header showed but body stayed empty). Effect cleanup aborts a
  // stale stream; the next effect run starts a fresh one. Idempotent on
  // the backend side — `/advance` re-streams from the LLM if called twice.
  useEffect(() => {
    if (explanationComplete) return;
    stream.run(`${API_BASE}/study/sessions/${sessionId}/advance`, {
      method: "POST",
      headers: { "Accept-Language": getLocaleFromCookie() },
    });
    return () => {
      stream.abort();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sessionId, explanationComplete]);

  useEffect(() => {
    bodyRef.current?.scrollTo({
      top: bodyRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [explanation]);

  const showTyping = stream.streaming && !explanation;

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -8 }}
      transition={{ duration: 0.25, ease: "easeOut" }}
      className="rounded-2xl border border-border/70 bg-card/60 p-4 shadow-editorial-sm ring-1 ring-foreground/5"
    >
      <div className="flex items-start gap-3">
        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-amber-400/15 text-amber-600 ring-1 ring-amber-400/25 dark:text-amber-300">
          <Lightbulb className="h-4 w-4" />
        </div>
        <div className="min-w-0 flex-1">
          <div className="font-mono text-[9.5px] uppercase tracking-[0.1em] text-muted-foreground">
            {t("phase.explain")}
          </div>
          <h3 className="mt-0.5 font-heading text-[14px] font-semibold tracking-tight">
            {t("explain_title")}
          </h3>
        </div>
      </div>

      <div
        ref={bodyRef}
        className="mt-3 max-h-[55vh] overflow-y-auto pr-1"
      >
        {showTyping ? (
          <div className="flex items-center gap-2 py-2 text-muted-foreground">
            <Loader2 className="h-3.5 w-3.5 animate-spin" />
            <span className="text-[12px]">{t("explain_waiting")}</span>
          </div>
        ) : (
          <div className="prose prose-sm dark:prose-invert max-w-none text-[13px] [&>*:first-child]:mt-0 [&>*:last-child]:mb-0">
            <Markdown>{explanation}</Markdown>
            {stream.streaming && (
              <span className="ml-0.5 inline-block h-3 w-1 animate-pulse bg-foreground/50 align-middle" />
            )}
          </div>
        )}
      </div>

      {explanationComplete && !stream.streaming && explanation && (
        <div className="mt-3 flex items-center justify-end">
          <Button
            size="sm"
            variant="primary"
            onClick={onExplanationDone}
            className="h-8 gap-1.5 rounded-full px-3 text-[12px]"
          >
            {t.has("explain_continue_cta")
              ? t("explain_continue_cta")
              : "I'm ready — start practice"}
            <ArrowRight className="h-3.5 w-3.5" />
          </Button>
        </div>
      )}
    </motion.div>
  );
}
