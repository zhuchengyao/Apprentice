import { proxyJson } from "@/lib/backend-fetch";

export async function POST() {
  return proxyJson("/api/billing/subscription/portal", { method: "POST" });
}
