from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

SRC = "/root/.claude/uploads/5ac0a329-489a-5db8-a7dc-75f4dd690dba/45b62a66-image.png"
OUT = "/mnt/user-data/outputs/alex_analytics_carousel_07"
FH = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"
FB = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FBB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FM = "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"
BLUE = (45, 107, 255)
S = 2

big = Image.open(SRC).convert("RGB")
QW, QH = 1849, 2297
origins = {1: (0, 0), 2: (1863, 0), 3: (0, 2311), 4: (1863, 2311)}
zones_rel = {1: (97, 1709, 1752, 2197), 2: (95, 1709, 1751, 2197), 3: (97, 1734, 1760, 2213), 4: (94, 1734, 1750, 2211)}
k = 1350 / QH
cropx = (QW * k - 1080) / 2

def photo(n):
    ox, oy = origins[n]
    q = big.crop((ox, oy, ox + QW, oy + QH)).resize((round(QW * k), 1350), Image.LANCZOS)
    left = round(cropx)
    return q.crop((left, 0, left + 1080, 1350))

def zone(n):
    x0, y0, x1, y1 = zones_rel[n]
    return (x0 * k - cropx, y0 * k, x1 * k - cropx, y1 * k)

def font(p, s): return ImageFont.truetype(p, int(s * S))

def fit_font(path, lines, maxw, start, minsize=30):
    s = start
    while s > minsize and max(font(path, s).getlength(l) for l in lines) > maxw * S:
        s -= 1
    return font(path, s), s

def wrap(text, f, maxw):
    words, out, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if f.getlength(t) <= maxw * S: cur = t
        else: out.append(cur); cur = w
    if cur: out.append(cur)
    return out

def render(n, title_lines, sub=None, cta=None, nick=None, title_size=54, sub_size=29):
    img = photo(n).convert("RGBA")
    x0, y0, x1, y1 = zone(n)
    pad = 34
    maxw = (x1 - x0) - 2 * pad
    ft, st = fit_font(FH, title_lines, maxw, title_size)
    blocks = []  # (kind, text, font, height)
    for l in title_lines:
        blocks.append(("t", l, ft, st * 1.12))
    gap = 12
    if sub:
        fs = font(FB, sub_size)
        for l in wrap(sub, fs, maxw):
            blocks.append(("s", l, fs, sub_size * 1.26))
    pill_h = 0
    if cta:
        pill_h = 52
    if nick:
        pass
    total = sum(b[3] for b in blocks) + (gap if sub else 0)
    if cta: total += 14 + pill_h
    if nick: total += 12 + 26
    zy = (y0 + y1) / 2 - total / 2
    layer = Image.new("RGBA", (1080 * S, 1350 * S), (0, 0, 0, 0))
    shadow = Image.new("RGBA", (1080 * S, 1350 * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer); sd = ImageDraw.Draw(shadow)
    y = zy
    first_sub = True
    for kind, txt, f, h in blocks:
        if kind == "s" and first_sub:
            y += gap; first_sub = False
        for dr, col, off in ((sd, (0, 0, 0, 170), 3), (d, (255, 255, 255, 255), 0)):
            dr.text(((x0 + pad) * S, (y + off) * S), txt, font=f, fill=col, anchor="la")
        y += h
    if cta:
        y += 14
        fc = font(FH, 30)
        w = fc.getlength(cta) / S + 56
        d.rounded_rectangle([(x0 + pad) * S, y * S, (x0 + pad + w) * S, (y + pill_h) * S], radius=int(26 * S), fill=BLUE + (255,))
        d.text(((x0 + pad + w / 2) * S, (y + pill_h / 2 + 1) * S), cta, font=fc, fill=(255, 255, 255, 255), anchor="mm")
        y += pill_h
    if nick:
        y += 12
        fn = font(FM, 24)
        for dr, col, off in ((sd, (0, 0, 0, 170), 2), (d, (255, 255, 255, 255), 0)):
            dr.text(((x0 + pad) * S, (y + off) * S), nick, font=fn, fill=col, anchor="la")
    shadow = shadow.filter(ImageFilter.GaussianBlur(S * 2))
    comp = Image.alpha_composite(shadow.resize((1080, 1350), Image.LANCZOS), layer.resize((1080, 1350), Image.LANCZOS))
    out = Image.alpha_composite(img, comp).convert("RGB")
    return out, (round(x0), round(y0), round(x1), round(y1)), total

res = {}
res[1] = render(1, ["ПОЧЕМУ ОДНИ ИГРОКИ", "ВСЕГДА НА ШАГ ВПЕРЕДИ?"], "Они видят игру до того, как шайба приходит к ним.", title_size=56)
res[2] = render(2, ["ПОСМОТРИ ДО ШАЙБЫ,", "А НЕ ПОСЛЕ ПОЛУЧЕНИЯ"], "Перед передачей найди партнёров, соперника и свободное место.", title_size=54, sub_size=28)
res[3] = render(3, ["ТРЕНЕР ВИДИТ", "НЕ ТОЛЬКО ШАЙБУ"], "Позиция, дистанции и решения без шайбы входят в оценку игрока.", title_size=56, sub_size=28)
res[4] = render(4, ["ПРОВЕРЬ СВОЮ СМЕНУ"], "Поставь паузу перед шайбой: что ты видел вокруг?", cta="НАПИШИ «ИГРА» В ДИРЕКТ", nick="@alex__analytics", title_size=54, sub_size=28)
names = {1: "01_cover.png", 2: "02_scan.png", 3: "03_coach.png", 4: "04_cta.png"}
for n, (im, z, tot) in res.items():
    im.save(os.path.join(OUT, names[n]), "PNG")
    print(n, im.size, "zone", z, "zone_h", z[3] - z[1], "text_h", round(tot))
