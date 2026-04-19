import { NextRequest } from "next/server";
import { proxyJson } from "@/lib/backend-fetch";

export async function GET(request: NextRequest) {
  const days = request.nextUrl.searchParams.get("days") || "30";
  return proxyJson(`/api/billing/usage?days=${days}`);
}
