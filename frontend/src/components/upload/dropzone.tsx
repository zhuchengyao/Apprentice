"use client";

import { useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { motion, AnimatePresence } from "framer-motion";
import { useTranslations } from "next-intl";
import { Upload, FileText, AlertCircle, CheckCircle2 } from "lucide-react";
import { Progress } from "@/components/ui/progress";
import { ACCEPTED_FILE_TYPES } from "@/lib/constants";
import { cn } from "@/lib/utils";

interface DropzoneProps {
  onFileSelected: (file: File) => void;
  isUploading: boolean;
  progress: number;
  error: string | null;
  selectedFile: File | null;
  uploadComplete: boolean;
}

export function Dropzone({
  onFileSelected,
  isUploading,
  progress,
  error,
  selectedFile,
  uploadComplete,
}: DropzoneProps) {
  const t = useTranslations("upload");
  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      if (acceptedFiles.length > 0) {
        onFileSelected(acceptedFiles[0]);
      }
    },
    [onFileSelected],
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: ACCEPTED_FILE_TYPES,
    maxFiles: 1,
    disabled: isUploading,
  });

  return (
    <div className="mx-auto w-full max-w-2xl">
      <motion.div
        whileHover={!isUploading ? { scale: 1.005 } : undefined}
        whileTap={!isUploading ? { scale: 0.995 } : undefined}
        transition={{ type: "spring", stiffness: 400, damping: 25 }}
      >
        <div
          {...getRootProps()}
          className={cn(
            "relative cursor-pointer overflow-hidden rounded-3xl border border-dashed px-6 py-14 text-center transition-all duration-300",
            isDragActive
              ? "border-primary bg-primary/5 ring-2 ring-primary/20"
              : "border-border/80 bg-subtle/30 hover:border-foreground/40 hover:bg-subtle/60",
            isUploading && "pointer-events-none opacity-80",
            error && "border-destructive/50 bg-destructive/5",
            uploadComplete && "border-primary/50 bg-primary/5",
          )}
        >
          {isDragActive && (
            <div
              aria-hidden
              className="aurora pointer-events-none absolute inset-0 opacity-40"
            />
          )}
          <input {...getInputProps()} />

          <AnimatePresence mode="wait">
            {uploadComplete ? (
              <motion.div
                key="complete"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="relative flex flex-col items-center gap-4"
              >
                <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-primary/10 text-primary ring-1 ring-primary/20">
                  <CheckCircle2 className="h-7 w-7" />
                </div>
                <div>
                  <p className="font-heading text-[17px] font-semibold tracking-tight">
                    {t("complete_title")}
                  </p>
                  <p className="mt-1 text-[13px] text-muted-foreground">
                    {t("complete_hint")}
                  </p>
                </div>
              </motion.div>
            ) : isUploading ? (
              <motion.div
                key="uploading"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="relative flex flex-col items-center gap-4"
              >
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                  className="flex h-14 w-14 items-center justify-center rounded-2xl bg-primary/10 text-primary ring-1 ring-primary/20"
                >
                  <Upload className="h-6 w-6" />
                </motion.div>
                <div className="w-full max-w-xs">
                  <p className="mb-2 font-mono text-[11px] uppercase tracking-[0.12em] text-muted-foreground">
                    {t("uploading", { name: selectedFile?.name ?? "" })}
                  </p>
                  <Progress value={progress} className="h-1.5" />
                </div>
              </motion.div>
            ) : error ? (
              <motion.div
                key="error"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="relative flex flex-col items-center gap-4"
              >
                <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-destructive/10 text-destructive ring-1 ring-destructive/20">
                  <AlertCircle className="h-6 w-6" />
                </div>
                <div>
                  <p className="font-heading text-[15px] font-medium text-destructive">
                    {error}
                  </p>
                  <p className="mt-1 text-[13px] text-muted-foreground">
                    {t("retry_hint")}
                  </p>
                </div>
              </motion.div>
            ) : selectedFile ? (
              <motion.div
                key="selected"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="relative flex flex-col items-center gap-4"
              >
                <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-primary/10 text-primary ring-1 ring-primary/20">
                  <FileText className="h-6 w-6" />
                </div>
                <div>
                  <p className="font-heading text-[15px] font-medium tracking-tight">
                    {selectedFile.name}
                  </p>
                  <p className="mt-1 font-mono text-[11px] uppercase tracking-[0.12em] text-muted-foreground">
                    {t("file_size", {
                      size: (selectedFile.size / 1024 / 1024).toFixed(1),
                    })}
                  </p>
                </div>
              </motion.div>
            ) : (
              <motion.div
                key="empty"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="relative flex flex-col items-center gap-4"
              >
                <motion.div
                  animate={isDragActive ? { y: -6 } : { y: 0 }}
                  transition={{ type: "spring", stiffness: 300, damping: 20 }}
                  className="flex h-14 w-14 items-center justify-center rounded-2xl bg-primary/10 text-primary ring-1 ring-primary/20"
                >
                  <Upload className="h-6 w-6" />
                </motion.div>
                <div>
                  <p className="font-heading text-[17px] font-semibold tracking-tight">
                    {isDragActive ? t("drop_active") : t("drop_prompt")}
                  </p>
                  <p className="mt-1.5 text-[13px] text-muted-foreground">
                    {t("max_size")}
                  </p>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </motion.div>
    </div>
  );
}
