import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Woosh - Ricerca Aziende",
  description: "Cerca e categorizza informazioni su aziende",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="it">
      <body>{children}</body>
    </html>
  );
}
