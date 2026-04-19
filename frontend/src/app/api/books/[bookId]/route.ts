import { NextRequest } from "next/server";
import { proxyJson } from "@/lib/backend-fetch";

export async function GET(
  _request: NextRequest,
  { params }: { params: Promise<{ bookId: string }> },
) {
  const { bookId } = await params;
  return proxyJson(`/api/books/${bookId}`);
}

export async function DELETE(
  _request: NextRequest,
  { params }: { params: Promise<{ bookId: string }> },
) {
  const { bookId } = await params;
  return proxyJson(`/api/books/${bookId}`, { method: "DELETE" });
}
