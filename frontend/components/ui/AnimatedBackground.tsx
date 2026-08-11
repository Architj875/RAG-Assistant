"use client";

export default function AnimatedBackground() {
  return (
    <div className="pointer-events-none fixed inset-0 -z-10 overflow-hidden">
      {/* Base background */}
      <div className="absolute inset-0 bg-[#090B0A]" />

      {/* Emerald glow */}
      <div
        className="
          absolute
          left-[-10%]
          top-[8%]
          h-[420px]
          w-[420px]
          rounded-full
          bg-emerald-500/10
          blur-[140px]
          animate-float
        "
      />

      {/* Copper glow */}
      <div
        className="
          absolute
          bottom-[5%]
          right-[-8%]
          h-[380px]
          w-[380px]
          rounded-full
          bg-amber-700/10
          blur-[140px]
          animate-float
        "
        style={{
          animationDelay: "2s",
        }}
      />

      {/* Secondary emerald glow */}
      <div
        className="
          absolute
          right-[20%]
          top-[20%]
          h-64
          w-64
          rounded-full
          bg-emerald-400/5
          blur-[100px]
          animate-float
        "
        style={{
          animationDelay: "4s",
        }}
      />
    </div>
  );
}