import { NextResponse } from "next/server";

export async function POST() {
  return NextResponse.json({ message: "Study sessions coming in Phase 3" });
}
