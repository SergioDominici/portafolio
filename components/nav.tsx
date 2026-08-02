"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { ThemeToggle } from "./theme-toggle";

const LINKS = [
  { id: "experiencia", label: "Experiencia" },
  { id: "proyectos", label: "Proyectos" },
  { id: "sobre-mi", label: "Sobre mí" },
  { id: "contacto", label: "Contacto" },
];

export function Nav() {
  const [active, setActive] = useState("");
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 24);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });

    const obs = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) setActive(e.target.id);
        });
      },
      { rootMargin: "-45% 0px -50% 0px" },
    );
    LINKS.forEach((l) => {
      const el = document.getElementById(l.id);
      if (el) obs.observe(el);
    });

    return () => {
      window.removeEventListener("scroll", onScroll);
      obs.disconnect();
    };
  }, []);

  return (
    <div className="fixed inset-x-0 top-4 z-50 flex justify-center px-3">
      <nav
        className={`flex items-center gap-0.5 rounded-full p-1 transition-all duration-300 sm:gap-1 ${
          scrolled
            ? "border border-line bg-bg2/80 shadow-lg shadow-black/25 backdrop-blur-xl"
            : "border border-transparent bg-transparent"
        }`}
      >
        {LINKS.map((l) => {
          const isActive = active === l.id;
          return (
            <a
              key={l.id}
              href={`#${l.id}`}
              className={`relative whitespace-nowrap rounded-full px-2.5 py-1.5 text-[13px] transition-colors sm:px-4 sm:text-sm ${
                isActive ? "text-accent" : "text-muted hover:text-ink"
              }`}
            >
              {isActive && (
                <motion.span
                  layoutId="nav-pill"
                  className="absolute inset-0 -z-10 rounded-full bg-bg3"
                  transition={{ type: "spring", stiffness: 380, damping: 30 }}
                />
              )}
              {l.label}
            </a>
          );
        })}
        <span className="mx-1 h-5 w-px bg-line" />
        <ThemeToggle />
      </nav>
    </div>
  );
}
