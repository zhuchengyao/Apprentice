"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { useTranslations } from "next-intl";
import { AlertCircle, BookOpen, Loader2, Sparkles } from "lucide-react";
import { api, ApiError } from "@/lib/api-client";
import { useStudySessionStore } from "@/lib/stores/study-session";
import type { HighlightController } from "@/components/tutor/use-tutor-highlight";
import { PhaseStepper } from "./phase-stepper";
import { ReadingScopePanel } from "./reading-scope-panel";
import { ExplanationPanel } from "./explanation-panel";
import { QuizCard } from "./quiz-card";
import { FeedbackCard } from "./feedback-card";
import type {
  AnswerResponse,
  NextScopeResponse,
  QuestionsResponse,
  StudySession,
} from "@/lib/types";

interface Props {
  bookId: string;
  chapterId: string;
  /** Highlight controller from the parent, so clearing on chapter change and
   *  our scope marks share the same DOM root. */
  highlight: HighlightController;
}

export function StudySessionPanel({
  bookId,
  chapterId,
  highlight,
}: Props) {
  const t = useTranslations("study");

  const sessionId = useStudySessionStore((s) => s.sessionId);
  const phase = useStudySessionStore((s) => s.phase);
  const session = useStudySessionStore((s) => s.session);
  const currentScopeIndex = useStudySessionStore((s) => s.currentScopeIndex);
  const totalScopes = useStudySessionStore((s) => s.totalScopes);
  const currentQuestionIndex = useStudySessionStore(
    (s) => s.currentQuestionIndex,
  );
  const questions = useStudySessionStore((s) => s.questions);
  const feedback = useStudySessionStore((s) => s.feedback);
  const scopeScore = useStudySessionStore((s) => s.scopeScore);
  const loading = useStudySessionStore((s) => s.loading);
  const error = useStudySessionStore((s) => s.error);

  const setSession = useStudySessionStore((s) => s.setSession);
  const setLoading = useStudySessionStore((s) => s.setLoading);
  const setError = useStudySessionStore((s) => s.setError);
  const setQuestions = useStudySessionStore((s) => s.setQuestions);
  const applyAnswer = useStudySessionStore((s) => s.applyAnswer);
  const advanceQuestion = useStudySessionStore((s) => s.advanceQuestion);
  const advanceScope = useStudySessionStore((s) => s.advanceScope);
  const reset = useStudySessionStore((s) => s.reset);

  const workingRef = useRef(false);
  const questionsKeyRef = useRef<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [advancingScope, setAdvancingScope] = useState(false);
  const [noContent, setNoContent] = useState(false);

  // ── Start or resume session when chapter changes ──────────────
  // No mount-dedup ref: in React 18 StrictMode dev the previous pattern
  // would mark the key on the first mount, get cancelled, then short-
  // circuit the second mount and leave `loading` stuck true forever.
  // POST /study/sessions is idempotent on (user_id, chapter_id), so the
  // worst case is one redundant request per chapter open in dev.
  useEffect(() => {
    let cancelled = false;

    async function start() {
      reset();
      setLoading(true);
      setError(null);
      setNoContent(false);
      try {
        const data = await api.post<StudySession>("/study/sessions", {
          book_id: bookId,
          chapter_id: chapterId,
        });
        if (cancelled) return;
        setSession(data);
      } catch (err) {
        if (cancelled) return;
        // 409 here means the chapter has no knowledge points yet — a real
        // condition for TOC/index/preface chapters, not a failure. Show a
        // neutral empty-state instead of a red error.
        if (err instanceof ApiError && err.status === 409) {
          setNoContent(true);
        } else {
          setError(err instanceof Error ? err.message : "Failed to start session");
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    start();

    return () => {
      cancelled = true;
      highlight.clearAll();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [bookId, chapterId]);

  const handleFinishReading = useCallback(async () => {
    // No POST here — the explanation stream endpoint owns the read→explain
    // transition. We just flip local state so the EXPLAIN panel mounts.
    useStudySessionStore.setState({ phase: "explain" });
  }, []);

  const handleExplanationDone = useCallback(() => {
    // Server flipped phase to `practice` at the end of the stream; reflect that.
    useStudySessionStore.setState({ phase: "practice" });
  }, []);

  const handleAdvanceScope = useCallback(async () => {
    if (!sessionId || workingRef.current) return;
    workingRef.current = true;
    setAdvancingScope(true);
    try {
      const data = await api.post<NextScopeResponse>(
        `/study/sessions/${sessionId}/next-scope`,
      );
      advanceScope(data.session, data.done);
      highlight.clearAll();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to advance scope");
    } finally {
      workingRef.current = false;
      setAdvancingScope(false);
    }
  }, [sessionId, advanceScope, highlight, setError]);

  // ── Fetch questions the first time we enter PRACTICE for a given scope ──
  useEffect(() => {
    if (!sessionId) return;
    if (phase !== "practice") return;
    const key = `${sessionId}:${currentScopeIndex}`;
    if (questionsKeyRef.current === key && questions.length > 0) return;
    questionsKeyRef.current = key;

    let cancelled = false;
    (async () => {
      try {
        const data = await api.get<QuestionsResponse>(
          `/study/sessions/${sessionId}/questions`,
        );
        if (cancelled) return;
        setQuestions(data);
      } catch (err) {
        if (cancelled) return;
        setError(
          err instanceof Error ? err.message : "Failed to load questions",
        );
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [sessionId, phase, currentScopeIndex, questions.length, setQuestions, setError]);

  const currentQuestion = useMemo(() => {
    if (!questions.length) return null;
    if (feedback) {
      const answered = questions.find((q) => q.id === feedback.question_id);
      if (answered) return answered;
    }
    return questions[Math.min(currentQuestionIndex, questions.length - 1)] ?? null;
  }, [questions, currentQuestionIndex, feedback]);

  const handleSubmitAnswer = useCallback(
    async (chosenOption: string, timeSpentMs: number) => {
      if (!sessionId || !currentQuestion || submitting) return;
      setSubmitting(true);
      try {
        const response = await api.post<AnswerResponse>(
          `/study/sessions/${sessionId}/answer`,
          {
            question_id: currentQuestion.id,
            chosen_option: chosenOption,
            time_spent_ms: timeSpentMs,
          },
        );
        applyAnswer(currentQuestion.id, chosenOption, response);
        if (response.scope_complete) {
          useStudySessionStore.setState({ phase: "feedback" });
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to submit answer");
      } finally {
        setSubmitting(false);
      }
    },
    [sessionId, currentQuestion, submitting, applyAnswer, setError],
  );

  const handleNextQuestion = useCallback(() => {
    advanceQuestion();
  }, [advanceQuestion]);

  // Backward navigation through the four phases. Cached state (explanation
  // text, questions, attempts) is preserved in the store so the previous
  // panels render immediately without re-fetching. The backend's phase is
  // intentionally not rolled back — it tracks where to resume on next load.
  const PHASE_ORDER = useMemo(
    () => ["read", "explain", "practice", "feedback"] as const,
    [],
  );
  const handleStepperNavigate = useCallback(
    (target: (typeof PHASE_ORDER)[number]) => {
      const targetIdx = PHASE_ORDER.indexOf(target);
      const currentIdx = PHASE_ORDER.indexOf(
        phase as (typeof PHASE_ORDER)[number],
      );
      if (targetIdx < 0 || currentIdx < 0 || targetIdx >= currentIdx) return;
      useStudySessionStore.setState({ phase: target });
    },
    [PHASE_ORDER, phase],
  );

  const currentScope = useMemo(() => session?.scope ?? null, [session]);
  const isLastScope = currentScopeIndex >= totalScopes - 1;

  if (loading) {
    return (
      <div className="rounded-2xl border border-border/70 bg-card/40 p-4 ring-1 ring-foreground/5">
        <div className="flex items-center gap-2 text-muted-foreground">
          <Loader2 className="h-3.5 w-3.5 animate-spin" />
          <span className="text-[12px]">{t("starting")}</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-2xl border border-destructive/40 bg-destructive/5 p-4 ring-1 ring-destructive/10">
        <div className="flex items-start gap-2 text-destructive">
          <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" />
          <span className="text-[12.5px]">{error}</span>
        </div>
      </div>
    );
  }

  if (noContent) {
    return (
      <div className="rounded-2xl border border-border/70 bg-card/40 p-5 ring-1 ring-foreground/5">
        <div className="flex items-start gap-3">
          <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-muted text-muted-foreground ring-1 ring-border/60">
            <BookOpen className="h-4 w-4" />
          </div>
          <div className="min-w-0">
            <h3 className="font-heading text-[13.5px] font-semibold tracking-tight">
              {t("no_kps_title")}
            </h3>
            <p className="mt-1 text-[12.5px] leading-relaxed text-muted-foreground">
              {t("no_kps_body")}
            </p>
          </div>
        </div>
      </div>
    );
  }

  if (!sessionId) return null;

  return (
    <div className="flex min-w-0 flex-col gap-3">
      <PhaseStepper
        phase={phase}
        scopeIndex={currentScopeIndex}
        totalScopes={totalScopes}
        onNavigate={handleStepperNavigate}
      />

      <AnimatePresence mode="wait" initial={false}>
        {phase === "done" && (
          <motion.div
            key="done"
            layout
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            className="rounded-2xl border border-border/70 bg-card/60 p-5 text-center shadow-editorial-sm ring-1 ring-foreground/5"
          >
            <Sparkles className="mx-auto h-6 w-6 text-primary" />
            <h3 className="mt-2 font-heading text-[14px] font-semibold tracking-tight">
              {t("session_complete")}
            </h3>
            <p className="mt-1 text-[12.5px] text-muted-foreground">
              {t("session_complete_hint")}
            </p>
          </motion.div>
        )}

        {phase === "read" && currentScope && (
          <motion.div key={`read-${currentScopeIndex}`} layout>
            <ReadingScopePanel
              scope={currentScope}
              highlight={highlight}
              onFinishReading={handleFinishReading}
              working={false}
            />
          </motion.div>
        )}

        {phase === "explain" && currentScope && (
          <motion.div key={`explain-${currentScopeIndex}`} layout>
            <ExplanationPanel
              sessionId={sessionId}
              onExplanationDone={handleExplanationDone}
            />
          </motion.div>
        )}

        {phase === "practice" && (
          !currentQuestion ? (
            <motion.div
              key={`practice-loading-${currentScopeIndex}`}
              layout
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -8 }}
              className="rounded-2xl border border-border/70 bg-card/60 p-4 shadow-editorial-sm ring-1 ring-foreground/5"
            >
              <div className="flex items-center gap-2 text-muted-foreground">
                <Loader2 className="h-3.5 w-3.5 animate-spin" />
                <span className="text-[12px]">{t("loading_questions")}</span>
              </div>
            </motion.div>
          ) : (
            <QuizCard
              key={currentQuestion.id}
              question={currentQuestion}
              index={questions.indexOf(currentQuestion)}
              total={questions.length}
              feedback={feedback}
              submitting={submitting}
              onSubmit={handleSubmitAnswer}
              onNext={handleNextQuestion}
            />
          )
        )}

        {phase === "feedback" && (
          <motion.div key={`feedback-${currentScopeIndex}`} layout>
            <FeedbackCard
              correct={scopeScore.correct}
              total={scopeScore.total}
              isLastScope={isLastScope}
              working={advancingScope}
              onAdvance={handleAdvanceScope}
            />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
