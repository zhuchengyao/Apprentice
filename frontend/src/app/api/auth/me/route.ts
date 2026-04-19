import { NextRequest, NextResponse } from "next/server";
import { backendFetch } from "@/lib/backend-fetch";

export async function GET() {
  const res = await backendFetch("/api/auth/me");

  if (!res.ok) {
    return NextResponse.json({ user: null }, { status: res.status });
  }

  const user = await res.json();
  return NextResponse.json({ user });
}

export async function PATCH(request: NextRequest) {
  const body = await request.json();
  const res = await backendFetch("/api/auth/me", {
    method: "PATCH",
    body: JSON.stringify(body),
  });

  const data = await res.json();
  if (!res.ok) {
    return NextResponse.json(data, { status: res.status });
  }
  return NextResponse.json({ user: data });
}
