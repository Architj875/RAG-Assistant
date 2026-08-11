import { ReactNode } from "react";

interface Props {
  children: ReactNode;
}

export default function AppShell({
  children,
}: Props) {
  return (
    <div className="h-screen overflow-hidden bg-background text-foreground">
      {children}
    </div>
  );
}