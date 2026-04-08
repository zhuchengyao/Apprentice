import { NextRequest } from "next/server";

const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8000";

export async function GET(
  _request: NextRequest,
  { params }: { params: Promise<{ bookId: string; chapterId: string }> },
) {
  const { bookId, chapterId } = await params;
  const res = await fetch(
    `${BACKEND_URL}/api/books/${bookId}/chapters/${chapterId}/progress/stream`,
    { cache: "no-store" },
  );

  if (!res.ok || !res.body) {
    return new Response(res.statusText, { status: res.status });
  }

  return new Response(res.body, {
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      Connection: "keep-alive",
    },
  });
}
