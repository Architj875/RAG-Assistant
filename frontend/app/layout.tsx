import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { Toaster } from "sonner";

import { WorkspaceProvider } from "@/context";

import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "RAG Assistant",
  description: "AI-powered document assistant",
};

interface RootLayoutProps {
  children: React.ReactNode;
}

const themeScript = `
(function () {
  try {
    var key = "rag-assistant-theme";
    var storedTheme = localStorage.getItem(key);

    var theme =
      storedTheme === "light" ||
      storedTheme === "dark" ||
      storedTheme === "system"
        ? storedTheme
        : "system";

    var root = document.documentElement;

    root.classList.remove("light", "dark");

    if (theme === "system") {
      root.classList.add(
        window.matchMedia("(prefers-color-scheme: dark)").matches
          ? "dark"
          : "light"
      );
    } else {
      root.classList.add(theme);
    }
  } catch (error) {
    document.documentElement.classList.remove("light");
    document.documentElement.classList.add(
      window.matchMedia("(prefers-color-scheme: dark)").matches
        ? "dark"
        : "light"
    );
  }
})();
`;

export default function RootLayout({
  children,
}: Readonly<RootLayoutProps>) {
  return (
    <html
      lang="en"
      suppressHydrationWarning
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <head>
        <script
          dangerouslySetInnerHTML={{
            __html: themeScript,
          }}
        />
      </head>

      <body className="h-full overflow-hidden bg-background">
        <WorkspaceProvider>
          {children}

          <Toaster
            position="top-right"
            richColors
            closeButton
            theme="system"
          />
        </WorkspaceProvider>
      </body>
    </html>
  );
}