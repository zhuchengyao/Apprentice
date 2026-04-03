import { create } from "zustand";
import type { StudySession, KPCardState, KPCardStatus } from "@/lib/types";

interface StudyState {
  session: StudySession | null;
  activeKPIndex: number;
  cardStates: KPCardState[];
  streamTarget: "illustration" | "question" | "deepen" | "secondQuestion" | null;
  streamContent: string;
  isStreaming: boolean;

  setSession: (session: StudySession) => void;
  setActiveKP: (index: number) => void;
  setCardStatus: (index: number, status: KPCardStatus) => void;
  setStreamTarget: (target: StudyState["streamTarget"]) => void;
  setStreaming: (streaming: boolean) => void;
  appendStreamContent: (chunk: string) => void;
  finalizeStream: (index: number) => void;
  setUserAnswer: (index: number, answer: string) => void;
  setFeedback: (index: number, quality: number, feedback: string) => void;
  setSecondAnswer: (index: number, answer: string) => void;
  setSecondFeedback: (index: number, quality: number, feedback: string) => void;
  reset: () => void;
}

function makeEmptyCardState(): KPCardState {
  return {
    status: "pending",
    illustration: "",
    question: "",
    userAnswer: "",
    feedback: null,
    deepenText: "",
    secondQuestion: "",
    secondAnswer: "",
    secondFeedback: null,
  };
}

export const useStudyStore = create<StudyState>((set, get) => ({
  session: null,
  activeKPIndex: 0,
  cardStates: [],
  streamTarget: null,
  streamContent: "",
  isStreaming: false,

  setSession: (session) => {
    // Find the first non-mastered KP to focus on
    const startIndex = session.knowledge_points.findIndex((kp) => !kp.mastered);
    const activeIndex = startIndex >= 0 ? startIndex : 0;

    set({
      session,
      activeKPIndex: activeIndex,
      cardStates: session.knowledge_points.map((kp) => {
        if (kp.mastered) {
          return {
            status: "completed" as const,
            illustration: kp.illustration || "",
            question: kp.question || "",
            userAnswer: "(previously completed)",
            feedback: { quality: 5, feedback: "Previously mastered." },
            deepenText: "",
            secondQuestion: "",
            secondAnswer: "",
            secondFeedback: null,
          };
        }
        return makeEmptyCardState();
      }),
    });
  },

  setActiveKP: (index) => set({ activeKPIndex: index }),

  setCardStatus: (index, status) =>
    set((state) => {
      const cards = [...state.cardStates];
      if (cards[index]) {
        cards[index] = { ...cards[index], status };
      }
      return { cardStates: cards };
    }),

  setStreamTarget: (target) => set({ streamTarget: target, streamContent: "" }),

  setStreaming: (isStreaming) => set({ isStreaming }),

  appendStreamContent: (chunk) =>
    set((state) => ({ streamContent: state.streamContent + chunk })),

  finalizeStream: (index) => {
    const { streamTarget, streamContent, cardStates } = get();
    const cards = [...cardStates];
    if (!cards[index] || !streamTarget) return;

    const card = { ...cards[index] };
    switch (streamTarget) {
      case "illustration":
        card.illustration = streamContent;
        break;
      case "question":
        card.question = streamContent;
        break;
      case "deepen":
        card.deepenText = streamContent;
        break;
      case "secondQuestion":
        card.secondQuestion = streamContent;
        break;
    }
    cards[index] = card;
    set({ cardStates: cards, streamContent: "", streamTarget: null, isStreaming: false });
  },

  setUserAnswer: (index, answer) =>
    set((state) => {
      const cards = [...state.cardStates];
      if (cards[index]) cards[index] = { ...cards[index], userAnswer: answer };
      return { cardStates: cards };
    }),

  setFeedback: (index, quality, feedback) =>
    set((state) => {
      const cards = [...state.cardStates];
      if (cards[index]) cards[index] = { ...cards[index], feedback: { quality, feedback } };
      return { cardStates: cards };
    }),

  setSecondAnswer: (index, answer) =>
    set((state) => {
      const cards = [...state.cardStates];
      if (cards[index]) cards[index] = { ...cards[index], secondAnswer: answer };
      return { cardStates: cards };
    }),

  setSecondFeedback: (index, quality, feedback) =>
    set((state) => {
      const cards = [...state.cardStates];
      if (cards[index]) cards[index] = { ...cards[index], secondFeedback: { quality, feedback } };
      return { cardStates: cards };
    }),

  reset: () =>
    set({
      session: null,
      activeKPIndex: 0,
      cardStates: [],
      streamTarget: null,
      streamContent: "",
      isStreaming: false,
    }),
}));
