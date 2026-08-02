
import { Nav } from "@/components/nav";
import { Hero } from "@/components/hero";
import { Experience } from "@/components/experience";
import { Projects } from "@/components/projects";
import { Technologies } from "@/components/technologies";
import { About } from "@/components/about";
import { Reveal } from "@/components/reveal";

const WHATSAPP = "https://wa.me/573125009552";
const INSTAGRAM = "https://www.instagram.com/_smdc1/";
const EMAIL = "mailto:sergiodominici.work@gmail.com"; // ← cámbialo si usas otro correo
const GITHUB = "https://github.com/SergioDominici"; // ← confirma tu usuario de GitHub

function MailIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="5" width="18" height="14" rx="2" />
      <path d="m3 7 9 6 9-6" />
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

export default function Home() {
  return (
    <main className="relative">
      <Nav />
      <Hero whatsapp={WHATSAPP} github={GITHUB} instagram={INSTAGRAM} />
      <Experience />
      <Projects whatsapp={WHATSAPP} />
      <Technologies />
      <About />

      {/* Contacto */}
      <section id="contacto" className="mx-auto max-w-3xl px-6 py-20 scroll-mt-24">
        <Reveal className="overflow-hidden rounded-2xl border border-line bg-bg2 p-8 text-center sm:p-12">
          <h2 className="text-2xl font-bold tracking-tight text-ink sm:text-3xl">
            ¿Tienes una idea? Hagámosla realidad.
          </h2>
          <p className="mx-auto mt-3 max-w-md text-[15px] leading-relaxed text-muted">
            Cuéntame qué necesitas y te respondo con una propuesta. Sin compromiso.
          </p>
          <div className="mt-7 flex flex-wrap items-center justify-center gap-3">
            <a
              href={WHATSAPP}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 rounded-xl border border-line bg-bg2 px-5 py-3 text-sm font-medium text-ink transition-colors hover:border-line2 hover:bg-bg3"
            >
              <WhatsAppIcon />
              Escríbeme por WhatsApp
            </a>
            <a
              href={EMAIL}
              className="inline-flex items-center gap-2 rounded-xl border border-line bg-bg px-5 py-3 text-sm font-medium text-ink transition-colors hover:border-line2 hover:bg-bg3"
            >
              <MailIcon />
              Enviar correo
            </a>
          </div>
        </Reveal>
      </section>

      {/* Footer */}
      <footer className="border-t border-line">
        <div className="mx-auto flex max-w-3xl flex-col items-center justify-between gap-4 px-6 py-8 text-sm text-muted sm:flex-row">
          <span>© 2026 Sergio Dominici · Cúcuta, Colombia</span>
          <span className="flex items-center gap-4">
            <a href={GITHUB} target="_blank" rel="noopener noreferrer" className="transition-colors hover:text-ink">GitHub</a>
            <a href={INSTAGRAM} target="_blank" rel="noopener noreferrer" className="transition-colors hover:text-ink">Instagram</a>
            <a href={EMAIL} className="transition-colors hover:text-ink">Correo</a>
          </span>
        </div>
      </footer>
    </main>
  );
}
