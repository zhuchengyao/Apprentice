import { NextRequest, NextResponse } from "next/server";
import { backendUpload } from "@/lib/backend-fetch";

export async function POST(request: NextRequest) {
  const formData = await request.formData();
  const res = await backendUpload("/api/books/upload", formData);
  const data = await res.json();
  return NextResponse.json(data, { status: res.status });
}
