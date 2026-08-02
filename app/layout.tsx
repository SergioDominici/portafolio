import type { Metadata, Viewport } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { SmoothScroll } from "@/components/smooth-scroll";

const geistSans = Geist({ variable: "--font-geist-sans", subsets: ["latin"] });
const geistMono = Geist_Mono({ variable: "--font-geist-mono", subsets: ["latin"] });

export const metadata: Metadata = {
  metadataBase: new URL("https://sergiodominici.com"),
  title: "Sergio Dominici — Desarrollador Web",
  description:
    "Desarrollador web en Cúcuta. Creo tiendas online y páginas rápidas, seguras y pensadas para vender. Creador de Dominici Lencería.",
  keywords: ["desarrollador web", "tienda online", "e-commerce", "Cúcuta", "Next.js", "React"],
  authors: [{ name: "Sergio Dominici" }],
  openGraph: {
    title: "Sergio Dominici — Desarrollador Web",
    description: "Tiendas online rápidas, seguras y pensadas para vender.",
    type: "website",
    locale: "es_CO",
  },
  robots: { index: true, follow: true },
};

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: dark)", color: "#08080a" },
    { media: "(prefers-color-scheme: light)", color: "#f7f7f5" },
  ],
};

const themeScript = `try{var t=localStorage.getItem('theme');if(t)document.documentElement.dataset.theme=t;}catch(e){}`;

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html
      lang="es"
      suppressHydrationWarning
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full">
        <script dangerouslySetInnerHTML={{ __html: themeScript }} />
        <SmoothScroll />
        {children}
      </body>
    </html>
  );
}
