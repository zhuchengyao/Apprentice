"use client";

import { useEffect, useCallback } from "react";
import { useStudyStore } from "@/stores/study-store";
import { useStudySession } from "@/hooks/use-study-session";
import { KPCard } from "./kp-card";
import { Progress, ProgressLabel, ProgressValue } from "@/components/ui/progress";
import type { StudySession } from "@/lib/types";

interface StudySessionClientProps {
  initialSession: StudySession;
}

const VISIBLE_BATCH = 4;

export function StudySessionClient({ initialSession }: StudySessionClientProps) {
  const { connect, disconnect, sendMessage } = useStudySession();
  const session = useStudyStore((s) => s.session);
  const activeKPIndex = useStudyStore((s) => s.activeKPIndex);
  const cardStates = useStudyStore((s) => s.cardStates);
  const streamContent = useStudyStore((s) => s.streamContent);
  const streamTarget = useStudyStore((s) => s.streamTarget);
  const isStreaming = useStudyStore((s) => s.isStreaming);
  const setSession = useStudyStore((s) => s.setSession);
  const setActiveKP = useStudyStore((s) => s.setActiveKP);
  const setUserAnswer = useStudyStore((s) => s.setUserAnswer);
  const setSecondAnswer = useStudyStore((s) => s.setSecondAnswer);
  const reset = useStudyStore((s) => s.reset);

  useEffect(() => {
    setSession(initialSession);
    const cleanup = connect(initialSession.id);
    return () => {
      cleanup?.();
      disconnect();
      reset();
    };
  }, [initialSession, setSession, connect, disconnect, reset]);

  const handleExpand = useCallback(
    (index: number) => {
      if (!session) return;
      const card = cardStates[index];
      if (!card) return;

      setActiveKP(index);

      // Tell the agent which KP the user selected (skip if already completed)
      if (card.status !== "completed") {
        sendMessage(session.id, `select:${index}`);
      }
    },
    [session, cardStates, setActiveKP, sendMessage],
  );

  const handleSendAnswer = useCallback(
    (answer: string) => {
      if (!session) return;
      const card = cardStates[activeKPIndex];
      if (!card) return;

      // Determine if this is a first or second answer
      if (card.feedback && card.feedback.quality < 3 && card.secondQuestion && !card.secondAnswer) {
        setSecondAnswer(activeKPIndex, answer);
      } else {
        setUserAnswer(activeKPIndex, answer);
      }

      sendMessage(session.id, answer);
    },
    [session, activeKPIndex, cardStates, setUserAnswer, setSecondAnswer, sendMessage],
  );

  if (!session) return null;

  const kps = session.knowledge_points;
  const completedCount = cardStates.filter((c) => c.status === "completed").length;
  const progressPercent = kps.length > 0 ? Math.round((completedCount / kps.length) * 100) : 0;

  // Show KPs up to max(activeKPIndex + VISIBLE_BATCH, last completed + VISIBLE_BATCH)
  const visibleCount = Math.min(
    kps.length,
    Math.max(activeKPIndex + VISIBLE_BATCH, completedCount + VISIBLE_BATCH),
  );

  return (
    <div className="space-y-4">
      {/* Progress header */}
      <Progress value={progressPercent}>
        <ProgressLabel>Progress</ProgressLabel>
        <ProgressValue>
          {() => `${completedCount}/${kps.length} knowledge points`}
        </ProgressValue>
      </Progress>

      {/* KP cards */}
      <div className="space-y-3">
        {kps.slice(0, visibleCount).map((kp, i) => (
          <KPCard
            key={kp.id}
            index={i}
            kp={kp}
            cardState={cardStates[i] ?? {
              status: "pending" as const,
              illustration: "",
              question: "",
              userAnswer: "",
              feedback: null,
              deepenText: "",
              secondQuestion: "",
              secondAnswer: "",
              secondFeedback: null,
            }}
            isActive={i === activeKPIndex}
            streamContent={i === activeKPIndex ? streamContent : ""}
            streamTarget={i === activeKPIndex ? streamTarget : null}
            isStreaming={i === activeKPIndex && isStreaming}
            onExpand={handleExpand}
            onSendAnswer={handleSendAnswer}
          />
        ))}
      </div>

      {visibleCount < kps.length && (
        <p className="text-center text-xs text-muted-foreground">
          {kps.length - visibleCount} more knowledge points below...
        </p>
      )}
    </div>
  );
}
