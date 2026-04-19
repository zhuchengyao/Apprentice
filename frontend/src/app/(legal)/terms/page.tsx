import type { Metadata } from "next";
import { TermsContent } from "./content";

export const metadata: Metadata = {
  title: "Terms of Service · Apprentice",
  description: "The terms that govern your use of Apprentice.",
};

export default function TermsPage() {
  return <TermsContent />;
}
