"use client";

import { motion, type HTMLMotionProps } from "framer-motion";
import type { ReactNode } from "react";
import { fadeUp, viewportOnce } from "@/lib/motion";

// Aparición sobria al entrar en pantalla.
export function Reveal({
  children,
  className = "",
  delay = 0,
  ...rest
}: { children: ReactNode; className?: string; delay?: number } & HTMLMotionProps<"div">) {
  return (
    <motion.div
      variants={fadeUp}
      initial="hidden"
      whileInView="show"
      viewport={viewportOnce}
      transition={{ delay: delay / 1000 }}
      className={className}
      {...rest}
    >
      {children}
    </motion.div>
  );
}
