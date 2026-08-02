import type { ReactNode } from "react";

// Logos de marca (SVG en línea) + color, para los badges de tecnología.
export type Tech = { name: string; color: string; icon: ReactNode };

const s = 15;

export const TECH: Record<string, Tech> = {
  "Next.js": {
    name: "Next.js",
    color: "#ffffff",
    icon: (
      <svg width={s} height={s} viewBox="0 0 24 24" aria-hidden>
        <circle cx="12" cy="12" r="11" fill="currentColor" />
        <path d="M8 7.5v9M8 7.5l7.5 9M16 7.5v6" stroke="var(--bg2)" strokeWidth="1.6" fill="none" strokeLinecap="round" />
      </svg>
    ),
  },
  React: {
    name: "React",
    color: "#61DAFB",
    icon: (
      <svg width={s} height={s} viewBox="-12 -11 24 22" aria-hidden fill="none">
        <circle r="2.1" fill="currentColor" />
        <g stroke="currentColor" strokeWidth="1">
          <ellipse rx="11" ry="4.2" />
          <ellipse rx="11" ry="4.2" transform="rotate(60)" />
          <ellipse rx="11" ry="4.2" transform="rotate(120)" />
        </g>
      </svg>
    ),
  },
  TypeScript: {
    name: "TypeScript",
    color: "#3178C6",
    icon: (
      <svg width={s} height={s} viewBox="0 0 24 24" aria-hidden>
        <rect width="24" height="24" rx="3" fill="currentColor" />
        <text x="12" y="17" textAnchor="middle" fontFamily="monospace" fontSize="11" fontWeight="700" fill="#fff">TS</text>
      </svg>
    ),
  },
  "Tailwind CSS": {
    name: "Tailwind CSS",
    color: "#38BDF8",
    icon: (
      <svg width={s} height={s} viewBox="0 0 24 24" aria-hidden fill="currentColor">
        <path d="M12 6c-2.67 0-4.33 1.33-5 4 1-1.33 2.17-1.83 3.5-1.5.76.19 1.3.74 1.91 1.35C13.4 10.85 14.53 12 17 12c2.67 0 4.33-1.33 5-4-1 1.33-2.17 1.83-3.5 1.5-.76-.19-1.3-.74-1.91-1.35C15.6 7.15 14.47 6 12 6Zm-5 6c-2.67 0-4.33 1.33-5 4 1-1.33 2.17-1.83 3.5-1.5.76.19 1.3.74 1.91 1.35C8.4 16.85 9.53 18 12 18c2.67 0 4.33-1.33 5-4-1 1.33-2.17 1.83-3.5 1.5-.76-.19-1.3-.74-1.91-1.35C10.6 13.15 9.47 12 7 12Z" />
      </svg>
    ),
  },
  Firebase: {
    name: "Firebase",
    color: "#FFCA28",
    icon: (
      <svg width={s} height={s} viewBox="0 0 24 24" aria-hidden fill="currentColor">
        <path d="M4.5 18.5 8 4.2c.15-.6.95-.7 1.24-.16L18 20 4.5 18.5Z" opacity=".7" />
        <path d="M4.5 18.5 19 20l-8 4.4c-.5.3-1.1.3-1.6 0L4.5 18.5Z" />
      </svg>
    ),
  },
  "Node.js": {
    name: "Node.js",
    color: "#539E43",
    icon: (
      <svg width={s} height={s} viewBox="0 0 24 24" aria-hidden fill="currentColor">
        <path d="M12 2.2 3.5 7v10L12 21.8 20.5 17V7L12 2.2Z" />
      </svg>
    ),
  },
  "Mercado Pago": {
    name: "Mercado Pago",
    color: "#00AEEF",
    icon: (
      <svg width={s} height={s} viewBox="0 0 24 24" aria-hidden fill="none" stroke="currentColor" strokeWidth="1.8">
        <rect x="2.5" y="6" width="19" height="12" rx="2.5" />
        <path d="M2.5 10h19" />
      </svg>
    ),
  },
  Vercel: {
    name: "Vercel",
    color: "#ffffff",
    icon: (
      <svg width={s} height={s} viewBox="0 0 24 24" aria-hidden>
        <path d="M12 3l10 18H2L12 3Z" fill="currentColor" />
      </svg>
    ),
  },
  Cloudinary: {
    name: "Cloudinary",
    color: "#3448C5",
    icon: (
      <svg width={s} height={s} viewBox="0 0 24 24" aria-hidden fill="currentColor">
        <path d="M7.2 19a4.2 4.2 0 0 1-.7-8.34A5.3 5.3 0 0 1 16.7 9.4a3.8 3.8 0 0 1 .8 7.5V19H7.2Z" />
      </svg>
    ),
  },
  "Framer Motion": {
    name: "Framer Motion",
    color: "#F24E1E",
    icon: (
      <svg width={s} height={s} viewBox="0 0 24 24" aria-hidden fill="currentColor">
        <path d="M5 2h14v7h-7zM5 9h7l7 7h-7v7l-7-7z" />
      </svg>
    ),
  },
};

export function getTech(name: string): Tech {
  return TECH[name] ?? { name, color: "#ffffff", icon: null };
}
