"use client";

import { useCallback, useRef } from "react";
import { useStudyStore } from "@/stores/study-store";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "/api";

const MAX_RECONNECT_RETRIES = 3;
const RECONNECT_DELAY_MS = 2000;

export function useStudySession() {
  const eventSourceRef = useRef<EventSource | null>(null);
  const retryCountRef = useRef(0);
  const store = useStudyStore;

  const connect = useCallback((sessionId: string) => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
    }

    const es = new EventSource(
      `${API_BASE}/study/sessions/${sessionId}/stream`,
    );
    eventSourceRef.current = es;

    es.addEventListener("state_change", (e) => {
      // Reset retry count on successful event
      retryCountRef.current = 0;

      const { state, current_kp_index } = JSON.parse(e.data);
      const s = store.getState();

      // Update session state
      if (s.session) {
        store.setState({
          session: { ...s.session, state, current_kp_index },
          activeKPIndex: current_kp_index,
        });
      }

      // Map backend state to card status + stream target
      switch (state) {
        case "explain":
          s.setCardStatus(current_kp_index, "illustrating");
          s.setStreamTarget("illustration");
          s.setStreaming(true);
          break;
        case "check": {
          const card = s.cardStates[current_kp_index];
          if (card?.deepenText) {
            // This is the second check after deepen
            s.setStreamTarget("secondQuestion");
          } else {
            s.setStreamTarget("question");
          }
          s.setCardStatus(current_kp_index, "checking");
          s.setStreaming(true);
          break;
        }
        case "evaluate":
          s.setCardStatus(current_kp_index, "evaluating");
          break;
        case "deepen":
          s.setCardStatus(current_kp_index, "deepening");
          s.setStreamTarget("deepen");
          s.setStreaming(true);
          break;
      }
    });

    es.addEventListener("token", (e) => {
      store.getState().appendStreamContent(e.data);
    });

    es.addEventListener("stream_complete", (e) => {
      const s = store.getState();
      s.finalizeStream(s.activeKPIndex);
    });

    es.addEventListener("feedback", (e) => {
      const { quality, feedback } = JSON.parse(e.data);
      const s = store.getState();
      const card = s.cardStates[s.activeKPIndex];
      // If we already have first feedback, this is second
      if (card?.feedback) {
        s.setSecondFeedback(s.activeKPIndex, quality, feedback);
      } else {
        s.setFeedback(s.activeKPIndex, quality, feedback);
      }
    });

    es.addEventListener("waiting_advance", () => {
      // Legacy — kept for compatibility
    });

    es.addEventListener("waiting", () => {
      // Agent is idle, waiting for user to select a KP or answer
    });

    es.addEventListener("kp_complete", (e) => {
      const { kp_index } = JSON.parse(e.data);
      store.getState().setCardStatus(kp_index, "completed");
    });

    es.addEventListener("error", () => {
      store.getState().setStreaming(false);
      es.close();
      eventSourceRef.current = null;

      // Auto-reconnect (backend will reconstruct the agent from DB state)
      if (retryCountRef.current < MAX_RECONNECT_RETRIES) {
        retryCountRef.current++;
        setTimeout(() => connect(sessionId), RECONNECT_DELAY_MS);
      }
    });

    es.addEventListener("done", () => {
      store.getState().setStreaming(false);
      es.close();
    });

    return () => {
      es.close();
      eventSourceRef.current = null;
    };
  }, []);

  const disconnect = useCallback(() => {
    eventSourceRef.current?.close();
    eventSourceRef.current = null;
    store.getState().setStreaming(false);
  }, []);

  const sendMessage = useCallback(async (sessionId: string, content: string) => {
    const res = await fetch(
      `${API_BASE}/study/sessions/${sessionId}/message`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content }),
      },
    );
    if (!res.ok) {
      throw new Error("Failed to send message");
    }
    return res.json();
  }, []);

  return { connect, disconnect, sendMessage };
}
