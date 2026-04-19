import { NextRequest } from "next/server";
import { proxyJson } from "@/lib/backend-fetch";

export async function POST(request: NextRequest) {
  const body = await request.text();
  return proxyJson("/api/billing/subscription/checkout", {
    method: "POST",
    body,
  });
}
