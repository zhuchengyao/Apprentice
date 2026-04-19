import { NextRequest } from "next/server";
import { proxySSE } from "@/lib/backend-fetch";

export async function POST(
  request: NextRequest,
  { params }: { params: Promise<{ sessionId: string }> },
) {
  const { sessionId } = await params;
  return proxySSE(`/api/study/sessions/${sessionId}/advance`, {
    method: "POST",
    signal: request.signal,
  });
}
