import { chromium } from "playwright";
import { mkdirSync } from "node:fs";

const OUT = "public/shots";
mkdirSync(OUT, { recursive: true });
const URL = "https://www.dominicilenceria.com";

const browser = await chromium.launch();

async function shot(name, { width, height, fullPage = false, path: subpath = "" }) {
  const ctx = await browser.newContext({
    viewport: { width, height },
    deviceScaleFactor: 2,
  });
  const page = await ctx.newPage();
  await page.goto(URL + subpath, { waitUntil: "networkidle", timeout: 60000 });
  await page.waitForTimeout(2500); // deja que carguen imágenes/animaciones
  // baja para forzar lazy-load y vuelve arriba
  await page.evaluate(async () => {
    await new Promise((r) => {
      let y = 0;
      const t = setInterval(() => {
        window.scrollBy(0, 600);
        y += 600;
        if (y > document.body.scrollHeight) {
          clearInterval(t);
          r();
        }
      }, 120);
    });
  });
  await page.waitForTimeout(1200);
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(800);
  await page.screenshot({ path: `${OUT}/${name}.png`, fullPage });
  console.log("✓", name);
  await ctx.close();
}

await shot("desktop-home", { width: 1440, height: 900 });
await shot("desktop-full", { width: 1440, height: 900, fullPage: true });
await shot("mobile-home", { width: 390, height: 844 });
await shot("mobile-full", { width: 390, height: 844, fullPage: true });

// intenta capturar una página de producto/categoría
try {
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 });
  const page = await ctx.newPage();
  await page.goto(URL, { waitUntil: "networkidle", timeout: 60000 });
  await page.waitForTimeout(2000);
  const href = await page.evaluate(() => {
    const a = [...document.querySelectorAll("a")].find((a) =>
      /producto|product|\/p\//i.test(a.getAttribute("href") || ""),
    );
    return a?.getAttribute("href") || null;
  });
  if (href) {
    await page.goto(new URL(href, URL).toString(), { waitUntil: "networkidle", timeout: 60000 });
    await page.waitForTimeout(2500);
    await page.screenshot({ path: `${OUT}/desktop-product.png` });
    console.log("✓ desktop-product", href);
  } else {
    console.log("· no product link found");
  }
  await ctx.close();
} catch (e) {
  console.log("· product shot skipped:", e.message);
}

await browser.close();
console.log("done");
