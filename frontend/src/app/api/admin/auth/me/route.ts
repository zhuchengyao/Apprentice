import { NextResponse } from "next/server";
import { backendFetch } from "@/lib/backend-fetch";

export async function GET() {
  const res = await backendFetch("/api/admin/me");
  if (!res.ok) {
    return NextResponse.json({ admin: null }, { status: res.status });
  }
  const admin = await res.json();
  return NextResponse.json({ admin });
}
