import sharp from "sharp";
import { readdirSync, unlinkSync } from "node:fs";

const DIR = "public/shots";

const jobs = [
  { in: "desktop-home.png", out: "desktop-home.webp", w: 1600 },
  { in: "desktop-full.png", out: "desktop-full.webp", w: 1440 },
  { in: "mobile-home.png", out: "mobile-home.webp", w: 620 },
  { in: "mobile-full.png", out: "mobile-full.webp", w: 560 },
];

for (const j of jobs) {
  const meta = await sharp(`${DIR}/${j.in}`)
    .resize({ width: j.w })
    .webp({ quality: 80 })
    .toFile(`${DIR}/${j.out}`);
  console.log(`✓ ${j.out}  ${(meta.size / 1024).toFixed(0)}KB  ${meta.width}x${meta.height}`);
}

// borra los PNG originales (pesados)
for (const f of readdirSync(DIR)) {
  if (f.endsWith(".png")) unlinkSync(`${DIR}/${f}`);
}
console.log("PNG originales eliminados");
