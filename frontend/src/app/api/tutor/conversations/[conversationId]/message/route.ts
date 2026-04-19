import { NextRequest } from "next/server";
import { proxySSE } from "@/lib/backend-fetch";

export async function POST(
  request: NextRequest,
  { params }: { params: Promise<{ conversationId: string }> },
) {
  const { conversationId } = await params;
  const body = await request.text();
  return proxySSE(`/api/tutor/conversations/${conversationId}/message`, {
    method: "POST",
    body,
  });
}
