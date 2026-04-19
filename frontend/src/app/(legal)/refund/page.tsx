import type { Metadata } from "next";
import { RefundContent } from "./content";

export const metadata: Metadata = {
  title: "Refund Policy · Apprentice",
  description: "When and how you can request a refund from Apprentice.",
};

export default function RefundPage() {
  return <RefundContent />;
}
