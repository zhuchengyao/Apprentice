"use client";

import { useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { motion, AnimatePresence } from "framer-motion";
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
    <div className="w-full max-w-2xl mx-auto">
      <motion.div
        whileHover={!isUploading ? { scale: 1.01 } : undefined}
        whileTap={!isUploading ? { scale: 0.99 } : undefined}
        transition={{ type: "spring", stiffness: 400, damping: 25 }}
      >
        <div
          {...getRootProps()}
          className={cn(
            "relative cursor-pointer rounded-2xl border-2 border-dashed p-12 text-center transition-all duration-300",
            isDragActive
              ? "border-foreground bg-accent/80 shadow-lg"
              : "border-border hover:border-foreground/30 hover:bg-accent/30",
            isUploading && "pointer-events-none opacity-70",
            error && "border-destructive/50",
            uploadComplete && "border-green-500/50 bg-green-50/50 dark:bg-green-950/20",
          )}
        >
          <input {...getInputProps()} />

          <AnimatePresence mode="wait">
            {uploadComplete ? (
              <motion.div
                key="complete"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="flex flex-col items-center gap-4"
              >
                <div className="flex h-16 w-16 items-center justify-center rounded-full bg-green-100 dark:bg-green-900/30">
                  <CheckCircle2 className="h-8 w-8 text-green-600 dark:text-green-400" />
                </div>
                <div>
                  <p className="text-lg font-medium">Upload complete!</p>
                  <p className="mt-1 text-sm text-muted-foreground">
                    Your book is being processed...
                  </p>
                </div>
              </motion.div>
            ) : isUploading ? (
              <motion.div
                key="uploading"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="flex flex-col items-center gap-4"
              >
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                  className="flex h-16 w-16 items-center justify-center rounded-full bg-accent"
                >
                  <Upload className="h-8 w-8 text-foreground" />
                </motion.div>
                <div className="w-full max-w-xs">
                  <p className="mb-2 text-sm font-medium">
                    Uploading {selectedFile?.name}...
                  </p>
                  <Progress value={progress} className="h-2" />
                </div>
              </motion.div>
            ) : error ? (
              <motion.div
                key="error"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="flex flex-col items-center gap-4"
              >
                <div className="flex h-16 w-16 items-center justify-center rounded-full bg-destructive/10">
                  <AlertCircle className="h-8 w-8 text-destructive" />
                </div>
                <div>
                  <p className="text-lg font-medium text-destructive">{error}</p>
                  <p className="mt-1 text-sm text-muted-foreground">
                    Click or drag to try again
                  </p>
                </div>
              </motion.div>
            ) : selectedFile ? (
              <motion.div
                key="selected"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="flex flex-col items-center gap-4"
              >
                <div className="flex h-16 w-16 items-center justify-center rounded-full bg-accent">
                  <FileText className="h-8 w-8 text-foreground" />
                </div>
                <div>
                  <p className="text-lg font-medium">{selectedFile.name}</p>
                  <p className="mt-1 text-sm text-muted-foreground">
                    {(selectedFile.size / 1024 / 1024).toFixed(1)} MB
                  </p>
                </div>
              </motion.div>
            ) : (
              <motion.div
                key="empty"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="flex flex-col items-center gap-4"
              >
                <motion.div
                  animate={isDragActive ? { y: -8 } : { y: 0 }}
                  transition={{ type: "spring", stiffness: 300, damping: 20 }}
                  className="flex h-16 w-16 items-center justify-center rounded-full bg-accent"
                >
                  <Upload className="h-8 w-8 text-muted-foreground" />
                </motion.div>
                <div>
                  <p className="text-lg font-medium">
                    {isDragActive
                      ? "Drop your book here"
                      : "Drop a book here, or click to browse"}
                  </p>
                  <p className="mt-1 text-sm text-muted-foreground">
                    Supports PDF, EPUB, and plain text files
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
