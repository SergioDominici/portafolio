import type { Variants } from "framer-motion";

export const EASE = [0.22, 1, 0.36, 1] as const;

// Aparición limpia (fade + subida), sobria.
export const fadeUp: Variants = {
  hidden: { opacity: 0, y: 18 },
  show: { opacity: 1, y: 0, transition: { duration: 0.6, ease: EASE } },
};

export const stagger: Variants = {
  hidden: {},
  show: { transition: { staggerChildren: 0.08 } },
};

export const viewportOnce = { once: true, margin: "0px 0px -10% 0px" } as const;
