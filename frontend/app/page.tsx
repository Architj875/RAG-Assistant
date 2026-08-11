import AppShell from "@/components/layout/AppShell";
import Container from "@/components/layout/Container";
import Header from "@/components/layout/Header";
import Workspace from "@/components/layout/Workspace";
import WorkspaceToolbar from "@/components/layout/WorkspaceToolbar";

export default function Home() {
  return (
    <AppShell>
      <Container>
        <div className="flex h-full min-h-0 flex-col">
          {/* Top area */}
          <div className="grid shrink-0 grid-cols-[minmax(300px,0.28fr)_minmax(0,1fr)] gap-6">
            <div>
              <Header />
            </div>

            <div className="pt-2">
              <WorkspaceToolbar />
            </div>
          </div>

          {/* Main workspace */}
          <div className="mt-6 min-h-0 flex-1">
            <Workspace />
          </div>
        </div>
      </Container>
    </AppShell>
  );
}