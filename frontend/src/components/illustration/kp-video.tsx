"use client";

interface KpVideoProps {
  filename: string;
  maxWidth?: number;
}

/** Inline MP4 player for KP animations rendered by the Manim pipeline. */
export function KpVideo({ filename, maxWidth = 340 }: KpVideoProps) {
  return (
    <div
      className="overflow-hidden rounded-xl border border-border/70 bg-black"
      style={{ maxWidth }}
    >
      <video
        src={`/api/manim/video/${filename}`}
        autoPlay
        loop
        muted
        playsInline
        controls
        className="block w-full"
      />
    </div>
  );
}
