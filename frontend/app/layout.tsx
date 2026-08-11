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

export default function RootLayout({
  children,
}: Readonly<RootLayoutProps>) {
  return (
    <html
  lang="en"
  className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
>
  <body className="h-full overflow-hidden bg-background">
    <WorkspaceProvider>
      {children}

      <Toaster
        position="top-right"
        richColors
        closeButton
        theme="dark"
      />
    </WorkspaceProvider>
  </body>
</html>
  );
}