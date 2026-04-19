import type { Metadata } from "next";
import { PrivacyContent } from "./content";

export const metadata: Metadata = {
  title: "Privacy Policy · Apprentice",
  description: "How Apprentice collects, uses, and protects your data.",
};

export default function PrivacyPage() {
  return <PrivacyContent />;
}
