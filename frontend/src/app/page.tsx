"use client";

import { useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { BookOpen, Sparkles, Brain, GraduationCap } from "lucide-react";
import { Dropzone } from "@/components/upload/dropzone";
import { ProcessingAnimation } from "@/components/upload/processing-animation";
import { useUpload } from "@/hooks/use-upload";
import type { BookStatus } from "@/lib/constants";

const features = [
  {
    icon: BookOpen,
    title: "Upload any book",
    description: "PDF, EPUB, or plain text — we handle the rest",
  },
  {
    icon: Brain,
    title: "Smart extraction",
    description: "AI identifies every concept and knowledge point",
  },
  {
    icon: GraduationCap,
    title: "Active teaching",
    description: "An AI tutor teaches you chapter by chapter",
  },
  {
    icon: Sparkles,
    title: "Spaced repetition",
    description: "Review at the perfect time to never forget",
  },
];

export default function HomePage() {
  const router = useRouter();
  const { isUploading, progress, error, book, upload } = useUpload();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleFileSelected = useCallback(
    async (file: File) => {
      setSelectedFile(file);
      const result = await upload(file);
      if (result) {
        setTimeout(() => router.push("/library"), 1500);
      }
    },
    [upload, router],
  );

  return (
    <div className="flex flex-col">
      {/* Hero */}
      <section className="relative flex flex-col items-center px-6 pt-20 pb-16">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-center"
        >
          <h1 className="text-5xl font-bold tracking-tight sm:text-6xl">
            Learn any book
            <br />
            <span className="text-muted-foreground">with an AI tutor</span>
          </h1>
          <p className="mx-auto mt-4 max-w-lg text-lg text-muted-foreground">
            Upload a book and let Apprentice teach you everything in it,
            concept by concept, at your own pace.
          </p>
        </motion.div>

        {/* Upload zone */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.5 }}
          className="mt-12 w-full max-w-2xl"
        >
          {book ? (
            <ProcessingAnimation status={book.status as BookStatus} />
          ) : (
            <Dropzone
              onFileSelected={handleFileSelected}
              isUploading={isUploading}
              progress={progress}
              error={error}
              selectedFile={selectedFile}
              uploadComplete={!!book}
            />
          )}
        </motion.div>

        {/* Features */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4, duration: 0.6 }}
          className="mt-24 grid w-full max-w-4xl grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4"
        >
          {features.map((feature, i) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 + i * 0.1, duration: 0.4 }}
              className="flex flex-col items-center rounded-xl border bg-card p-6 text-center"
            >
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-accent">
                <feature.icon className="h-5 w-5 text-muted-foreground" />
              </div>
              <h3 className="mt-3 text-sm font-semibold">{feature.title}</h3>
              <p className="mt-1 text-xs text-muted-foreground leading-relaxed">
                {feature.description}
              </p>
            </motion.div>
          ))}
        </motion.div>
      </section>
    </div>
  );
}
