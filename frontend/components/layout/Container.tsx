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

      <main className="relative flex h-full min-h-0 flex-col">
        <div className="mx-auto flex min-h-0 flex-1 w-full max-w-[1700px] flex-col px-8 py-3">
          {children}
        </div>
      </main>
    </>
  );
}