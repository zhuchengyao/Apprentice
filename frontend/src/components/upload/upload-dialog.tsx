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
import { useUpload } from "@/hooks/use-upload";

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
      onClose();
      router.push(`/book/${result.id}`);
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
          <Dropzone
            onFileSelected={handleFileSelected}
            isUploading={isUploading}
            progress={progress}
            error={error}
            selectedFile={selectedFile}
            uploadComplete={!!book}
          />
        </div>
      </DialogContent>
    </Dialog>
  );
}
