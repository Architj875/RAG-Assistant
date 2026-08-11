import { ReactNode } from "react";

import AnimatedBackground from "@/components/ui/AnimatedBackground";

interface Props {
  children: ReactNode;
}

export default function Container({
  children,
}: Props) {
  return (
    <>
      <AnimatedBackground />

      <main className="relative h-full">
        <div className="mx-auto flex h-full max-w-[1700px] flex-col px-8 py-6">
          {children}
        </div>
      </main>
    </>
  );
}