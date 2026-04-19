/**
 * Parse a `fetch()` Response body as a Server-Sent Events stream.
 *
 * Yields one `{ event, data }` pair per blank-line-terminated SSE block.
 * Per the SSE spec, multi-line payloads are encoded as multiple `data:`
 * lines; we concatenate them with `\n` (which is what the server intended
 * and what the client needs to reassemble multi-line tokens / JSON that
 * happen to contain embedded newlines).
 *
 * Use with EventSourceResponse-style SSE from the backend where the server
 * emits `event:` + one-or-more `data:` lines separated by a blank line.
 */
export async function* parseSSEStream(
  res: Response,
): AsyncGenerator<{ event: string; data: string }> {
  const reader = res.body?.getReader();
  if (!reader) return;

  const decoder = new TextDecoder();
  let buffer = "";

  function* parseBlock(block: string): Generator<{ event: string; data: string }> {
    let event = "";
    const dataLines: string[] = [];
    for (const raw of block.split("\n")) {
      // Strip a single trailing \r for CRLF-terminated streams.
      const line = raw.endsWith("\r") ? raw.slice(0, -1) : raw;
      if (!line) continue;
      if (line.startsWith("event:")) {
        event = line.slice(6).trimStart();
      } else if (line.startsWith("data:")) {
        // `data:` with no space is valid; `data: foo` strips one leading space.
        const rest = line.slice(5);
        dataLines.push(rest.startsWith(" ") ? rest.slice(1) : rest);
      }
      // Other SSE fields (`id:`, `retry:`, comments starting with `:`) ignored.
    }
    if (event || dataLines.length > 0) {
      yield { event, data: dataLines.join("\n") };
    }
  }

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });

      // SSE blocks are separated by a blank line. Accept both "\n\n" and
      // "\r\n\r\n". Split greedily; keep the trailing partial block in `buffer`.
      const parts = buffer.split(/\r?\n\r?\n/);
      buffer = parts.pop() ?? "";
      for (const block of parts) {
        yield* parseBlock(block);
      }
    }
    // Flush any trailing block that wasn't terminated by a blank line.
    if (buffer.length > 0) {
      yield* parseBlock(buffer);
    }
  } finally {
    reader.releaseLock();
  }
}
