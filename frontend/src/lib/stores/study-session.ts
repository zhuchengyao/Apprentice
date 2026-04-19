"use client";

import { create } from "zustand";
import type {
  AnswerResponse,
  QuestionsResponse,
  QuizQuestion,
  StudyAttempt,
  StudyPhase,
  StudySession,
} from "@/lib/types";

export interface QuestionFeedback {
  question_id: string;
  correct: boolean;
  correct_option: string;
  chosen_option: string;
  explanation: string;
}

interface StudySessionState {
  sessionId: string | null;
  bookId: string | null;
  chapterId: string | null;
  phase: StudyPhase;
  session: StudySession | null;

  currentScopeIndex: number;
  totalScopes: number;
  currentQuestionIndex: number;

  questions: QuizQuestion[];
  attempts: StudyAttempt[];
  feedback: QuestionFeedback | null;
  scopeScore: { correct: number; total: number };

  explanation: string;
  explanationStreaming: boolean;
  explanationComplete: boolean;

  loading: boolean;
  error: string | null;

  // Actions
  setSession: (session: StudySession) => void;
  setPhase: (phase: StudyPhase) => void;
  setQuestions: (payload: QuestionsResponse) => void;
  applyAnswer: (
    questionId: string,
    chosenOption: string,
    response: AnswerResponse,
  ) => void;
  advanceQuestion: () => void;
  advanceScope: (session: StudySession, done: boolean) => void;
  setExplanation: (text: string, streaming: boolean) => void;
  appendExplanation: (chunk: string) => void;
  completeExplanation: () => void;
  setLoading: (v: boolean) => void;
  setError: (msg: string | null) => void;
  reset: () => void;
}

const initialState = {
  sessionId: null,
  bookId: null,
  chapterId: null,
  phase: "read" as StudyPhase,
  session: null,
  currentScopeIndex: 0,
  totalScopes: 0,
  currentQuestionIndex: 0,
  questions: [],
  attempts: [],
  feedback: null,
  scopeScore: { correct: 0, total: 0 },
  explanation: "",
  explanationStreaming: false,
  explanationComplete: false,
  loading: false,
  error: null,
};

export const useStudySessionStore = create<StudySessionState>((set) => ({
  ...initialState,

  setSession: (session) =>
    set(() => {
      const correct = session.attempts.filter((a) => a.correct).length;
      return {
        sessionId: session.id,
        bookId: session.book_id,
        chapterId: session.chapter_id,
        phase: session.phase,
        session,
        currentScopeIndex: session.current_scope_index,
        totalScopes: session.total_scopes,
        currentQuestionIndex: session.current_question_index,
        attempts: session.attempts,
        scopeScore: { correct, total: session.attempts.length },
        feedback: null,
        explanation: "",
        explanationStreaming: false,
        explanationComplete: session.phase !== "read" && session.phase !== "explain",
      };
    }),

  setPhase: (phase) =>
    set((s) => ({
      phase,
      session: s.session ? { ...s.session, phase } : s.session,
    })),

  setQuestions: (payload) =>
    set(() => {
      const correct = payload.answered.filter((a) => a.correct).length;
      return {
        questions: payload.questions,
        attempts: payload.answered,
        scopeScore: { correct, total: payload.answered.length },
        currentQuestionIndex: Math.min(
          payload.answered.length,
          Math.max(0, payload.total - 1),
        ),
      };
    }),

  applyAnswer: (questionId, chosenOption, response) =>
    set((s) => {
      const nextAttempts = [
        ...s.attempts.filter((a) => a.question_id !== questionId),
        {
          question_id: questionId,
          chosen_option: chosenOption,
          correct: response.correct,
        },
      ];
      const feedback: QuestionFeedback = {
        question_id: questionId,
        correct: response.correct,
        correct_option: response.correct_option,
        chosen_option: chosenOption,
        explanation: response.explanation,
      };
      return {
        attempts: nextAttempts,
        feedback,
        scopeScore: response.scope_score,
      };
    }),

  advanceQuestion: () =>
    set((s) => {
      const answeredIds = new Set(s.attempts.map((a) => a.question_id));
      const nextIdx = s.questions.findIndex((q) => !answeredIds.has(q.id));
      if (nextIdx === -1) {
        return {
          currentQuestionIndex: s.questions.length,
          feedback: null,
          phase: "feedback",
        };
      }
      return {
        currentQuestionIndex: nextIdx,
        feedback: null,
      };
    }),

  advanceScope: (session, done) =>
    set(() => {
      const correct = session.attempts.filter((a) => a.correct).length;
      return {
        session,
        phase: done ? "done" : session.phase,
        currentScopeIndex: session.current_scope_index,
        totalScopes: session.total_scopes,
        currentQuestionIndex: session.current_question_index,
        questions: [],
        attempts: session.attempts,
        feedback: null,
        scopeScore: { correct, total: session.attempts.length },
        explanation: "",
        explanationStreaming: false,
        explanationComplete: false,
      };
    }),

  setExplanation: (text, streaming) =>
    set(() => ({ explanation: text, explanationStreaming: streaming })),

  appendExplanation: (chunk) =>
    set((s) => ({
      explanation: s.explanation + chunk,
      explanationStreaming: true,
    })),

  completeExplanation: () =>
    set(() => ({
      explanationStreaming: false,
      explanationComplete: true,
    })),

  setLoading: (v) => set(() => ({ loading: v })),
  setError: (msg) => set(() => ({ error: msg })),

  reset: () => set(() => ({ ...initialState })),
}));
