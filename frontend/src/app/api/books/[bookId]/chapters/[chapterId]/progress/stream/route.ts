import { NextRequest } from "next/server";
import { proxySSE } from "@/lib/backend-fetch";

export async function GET(
  _request: NextRequest,
  { params }: { params: Promise<{ bookId: string; chapterId: string }> },
) {
  const { bookId, chapterId } = await params;
  return proxySSE(
    `/api/books/${bookId}/chapters/${chapterId}/progress/stream`,
  );
}
