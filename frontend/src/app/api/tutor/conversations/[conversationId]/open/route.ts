import { NextRequest } from "next/server";
import { proxySSE } from "@/lib/backend-fetch";

export async function POST(
  request: NextRequest,
  { params }: { params: Promise<{ conversationId: string }> },
) {
  const { conversationId } = await params;
  return proxySSE(`/api/tutor/conversations/${conversationId}/open`, {
    method: "POST",
    signal: request.signal,
  });
}
