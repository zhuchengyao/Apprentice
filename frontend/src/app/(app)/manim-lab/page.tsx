"use client";

import { useState } from "react";
import { useTranslations } from "next-intl";
import { Clapperboard, Loader2, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { api } from "@/lib/api-client";

interface GenerateResponse {
  accepted: boolean;
  failure_kind: string;
  failure_detail: string | null;
  decline_reason: string | null;
  latency_ms: number;
  filename: string | null;
  render_stderr_tail: string | null;
  code: string | null;
}

type Quality = "low" | "medium" | "high";

export default function ManimLabPage() {
  const t = useTranslations("manim_lab");
  const [concept, setConcept] = useState("Newton's second law");
  const [explanation, setExplanation] = useState(
    "Net force on an object equals its mass times its acceleration: F = ma. " +
      "A larger force causes a larger acceleration for the same mass; a larger " +
      "mass resists acceleration for the same force.",
  );
  const [quality, setQuality] = useState<Quality>("low");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<GenerateResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const onGenerate = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await api.post<GenerateResponse>("/manim/generate", {
        concept,
        explanation,
        quality,
      });
      setResult(res);
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setLoading(false);
    }
  };

  const videoSrc = result?.filename ? `/api/manim/video/${result.filename}` : null;

  return (
    <div className="mx-auto w-full max-w-4xl px-5 py-10 sm:px-8 sm:py-12">
      <div className="flex items-center gap-3">
        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary/10 text-primary ring-1 ring-primary/20">
          <Clapperboard className="h-4 w-4" />
        </div>
        <div>
          <p className="eyebrow">{t("eyebrow")}</p>
          <h1 className="font-display text-3xl font-semibold tracking-tight sm:text-4xl">
            {t("heading")}
          </h1>
        </div>
      </div>
      <p className="mt-3 max-w-xl text-[14.5px] leading-relaxed text-muted-foreground">
        {t("lede")}
      </p>

      <div className="mt-8 space-y-4 rounded-2xl border border-border/70 bg-card p-5">
        <div>
          <label className="mb-1.5 block text-[13px] font-medium">
            {t("concept")}
          </label>
          <input
            type="text"
            value={concept}
            onChange={(e) => setConcept(e.target.value)}
            className="w-full rounded-lg border border-border bg-background px-3 py-2 text-sm outline-none focus-visible:border-primary focus-visible:ring-2 focus-visible:ring-primary/20"
            placeholder={t("concept_placeholder")}
          />
        </div>

        <div>
          <label className="mb-1.5 block text-[13px] font-medium">
            {t("explanation")}
          </label>
          <textarea
            value={explanation}
            onChange={(e) => setExplanation(e.target.value)}
            rows={5}
            className="w-full resize-y rounded-lg border border-border bg-background px-3 py-2 font-mono text-[12.5px] leading-relaxed outline-none focus-visible:border-primary focus-visible:ring-2 focus-visible:ring-primary/20"
            placeholder={t("explanation_placeholder")}
          />
        </div>

        <div className="flex items-end gap-3">
          <div>
            <label className="mb-1.5 block text-[13px] font-medium">
              {t("quality")}
            </label>
            <select
              value={quality}
              onChange={(e) => setQuality(e.target.value as Quality)}
              className="rounded-lg border border-border bg-background px-3 py-2 text-sm outline-none focus-visible:border-primary focus-visible:ring-2 focus-visible:ring-primary/20"
            >
              <option value="low">{t("quality_low")}</option>
              <option value="medium">{t("quality_medium")}</option>
              <option value="high">{t("quality_high")}</option>
            </select>
          </div>

          <Button
            variant="primary"
            size="lg"
            onClick={onGenerate}
            disabled={loading || !concept.trim() || !explanation.trim()}
            className="ml-auto gap-2"
          >
            {loading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Sparkles className="h-4 w-4" />
            )}
            {loading ? t("rendering") : t("generate")}
          </Button>
        </div>
      </div>

      {error && (
        <div className="mt-4 rounded-lg border border-destructive/40 bg-destructive/5 p-3 text-sm text-destructive">
          {error}
        </div>
      )}

      {loading && (
        <div className="mt-6 rounded-2xl border border-border/70 bg-card p-5 text-sm text-muted-foreground">
          {t("rendering_note")}
        </div>
      )}

      {result && (
        <div className="mt-6 space-y-3">
          {videoSrc ? (
            <div className="overflow-hidden rounded-2xl border border-border/70 bg-black">
              <video
                key={videoSrc}
                src={videoSrc}
                controls
                autoPlay
                playsInline
                className="block w-full"
              />
            </div>
          ) : (
            <div className="rounded-2xl border border-amber-500/40 bg-amber-500/5 p-4 text-sm">
              <div className="font-medium text-amber-700 dark:text-amber-300">
                {result.failure_kind === "declined"
                  ? t("declined")
                  : t("failed", { kind: result.failure_kind })}
              </div>
              {result.decline_reason && (
                <p className="mt-1 text-muted-foreground">
                  {t("decline_reason", { reason: result.decline_reason })}
                </p>
              )}
              {result.failure_detail && (
                <p className="mt-1 font-mono text-[12px] text-muted-foreground">
                  {result.failure_detail}
                </p>
              )}
            </div>
          )}

          <details className="rounded-xl border border-border/70 bg-card/60 text-[12.5px]">
            <summary className="cursor-pointer px-4 py-2.5 text-muted-foreground hover:text-foreground">
              {t("details_summary", {
                seconds: (result.latency_ms / 1000).toFixed(1),
                kind: result.failure_kind,
              })}
            </summary>
            {result.code && (
              <div className="border-t border-border/70 p-4">
                <div className="mb-2 text-[11px] uppercase tracking-wider text-muted-foreground">
                  {t("generated_code")}
                </div>
                <pre className="max-h-80 overflow-auto rounded-lg bg-muted/40 p-3 font-mono text-[11.5px] leading-relaxed">
                  {result.code}
                </pre>
              </div>
            )}
            {result.render_stderr_tail && (
              <div className="border-t border-border/70 p-4">
                <div className="mb-2 text-[11px] uppercase tracking-wider text-muted-foreground">
                  {t("render_stderr")}
                </div>
                <pre className="max-h-60 overflow-auto rounded-lg bg-muted/40 p-3 font-mono text-[11.5px] leading-relaxed">
                  {result.render_stderr_tail}
                </pre>
              </div>
            )}
          </details>
        </div>
      )}
    </div>
  );
}
