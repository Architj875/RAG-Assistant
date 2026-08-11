"use client";

import Sidebar from "./Sidebar";
import MainPanel from "./MainPanel";

export default function Workspace() {
  return (
    <div
      className="
        grid
        h-full
        min-h-0
        w-full
        grid-cols-[minmax(300px,0.28fr)_minmax(0,1fr)]
        gap-6
      "
    >
      <aside className="min-h-0 min-w-0">
        <Sidebar />
      </aside>

      <main className="min-h-0 min-w-0">
        <MainPanel />
      </main>
    </div>
  );
}