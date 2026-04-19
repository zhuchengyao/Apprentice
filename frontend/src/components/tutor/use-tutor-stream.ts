"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { parseSSEStream } from "@/lib/sse";

export interface StreamEventHandlers {
  /** Called for each non-token SSE event. Return `true` to signal completion
   *  (e.g. on `done` or `error`) so the hook flips `streaming` back to false. */
  onEvent?: (event: string, data: string) => boolean | void;
}

export interface StreamController {
  streaming: boolean;
  buffer: string;
  /** POST to `url` and consume SSE. Resets buffer on start; tokens accumulate
   *  into `buffer`. The returned promise resolves once the stream ends. */
  run: (url: string, init?: RequestInit) => Promise<void>;
  abort: () => void;
  resetBuffer: () => void;
}

/** Thin SSE streaming wrapper. The caller supplies a handler for non-token
 *  events — this hook owns the abort controller, token accumulation, and the
 *  `streaming` flag so components don't have to reinvent them. */
export function useTutorStream(
  handlers: StreamEventHandlers = {},
): StreamController {
  const [streaming, setStreaming] = useState(false);
  const [buffer, setBuffer] = useState("");
  const abortRef = useRef<AbortController | null>(null);
  const handlersRef = useRef(handlers);
  handlersRef.current = handlers;

  useEffect(() => {
    return () => {
      abortRef.current?.abort();
    };
  }, []);

  const abort = useCallback(() => {
    abortRef.current?.abort();
    abortRef.current = null;
    setStreaming(false);
  }, []);

  const resetBuffer = useCallback(() => setBuffer(""), []);

  const run = useCallback(
    async (url: string, init?: RequestInit) => {
      abortRef.current?.abort();
      const controller = new AbortController();
      abortRef.current = controller;
      setStreaming(true);
      setBuffer("");

      let accumulated = "";

      try {
        const res = await fetch(url, { ...init, signal: controller.signal });
        if (!res.ok) {
          handlersRef.current.onEvent?.(
            "error",
            `HTTP ${res.status}: ${await res.text().catch(() => "")}`,
          );
          return;
        }
        for await (const { event, data } of parseSSEStream(res)) {
          if (event === "token") {
            accumulated += data;
            setBuffer(accumulated);
            continue;
          }
          const done = handlersRef.current.onEvent?.(event, data);
          if (done) return;
        }
      } catch (err) {
        if (err instanceof DOMException && err.name === "AbortError") return;
        handlersRef.current.onEvent?.(
          "error",
          err instanceof Error ? err.message : String(err),
        );
      } finally {
        setStreaming(false);
        if (abortRef.current === controller) abortRef.current = null;
      }
    },
    [],
  );

  return { streaming, buffer, run, abort, resetBuffer };
}
