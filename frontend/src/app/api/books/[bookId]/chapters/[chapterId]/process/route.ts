import { NextRequest, NextResponse } from "next/server";

const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8000";

export async function POST(
  _request: NextRequest,
  { params }: { params: Promise<{ bookId: string; chapterId: string }> },
) {
  const { bookId, chapterId } = await params;
  const res = await fetch(
    `${BACKEND_URL}/api/books/${bookId}/chapters/${chapterId}/process`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    },
  );
  const data = await res.json();
  return NextResponse.json(data, { status: res.status });
}
