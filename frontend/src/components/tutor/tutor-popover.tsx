"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";
import { useTranslations } from "next-intl";
import {
  ChevronRight,
  GraduationCap,
  Loader2,
  Minus,
  Pause,
  Send,
  X,
  CheckCircle2,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { KpVideo } from "@/components/illustration/kp-video";
import { Markdown } from "@/components/ui/markdown";
import { getLocaleFromCookie } from "@/lib/api-client";
import { parseSSEStream } from "@/lib/sse";
import { cn } from "@/lib/utils";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "/api";

export interface KPHighlight {
  id: string;
  concept: string;
  section_id: string;
  explanation: string;
  source_anchor?: string | null;
  illustration_video?: string | null;
}

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  metadata?: {
    type?: string;
    knowledge_point_ids?: string[];
    action?: string;
  } | null;
}

// The animation to show belongs to the KP(s) taught in the most recent
// teach step. We key it off the message's knowledge_point_ids so scrolling
// back and forth through the conversation doesn't leak stale visuals.
function illustrationForMessage(
  msg: Message,
  kpsById: Map<string, KPHighlight>,
): string | null {
  if (msg.metadata?.type !== "teach") return null;
  const id = msg.metadata.knowledge_point_ids?.[0];
  if (!id) return null;
  return kpsById.get(id)?.illustration_video ?? null;
}

type Action = "continue" | "pause" | "finished";

interface TutorPopoverProps {
  bookId: string;
  chapterId: string;
  scrollContainer: HTMLElement | null;
  onHighlight: (kps: KPHighlight[]) => HTMLElement | null;
  onKpsCovered: (kpIds: string[]) => void;
  onClose?: () => void;
}

const POPOVER_WIDTH = 384; // w-96
const POPOVER_MAX_H = 520;
const ANCHOR_GAP = 12;
const VIEWPORT_MARGIN = 12;

export function TutorPopover({
  bookId,
  chapterId,
  scrollContainer,
  onHighlight,
  onKpsCovered,
  onClose,
}: TutorPopoverProps) {
  const t = useTranslations("tutor");
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [streamContent, setStreamContent] = useState("");
  const [streaming, setStreaming] = useState(false);
  const [loading, setLoading] = useState(false);
  const [kpProgress, setKpProgress] = useState({ current: 0, total: 0 });
  const [currentKps, setCurrentKps] = useState<KPHighlight[]>([]);
  // Every KP the tutor has highlighted during this session. Lets us render
  // its illustration next to the corresponding teach message — both the
  // one currently streaming and earlier ones the student scrolls back to.
  const [kpsById, setKpsById] = useState<Map<string, KPHighlight>>(
    () => new Map(),
  );
  const [anchorEl, setAnchorEl] = useState<HTMLElement | null>(null);
  const [anchorRect, setAnchorRect] = useState<DOMRect | null>(null);
  const [input, setInput] = useState("");
  const [minimized, setMinimized] = useState(false);
  const [autoContinuePaused, setAutoContinuePaused] = useState(false);

  const abortRef = useRef<AbortController | null>(null);
  const bodyRef = useRef<HTMLDivElement>(null);

  // Derived from the latest assistant message's metadata — updated automatically
  // when setMessages appends a new message at stream end.
  const lastAssistant = [...messages].reverse().find((m) => m.role === "assistant");
  const lastAction = (lastAssistant?.metadata?.action as Action | undefined) ?? null;
  const chapterComplete = conversationId !== null &&
    (kpProgress.total === 0 || lastAction === "finished");

  // ── Init conversation when chapter changes ──────────────────
  useEffect(() => {
    let cancelled = false;

    async function init() {
      setLoading(true);
      setMessages([]);
      setStreamContent("");
      setCurrentKps([]);
      setKpsById(new Map());
      setAnchorEl(null);
      setConversationId(null);

      try {
        const res = await fetch(`${API_BASE}/tutor/conversations`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Accept-Language": getLocaleFromCookie(),
          },
          body: JSON.stringify({ book_id: bookId, chapter_id: chapterId }),
        });
        if (!res.ok) throw new Error("Failed to create conversation");
        const data = await res.json();
        if (cancelled) return;

        setConversationId(data.id);
        setKpProgress({ current: data.current_kp_index, total: data.total_kps });

        if (data.total_kps === 0) {
          setLoading(false);
          return;
        }

        if (data.messages && data.messages.length > 0) {
          setMessages(
            data.messages.map((m: Message) => ({
              id: m.id,
              role: m.role,
              content: m.content,
              metadata: m.metadata,
            })),
          );
          setLoading(false);
        } else {
          setLoading(false);
          await streamOpening(data.id);
        }
      } catch (err) {
        console.error("Tutor init failed:", err);
        setLoading(false);
      }
    }

    init();
    return () => {
      cancelled = true;
      abortRef.current?.abort();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [bookId, chapterId]);

  // ── Reposition on scroll / resize ───────────────────────────
  useEffect(() => {
    if (!anchorEl) {
      setAnchorRect(null);
      return;
    }
    const update = () => setAnchorRect(anchorEl.getBoundingClientRect());
    update();
    const scroller = scrollContainer || window;
    scroller.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    return () => {
      scroller.removeEventListener("scroll", update);
      window.removeEventListener("resize", update);
    };
  }, [anchorEl, scrollContainer]);

  // ── Auto-scroll body on new content ─────────────────────────
  useEffect(() => {
    bodyRef.current?.scrollTo({ top: bodyRef.current.scrollHeight, behavior: "smooth" });
  }, [streamContent, messages.length]);

  // Reset the user's pause as soon as a new assistant message lands so the
  // auto-continue timer is armed again for the next teach step.
  useEffect(() => {
    setAutoContinuePaused(false);
  }, [messages.length]);

  // ── Auto-continue when action=continue ──────────────────────
  // The delay scales with the length of the message the student just got,
  // so they have a moment to read before the next KP starts streaming.
  // Clamped so short messages don't feel sluggish and long ones don't stall.
  useEffect(() => {
    if (
      lastAction === "continue" &&
      !streaming &&
      conversationId &&
      !autoContinuePaused
    ) {
      const chars = lastAssistant?.content.length ?? 0;
      const delay = Math.min(3500, Math.max(800, chars * 4));
      const handle = setTimeout(() => teachNext(), delay);
      return () => clearTimeout(handle);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [lastAction, streaming, conversationId, autoContinuePaused]);

  const streamOpening = useCallback(async (convId: string) => {
    setStreaming(true);
    setStreamContent("");
    try {
      const res = await fetch(
        `${API_BASE}/tutor/conversations/${convId}/open`,
        {
          method: "POST",
          headers: { "Accept-Language": getLocaleFromCookie() },
        },
      );
      if (!res.ok) {
        setStreaming(false);
        return;
      }
      await processSSEStream(res);
    } catch (err) {
      console.error("Opening stream error:", err);
      setStreaming(false);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const teachNext = useCallback(async () => {
    if (!conversationId || streaming) return;
    setStreaming(true);
    setStreamContent("");
    try {
      const controller = new AbortController();
      abortRef.current = controller;
      const res = await fetch(
        `${API_BASE}/tutor/conversations/${conversationId}/teach`,
        {
          method: "POST",
          headers: { "Accept-Language": getLocaleFromCookie() },
          signal: controller.signal,
        },
      );
      if (!res.ok) throw new Error("Failed to teach next");
      await processSSEStream(res);
    } catch (err) {
      if (err instanceof DOMException && err.name === "AbortError") return;
      console.error("Teach error:", err);
      setStreaming(false);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [conversationId, streaming]);

  const sendMessage = useCallback(async () => {
    const content = input.trim();
    if (!content || !conversationId || streaming) return;

    const userMsg: Message = {
      id: `temp-${Date.now()}`,
      role: "user",
      content,
    };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setStreaming(true);
    setStreamContent("");

    try {
      const controller = new AbortController();
      abortRef.current = controller;
      const res = await fetch(
        `${API_BASE}/tutor/conversations/${conversationId}/message`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Accept-Language": getLocaleFromCookie(),
          },
          body: JSON.stringify({ content }),
          signal: controller.signal,
        },
      );
      if (!res.ok) throw new Error("Failed to send message");
      await processSSEStream(res);
    } catch (err) {
      if (err instanceof DOMException && err.name === "AbortError") return;
      console.error("Send message error:", err);
      setStreaming(false);
    }
  }, [input, conversationId, streaming]);

  async function processSSEStream(res: Response) {
    let accumulated = "";
    try {
      for await (const { event, data } of parseSSEStream(res)) {
        if (event === "highlight") {
          try {
            const payload = JSON.parse(data);
            const kps: KPHighlight[] = payload.knowledge_points || [];
            setCurrentKps(kps);
            setKpsById((prev) => {
              const next = new Map(prev);
              for (const kp of kps) next.set(kp.id, kp);
              return next;
            });
            const el = onHighlight(kps);
            setAnchorEl(el);
            onKpsCovered(kps.map((k) => k.id));
          } catch { /* ignore */ }
        } else if (event === "token") {
          accumulated += data;
          setStreamContent(accumulated);
        } else if (event === "done") {
          let parsed: Record<string, unknown> | null = null;
          try {
            parsed = JSON.parse(data);
          } catch { /* ignore */ }
          setMessages((prev) => [
            ...prev,
            {
              id: (parsed?.id as string) || `msg-${Date.now()}`,
              role: "assistant",
              content: (parsed?.content as string) || accumulated,
              metadata: parsed?.metadata as Message["metadata"],
            },
          ]);
          setStreamContent("");
          setStreaming(false);

          const action = parsed?.action as Action | undefined;
          if (action && action !== "finished" && typeof parsed?.kp_index === "number") {
            setKpProgress((prev) => ({
              ...prev,
              current: parsed!.kp_index as number,
            }));
          }
          return;
        } else if (event === "error") {
          console.error("Stream error:", data);
          setStreaming(false);
          return;
        }
      }
    } finally {
      setStreaming(false);
    }
  }

  // ── Render positioning ──────────────────────────────────────
  const pos = computePosition(anchorRect, scrollContainer);

  if (loading) return null;

  if (minimized) {
    return createPortal(
      <button
        onClick={() => setMinimized(false)}
        className="fixed bottom-6 right-6 z-50 flex h-12 w-12 items-center justify-center rounded-full bg-primary text-primary-foreground shadow-editorial-lg ring-4 ring-primary/15 transition-transform hover:scale-105"
        aria-label={t("open")}
      >
        <GraduationCap className="h-5 w-5" />
      </button>,
      document.body,
    );
  }

  const showContinue =
    lastAction === "pause" && !streaming && !chapterComplete && conversationId;
  const showAutoContinue =
    lastAction === "continue" &&
    !streaming &&
    !chapterComplete &&
    !!conversationId;
  const currentConcept = currentKps[0]?.concept;
  // Show the whole conversation so the student can scroll back through
  // earlier KPs and Q&A. The body is scroll-constrained and auto-scrolls
  // to the bottom on new content.
  const displayMessages: Message[] = messages;

  return createPortal(
    <div
      className="fixed z-40 w-96 overflow-hidden rounded-2xl border border-border/70 bg-popover shadow-editorial-lg ring-1 ring-foreground/5"
      style={{
        top: pos.top,
        left: pos.left,
        maxHeight: POPOVER_MAX_H,
      }}
    >
      {/* Header */}
      <div className="flex items-center gap-2.5 border-b border-border/60 bg-card/60 px-3.5 py-2.5">
        <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-primary/15 text-primary ring-1 ring-primary/20">
          <GraduationCap className="h-3.5 w-3.5" />
        </div>
        <div className="min-w-0 flex-1">
          <div className="truncate font-heading text-[13.5px] font-semibold tracking-tight">
            {currentConcept || t("title")}
          </div>
          {kpProgress.total > 0 && (
            <div className="mt-0.5 font-mono text-[10px] uppercase tracking-[0.08em] text-muted-foreground tabular-nums">
              {kpProgress.current} / {kpProgress.total} · {t("kp_unit")}
            </div>
          )}
        </div>
        <button
          onClick={() => setMinimized(true)}
          className="rounded-md p-1 text-muted-foreground transition-colors hover:bg-subtle hover:text-foreground"
          aria-label={t("minimize")}
        >
          <Minus className="h-3.5 w-3.5" />
        </button>
      </div>

      {/* Progress */}
      {kpProgress.total > 0 && (
        <div className="h-0.5 bg-subtle">
          <div
            className="h-full bg-primary transition-all duration-500 ease-out"
            style={{
              width: `${(kpProgress.current / kpProgress.total) * 100}%`,
            }}
          />
        </div>
      )}

      {/* Body */}
      <div
        ref={bodyRef}
        className="overflow-y-auto px-3 py-2.5 text-sm"
        style={{ maxHeight: POPOVER_MAX_H - 160 }}
      >
        {displayMessages.map((msg) => {
          const illustration =
            msg.role === "assistant" ? illustrationForMessage(msg, kpsById) : null;
          return (
            <div key={msg.id} className="mb-2 last:mb-0">
              {msg.role === "user" ? (
                <div className="ml-auto w-fit max-w-[90%] rounded-2xl rounded-br-md bg-primary/10 px-3 py-2 text-[13px] ring-1 ring-primary/15">
                  <p className="whitespace-pre-wrap">{msg.content}</p>
                </div>
              ) : (
                <>
                  {illustration ? (
                    <div className="mb-2">
                      <KpVideo filename={illustration} maxWidth={340} />
                    </div>
                  ) : null}
                  <div className="prose prose-sm dark:prose-invert max-w-none text-[13px] [&>*:first-child]:mt-0 [&>*:last-child]:mb-0">
                    <Markdown>{msg.content}</Markdown>
                  </div>
                </>
              )}
            </div>
          );
        })}
        {streaming && streamContent && (
          <>
            {currentKps[0]?.illustration_video ? (
              <div className="mb-2">
                <KpVideo
                  filename={currentKps[0].illustration_video}
                  maxWidth={340}
                />
              </div>
            ) : null}
            <div className="prose prose-sm dark:prose-invert max-w-none text-[13px] [&>*:first-child]:mt-0 [&>*:last-child]:mb-0">
              <span className="whitespace-pre-wrap">{streamContent}</span>
              <span className="ml-0.5 inline-block h-3 w-1 animate-pulse bg-foreground/50 align-middle" />
            </div>
          </>
        )}
        {streaming && !streamContent && (
          <div className="flex items-center gap-2 py-1 text-muted-foreground">
            <Loader2 className="h-3.5 w-3.5 animate-spin" />
            <span className="text-[12px]">{t("thinking")}</span>
          </div>
        )}
        {chapterComplete && (
          <div className="flex flex-col items-center gap-1.5 py-3 text-center">
            <CheckCircle2 className="h-6 w-6 text-primary" />
            <p className="font-heading text-[13px] font-medium">
              {t("complete")}
            </p>
            <p className="text-[11px] leading-relaxed text-muted-foreground">
              {t("complete_hint")}
            </p>
          </div>
        )}
      </div>

      {/* Footer: input + continue */}
      <div className="border-t border-border/60 bg-card/40 px-3 py-2.5">
        {showContinue && (
          <div className="mb-2 flex items-center justify-between gap-2 rounded-xl bg-primary/8 px-3 py-1.5 ring-1 ring-primary/12">
            <span className="font-mono text-[10px] uppercase tracking-[0.08em] text-muted-foreground">
              {t("continue_prompt")}
            </span>
            <Button
              size="sm"
              variant="primary"
              className="h-7 gap-1 rounded-full px-2.5 text-[11px]"
              onClick={teachNext}
            >
              {t("understood")}
              <ChevronRight className="h-3 w-3" />
            </Button>
          </div>
        )}
        {showAutoContinue && (
          <div className="mb-2 flex items-center justify-between gap-2 rounded-xl bg-subtle/60 px-3 py-1.5 ring-1 ring-border/60">
            <span className="font-mono text-[10px] uppercase tracking-[0.08em] text-muted-foreground">
              {autoContinuePaused ? t("paused") : t("up_next")}
            </span>
            {autoContinuePaused ? (
              <Button
                size="sm"
                variant="primary"
                className="h-7 gap-1 rounded-full px-2.5 text-[11px]"
                onClick={teachNext}
              >
                {t("continue")}
                <ChevronRight className="h-3 w-3" />
              </Button>
            ) : (
              <Button
                size="sm"
                variant="ghost"
                className="h-7 gap-1 rounded-full px-2.5 text-[11px]"
                onClick={() => setAutoContinuePaused(true)}
              >
                <Pause className="h-3 w-3" />
                {t("wait")}
              </Button>
            )}
          </div>
        )}
        <div className="flex items-end gap-1.5 rounded-2xl border border-border/60 bg-background px-3 py-1.5 transition-colors focus-within:border-ring/60 focus-within:ring-2 focus-within:ring-ring/20">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
              }
            }}
            placeholder={t("input_placeholder")}
            rows={1}
            className="flex-1 resize-none bg-transparent py-1 text-[13px] outline-none placeholder:text-muted-foreground"
            disabled={streaming || !conversationId}
          />
          <Button
            size="icon-sm"
            variant="primary"
            className="shrink-0 rounded-full"
            onClick={sendMessage}
            disabled={!input.trim() || streaming || !conversationId}
          >
            <Send className="h-3.5 w-3.5" />
          </Button>
        </div>
      </div>
      {onClose && (
        <button
          onClick={onClose}
          className={cn(
            "absolute -top-2 -right-2 hidden h-6 w-6 items-center justify-center rounded-full border bg-background text-muted-foreground shadow hover:text-foreground",
          )}
          aria-label={t("close")}
        >
          <X className="h-3 w-3" />
        </button>
      )}
    </div>,
    document.body,
  );
}

/** Compute fixed-position coords given the anchor's viewport rect. */
function computePosition(
  rect: DOMRect | null,
  scroller: HTMLElement | null,
): { top: number; left: number } {
  const vw = typeof window !== "undefined" ? window.innerWidth : 1280;
  const vh = typeof window !== "undefined" ? window.innerHeight : 800;

  // Fallback when no anchor: top-right of scroll container (or viewport).
  if (!rect) {
    const base = scroller?.getBoundingClientRect();
    return {
      top: (base?.top ?? 0) + 16,
      left: Math.max(VIEWPORT_MARGIN, (base?.right ?? vw) - POPOVER_WIDTH - 16),
    };
  }

  // Prefer right of anchor.
  const spaceRight = vw - rect.right - ANCHOR_GAP;
  const spaceLeft = rect.left - ANCHOR_GAP;
  let left: number;
  if (spaceRight >= POPOVER_WIDTH + VIEWPORT_MARGIN) {
    left = rect.right + ANCHOR_GAP;
  } else if (spaceLeft >= POPOVER_WIDTH + VIEWPORT_MARGIN) {
    left = rect.left - ANCHOR_GAP - POPOVER_WIDTH;
  } else {
    // Not enough horizontal space — place below/above, centered on anchor.
    left = Math.min(
      Math.max(VIEWPORT_MARGIN, rect.left + rect.width / 2 - POPOVER_WIDTH / 2),
      vw - POPOVER_WIDTH - VIEWPORT_MARGIN,
    );
  }

  let top = rect.top;
  // Clamp vertically so popover stays on screen.
  top = Math.min(Math.max(VIEWPORT_MARGIN, top), vh - 200 - VIEWPORT_MARGIN);
  return { top, left };
}
