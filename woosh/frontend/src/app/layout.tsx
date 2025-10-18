import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Woosh - Company Search Tool",
  description: "Search and categorize information about companies",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="font-sans">{children}</body>
    </html>
  );
}
