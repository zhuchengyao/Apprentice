"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useTranslations } from "next-intl";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Dropzone } from "@/components/upload/dropzone";
import { ProcessingAnimation } from "@/components/upload/processing-animation";
import { useUpload } from "@/hooks/use-upload";
import type { BookStatus } from "@/lib/constants";

interface UploadDialogProps {
  open: boolean;
  onClose: () => void;
}

export function UploadDialog({ open, onClose }: UploadDialogProps) {
  const router = useRouter();
  const t = useTranslations("upload");
  const { isUploading, progress, error, book, upload, reset } = useUpload();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  useEffect(() => {
    if (!open) {
      setSelectedFile(null);
      reset();
    }
  }, [open, reset]);

  async function handleFileSelected(file: File) {
    setSelectedFile(file);
    const result = await upload(file);
    if (result) {
      setTimeout(() => {
        onClose();
        router.push(`/book/${result.id}`);
      }, 1200);
    }
  }

  return (
    <Dialog
      open={open}
      onOpenChange={(next) => {
        if (!next && !isUploading) onClose();
      }}
    >
      <DialogContent className="sm:max-w-2xl">
        <DialogHeader>
          <DialogTitle>{t("title")}</DialogTitle>
          <DialogDescription>{t("lede")}</DialogDescription>
        </DialogHeader>
        <div className="pt-2">
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
        </div>
      </DialogContent>
    </Dialog>
  );
}
