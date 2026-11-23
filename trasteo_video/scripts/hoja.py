import sys
from pathlib import Path
from PIL import Image, ImageDraw
files = sorted(Path(sys.argv[1]).glob("clave_*.png"))
tw, th = 360, 640
sheet = Image.new("RGB", (tw * len(files), th), "black")
for i, f in enumerate(files):
    im = Image.open(f).convert("RGBA")
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    red = (255, 0, 0, 70)
    d.rectangle((0, 0, 1080, 192), fill=red); d.rectangle((0, 1536, 1080, 1920), fill=red); d.rectangle((918, 0, 1080, 1920), fill=red)
    im = Image.alpha_composite(im, ov).convert("RGB").resize((tw, th))
    sheet.paste(im, (i * tw, 0))
sheet.save(sys.argv[2])
