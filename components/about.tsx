"use client";

import { Reveal } from "./reveal";
import { SectionHeading } from "./section-heading";

function UserIcon() {
  return (
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <path d="M20 21a8 8 0 0 0-16 0" />
      <circle cx="12" cy="7" r="4" />
    </svg>
  );
}

export function About() {
  return (
    <section id="sobre-mi" className="mx-auto max-w-3xl px-6 py-16 scroll-mt-24">
      <SectionHeading icon={<UserIcon />}>Sobre mí</SectionHeading>

      <div className="grid gap-8 sm:grid-cols-[1fr_auto] sm:items-start">
        <Reveal className="space-y-4 text-[15px] leading-relaxed text-muted">
          <p>
            Soy Sergio, desarrollador web de{" "}
            <span className="text-ink">Cúcuta, Colombia</span>. Me apasiona convertir
            ideas de negocio en productos digitales que se ven bien y, sobre todo,
            que venden.
          </p>
          <p>
            Trabajo con <span className="text-ink">Next.js, React, TypeScript y
            Firebase</span>, y cuido cada detalle: que la página cargue rápido, se
            sienta fluida y proteja los datos de tus clientes.
          </p>
          <p>
            Mi proyecto más completo hasta ahora es{" "}
            <a href="https://www.dominicilenceria.com" target="_blank" rel="noopener noreferrer" className="text-accent underline decoration-accent/30 underline-offset-4 hover:decoration-accent">
              Dominici Lencería
            </a>
            , una tienda online real y en producción. Ahora busco nuevos proyectos
            y clientes con quienes crecer.
          </p>
        </Reveal>

        <Reveal delay={100} className="hidden sm:block">
          {/* 📸 Cambia /avatar.jpg por tu foto (public/avatar.jpg) */}
          <img
            src="/avatar.jpg"
            alt="Sergio Dominici"
            width={144}
            height={144}
            className="size-36 rounded-2xl object-cover ring-1 ring-line"
          />
        </Reveal>
      </div>
    </section>
  );
}
