"use client";

import { create } from "zustand";
import type {
  AnswerResponse,
  QuestionsResponse,
  QuizQuestion,
  ScopeSummary,
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

  scopes: ScopeSummary[];
  maxScopeReached: number;

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
  gotoScope: (session: StudySession) => void;
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
  scopes: [] as ScopeSummary[],
  maxScopeReached: 0,
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
      const cachedExplanation = session.scope?.explanation_text || "";
      return {
        sessionId: session.id,
        bookId: session.book_id,
        chapterId: session.chapter_id,
        phase: session.phase,
        session,
        currentScopeIndex: session.current_scope_index,
        totalScopes: session.total_scopes,
        currentQuestionIndex: session.current_question_index,
        scopes: session.scopes,
        maxScopeReached: session.max_scope_reached,
        attempts: session.attempts,
        scopeScore: { correct, total: session.attempts.length },
        feedback: null,
        explanation: cachedExplanation,
        explanationStreaming: false,
        // If the server already has a cached explanation for this scope,
        // mark complete so ExplanationPanel skips its re-stream guard.
        explanationComplete:
          !!cachedExplanation ||
          (session.phase !== "read" && session.phase !== "explain"),
      };
    }),

  setPhase: (phase) =>
    set((s) => ({
      phase,
      session: s.session ? { ...s.session, phase } : s.session,
    })),

  setQuestions: (payload) =>
    set((s) => {
      const correct = payload.answered.filter((a) => a.correct).length;
      const allAnswered =
        payload.total > 0 && payload.answered.length >= payload.total;
      return {
        questions: payload.questions,
        attempts: payload.answered,
        scopeScore: { correct, total: payload.answered.length },
        // Review mode (every question already answered): start at the first
        // question so the user can step through their prior answers. Live
        // mode: jump to the first unanswered question.
        currentQuestionIndex: allAnswered
          ? 0
          : Math.min(
              payload.answered.length,
              Math.max(0, payload.total - 1),
            ),
        // Reconcile against authoritative server phase.
        phase: payload.phase,
        session: s.session ? { ...s.session, phase: payload.phase } : s.session,
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
        // Trust the server's authoritative phase. Previously the submit
        // handler derived this locally from `scope_complete`, which meant
        // a second tab could stay on PRACTICE after the server (driven
        // by the other tab) had already moved to FEEDBACK.
        phase: response.phase,
        session: s.session ? { ...s.session, phase: response.phase } : s.session,
      };
    }),

  advanceQuestion: () =>
    set((s) => {
      const answeredIds = new Set(s.attempts.map((a) => a.question_id));
      const allAnswered =
        s.questions.length > 0 && answeredIds.size >= s.questions.length;
      // Review mode: walk linearly so the user can re-read each prior
      // attempt. Past the last question, fall through to feedback.
      if (allAnswered) {
        const nextIdx = s.currentQuestionIndex + 1;
        if (nextIdx >= s.questions.length) {
          return {
            currentQuestionIndex: s.questions.length,
            feedback: null,
            phase: "feedback",
          };
        }
        return { currentQuestionIndex: nextIdx, feedback: null };
      }
      // Live mode: jump to the next unanswered question.
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
        scopes: session.scopes,
        maxScopeReached: session.max_scope_reached,
        questions: [],
        attempts: session.attempts,
        feedback: null,
        scopeScore: { correct, total: session.attempts.length },
        explanation: "",
        explanationStreaming: false,
        explanationComplete: false,
      };
    }),

  // Jump to a previously-reached scope for review. The server returns the
  // session pinned at `feedback` for the target scope and (for finished
  // scopes) attaches the cached explanation. We hydrate that here so the
  // user can re-open Explain without triggering a fresh LLM stream.
  gotoScope: (session) =>
    set(() => {
      const correct = session.attempts.filter((a) => a.correct).length;
      const cachedExplanation = session.scope?.explanation_text || "";
      return {
        session,
        phase: session.phase,
        currentScopeIndex: session.current_scope_index,
        totalScopes: session.total_scopes,
        currentQuestionIndex: session.current_question_index,
        scopes: session.scopes,
        maxScopeReached: session.max_scope_reached,
        questions: [],
        attempts: session.attempts,
        feedback: null,
        scopeScore: { correct, total: session.attempts.length },
        explanation: cachedExplanation,
        explanationStreaming: false,
        explanationComplete: !!cachedExplanation,
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
