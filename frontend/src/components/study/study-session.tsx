"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { motion } from "framer-motion";
import { useTranslations } from "next-intl";
import { AlertCircle, BookOpen, Loader2, Sparkles } from "lucide-react";
import { api, ApiError } from "@/lib/api-client";
import { useStudySessionStore } from "@/lib/stores/study-session";
import type { HighlightController } from "@/components/tutor/use-tutor-highlight";
import { ReadingScopePanel } from "./reading-scope-panel";
import { ExplanationPanel } from "./explanation-panel";
import { QuizCard } from "./quiz-card";
import { FeedbackCard } from "./feedback-card";
import { ScopeSelector } from "./scope-selector";
import type { PhaseKey, PhaseState } from "./phase-shell";
import type {
  AnswerResponse,
  NextScopeResponse,
  QuestionsResponse,
  StudyPhase,
  StudySession,
} from "@/lib/types";

interface Props {
  bookId: string;
  chapterId: string;
  highlight: HighlightController;
}

const PHASE_ORDER: readonly Exclude<StudyPhase, "done">[] = [
  "read",
  "explain",
  "practice",
  "feedback",
] as const;

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
  const attempts = useStudySessionStore((s) => s.attempts);
  const feedback = useStudySessionStore((s) => s.feedback);
  const scopeScore = useStudySessionStore((s) => s.scopeScore);
  const scopes = useStudySessionStore((s) => s.scopes);
  const maxScopeReached = useStudySessionStore((s) => s.maxScopeReached);
  const loading = useStudySessionStore((s) => s.loading);
  const error = useStudySessionStore((s) => s.error);

  const setSession = useStudySessionStore((s) => s.setSession);
  const setLoading = useStudySessionStore((s) => s.setLoading);
  const setError = useStudySessionStore((s) => s.setError);
  const setQuestions = useStudySessionStore((s) => s.setQuestions);
  const applyAnswer = useStudySessionStore((s) => s.applyAnswer);
  const advanceQuestion = useStudySessionStore((s) => s.advanceQuestion);
  const advanceScope = useStudySessionStore((s) => s.advanceScope);
  const gotoScope = useStudySessionStore((s) => s.gotoScope);
  const reset = useStudySessionStore((s) => s.reset);

  const workingRef = useRef(false);
  const questionsKeyRef = useRef<string | null>(null);
  const threadRef = useRef<HTMLDivElement>(null);
  const [submitting, setSubmitting] = useState(false);
  const [advancingScope, setAdvancingScope] = useState(false);
  const [noContent, setNoContent] = useState(false);

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
        if (err instanceof ApiError && err.status === 409) {
          setNoContent(true);
        } else {
          setError(
            err instanceof Error ? err.message : "Failed to start session",
          );
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
    useStudySessionStore.setState({ phase: "explain" });
  }, []);

  const handleExplanationDone = useCallback(() => {
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
      setError(
        err instanceof Error ? err.message : "Failed to advance scope",
      );
    } finally {
      workingRef.current = false;
      setAdvancingScope(false);
    }
  }, [sessionId, advanceScope, highlight, setError]);

  const handleSelectScope = useCallback(
    async (targetIndex: number) => {
      if (!sessionId || workingRef.current) return;
      if (targetIndex === currentScopeIndex) return;
      workingRef.current = true;
      setAdvancingScope(true);
      try {
        const session = await api.post<StudySession>(
          `/study/sessions/${sessionId}/goto-scope`,
          { scope_index: targetIndex },
        );
        gotoScope(session);
        highlight.clearAll();
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "Failed to switch scope",
        );
      } finally {
        workingRef.current = false;
        setAdvancingScope(false);
      }
    },
    [sessionId, currentScopeIndex, gotoScope, highlight, setError],
  );

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

  // For finished scopes the user is reviewing, derive feedback from the
  // stored attempt + the answer details the API joins in. Lets the QuizCard
  // render prior verdicts without re-submitting each question.
  const displayFeedback = useMemo(() => {
    if (feedback) return feedback;
    if (!currentQuestion) return null;
    const attempt = attempts.find((a) => a.question_id === currentQuestion.id);
    if (!attempt || !attempt.correct_option) return null;
    return {
      question_id: attempt.question_id,
      correct: attempt.correct,
      correct_option: attempt.correct_option,
      chosen_option: attempt.chosen_option,
      explanation: attempt.explanation || "",
    };
  }, [feedback, currentQuestion, attempts]);

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
        // applyAnswer installs response.phase into the store — no more
        // local "if scope_complete set feedback" heuristic. See store.
        applyAnswer(currentQuestion.id, chosenOption, response);
      } catch (err) {
        // 409 means the session advanced elsewhere (another tab finished
        // the scope, or /next-scope was called). Re-fetch so the UI
        // realigns instead of showing a stale quiz.
        if (err instanceof ApiError && err.status === 409) {
          try {
            const fresh = await api.post<StudySession>("/study/sessions", {
              book_id: bookId,
              chapter_id: chapterId,
            });
            setSession(fresh);
          } catch {
            setError(err.message);
          }
        } else {
          setError(
            err instanceof Error ? err.message : "Failed to submit answer",
          );
        }
      } finally {
        setSubmitting(false);
      }
    },
    [
      sessionId,
      currentQuestion,
      submitting,
      applyAnswer,
      setError,
      setSession,
      bookId,
      chapterId,
    ],
  );

  const handleNextQuestion = useCallback(() => {
    advanceQuestion();
  }, [advanceQuestion]);

  const navigateTo = useCallback((target: Exclude<StudyPhase, "done">) => {
    useStudySessionStore.setState({ phase: target });
  }, []);

  const currentScope = useMemo(() => session?.scope ?? null, [session]);
  const isLastScope = currentScopeIndex >= totalScopes - 1;

  const phaseIdx = (() => {
    if (phase === "done") return PHASE_ORDER.length;
    return PHASE_ORDER.indexOf(phase as Exclude<StudyPhase, "done">);
  })();

  const stateOf = useCallback(
    (p: PhaseKey): PhaseState => {
      const target: Exclude<StudyPhase, "done"> =
        p === "read"
          ? "read"
          : p === "explain"
            ? "explain"
            : p === "practice"
              ? "practice"
              : "feedback";
      const i = PHASE_ORDER.indexOf(target);
      if (phase === "done") return "done";
      if (i < phaseIdx) return "done";
      if (i === phaseIdx) return "active";
      return "pending";
    },
    [phase, phaseIdx],
  );

  useEffect(() => {
    const node = threadRef.current?.querySelector(
      "[data-active-phase='true']",
    );
    (node as HTMLElement | null)?.scrollIntoView?.({
      behavior: "smooth",
      block: "center",
    });
  }, [phase]);

  if (loading) {
    return (
      <div className="p-4">
        <div className="rounded-2xl border border-border/70 bg-card/40 p-4 ring-1 ring-foreground/5">
          <div className="flex items-center gap-2 text-muted-foreground">
            <Loader2 className="h-3.5 w-3.5 animate-spin" />
            <span className="text-[12px]">{t("starting")}</span>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4">
        <div className="rounded-2xl border border-destructive/40 bg-destructive/5 p-4 ring-1 ring-destructive/10">
          <div className="flex items-start gap-2 text-destructive">
            <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" />
            <span className="text-[12.5px]">{error}</span>
          </div>
        </div>
      </div>
    );
  }

  if (noContent) {
    return (
      <div className="p-4">
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
      </div>
    );
  }

  if (!sessionId) return null;

  const sessionDone = phase === "done";
  // A scope is "finished" if the user has already moved past it (so it's
  // strictly below their max-reached). Used to surface a Reviewing badge so
  // the user knows nothing they do here will re-grade or re-charge.
  const reviewingFinishedScope = currentScopeIndex < maxScopeReached;

  return (
    <div className="flex min-w-0 flex-col">
      <header className="sticky top-0 z-10 flex flex-col gap-2.5 border-b border-sidebar-border/60 bg-sidebar/90 px-4 pb-3 pt-4 backdrop-blur-md">
        <div className="flex items-center gap-2">
          <Sparkles className="h-3 w-3 shrink-0 text-primary" />
          <span className="whitespace-nowrap font-mono text-[10.5px] font-medium uppercase tracking-[0.14em] text-muted-foreground">
            {t("guided_study")}
          </span>
          {reviewingFinishedScope && (
            <span
              title={t("scope_finished_hint")}
              className="ml-auto inline-flex items-center gap-1 rounded-full border border-emerald-500/30 bg-emerald-500/10 px-2 py-[1px] font-mono text-[9.5px] font-semibold uppercase tracking-[0.12em] text-emerald-600 dark:text-emerald-400"
            >
              <span className="inline-block h-1.5 w-1.5 rounded-full bg-emerald-500" />
              {t("scope_finished_badge")}
            </span>
          )}
        </div>
        <h2 className="font-heading text-[16px] font-semibold leading-tight tracking-tight">
          {t("chapter_session")}
        </h2>
        <ScopeSelector
          scopes={scopes}
          currentScopeIndex={currentScopeIndex}
          maxScopeReached={maxScopeReached}
          working={advancingScope}
          onSelect={handleSelectScope}
        />
      </header>

      <div ref={threadRef} className="flex flex-col gap-2 px-4 pb-4 pt-3">
        {sessionDone && (
          <motion.div
            layout
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.25, ease: "easeOut" }}
            className="rounded-2xl border border-border/70 bg-card/60 p-5 text-center ring-1 ring-foreground/5"
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

        <div data-active-phase={stateOf("read") === "active"}>
          {currentScope && (
            <ReadingScopePanel
              scope={currentScope}
              highlight={highlight}
              onFinishReading={handleFinishReading}
              working={false}
              state={stateOf("read")}
              onExpand={() => navigateTo("read")}
            />
          )}
        </div>

        <div data-active-phase={stateOf("explain") === "active"}>
          {sessionId && currentScope && (
            <ExplanationPanel
              sessionId={sessionId}
              onExplanationDone={handleExplanationDone}
              state={stateOf("explain")}
              onExpand={() => navigateTo("explain")}
            />
          )}
        </div>

        <div data-active-phase={stateOf("practice") === "active"}>
          {stateOf("practice") === "active" && !currentQuestion ? (
            <div className="rounded-2xl border border-border/70 bg-card/60 p-4 ring-1 ring-foreground/5">
              <div className="flex items-center gap-2 text-muted-foreground">
                <Loader2 className="h-3.5 w-3.5 animate-spin" />
                <span className="text-[12px]">{t("loading_questions")}</span>
              </div>
            </div>
          ) : currentQuestion ? (
            <QuizCard
              question={currentQuestion}
              index={questions.indexOf(currentQuestion)}
              total={questions.length}
              feedback={displayFeedback}
              submitting={submitting}
              onSubmit={handleSubmitAnswer}
              onNext={handleNextQuestion}
              state={stateOf("practice")}
              onExpand={() => navigateTo("practice")}
            />
          ) : (
            <QuizCardPlaceholder state={stateOf("practice")} />
          )}
        </div>

        <div data-active-phase={stateOf("feedback") === "active"}>
          <FeedbackCard
            correct={scopeScore.correct}
            total={scopeScore.total}
            isLastScope={isLastScope}
            working={advancingScope}
            onAdvance={handleAdvanceScope}
            state={stateOf("feedback")}
            onExpand={() => navigateTo("feedback")}
          />
        </div>
      </div>
    </div>
  );
}

function QuizCardPlaceholder({ state }: { state: PhaseState }) {
  const t = useTranslations("study");
  if (state === "pending") {
    return (
      <div className="flex items-center gap-3 px-1 py-2.5 text-muted-foreground/75">
        <div className="flex h-[22px] w-[22px] shrink-0 items-center justify-center rounded-full border border-dashed border-border/70 bg-subtle/50">
          <span className="font-mono text-[9.5px] tabular-nums text-muted-foreground/70">
            3
          </span>
        </div>
        <span className="shrink-0 font-mono text-[10.5px] font-medium uppercase tracking-[0.1em]">
          {t("phase.practice")}
        </span>
        <span className="h-px flex-1 bg-border/50" />
        <span className="font-mono text-[10px] uppercase tracking-[0.08em] text-muted-foreground/70">
          {t("phase_waiting")}
        </span>
      </div>
    );
  }
  return null;
}
