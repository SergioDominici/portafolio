"use client";

import { motion } from "framer-motion";
import { EASE } from "@/lib/motion";

function GitHubIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden>
      <path d="M12 2C6.48 2 2 6.58 2 12.25c0 4.53 2.87 8.37 6.84 9.73.5.1.68-.22.68-.49v-1.7c-2.78.62-3.37-1.37-3.37-1.37-.45-1.18-1.1-1.5-1.1-1.5-.91-.63.07-.62.07-.62 1 .07 1.53 1.06 1.53 1.06.9 1.57 2.35 1.12 2.92.85.09-.66.35-1.12.63-1.37-2.22-.26-4.56-1.14-4.56-5.06 0-1.12.39-2.03 1.03-2.75-.1-.26-.45-1.3.1-2.71 0 0 .84-.28 2.75 1.05a9.3 9.3 0 0 1 5 0c1.91-1.33 2.75-1.05 2.75-1.05.55 1.41.2 2.45.1 2.71.64.72 1.03 1.63 1.03 2.75 0 3.93-2.35 4.79-4.58 5.05.36.32.68.94.68 1.9v2.82c0 .27.18.6.69.49A10.02 10.02 0 0 0 22 12.25C22 6.58 17.52 2 12 2Z" />
    </svg>
  );
}
function InstagramIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden>
      <rect x="3" y="3" width="18" height="18" rx="5" />
      <circle cx="12" cy="12" r="4" />
      <circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none" />
    </svg>
  );
}
function WhatsAppIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden>
      <path d="M12 2a10 10 0 0 0-8.5 15.3L2 22l4.8-1.5A10 10 0 1 0 12 2Zm4.4 12c-.2-.1-1.4-.7-1.6-.8-.2-.1-.4-.1-.5.1l-.7.9c-.1.2-.3.2-.5.1a6.6 6.6 0 0 1-3.2-2.8c-.1-.2 0-.4.1-.5l.4-.5c.1-.2.2-.3.2-.5V9.4c0-.2-.5-1.2-.7-1.6-.2-.4-.4-.4-.5-.4h-.5c-.2 0-.5.1-.7.3-.9.9-.9 2.1-.6 3.3a10 10 0 0 0 4.9 5.3c1.6.7 2.9.9 3.9.6.6-.2 1.4-.6 1.6-1.2.2-.6.2-1.1.1-1.2Z" />
    </svg>
  );
}

export function Hero({
  whatsapp,
  github,
  instagram,
}: {
  whatsapp: string;
  github: string;
  instagram: string;
}) {
  return (
    <section id="top" className="relative">
      {/* Fondo: resplandor + cuadrícula sutil, solo aquí */}
      <div aria-hidden className="pointer-events-none absolute inset-x-0 top-0 h-[520px]">
        <div className="grid-bg absolute inset-0 opacity-30" />
      </div>

      <div className="relative mx-auto max-w-3xl px-6 pb-14 pt-24 sm:pt-28">
        {/* Avatar + disponibilidad */}
        <motion.div
          initial={{ opacity: 0, y: 14 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: EASE }}
          className="flex items-center gap-4"
        >
          {/* Cambia /avatar.jpg por tu foto (ponla en public/avatar.jpg) */}
          <img
            src="/avatar.jpg"
            alt="Sergio Dominici"
            width={72}
            height={72}
            className="size-[72px] rounded-full object-cover ring-2 ring-accent/70"
          />
          <a
            href={whatsapp}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 rounded-full border border-line bg-bg2 px-3 py-1 text-sm text-muted transition-colors hover:border-line2 hover:text-ink"
          >
            <span className="relative grid size-2 place-items-center">
              <span className="absolute size-2 animate-ping rounded-full bg-accent/60" />
              <span className="size-1.5 rounded-full bg-accent" />
            </span>
            Disponible para trabajar
          </a>
        </motion.div>

        {/* Saludo */}
        <motion.h1
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.08, duration: 0.6, ease: EASE }}
          className="mt-6 text-4xl font-bold tracking-tight text-ink sm:text-5xl"
        >
          Hey, soy <span className="text-accent">Sergio</span>
        </motion.h1>

        {/* Subtítulo */}
        <motion.p
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.16, duration: 0.6, ease: EASE }}
          className="mt-5 text-lg leading-relaxed text-muted sm:text-xl"
        >
          Desarrollador web en Cúcuta, Colombia. Creo{" "}
          <strong className="font-semibold text-ink">tiendas online y páginas web</strong>{" "}
          rápidas, seguras y pensadas para{" "}
          <strong className="font-semibold text-ink">vender</strong>.
        </motion.p>

        {/* Botones */}
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.24, duration: 0.6, ease: EASE }}
          className="mt-8 flex flex-wrap items-center gap-3"
        >
          <a
            href={whatsapp}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 rounded-xl border border-line bg-bg2 px-4 py-2.5 text-sm font-medium text-ink transition-colors hover:border-line2 hover:bg-bg3"
          >
            <WhatsAppIcon />
            Contáctame
          </a>
          <a
            href={github}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 rounded-xl border border-line bg-bg2 px-4 py-2.5 text-sm font-medium text-ink transition-colors hover:border-line2 hover:bg-bg3"
          >
            <GitHubIcon />
            GitHub
          </a>
          <a
            href={instagram}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 rounded-xl border border-line bg-bg2 px-4 py-2.5 text-sm font-medium text-ink transition-colors hover:border-line2 hover:bg-bg3"
          >
            <InstagramIcon />
            Instagram
          </a>
        </motion.div>
      </div>
    </section>
  );
}
