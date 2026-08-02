"use client";

import { motion } from "framer-motion";
import { fadeUp, stagger, viewportOnce } from "@/lib/motion";
import { SectionHeading } from "./section-heading";
import { TECH } from "./tech-logos";

function StackIcon() {
  return (
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <path d="m12 3 9 5-9 5-9-5 9-5Z" />
      <path d="m3 13 9 5 9-5" />
    </svg>
  );
}

export function Technologies() {
  const list = Object.values(TECH);
  return (
    <section id="tecnologias" className="mx-auto max-w-3xl px-6 py-16 scroll-mt-24">
      <SectionHeading icon={<StackIcon />}>Tecnologías</SectionHeading>

      <motion.ul
        variants={stagger}
        initial="hidden"
        whileInView="show"
        viewport={viewportOnce}
        className="grid grid-cols-2 gap-3 sm:grid-cols-3"
      >
        {list.map((t) => (
          <motion.li
            key={t.name}
            variants={fadeUp}
            className="group flex items-center gap-2.5 rounded-xl border border-line bg-bg2 px-4 py-3 transition-all duration-300 hover:-translate-y-0.5 hover:border-line2 hover:bg-bg3"
          >
            <span
              className="grid size-5 place-items-center transition-transform duration-300 group-hover:scale-110"
              style={{ color: t.color }}
            >
              {t.icon}
            </span>
            <span className="text-sm font-medium text-ink">{t.name}</span>
          </motion.li>
        ))}
      </motion.ul>
    </section>
  );
}
