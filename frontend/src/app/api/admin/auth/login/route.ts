import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";

const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8000";
const COOKIE_MAX_AGE = 7 * 24 * 60 * 60;

export async function POST(request: NextRequest) {
  const body = await request.json();

  const loginRes = await fetch(`${BACKEND_URL}/api/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const loginData = await loginRes.json();
  if (!loginRes.ok) {
    return NextResponse.json(loginData, { status: loginRes.status });
  }

  const token = loginData.access_token as string;
  const verifyRes = await fetch(`${BACKEND_URL}/api/admin/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (!verifyRes.ok) {
    return NextResponse.json(
      { detail: "This account does not have admin access" },
      { status: 403 },
    );
  }

  const adminProfile = await verifyRes.json();

  const cookieStore = await cookies();
  cookieStore.set("auth_token", token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax",
    path: "/",
    maxAge: COOKIE_MAX_AGE,
  });

  return NextResponse.json({ admin: adminProfile });
}
