import { NextRequest } from "next/server";
import { proxyJson } from "@/lib/backend-fetch";

export async function POST(
  request: NextRequest,
  { params }: { params: Promise<{ sessionId: string }> },
) {
  const { sessionId } = await params;
  const body = await request.text();
  return proxyJson(`/api/study/sessions/${sessionId}/goto-scope`, {
    method: "POST",
    body,
  });
}
