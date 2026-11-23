"""Renderiza el video del trasteo en motion graphics (1080x1920, 30 fps).

Uso:
  python3 scripts/render.py video   -> clips/escenas.mp4 (sin audio)
  python3 scripts/render.py frames  -> frames/clave_*.png (cuadros clave para revisar)
  python3 scripts/render.py portada -> final/portada.png

Los datos del negocio salen de config.json. Zonas seguras respetadas:
nada importante en el 10% de arriba (y<192), el 20% de abajo (y>1536)
ni el 15% de la derecha (x>918).
"""
import json
import math
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
CIUDAD = CFG["ciudad"]

W, H, FPS = 1080, 1920, 30
DUR = 27.0
SAFE_L, SAFE_T, SAFE_R, SAFE_B = 60, 200, 900, 1520
CX = (SAFE_L + SAFE_R) // 2  # 480: centro de la zona segura
SS = 2  # supersampling de los sprites

FD = "/usr/share/fonts/opentype/inter/"
F_BLACK = FD + "InterDisplay-Black.otf"
F_XB = FD + "InterDisplay-ExtraBold.otf"
F_BOLD = FD + "InterDisplay-Bold.otf"
F_SEMI = FD + "InterDisplay-SemiBold.otf"

NAVY = (18, 38, 79)
NAVY2 = (11, 26, 58)
ORANGE = (255, 122, 26)
YELLOW = (255, 201, 60)
CREAM = (255, 244, 228)
WHITE = (255, 255, 255)
GREEN = (37, 211, 102)
GREEN_D = (18, 140, 126)
CARD = (205, 140, 78)
CARD_T = (226, 168, 100)
TAPE = (242, 214, 160)


# ---------------------------------------------------------------- utilidades
@lru_cache(None)
def font(path, size):
    return ImageFont.truetype(path, size)


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def prog(t, a, b):
    return clamp((t - a) / (b - a))


def ease_out_cubic(x):
    return 1 - (1 - x) ** 3


def ease_in_out(x):
    return 3 * x * x - 2 * x * x * x


def ease_out_back(x, s=1.7):
    c3 = s + 1
    return 1 + c3 * (x - 1) ** 3 + s * (x - 1) ** 2


def ease_out_bounce(x):
    n1, d1 = 7.5625, 2.75
    if x < 1 / d1:
        return n1 * x * x
    if x < 2 / d1:
        x -= 1.5 / d1
        return n1 * x * x + 0.75
    if x < 2.5 / d1:
        x -= 2.25 / d1
        return n1 * x * x + 0.9375
    x -= 2.625 / d1
    return n1 * x * x + 0.984375


def hi(w, h):
    img = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    return img, ImageDraw.Draw(img)


def fin(img, w, h):
    return img.resize((w, h), Image.LANCZOS)


def S(*v):
    return [x * SS for x in v]


def with_alpha(sprite, a):
    if a >= 0.999:
        return sprite
    s = sprite.copy()
    s.putalpha(s.getchannel("A").point(lambda v: int(v * a)))
    return s


def paste(canvas, sprite, cx, cy, scale=1.0, rot=0.0, alpha=1.0):
    if alpha <= 0.01 or scale <= 0.01:
        return
    sp = sprite
    if abs(scale - 1) > 1e-3:
        sp = sp.resize((max(1, int(sp.width * scale)), max(1, int(sp.height * scale))), Image.BILINEAR)
    if abs(rot) > 0.05:
        sp = sp.rotate(rot, resample=Image.BICUBIC, expand=True)
    sp = with_alpha(sp, alpha)
    canvas.paste(sp, (int(cx - sp.width / 2), int(cy - sp.height / 2)), sp)


def wrap(text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if f.getlength(test.replace("*", "")) <= maxw or not cur:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_font(text, path, size, maxw, minsize=30):
    while size > minsize and font(path, size).getlength(text) > maxw:
        size -= 2
    return font(path, size)


def vgrad(w, h, top, bottom):
    g = Image.new("RGB", (1, h))
    for y in range(h):
        k = y / (h - 1)
        g.putpixel((0, y), tuple(int(top[i] + (bottom[i] - top[i]) * k) for i in range(3)))
    return g.resize((w, h))


def shadow(sprite, blur=18, off=(0, 14), alpha=0.28):
    """Devuelve sprite con sombra suave (mismo centro aprox.)."""
    pad = blur * 3
    out = Image.new("RGBA", (sprite.width + 2 * pad, sprite.height + 2 * pad), (0, 0, 0, 0))
    a = sprite.getchannel("A").point(lambda v: int(v * alpha))
    sh = Image.new("RGBA", sprite.size, (0, 0, 0, 255))
    sh.putalpha(a)
    out.paste(sh, (pad + off[0], pad + off[1]), sh)
    out = out.filter(ImageFilter.GaussianBlur(blur))
    out.paste(sprite, (pad, pad), sprite)
    return out


# ------------------------------------------------------------------- sprites
@lru_cache(None)
def box_sprite(w, h, tint=0):
    img, d = hi(w, h)
    c = tuple(clamp(v + tint, 0, 255) for v in CARD)
    ct = tuple(clamp(v + tint, 0, 255) for v in CARD_T)
    c, ct = tuple(map(int, c)), tuple(map(int, ct))
    d.rounded_rectangle(S(0, 0, w, h), radius=10 * SS, fill=c)
    d.rectangle(S(0, 0, w, int(h * 0.22)), fill=ct)
    d.rounded_rectangle(S(0, 0, w, int(h * 0.22)), radius=10 * SS, fill=ct)
    d.line(S(0, int(h * 0.22), w, int(h * 0.22)), fill=(150, 95, 45), width=3 * SS)
    tw = int(w * 0.18)
    d.rectangle(S(w // 2 - tw // 2, 0, w // 2 + tw // 2, int(h * 0.5)), fill=TAPE)
    # etiqueta con flechas "este lado arriba"
    lx, ly = int(w * 0.12), int(h * 0.6)
    d.rectangle(S(lx, ly, lx + int(w * 0.28), ly + int(h * 0.25)), fill=(250, 240, 222))
    for k in (0.33, 0.66):
        ax = lx + int(w * 0.28 * k)
        d.line(S(ax, ly + int(h * 0.21), ax, ly + int(h * 0.05)), fill=(90, 60, 30), width=3 * SS)
        d.polygon(S(ax - 6, ly + int(h * 0.09), ax + 6, ly + int(h * 0.09), ax, ly + int(h * 0.03)), fill=(90, 60, 30))
    return fin(img, w, h)


@lru_cache(None)
def wheel_sprite(r=46):
    img, d = hi(2 * r, 2 * r)
    d.ellipse(S(0, 0, 2 * r, 2 * r), fill=(30, 34, 40))
    d.ellipse(S(r * 0.38, r * 0.38, r * 1.62, r * 1.62), fill=(184, 194, 207))
    for k in range(5):
        a = k * 2 * math.pi / 5
        d.line(S(r, r, r + math.cos(a) * r * 0.55, r + math.sin(a) * r * 0.55), fill=(110, 120, 134), width=5 * SS)
    d.ellipse(S(r * 0.82, r * 0.82, r * 1.18, r * 1.18), fill=(90, 100, 112))
    return fin(img, 2 * r, 2 * r)


TRUCK_W, TRUCK_H = 780, 400
WHEELS = [(150, 352), (250, 352), (650, 352)]


@lru_cache(None)
def truck_body():
    """Furgón blanco sin logos, vista lateral, cabina a la derecha."""
    w, h = TRUCK_W, TRUCK_H
    img, d = hi(w, h)
    # chasis
    d.rounded_rectangle(S(20, 300, 760, 336), radius=8 * SS, fill=(43, 47, 54))
    # caja de carga
    d.rounded_rectangle(S(0, 10, 540, 312), radius=16 * SS, fill=(247, 249, 252), outline=(205, 214, 226), width=3 * SS)
    for x in (135, 270, 405):
        d.line(S(x, 22, x, 300), fill=(222, 229, 238), width=3 * SS)
    d.rectangle(S(0, 288, 540, 312), fill=(225, 231, 240))
    # cabina
    cab = [(548, 330), (548, 100), (660, 100), (735, 200), (760, 215), (760, 330)]
    d.polygon([(x * SS, y * SS) for x, y in cab], fill=(250, 251, 253), outline=(205, 214, 226))
    d.polygon(S(565, 118, 652, 118, 712, 200, 565, 200), fill=(150, 205, 240))
    d.polygon(S(600, 118, 625, 118, 600, 160), fill=(205, 233, 250))
    d.line(S(640, 205, 640, 320), fill=(205, 214, 226), width=3 * SS)
    d.rounded_rectangle(S(650, 232, 680, 240), radius=3 * SS, fill=(170, 180, 192))
    d.rounded_rectangle(S(742, 236, 764, 262), radius=5 * SS, fill=YELLOW)
    d.rounded_rectangle(S(700, 310, 772, 338), radius=8 * SS, fill=(60, 66, 76))
    d.rectangle(S(556, 300, 760, 304), fill=ORANGE)
    # pasos de rueda
    for x, y in WHEELS:
        d.ellipse(S(x - 56, y - 56, x + 56, y + 56), fill=(43, 47, 54))
    return fin(img, w, h)


def truck(canvas, cx, cy, angle=0.0, scale=1.0, bob=0.0):
    body = truck_body()
    sw = wheel_sprite()
    if scale != 1:
        body = body.resize((int(body.width * scale), int(body.height * scale)), Image.LANCZOS)
        sw = sw.resize((int(sw.width * scale), int(sw.height * scale)), Image.LANCZOS)
    x0 = cx - body.width / 2
    y0 = cy - body.height / 2
    # sombra en el piso
    sh = Image.new("RGBA", (int(body.width * 1.05), 40), (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse((0, 0, sh.width, 40), fill=(0, 0, 0, 70))
    sh = sh.filter(ImageFilter.GaussianBlur(8))
    canvas.paste(sh, (int(cx - sh.width / 2), int(y0 + 380 * scale)), sh)
    canvas.paste(body, (int(x0), int(y0 + bob)), body)
    for wx, wy in WHEELS:
        r = sw.rotate(-angle, resample=Image.BICUBIC)
        canvas.paste(r, (int(x0 + wx * scale - r.width / 2), int(y0 + wy * scale - r.height / 2)), r)


SOFA_W, SOFA_H = 600, 320


def sofa_shape(d, fill, outline=None):
    d.rounded_rectangle(S(40, 20, 560, 200), radius=40 * SS, fill=fill)          # respaldo
    d.rounded_rectangle(S(0, 110, 120, 280), radius=36 * SS, fill=fill)          # brazo izq
    d.rounded_rectangle(S(480, 110, 600, 280), radius=36 * SS, fill=fill)        # brazo der
    d.rounded_rectangle(S(70, 170, 530, 280), radius=26 * SS, fill=fill)         # asiento


@lru_cache(None)
def sofa_sprite():
    img, d = hi(SOFA_W, SOFA_H)
    for x in (70, 510):
        d.rounded_rectangle(S(x, 270, x + 22, 318), radius=6 * SS, fill=(90, 60, 40))
    sofa_shape(d, (231, 111, 81))
    d.rounded_rectangle(S(85, 182, 296, 250), radius=20 * SS, fill=(244, 140, 110))
    d.rounded_rectangle(S(304, 182, 515, 250), radius=20 * SS, fill=(244, 140, 110))
    d.rounded_rectangle(S(75, 45, 295, 165), radius=26 * SS, fill=(240, 128, 98))
    d.rounded_rectangle(S(305, 45, 525, 165), radius=26 * SS, fill=(240, 128, 98))
    return fin(img, SOFA_W, SOFA_H)


@lru_cache(None)
def blanket_sprite():
    """Sofá cubierto con manta acolchada azul."""
    img, d = hi(SOFA_W, SOFA_H)
    mask_img, md = hi(SOFA_W, SOFA_H)
    sofa_shape(md, (255, 255, 255))
    md.rounded_rectangle(S(60, 260, 540, 300), radius=12 * SS, fill=(255, 255, 255))
    quilt = Image.new("RGBA", img.size, (58, 110, 165, 255))
    qd = ImageDraw.Draw(quilt)
    step = 46 * SS
    for k in range(-20, 40):
        qd.line([(k * step, 0), (k * step + img.height, img.height)], fill=(80, 135, 192), width=3 * SS)
        qd.line([(k * step, img.height), (k * step + img.height, 0)], fill=(80, 135, 192), width=3 * SS)
    img.paste(quilt, (0, 0), mask_img.getchannel("A"))
    d.line(S(40, 292, 560, 292), fill=(34, 74, 120), width=6 * SS)  # borde de la manta
    return fin(img, SOFA_W, SOFA_H)


@lru_cache(None)
def vinipel_sprite():
    """Capa de vinipel: transparente con brillos diagonales."""
    img, d = hi(SOFA_W, SOFA_H)
    mask_img, md = hi(SOFA_W, SOFA_H)
    sofa_shape(md, (255, 255, 255))
    md.rounded_rectangle(S(60, 260, 540, 300), radius=12 * SS, fill=(255, 255, 255))
    film = Image.new("RGBA", img.size, (220, 240, 255, 70))
    fd = ImageDraw.Draw(film)
    for k in range(-6, 14):
        x = k * 70 * SS
        fd.line([(x, img.height), (x + img.height * 0.7, 0)], fill=(255, 255, 255, 150), width=7 * SS)
        fd.line([(x + 22 * SS, img.height), (x + 22 * SS + img.height * 0.7, 0)], fill=(255, 255, 255, 70), width=3 * SS)
    for y in (90, 175, 245):  # vueltas del rollo
        fd.line([(0, y * SS), (img.width, (y - 18) * SS)], fill=(255, 255, 255, 120), width=4 * SS)
    img.paste(film, (0, 0), mask_img.getchannel("A"))
    return fin(img, SOFA_W, SOFA_H)


# iconos (tamaño s x s)
@lru_cache(None)
def icon(name, s=96, color=NAVY):
    img, d = hi(s, s)
    k = s / 96
    P = lambda *v: [x * k * SS for x in v]
    if name == "check":
        d.ellipse(P(0, 0, 96, 96), fill=GREEN)
        d.line(P(26, 50, 42, 66, 72, 32), fill=WHITE, width=int(11 * k * SS), joint="curve")
    elif name == "pin":
        d.ellipse(P(18, 6, 78, 66), fill=ORANGE)
        d.polygon(P(22, 48, 74, 48, 48, 92), fill=ORANGE)
        d.ellipse(P(35, 23, 61, 49), fill=WHITE)
    elif name == "camera":
        d.rounded_rectangle(P(6, 26, 90, 84), radius=int(12 * k * SS), fill=ORANGE)
        d.rounded_rectangle(P(30, 14, 62, 32), radius=int(6 * k * SS), fill=ORANGE)
        d.ellipse(P(28, 34, 68, 74), fill=WHITE)
        d.ellipse(P(37, 43, 59, 65), fill=NAVY)
    elif name == "stairs":
        d.line(P(6, 86, 6, 70, 22, 70, 22, 54, 38, 54, 38, 38, 54, 38), fill=ORANGE, width=int(9 * k * SS), joint="curve")
        d.rounded_rectangle(P(58, 8, 92, 88), radius=int(6 * k * SS), outline=ORANGE, width=int(7 * k * SS))
        d.polygon(P(66, 40, 84, 40, 75, 24), fill=ORANGE)
        d.polygon(P(66, 56, 84, 56, 75, 72), fill=ORANGE)
    elif name == "chat":
        d.ellipse(P(4, 4, 92, 86), fill=WHITE)
        d.polygon(P(10, 92, 20, 62, 40, 80), fill=WHITE)
        d.rounded_rectangle(P(30, 26, 66, 62), radius=int(10 * k * SS), outline=GREEN, width=int(8 * k * SS))
        d.rectangle(P(40, 20, 56, 32), fill=WHITE)
        d.rectangle(P(40, 56, 56, 68), fill=WHITE)
    elif name == "calendar":
        d.rounded_rectangle(P(6, 14, 90, 92), radius=int(12 * k * SS), fill=WHITE)
        d.rounded_rectangle(P(6, 14, 90, 38), radius=int(12 * k * SS), fill=ORANGE)
        d.rectangle(P(6, 28, 90, 38), fill=ORANGE)
        for x in (26, 70):
            d.rounded_rectangle(P(x - 5, 4, x + 5, 24), radius=int(4 * k * SS), fill=NAVY)
        d.line(P(28, 64, 42, 78, 70, 50), fill=GREEN, width=int(9 * k * SS), joint="curve")
    elif name == "truck":
        d.rounded_rectangle(P(2, 22, 60, 70), radius=int(6 * k * SS), fill=color)
        d.polygon(P(62, 36, 80, 36, 94, 54, 94, 70, 62, 70), fill=color)
        d.polygon(P(68, 41, 79, 41, 88, 54, 68, 54), fill=(255, 255, 255, 200))
        for x in (22, 76):
            d.ellipse(P(x - 11, 62, x + 11, 84), fill=color)
            d.ellipse(P(x - 5, 68, x + 5, 78), fill=(255, 255, 255, 230))
    return fin(img, s, s)


# -------------------------------------------------------- textos y tarjetas
def rich_line(d, x, y, line, f, base, hl, stroke=0, stroke_fill=None):
    """Dibuja una línea donde las palabras entre *asteriscos* van resaltadas."""
    for tok in line.split(" "):
        color = hl if tok.startswith("*") or tok.endswith("*") or "*" in tok else base
        word = tok.replace("*", "")
        d.text((x, y), word, font=f, fill=color, stroke_width=stroke, stroke_fill=stroke_fill)
        x += f.getlength(word + " ")


@lru_cache(None)
def subtitle_sprite(text):
    f = font(F_BLACK, 72)
    lines = wrap(text, f, 760)
    lh = 86
    tw = max(f.getlength(l.replace("*", "")) for l in lines)
    pw, ph = int(tw + 70), int(lh * len(lines) + 46)
    img = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, pw, ph), radius=30, fill=(*NAVY2, 230))
    for i, l in enumerate(lines):
        lw = f.getlength(l.replace("*", ""))
        rich_line(d, (pw - lw) / 2, 18 + i * lh, l, f, WHITE, YELLOW)
    return img


@lru_cache(None)
def chip_sprite(text, w=405, h=96, bg=WHITE, fg=NAVY):
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w, h), radius=h // 2, fill=bg)
    ic = icon("check", 62)
    img.paste(ic, (17, (h - 62) // 2), ic)
    f = fit_font(text, F_XB, 40, w - 110)
    d.text((92, h / 2), text, font=f, fill=fg, anchor="lm")
    return shadow(img, blur=10, off=(0, 8), alpha=0.18)


@lru_cache(None)
def step_card(n, ic, text):
    w, h = 840, 150
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w, h), radius=34, fill=WHITE)
    d.ellipse((28, 30, 118, 120), fill=ORANGE)
    d.text((73, 75), str(n), font=font(F_BLACK, 56), fill=WHITE, anchor="mm")
    i = icon(ic, 84)
    img.paste(i, (140, 33), i)
    f = fit_font(text, F_XB, 50, w - 270)
    d.text((250, h / 2), text, font=f, fill=NAVY, anchor="lm")
    return shadow(img, blur=14, off=(0, 10), alpha=0.35)


@lru_cache(None)
def stamp_sprite():
    w, h = 760, 190
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w, h), radius=30, fill=YELLOW)
    d.rounded_rectangle((10, 10, w - 10, h - 10), radius=24, outline=NAVY, width=5)
    d.text((w / 2, 62), "PRECIO CLARO,", font=font(F_BLACK, 62), fill=NAVY, anchor="mm")
    d.text((w / 2, 130), "SIN SORPRESAS", font=font(F_BLACK, 62), fill=ORANGE, anchor="mm")
    return shadow(img, blur=16, off=(0, 12), alpha=0.35)


@lru_cache(None)
def brand_chip():
    name = CFG["nombre_corto"]
    f = font(F_XB, 34)
    tw = f.getlength(name)
    w, h = int(tw + 110), 66
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w, h), radius=33, fill=(*NAVY2, 220))
    logo = CFG.get("logo")
    if logo and Path(ROOT / logo).exists():
        lg = Image.open(ROOT / logo).convert("RGBA")
        lg.thumbnail((50, 50))
        img.paste(lg, (14, (h - lg.height) // 2), lg)
    else:
        ic = icon("truck", 50, WHITE)
        img.paste(ic, (16, 8), ic)
    d.text((80, h / 2), name, font=f, fill=WHITE, anchor="lm")
    return img


@lru_cache(None)
def bubble(text, out=True, maxw=330):
    f = font(F_SEMI, 34)
    lines = wrap(text, f, maxw)
    tw = max(f.getlength(l) for l in lines)
    w, h = int(tw + 44), int(len(lines) * 44 + 30)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w, h), radius=22, fill=(220, 248, 198) if out else WHITE)
    for i, l in enumerate(lines):
        d.text((22, 14 + i * 44), l, font=f, fill=(30, 40, 50))
    return shadow(img, blur=6, off=(0, 3), alpha=0.15)


# --------------------------------------------------------------- subtítulos
# (inicio, fin, texto). Las palabras entre *...* se resaltan en amarillo.
SUBS = [
    (0.10, 1.50, "¿Te vas a *trastear*"),
    (1.50, 3.00, "y no sabes por dónde *empezar*?"),
    (3.00, 4.30, "*Tranquilo*,"),
    (4.30, 6.00, "nosotros lo *movemos* por ti."),
    (6.00, 7.70, "*Cargamos*, *descargamos*"),
    (7.70, 9.20, "y *protegemos* tus muebles"),
    (9.20, 10.60, "con *mantas* y *vinipel*,"),
    (10.60, 12.00, f"en *{CIUDAD}* y fuera de la ciudad."),
    (12.00, 13.20, "Cotizar es *fácil*:"),
    (13.20, 14.60, "mándanos las *direcciones*,"),
    (14.60, 15.80, "*fotos* de tus muebles,"),
    (15.80, 17.40, "y cuéntanos si hay *ascensor* o *escaleras*."),
    (17.40, 19.00, "*Precio claro*, sin sorpresas."),
    (19.00, 21.50, "¡Escríbenos ya al *WhatsApp*"),
    (21.50, 24.00, "y separa tu *fecha*!"),
]
SUB_CY = 1345


def draw_subs(canvas, t):
    for a, b, txt in SUBS:
        if a <= t < b:
            p = prog(t, a, a + 0.16)
            sp = subtitle_sprite(txt)
            paste(canvas, sp, CX, SUB_CY, scale=0.9 + 0.1 * ease_out_back(p), alpha=p)


# -------------------------------------------------------------- escenas
@lru_cache(None)
def bg(name):
    if name == "s1":
        img = vgrad(W, H, (255, 248, 236), (255, 228, 196))
        d = ImageDraw.Draw(img)
        d.rectangle((0, 1150, W, H), fill=(236, 205, 168))   # piso
        d.rectangle((0, 1150, W, 1162), fill=(214, 180, 140))
        d.rounded_rectangle((90, 300, 330, 620), radius=10, fill=(255, 255, 255), outline=(230, 210, 186), width=8)  # ventana
        d.line((210, 300, 210, 620), fill=(230, 210, 186), width=6)
        d.line((90, 460, 330, 460), fill=(230, 210, 186), width=6)
        return img
    if name == "s2":
        img = vgrad(W, H, (126, 196, 246), (220, 240, 255))
        d = ImageDraw.Draw(img)
        d.ellipse((700, 260, 860, 420), fill=(255, 221, 120))
        # conjunto residencial
        for x0, bw, bh, col in ((-40, 260, 520, (176, 196, 222)), (230, 220, 420, (196, 212, 232)),
                                (460, 280, 600, (168, 188, 216)), (760, 360, 470, (190, 206, 228))):
            top = 1060 - bh
            d.rectangle((x0, top, x0 + bw, 1060), fill=col)
            for wy in range(top + 40, 1020, 70):
                for wx in range(x0 + 30, x0 + bw - 40, 62):
                    d.rectangle((wx, wy, wx + 30, wy + 38), fill=(235, 243, 252))
        d.rectangle((0, 1040, W, 1070), fill=(120, 170, 110))   # zona verde
        d.rectangle((0, 1070, W, H), fill=(80, 86, 98))          # vía
        d.rectangle((0, 1070, W, 1080), fill=(200, 200, 200))
        return img
    if name == "s3":
        img = vgrad(W, H, (236, 243, 250), (214, 226, 242))
        d = ImageDraw.Draw(img)
        d.rectangle((0, 860, W, H), fill=(196, 172, 140))
        for x in range(-200, W + 200, 120):
            d.line((x, 860, x - 160, H), fill=(184, 158, 124), width=4)
        return img
    if name == "s4":
        img = vgrad(W, H, NAVY, NAVY2)
        d = ImageDraw.Draw(img, "RGBA")
        for i in range(9):
            d.ellipse((-300 + i * 160, -200 + i * 210, -60 + i * 160, 40 + i * 210), fill=(255, 255, 255, 10))
        return img
    if name == "s5":
        return vgrad(W, H, (42, 214, 112), GREEN_D)
    if name == "s6":
        img = vgrad(W, H, NAVY, NAVY2)
        d = ImageDraw.Draw(img, "RGBA")
        d.polygon([(0, 0), (W, 0), (W, 120), (0, 260)], fill=(*ORANGE, 255))
        d.polygon([(0, H), (W, H), (W, 1700), (0, 1820)], fill=(*ORANGE, 255))
        return img
    raise KeyError(name)


BOXES = [  # (x, y_final, w, h, rot, retraso, tinte)
    (300, 1050, 230, 200, -3, 0.00, 0),
    (540, 1060, 250, 180, 2, 0.15, -12),
    (760, 1065, 200, 170, -2, 0.30, 8),
    (420, 860, 220, 190, 6, 0.45, 10),
    (650, 880, 200, 160, -7, 0.60, -6),
    (530, 690, 180, 150, 10, 0.75, 4),
]


def scene1(c, t):
    c.paste(bg("s1"))
    for x, y, w, h, rot, dl, tint in BOXES:
        p = ease_out_bounce(prog(t, dl, dl + 0.7))
        yy = -300 + (y - (-300)) * p
        wob = math.sin(t * 6 + x) * 2.5 * prog(t, 1.2, 1.6)
        paste(c, box_sprite(w, h, tint), x - 60, yy - h / 2, rot=rot + wob)
    # signos de pregunta (estrés)
    for i, (qx, qy, sz) in enumerate(((180, 560, 150), (760, 520, 120), (640, 400, 90))):
        p = prog(t, 1.0 + i * 0.25, 1.35 + i * 0.25)
        if p > 0:
            f = font(F_BLACK, sz)
            q = Image.new("RGBA", (sz, int(sz * 1.3)), (0, 0, 0, 0))
            ImageDraw.Draw(q).text((sz / 2, sz * 0.65), "?", font=f, fill=ORANGE, anchor="mm")
            paste(c, q, qx, qy + math.sin(t * 5 + i) * 10, scale=ease_out_back(p), rot=math.sin(t * 4 + i) * 12)


def scene2(c, t):
    c.paste(bg("s2"))
    d = ImageDraw.Draw(c)
    lt = t - 3.0
    arrive = 1.5
    p = ease_out_cubic(prog(lt, 0, arrive))
    x = -500 + (CX - (-500)) * p
    speed = 1 - p
    # líneas de la vía
    off = (x * 1.0) % 160
    for k in range(-1, 9):
        xx = k * 160 - off * 0
        d.rectangle((k * 160 + 30, 1170, k * 160 + 120, 1184), fill=(235, 235, 235))
    # líneas de velocidad
    for i in range(5):
        if speed > 0.05:
            ly = 760 + i * 55
            d.rounded_rectangle((x - 520 - i * 30, ly, x - 420 - i * 30 + 160 * speed, ly + 10), radius=5, fill=(255, 255, 255))
    ang = (x + 500) / 46 * 180 / math.pi
    bob = math.sin(prog(lt, arrive - 0.1, arrive + 0.5) * math.pi * 2) * 6 * (1 - prog(lt, arrive, arrive + 0.6))
    truck(c, x, 900, angle=ang, bob=bob)


def scene3(c, t):
    c.paste(bg("s3"))
    lt = t - 6.0
    cy = 600
    # sombra del sofá
    sh = Image.new("RGBA", (640, 50), (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse((0, 0, 640, 50), fill=(0, 0, 0, 60))
    sh = sh.filter(ImageFilter.GaussianBlur(10))
    c.paste(sh, (CX - 320, cy + 140), sh)
    sc = 0.94 + 0.06 * ease_out_back(prog(lt, 0, 0.4))
    x0, y0 = int(CX - SOFA_W / 2), int(cy - SOFA_H / 2)
    c.paste(sofa_sprite(), (x0, y0), sofa_sprite())
    # manta: se envuelve de izquierda a derecha
    pb = ease_in_out(prog(lt, 1.2, 2.4))
    if pb > 0:
        bw = int(SOFA_W * pb)
        crop = blanket_sprite().crop((0, 0, max(1, bw), SOFA_H))
        c.paste(crop, (x0, y0), crop)
    # vinipel
    pv = ease_in_out(prog(lt, 3.2, 4.2))
    if pv > 0:
        vw = int(SOFA_W * pv)
        crop = vinipel_sprite().crop((0, 0, max(1, vw), SOFA_H))
        c.paste(crop, (x0, y0), crop)
        if pv < 1:  # rollo de vinipel
            d = ImageDraw.Draw(c, "RGBA")
            rx = x0 + vw
            d.rounded_rectangle((rx - 18, y0 - 10, rx + 18, y0 + SOFA_H + 10), radius=18, fill=(230, 245, 255, 220), outline=(170, 200, 225), width=3)
    # etiquetas de manta / vinipel
    for txt, a, xx in (("MANTAS", 1.6, CX - 170), ("VINIPEL", 3.6, CX + 170)):
        p = prog(lt, a, a + 0.3)
        if p > 0:
            f = font(F_BLACK, 40)
            tw = int(f.getlength(txt)) + 50
            tag = Image.new("RGBA", (tw, 70), (0, 0, 0, 0))
            dd = ImageDraw.Draw(tag)
            dd.rounded_rectangle((0, 0, tw, 70), radius=35, fill=ORANGE)
            dd.text((tw / 2, 35), txt, font=f, fill=WHITE, anchor="mm")
            paste(c, tag, xx, 330, scale=ease_out_back(p))
    # chips: lo que incluye
    chips = [("Cargue", 3.9, SAFE_L + 205, 900), ("Descargue", 4.15, SAFE_L + 635, 900),
             ("Mantas y vinipel", 4.4, SAFE_L + 205, 1015), (f"{CIUDAD} y fuera", 4.65, SAFE_L + 635, 1015)]
    for txt, a, xx, yy in chips:
        p = prog(lt, a, a + 0.3)
        if p > 0:
            paste(c, chip_sprite(txt), xx, yy, scale=ease_out_back(p), alpha=p)


def scene4(c, t):
    c.paste(bg("s4"))
    lt = t - 12.0
    p = ease_out_back(prog(lt, 0.05, 0.4))
    f = font(F_BLACK, 84)
    title = Image.new("RGBA", (840, 110), (0, 0, 0, 0))
    ImageDraw.Draw(title).text((420, 55), "COTIZAR ES FÁCIL", font=f, fill=YELLOW, anchor="mm")
    paste(c, title, CX, 340, scale=p, alpha=prog(lt, 0.05, 0.2))
    steps = [(1, "pin", "Las direcciones", 1.2, 490),
             (2, "camera", "Fotos de tus muebles", 2.6, 665),
             (3, "stairs", "¿Ascensor o escaleras?", 3.8, 840)]
    for n, ic, txt, a, yy in steps:
        p = prog(lt, a, a + 0.35)
        if p > 0:
            e = ease_out_cubic(p)
            paste(c, step_card(n, ic, txt), CX + (1 - e) * 500, yy, alpha=p)
    p = prog(lt, 5.4, 5.7)
    if p > 0:
        paste(c, stamp_sprite(), CX, 1065, scale=1.6 - 0.6 * ease_out_back(p), rot=4, alpha=p)


def scene5(c, t):
    c.paste(bg("s5"))
    lt = t - 19.0
    # teléfono
    pw, ph = 470, 800
    px0, py0 = CX - pw // 2, 250
    d = ImageDraw.Draw(c, "RGBA")
    rise = (1 - ease_out_cubic(prog(lt, 0, 0.45))) * 900
    py0 += int(rise)
    d.rounded_rectangle((px0 + 8, py0 + 18, px0 + pw + 8, py0 + ph + 18), radius=64, fill=(0, 0, 0, 50))
    d.rounded_rectangle((px0, py0, px0 + pw, py0 + ph), radius=64, fill=(25, 30, 38))
    sx0, sy0, sx1, sy1 = px0 + 18, py0 + 18, px0 + pw - 18, py0 + ph - 18
    d.rounded_rectangle((sx0, sy0, sx1, sy1), radius=48, fill=(236, 229, 221))
    d.rounded_rectangle((sx0, sy0, sx1, sy0 + 120), radius=48, fill=GREEN_D)
    d.rectangle((sx0, sy0 + 60, sx1, sy0 + 120), fill=GREEN_D)
    d.ellipse((sx0 + 24, sy0 + 40, sx0 + 84, sy0 + 100), fill=WHITE)
    ic = icon("truck", 44, NAVY)
    c.paste(ic, (sx0 + 32, sy0 + 48), ic)
    nm = fit_font(CFG["nombre_corto"], F_BOLD, 32, 300)
    d.text((sx0 + 100, sy0 + 70), CFG["nombre_corto"], font=nm, fill=WHITE, anchor="lm")
    # mensajes
    msgs = [(0.6, "Hola, quiero cotizar mi trasteo", True),
            (2.5, "¡Claro! Envíanos las direcciones y fotos", False),
            (3.2, "¿Qué fecha te sirve?", False)]
    yy = sy0 + 160
    for a, txt, out in msgs:
        p = prog(lt, a, a + 0.25)
        b = bubble(txt, out)
        if p > 0:
            bx = sx1 - b.width / 2 + 6 if out else sx0 + b.width / 2 - 6
            paste(c, b, bx, yy + b.height / 2, scale=0.8 + 0.2 * ease_out_back(p), alpha=p)
        yy += b.height - 10
    # escribiendo...
    if 1.3 < lt < 2.5:
        d.rounded_rectangle((sx0 + 20, yy + 10, sx0 + 140, yy + 66), radius=24, fill=WHITE)
        for i in range(3):
            o = abs(math.sin(lt * 8 + i * 0.9)) * 8
            d.ellipse((sx0 + 44 + i * 30, yy + 30 - o, sx0 + 60 + i * 30, yy + 46 - o), fill=(140, 150, 160))
    # chip "separa tu fecha"
    p = prog(lt, 3.2, 3.5)
    if p > 0:
        w, h = 560, 110
        chip = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        cd = ImageDraw.Draw(chip)
        cd.rounded_rectangle((0, 0, w, h), radius=55, fill=WHITE)
        cal = icon("calendar", 76)
        chip.paste(cal, (22, 17), cal)
        cd.text((118, h / 2), "Separa tu fecha", font=font(F_BLACK, 50), fill=NAVY, anchor="lm")
        paste(c, shadow(chip, 12, (0, 8), 0.25), CX, 1110, scale=ease_out_back(p), alpha=p)


def scene6(c, t):
    c.paste(bg("s6"))
    lt = t - 24.0
    d = ImageDraw.Draw(c)
    p = ease_out_back(prog(lt, 0.0, 0.35))
    # logo o icono
    logo = CFG.get("logo")
    if logo and Path(ROOT / logo).exists():
        lg = Image.open(ROOT / logo).convert("RGBA")
        lg.thumbnail((260, 200))
        paste(c, lg, CX, 330, scale=p)
    else:
        paste(c, icon("truck", 190, WHITE), CX, 330, scale=p)
    # nombre
    pn = prog(lt, 0.1, 0.4)
    f = font(F_BLACK, 96)
    lines = wrap(CFG["nombre"], f, 800)
    if len(lines) > 2:
        f = font(F_BLACK, 76)
        lines = wrap(CFG["nombre"], f, 800)
    namebox = Image.new("RGBA", (840, len(lines) * 108 + 10), (0, 0, 0, 0))
    nd = ImageDraw.Draw(namebox)
    for i, l in enumerate(lines):
        nd.text((420, 54 + i * 108), l, font=f, fill=WHITE, anchor="mm")
    paste(c, namebox, CX, 560, alpha=pn, scale=0.95 + 0.05 * ease_out_cubic(pn))
    sub = f"Trasteos en {CIUDAD} y fuera de la ciudad"
    fs = fit_font(sub, F_SEMI, 42, 800)
    sb = Image.new("RGBA", (840, 60), (0, 0, 0, 0))
    ImageDraw.Draw(sb).text((420, 30), sub, font=fs, fill=(200, 214, 240), anchor="mm")
    paste(c, sb, CX, 720, alpha=prog(lt, 0.25, 0.5))
    # WhatsApp grande
    pw = prog(lt, 0.4, 0.75)
    if pw > 0:
        w, h = 840, 250
        wa = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        wd = ImageDraw.Draw(wa)
        wd.rounded_rectangle((0, 0, w, h), radius=44, fill=GREEN)
        ch = icon("chat", 70)
        wa.paste(ch, (40, 26), ch)
        wd.text((128, 61), "WhatsApp", font=font(F_XB, 52), fill=WHITE, anchor="lm")
        fnum = fit_font(CFG["whatsapp"], F_BLACK, 116, w - 60)
        wd.text((w / 2, 172), CFG["whatsapp"], font=fnum, fill=WHITE, anchor="mm")
        paste(c, shadow(wa, 16, (0, 12), 0.35), CX, 930, scale=0.85 + 0.15 * ease_out_back(pw), alpha=pw)
    # botón "Escríbenos ya" con pulso
    pb = prog(lt, 0.9, 1.2)
    if pb > 0:
        w, h = 620, 130
        bt = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        bd = ImageDraw.Draw(bt)
        bd.rounded_rectangle((0, 0, w, h), radius=65, fill=YELLOW)
        bd.text((w / 2, h / 2), "Escríbenos ya", font=font(F_BLACK, 66), fill=NAVY, anchor="mm")
        pulse = 1 + 0.04 * math.sin(max(0, lt - 1.2) * 7)
        paste(c, shadow(bt, 12, (0, 10), 0.3), CX, 1200, scale=ease_out_back(pb) * pulse, alpha=pb)


SCENES = [(0, 3, scene1), (3, 6, scene2), (6, 12, scene3), (12, 19, scene4), (19, 24, scene5), (24, 27.01, scene6)]
CUTS = [3, 6, 12, 19, 24]


def transition(c, t):
    """Barrido diagonal naranja en cada cambio de escena (0.36 s)."""
    for cut in CUTS:
        if cut - 0.18 <= t < cut + 0.18:
            k = (t - (cut - 0.18)) / 0.36
            x = -1500 + k * (W + 2600)
            d = ImageDraw.Draw(c)
            d.polygon([(x, 0), (x + 900, 0), (x + 400, H), (x - 500, H)], fill=ORANGE)
            d.polygon([(x + 900, 0), (x + 1000, 0), (x + 500, H), (x + 400, H)], fill=YELLOW)


def frame(t):
    c = Image.new("RGB", (W, H))
    for a, b, fn in SCENES:
        if a <= t < b:
            fn(c, t)
            break
    if t < 24:
        bc = brand_chip()
        c.paste(bc, (SAFE_L, 212), bc)
    draw_subs(c, t)
    transition(c, t)
    return c


def render_video(out):
    n = int(DUR * FPS)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "16",
           "-pix_fmt", "yuv420p", str(out)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(frame(i / FPS).tobytes())
        if i % 90 == 0:
            print(f"  cuadro {i}/{n}", flush=True)
    p.stdin.close()
    p.wait()


def portada(out):
    c = Image.new("RGB", (W, H))
    c.paste(bg("s4"))
    d = ImageDraw.Draw(c, "RGBA")
    d.polygon([(0, H), (W, H), (W, 1640), (0, 1780)], fill=ORANGE)
    bc = brand_chip()
    c.paste(bc, (SAFE_L, 212), bc)
    f = font(F_BLACK, 118)
    for i, l in enumerate(["¿TE VAS A", "TRASTEAR?"]):
        d.text((CX, 400 + i * 132), l, font=f, fill=YELLOW if i else WHITE, anchor="mm")
    d.text((CX, 640), "Nosotros lo movemos por ti", font=fit_font("Nosotros lo movemos por ti", F_XB, 58, 820), fill=WHITE, anchor="mm")
    truck(c, CX, 900, scale=1.0)
    paste(c, box_sprite(150, 130), CX - 330, 1060, rot=-6)
    sub = f"{CIUDAD} y fuera de la ciudad"
    d.text((CX, 1185), sub, font=fit_font(sub, F_SEMI, 46, 820), fill=(200, 214, 240), anchor="mm")
    w, h = 840, 200
    wa = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    wd = ImageDraw.Draw(wa)
    wd.rounded_rectangle((0, 0, w, h), radius=44, fill=GREEN)
    ch = icon("chat", 64)
    wa.paste(ch, (34, 22), ch)
    wd.text((112, 54), "Cotiza por WhatsApp", font=font(F_XB, 46), fill=WHITE, anchor="lm")
    wd.text((w / 2, 142), CFG["whatsapp"], font=fit_font(CFG["whatsapp"], F_BLACK, 92, w - 60), fill=WHITE, anchor="mm")
    paste(c, shadow(wa, 16, (0, 12), 0.35), CX, 1380)
    c.save(out)


def keyframes(outdir, times):
    outdir.mkdir(parents=True, exist_ok=True)
    for t in times:
        img = frame(t)
        img.save(outdir / f"clave_{t:05.2f}.png")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "video"
    if mode == "video":
        render_video(ROOT / "clips" / "escenas.mp4")
    elif mode == "frames":
        ts = [float(x) for x in sys.argv[2:]] or [1.2, 4.8, 11.0, 18.2, 23.0, 26.0]
        keyframes(ROOT / "frames", ts)
    elif mode == "portada":
        portada(ROOT / "final" / "portada.png")
    print("ok")
