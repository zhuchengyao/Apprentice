import { NextRequest } from "next/server";
import { proxyJson } from "@/lib/backend-fetch";

export async function POST(
  _request: NextRequest,
  { params }: { params: Promise<{ bookId: string; chapterId: string }> },
) {
  const { bookId, chapterId } = await params;
  return proxyJson(`/api/books/${bookId}/chapters/${chapterId}/process`, {
    method: "POST",
  });
}
