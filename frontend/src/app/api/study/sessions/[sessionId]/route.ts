import { NextRequest } from "next/server";
import { proxyJson } from "@/lib/backend-fetch";

export async function GET(
  _request: NextRequest,
  { params }: { params: Promise<{ sessionId: string }> },
) {
  const { sessionId } = await params;
  return proxyJson(`/api/study/sessions/${sessionId}`);
}
