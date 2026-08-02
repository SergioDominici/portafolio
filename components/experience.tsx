"use client";

import { motion } from "framer-motion";
import { fadeUp, viewportOnce } from "@/lib/motion";
import { SectionHeading } from "./section-heading";

const ITEMS = [
  {
    role: "Desarrollador Web",
    org: "Dominici Lencería · Freelance",
    date: "2025",
    desc: "Diseñé y desarrollé la tienda online completa: catálogo con variantes, carrito, pagos con Mercado Pago, cuentas de clientas, reseñas y panel de administración. Está en producción y en uso real.",
  },
  {
    role: "Aprendiz autodidacta & proyectos propios",
    org: "Cúcuta, Colombia",
    date: "2024 — Actualidad",
    desc: "Me formo por mi cuenta y practico construyendo proyectos con Next.js, React, TypeScript y Firebase. Busco mis primeros clientes para seguir creciendo y ganar experiencia real.",
  },
];

function BriefcaseIcon() {
  return (
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="7" width="18" height="13" rx="2" />
      <path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 12h18" />
    </svg>
  );
}

export function Experience() {
  return (
    <section id="experiencia" className="mx-auto max-w-3xl px-6 py-16 scroll-mt-24">
      <SectionHeading icon={<BriefcaseIcon />}>Experiencia</SectionHeading>

      <ol className="relative ml-1 border-l border-line">
        {ITEMS.map((it, i) => (
          <motion.li
            key={it.role}
            variants={fadeUp}
            initial="hidden"
            whileInView="show"
            viewport={viewportOnce}
            transition={{ delay: i * 0.1 }}
            className="mb-10 ml-6 last:mb-0"
          >
            <span className="absolute -left-[7px] mt-1.5 size-3.5 rounded-full border-2 border-bg bg-accent" />
            <h3 className="text-lg font-semibold text-accent">{it.role}</h3>
            <p className="mt-0.5 text-sm font-medium text-ink">{it.org}</p>
            <p className="mt-1 font-mono text-xs text-faint">{it.date}</p>
            <p className="mt-2.5 text-[15px] leading-relaxed text-muted">{it.desc}</p>
          </motion.li>
        ))}
      </ol>
    </section>
  );
}
