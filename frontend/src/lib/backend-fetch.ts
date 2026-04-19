import { cookies } from "next/headers";
import { NextResponse } from "next/server";
import { defaultLocale, isLocale, LOCALE_COOKIE } from "@/i18n/config";

const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8000";

async function resolveLocale(): Promise<string> {
  const cookieStore = await cookies();
  const value = cookieStore.get(LOCALE_COOKIE)?.value;
  return isLocale(value) ? value : defaultLocale;
}

/**
 * Fetch from backend with auth token forwarded from the cookie.
 * Use this in all Next.js API route handlers instead of raw fetch.
 */
export async function backendFetch(
  path: string,
  init?: RequestInit,
): Promise<Response> {
  const cookieStore = await cookies();
  const token = cookieStore.get("auth_token")?.value;
  const locale = await resolveLocale();

  const headers = new Headers(init?.headers);
  if (!headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }
  if (!headers.has("Accept-Language")) {
    headers.set("Accept-Language", locale);
  }

  return fetch(`${BACKEND_URL}${path}`, {
    ...init,
    headers,
  });
}

/**
 * Fetch for file uploads (FormData) — does NOT set Content-Type.
 */
export async function backendUpload(
  path: string,
  body: FormData,
): Promise<Response> {
  const cookieStore = await cookies();
  const token = cookieStore.get("auth_token")?.value;
  const locale = await resolveLocale();

  const headers = new Headers();
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }
  headers.set("Accept-Language", locale);

  return fetch(`${BACKEND_URL}${path}`, {
    method: "POST",
    headers,
    body,
  });
}

/**
 * Proxy a JSON request/response through to the backend. Forwards the auth
 * cookie, preserves status code, and returns the parsed JSON body.
 */
export async function proxyJson(
  path: string,
  init?: RequestInit,
): Promise<NextResponse> {
  const res = await backendFetch(path, init);
  const data = await res.json();
  return NextResponse.json(data, { status: res.status });
}

/**
 * Proxy a Server-Sent Events response through to the backend. Streams the
 * body unchanged and sets SSE headers on the downstream response.
 */
export async function proxySSE(
  path: string,
  init?: RequestInit,
): Promise<Response> {
  const res = await backendFetch(path, { cache: "no-store", ...init });
  if (!res.ok || !res.body) {
    return new Response(res.statusText || (await res.text()), {
      status: res.status,
    });
  }
  return new Response(res.body, {
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      Connection: "keep-alive",
    },
  });
}
