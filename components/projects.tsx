"use client";

import { motion } from "framer-motion";
import { fadeUp, viewportOnce } from "@/lib/motion";
import { SectionHeading } from "./section-heading";
import { TechBadge } from "./badge";
import { PROJECTS, type Project } from "@/lib/projects";

function RocketIcon() {
  return (
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <path d="M4.5 16.5c-1.5 1.3-2 5-2 5s3.7-.5 5-2c.7-.8.7-2 0-2.8a2 2 0 0 0-3 -.2Z" />
      <path d="M12 15l-3-3a11 11 0 0 1 5-8c2.5-1.5 6-1.5 6-1.5s0 3.5-1.5 6a11 11 0 0 1-8 5Z" />
      <path d="M9 12H4s.5-2.8 2-4c1.2-1 3-1 3-1M12 15v5s2.8-.5 4-2c1-1.2 1-3 1-3" />
    </svg>
  );
}
function ExternalIcon() {
  return (
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M15 3h6v6M10 14 21 3M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
    </svg>
  );
}

export function Projects({ whatsapp }: { whatsapp: string }) {
  return (
    <section id="proyectos" className="mx-auto max-w-3xl px-6 py-16 scroll-mt-24">
      <SectionHeading icon={<RocketIcon />}>Proyectos</SectionHeading>

      <div className="flex flex-col gap-8">
        {PROJECTS.map((p, i) => (
          <ProjectCard key={p.slug} p={p} index={i} />
        ))}
        <NextCard whatsapp={whatsapp} />
      </div>
    </section>
  );
}

function ProjectCard({ p, index }: { p: Project; index: number }) {
  return (
    <motion.article
      variants={fadeUp}
      initial="hidden"
      whileInView="show"
      viewport={viewportOnce}
      transition={{ delay: index * 0.05 }}
      className="group overflow-hidden rounded-2xl border border-line bg-bg2 transition-all duration-300 hover:-translate-y-1 hover:border-line2 hover:shadow-2xl hover:shadow-black/30 md:grid md:grid-cols-2"
    >
      {/* Captura */}
      <a
        href={p.url}
        target="_blank"
        rel="noopener noreferrer"
        className="relative block aspect-video overflow-hidden border-b border-line md:order-2 md:aspect-auto md:border-b-0 md:border-l"
      >
        <img
          src={p.cover}
          alt={p.name}
          loading="lazy"
          decoding="async"
          className="size-full object-cover object-top transition-transform duration-700 ease-out group-hover:scale-[1.04]"
        />
        <span className="absolute inset-0 bg-gradient-to-t from-bg2/40 to-transparent opacity-0 transition-opacity group-hover:opacity-100" />
      </a>

      {/* Texto */}
      <div className="flex flex-col p-6 sm:p-7 md:order-1">
        <h3 className="text-xl font-semibold tracking-tight text-ink">{p.name}</h3>
        <p className="mt-2 flex-1 text-[15px] leading-relaxed text-muted">
          {p.description}
        </p>
        <ul className="mt-4 flex flex-wrap gap-1.5">
          {p.stack.map((s) => (
            <li key={s}>
              <TechBadge name={s} />
            </li>
          ))}
        </ul>
        <div className="mt-5">
          <a
            href={p.url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 rounded-xl border border-line bg-bg2 px-4 py-2.5 text-sm font-medium text-ink transition-colors hover:border-line2 hover:bg-bg3"
          >
            <ExternalIcon />
            {p.cta ?? "Visitar sitio"}
          </a>
        </div>
      </div>
    </motion.article>
  );
}

// Tarjeta que invita a que el próximo proyecto sea del cliente.
function NextCard({ whatsapp }: { whatsapp: string }) {
  return (
    <motion.a
      href={whatsapp}
      target="_blank"
      rel="noopener noreferrer"
      variants={fadeUp}
      initial="hidden"
      whileInView="show"
      viewport={viewportOnce}
      className="group flex flex-col items-start gap-3 rounded-2xl border border-dashed border-line2 bg-bg2/40 p-7 transition-colors hover:border-accent/60 hover:bg-bg2"
    >
      <span className="grid size-10 place-items-center rounded-xl border border-line bg-bg text-accent transition-transform group-hover:-translate-y-0.5">
        <ExternalIcon />
      </span>
      <h3 className="text-lg font-semibold text-ink">¿Tu proyecto aquí?</h3>
      <p className="text-[15px] leading-relaxed text-muted">
        Cuéntame tu idea por WhatsApp y la convierto en una tienda o página que
        trabaje para ti.
      </p>
    </motion.a>
  );
}
