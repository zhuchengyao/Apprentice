import { NextRequest, NextResponse } from "next/server";
import { backendFetch } from "@/lib/backend-fetch";

export async function GET(
  _request: NextRequest,
  { params }: { params: Promise<{ filename: string }> },
) {
  const { filename } = await params;
  const res = await backendFetch(`/api/manim/video/${filename}`);

  if (!res.ok) {
    return NextResponse.json(
      { error: "Video not found" },
      { status: res.status },
    );
  }

  const contentType = res.headers.get("content-type") || "video/mp4";
  const buffer = await res.arrayBuffer();

  return new NextResponse(buffer, {
    status: 200,
    headers: {
      "Content-Type": contentType,
      "Cache-Control": "public, max-age=3600",
    },
  });
}
