import { proxyJson } from "@/lib/backend-fetch";

export async function GET() {
  return proxyJson("/api/billing/credits");
}
