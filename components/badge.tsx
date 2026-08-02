import { getTech } from "./tech-logos";

// Badge de tecnología con el color de la marca (estilo porfolio.dev).
export function TechBadge({ name }: { name: string }) {
  const t = getTech(name);
  return (
    <span
      className="inline-flex items-center gap-1.5 rounded-lg border px-2.5 py-1 text-xs font-medium"
      style={{
        color: t.color,
        borderColor: `color-mix(in oklab, ${t.color} 28%, transparent)`,
        backgroundColor: `color-mix(in oklab, ${t.color} 10%, transparent)`,
      }}
    >
      <span className="grid size-3.5 place-items-center" style={{ color: t.color }}>
        {t.icon}
      </span>
      {t.name}
    </span>
  );
}
