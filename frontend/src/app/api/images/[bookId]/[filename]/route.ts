import { NextRequest, NextResponse } from "next/server";
import { backendFetch } from "@/lib/backend-fetch";

export async function GET(
  _request: NextRequest,
  { params }: { params: Promise<{ bookId: string; filename: string }> },
) {
  const { bookId, filename } = await params;
  const res = await backendFetch(`/api/images/${bookId}/${filename}`);

  if (!res.ok) {
    return NextResponse.json({ error: "Image not found" }, { status: res.status });
  }

  const contentType = res.headers.get("content-type") || "image/png";
  const buffer = await res.arrayBuffer();

  return new NextResponse(buffer, {
    status: 200,
    headers: {
      "Content-Type": contentType,
      "Cache-Control": "public, max-age=31536000, immutable",
    },
  });
}
