import { NextRequest } from "next/server";

const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8000";

export async function GET(
  _request: NextRequest,
  { params }: { params: Promise<{ sessionId: string }> },
) {
  const { sessionId } = await params;

  const backendRes = await fetch(
    `${BACKEND_URL}/api/study/sessions/${sessionId}/stream`,
    {
      headers: { Accept: "text/event-stream" },
    },
  );

  if (!backendRes.ok || !backendRes.body) {
    return new Response("Failed to connect to stream", {
      status: backendRes.status,
    });
  }

  return new Response(backendRes.body, {
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      Connection: "keep-alive",
    },
  });
}
