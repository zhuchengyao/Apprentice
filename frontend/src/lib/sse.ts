/**
 * Parse a `fetch()` Response body as a Server-Sent Events stream.
 *
 * Yields one `{ event, data }` pair per `event: x\ndata: y` block. Any leading
 * stream content before the first `event:` line is skipped. Malformed blocks
 * (e.g., `event:` with no following `data:`) still yield with an empty `data`.
 *
 * Use with EventSourceResponse-style SSE from the backend where the server
 * emits `event:` + `data:` line pairs separated by blank lines.
 */
export async function* parseSSEStream(
  res: Response,
): AsyncGenerator<{ event: string; data: string }> {
  const reader = res.body?.getReader();
  if (!reader) return;

  const decoder = new TextDecoder();
  let buffer = "";

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop() ?? "";

      for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        if (!line.startsWith("event: ")) continue;

        const event = line.slice(7).trim();
        let data = "";
        if (i + 1 < lines.length && lines[i + 1].startsWith("data: ")) {
          data = lines[i + 1].slice(6);
          i++;
        }
        yield { event, data };
      }
    }
  } finally {
    reader.releaseLock();
  }
}
