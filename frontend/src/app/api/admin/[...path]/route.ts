import { NextRequest, NextResponse } from "next/server";
import { backendFetch } from "@/lib/backend-fetch";

async function proxy(request: NextRequest, pathSegments: string[]) {
  const subPath = pathSegments.join("/");
  // Forbid the auth/* subtree — those have their own handlers that manage cookies.
  if (subPath.startsWith("auth/")) {
    return NextResponse.json({ detail: "Not found" }, { status: 404 });
  }

  const search = request.nextUrl.search;
  const backendPath = `/api/admin/${subPath}${search}`;

  const method = request.method;
  const init: RequestInit = { method };
  if (method !== "GET" && method !== "HEAD") {
    const text = await request.text();
    if (text) init.body = text;
  }

  const res = await backendFetch(backendPath, init);
  const contentType = res.headers.get("content-type") || "application/json";
  const body = await res.text();
  return new NextResponse(body, {
    status: res.status,
    headers: { "content-type": contentType },
  });
}

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> },
) {
  const { path } = await params;
  return proxy(request, path);
}

export async function POST(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> },
) {
  const { path } = await params;
  return proxy(request, path);
}

export async function PATCH(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> },
) {
  const { path } = await params;
  return proxy(request, path);
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> },
) {
  const { path } = await params;
  return proxy(request, path);
}
