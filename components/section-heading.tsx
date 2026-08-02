import type { ReactNode } from "react";
import { Reveal } from "./reveal";

// Encabezado de sección: icono + título (estilo porfolio.dev).
export function SectionHeading({
  icon,
  children,
}: {
  icon: ReactNode;
  children: ReactNode;
}) {
  return (
    <Reveal className="mb-8">
      <div className="flex items-center gap-2.5 text-ink">
        <span className="text-accent">{icon}</span>
        <h2 className="text-2xl font-semibold tracking-tight sm:text-3xl">{children}</h2>
      </div>
      <span className="mt-3 block h-1 w-12 rounded-full bg-accent" />
    </Reveal>
  );
}
