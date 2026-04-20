"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { useTranslations } from "next-intl";
import { ArrowRight, Check, Loader2, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Markdown } from "@/components/ui/markdown";
import { cn } from "@/lib/utils";
import type { QuizQuestion } from "@/lib/types";
import type { QuestionFeedback } from "@/lib/stores/study-session";
import { PhaseShell, type PhaseState } from "./phase-shell";

interface Props {
  question: QuizQuestion;
  index: number;
  total: number;
  feedback: QuestionFeedback | null;
  submitting: boolean;
  onSubmit: (chosenOption: string, timeSpentMs: number) => Promise<void> | void;
  onNext: () => void;
  state: PhaseState;
  onExpand?: () => void;
}

export function QuizCard({
  question,
  index,
  total,
  feedback,
  submitting,
  onSubmit,
  onNext,
  state,
  onExpand,
}: Props) {
  const t = useTranslations("study");
  const [selected, setSelected] = useState<string | null>(null);
  const [startedAt] = useState<number>(() => Date.now());

  const answered = feedback?.question_id === question.id;

  if (state === "pending") {
    return <PhaseShell phase="practice" state="pending" />;
  }

  if (state === "done") {
    return (
      <PhaseShell
        phase="practice"
        state="done"
        meta={t("quiz_question_progress", {
          current: index + 1,
          total,
        })}
        onExpand={onExpand}
      />
    );
  }

  const submit = async () => {
    if (!selected || answered || submitting) return;
    const elapsed = Date.now() - startedAt;
    await onSubmit(selected, elapsed);
  };

  return (
    <PhaseShell
      phase="practice"
      state="active"
      meta={t("quiz_question_progress", { current: index + 1, total })}
    >
      <motion.div
        key={question.id}
        animate={
          answered && feedback?.correct
            ? {
                scale: [1, 1.015, 1],
                transition: { duration: 0.45, times: [0, 0.4, 1] },
              }
            : answered && feedback && !feedback.correct
              ? {
                  x: [0, -5, 5, -3, 3, 0],
                  transition: { duration: 0.45 },
                }
              : { scale: 1, x: 0 }
        }
        className="flex flex-col gap-3"
      >
        <div className="prose prose-sm dark:prose-invert max-w-none font-heading text-[15.5px] font-semibold leading-snug tracking-tight [&>*:first-child]:mt-0 [&>*:last-child]:mb-0">
          <Markdown>{question.stem}</Markdown>
        </div>

        <div className="flex flex-col gap-1.5">
          {question.options.map((opt, i) => {
            const isChosen = answered
              ? feedback?.chosen_option === opt.key
              : selected === opt.key;
            const showAsCorrect = answered && opt.key === feedback?.correct_option;
            const showAsWrong = answered && isChosen && !feedback?.correct;

            return (
              <button
                key={opt.key}
                type="button"
                onClick={() => !answered && !submitting && setSelected(opt.key)}
                disabled={answered || submitting}
                className={cn(
                  "group flex items-start gap-2.5 rounded-xl border px-3 py-2 text-left text-[13px] transition-all",
                  !answered &&
                    (isChosen
                      ? "border-primary/45 bg-primary/8"
                      : "border-border/60 bg-background hover:border-border/80 hover:bg-subtle/40"),
                  showAsCorrect &&
                    "border-emerald-500/45 bg-emerald-500/10",
                  showAsWrong && "border-rose-500/45 bg-rose-500/10",
                  answered && !showAsCorrect && !showAsWrong && "opacity-70",
                )}
              >
                <span
                  className={cn(
                    "mt-[3px] w-[14px] shrink-0 font-mono text-[10px] font-semibold uppercase tracking-[0.08em] tabular-nums",
                    showAsCorrect && "text-emerald-600 dark:text-emerald-400",
                    showAsWrong && "text-rose-600 dark:text-rose-400",
                    !showAsCorrect && !showAsWrong && "text-muted-foreground",
                  )}
                >
                  {String.fromCharCode(65 + i)}
                </span>
                <span className="prose prose-sm dark:prose-invert min-w-0 max-w-none flex-1 text-[13px] leading-[1.5] [&>*:first-child]:mt-0 [&>*:last-child]:mb-0">
                  <Markdown>{opt.text}</Markdown>
                </span>
                {showAsCorrect && (
                  <Check className="mt-0.5 h-3.5 w-3.5 shrink-0 text-emerald-600 dark:text-emerald-400" />
                )}
                {showAsWrong && (
                  <X className="mt-0.5 h-3.5 w-3.5 shrink-0 text-rose-600 dark:text-rose-400" />
                )}
              </button>
            );
          })}
        </div>

        {answered && feedback && (
          <motion.div
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.2 }}
            className={cn(
              "rounded-xl border px-3 py-2.5 text-[12.5px] leading-[1.55]",
              feedback.correct
                ? "border-emerald-500/25 bg-emerald-500/5"
                : "border-primary/20 bg-primary/5",
            )}
          >
            <div
              className={cn(
                "mb-1 font-mono text-[10px] font-semibold uppercase tracking-[0.1em]",
                feedback.correct
                  ? "text-emerald-600 dark:text-emerald-400"
                  : "text-primary",
              )}
            >
              {feedback.correct ? t("correct") : t("incorrect")}
            </div>
            {!feedback.correct && (
              <p className="mb-1 text-[11.5px] text-muted-foreground">
                {t("correct_answer_was", { option: feedback.correct_option })}
              </p>
            )}
            <div className="prose prose-sm dark:prose-invert max-w-none text-[12.5px] leading-[1.55] text-foreground/90 [&>*:first-child]:mt-0 [&>*:last-child]:mb-0">
              <Markdown>{feedback.explanation}</Markdown>
            </div>
            {!feedback.correct && (
              <p className="mt-1 text-[11.5px] italic text-muted-foreground">
                {t("missed_it_reassure")}
              </p>
            )}
          </motion.div>
        )}

        <div className="flex justify-end gap-2">
          {!answered ? (
            <Button
              size="sm"
              variant="primary"
              disabled={!selected || submitting}
              onClick={submit}
              className="h-8 gap-1.5 rounded-full px-3 text-[12px]"
            >
              {submitting ? (
                <Loader2 className="h-3.5 w-3.5 animate-spin" />
              ) : (
                <>
                  {t("quiz_submit")}
                  <ArrowRight className="h-3.5 w-3.5" />
                </>
              )}
            </Button>
          ) : (
            <Button
              size="sm"
              variant="primary"
              onClick={onNext}
              className="h-8 gap-1.5 rounded-full px-3 text-[12px]"
            >
              {t("quiz_next")}
              <ArrowRight className="h-3.5 w-3.5" />
            </Button>
          )}
        </div>
      </motion.div>
    </PhaseShell>
  );
}
