// ─────────────────────────────────────────────────────────────
//  PROYECTOS — para añadir uno nuevo, agrega un objeto al arreglo.
// ─────────────────────────────────────────────────────────────

export type Project = {
  slug: string;
  name: string;
  description: string;
  cover: string; // captura para la tarjeta (webp)
  url: string;
  stack: string[]; // nombres que existen en tech-logos → badges
};

export const PROJECTS: Project[] = [
  {
    slug: "dominici-lenceria",
    name: "Dominici Lencería",
    description:
      "Tienda online completa para una marca de lencería en Cúcuta. Catálogo con variantes y colores, carrito, pagos con Mercado Pago, cuentas de clientas, reseñas verificadas y un panel de administración para gestionar todo sin tocar código.",
    cover: "/shots/desktop-home.webp",
    url: "https://www.dominicilenceria.com",
    stack: ["Next.js", "React", "TypeScript", "Tailwind CSS", "Firebase", "Mercado Pago"],
  },
  // 👉 Próximos proyectos: copia el bloque de arriba y cambia los datos.
];
