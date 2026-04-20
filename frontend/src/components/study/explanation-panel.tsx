"use client";

import { useEffect, useMemo, useRef } from "react";
import { useTranslations } from "next-intl";
import { ArrowRight, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Markdown } from "@/components/ui/markdown";
import { KpVideo } from "@/components/illustration/kp-video";
import { useTutorStream } from "@/components/tutor/use-tutor-stream";
import { useStudySessionStore } from "@/lib/stores/study-session";
import { getLocaleFromCookie } from "@/lib/api-client";
import { PhaseShell, type PhaseState } from "./phase-shell";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "/api";

interface Props {
  sessionId: string;
  onExplanationDone: () => void;
  state: PhaseState;
  onExpand?: () => void;
}

export function ExplanationPanel({
  sessionId,
  onExplanationDone,
  state,
  onExpand,
}: Props) {
  const t = useTranslations("study");
  const bodyRef = useRef<HTMLDivElement>(null);

  const explanation = useStudySessionStore((s) => s.explanation);
  const setExplanation = useStudySessionStore((s) => s.setExplanation);
  const completeExplanation = useStudySessionStore(
    (s) => s.completeExplanation,
  );
  const explanationComplete = useStudySessionStore(
    (s) => s.explanationComplete,
  );
  const scopeKps = useStudySessionStore((s) => s.session?.scope?.kps ?? null);

  // KPs in this scope that have a Manim animation. The `kps` field is
  // populated by `_scope_view` on the backend; legacy sessions created
  // before that change return null, so fall back to an empty list.
  const illustratedKps = useMemo(
    () => (scopeKps ?? []).filter((kp) => kp.illustration_video),
    [scopeKps],
  );

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

  useEffect(() => {
    if (stream.streaming) {
      setExplanation(stream.buffer, true);
    }
  }, [stream.buffer, stream.streaming, setExplanation]);

  useEffect(() => {
    if (state !== "active") return;
    const { explanation: cached, explanationComplete: completed } =
      useStudySessionStore.getState();
    if (completed && cached) return;
    stream.run(`${API_BASE}/study/sessions/${sessionId}/advance`, {
      method: "POST",
      headers: { "Accept-Language": getLocaleFromCookie() },
    });
    return () => {
      stream.abort();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sessionId, state]);

  useEffect(() => {
    bodyRef.current?.scrollTo({
      top: bodyRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [explanation]);

  if (state === "pending") {
    return <PhaseShell phase="explain" state="pending" />;
  }

  if (state === "done") {
    const firstLine = (explanation || "").split("\n").find((l) => l.trim());
    return (
      <PhaseShell
        phase="explain"
        state="done"
        meta={t("phase_ready")}
        compactSummary={firstLine?.trim() || undefined}
        onExpand={onExpand}
      />
    );
  }

  const showTyping = stream.streaming && !explanation;

  return (
    <PhaseShell
      phase="explain"
      state="active"
      meta={stream.streaming ? t("phase_writing") : t("phase_ready")}
    >
      <div className="flex flex-col gap-3">
        <h3 className="font-heading text-[14px] font-semibold leading-snug tracking-tight">
          {t("explain_title")}
        </h3>
        <div ref={bodyRef} className="max-h-[55vh] overflow-y-auto pr-1">
          {showTyping ? (
            <div className="flex items-center gap-2 py-2 text-muted-foreground">
              <Loader2 className="h-3.5 w-3.5 animate-spin" />
              <span className="text-[12px]">{t("explain_waiting")}</span>
            </div>
          ) : (
            <div className="prose prose-sm dark:prose-invert max-w-none text-[13.5px] leading-[1.65] text-subtle-foreground [&>*:first-child]:mt-0 [&>*:last-child]:mb-0">
              <Markdown>{explanation}</Markdown>
              {stream.streaming && (
                <span className="ml-0.5 inline-block h-[1em] w-[3px] animate-pulse bg-foreground/50 align-[-2px]" />
              )}
            </div>
          )}
          {illustratedKps.length > 0 && !showTyping && (
            <div className="mt-4 flex flex-col gap-3 border-t border-border/60 pt-4">
              {illustratedKps.map((kp) => (
                <figure key={kp.id} className="flex flex-col gap-1.5">
                  <KpVideo filename={kp.illustration_video!} />
                  <figcaption className="text-[11.5px] font-medium text-muted-foreground">
                    {kp.concept}
                  </figcaption>
                </figure>
              ))}
            </div>
          )}
        </div>
        {explanationComplete && !stream.streaming && explanation && (
          <div className="flex justify-end">
            <Button
              size="sm"
              variant="primary"
              onClick={onExplanationDone}
              className="h-8 gap-1.5 rounded-full px-3 text-[12px]"
            >
              {t("explain_continue_cta")}
              <ArrowRight className="h-3.5 w-3.5" />
            </Button>
          </div>
        )}
      </div>
    </PhaseShell>
  );
}
