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
  cta?: string; // texto del botón (por defecto "Visitar sitio")
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
  {
    slug: "cumbre-cero",
    name: "Cumbre Cero",
    description:
      "Plataforma de IA conversacional que en mes y medio escaló a más de 7.000 visitas diarias y 3.000 usuarios registrados, en 6 idiomas. Como cofundador fui parte del sistema de generación de imágenes, que subió el tiempo en pantalla un 40%. La cerramos por decisión propia pese al crecimiento.",
    cover: "/shots/cumbre-cero.webp",
    url: "https://cumbrecero.online/thanks",
    stack: ["Next.js", "TypeScript", "Node.js", "IA", "VPS"],
    cta: "Ver la historia",
  },
  // 👉 Próximos proyectos: copia el bloque de arriba y cambia los datos.
];
