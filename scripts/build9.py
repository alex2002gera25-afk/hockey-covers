from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
D = "/root/.claude/uploads/5ac0a329-489a-5db8-a7dc-75f4dd690dba/"
OUT = "/mnt/user-data/outputs/alex_analytics_carousel_08"
FH = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"
FB = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FBB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FM = "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"
BLUE = (45, 107, 255)
S = 2
k = 1350 / 4608
cropx = (3712 * k - 1080) / 2

def photo(name):
    im = Image.open(D + name).convert("RGB")
    q = im.resize((round(3712 * k), 1350), Image.LANCZOS)
    l = round(cropx)
    return q.crop((l, 0, l + 1080, 1350))

def font(p, s): return ImageFont.truetype(p, int(s * S))
def tw(t, f): return f.getlength(t) / S

def wrap(text, f, maxw):
    words, out, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(t, f) <= maxw: cur = t
        else: out.append(cur); cur = w
    if cur: out.append(cur)
    return out

def fit(path, lines, maxw, start, minsize=30):
    s = start
    while s > minsize and max(tw(l, font(path, s)) for l in lines) > maxw: s -= 1
    return font(path, s), s

def render(name, zone, blocks, pad=34):
    img = photo(name).convert("RGBA")
    x0, y0, x1, y1 = zone
    maxw = (x1 - x0) - 2 * pad
    items = []   # (kind, payload, height)
    for b in blocks:
        kind = b[0]
        if kind == "title":
            lines, size = b[1], b[2]
            ft, st = fit(FH, lines, maxw, size)
            for l in lines: items.append(("t", (l, ft), st * 1.13))
        elif kind == "sub":
            fs = font(FB, b[2])
            items.append(("gap", None, 12))
            for l in wrap(b[1], fs, maxw): items.append(("s", (l, fs), b[2] * 1.27))
        elif kind == "bullets":
            fb = font(FBB, b[2])
            items.append(("gap", None, 14))
            for i, t in enumerate(b[1], 1):
                items.append(("b", (i, t, fb, b[2]), b[2] * 1.62))
        elif kind == "cta":
            items.append(("gap", None, 16)); items.append(("c", b[1], 52))
        elif kind == "nick":
            items.append(("gap", None, 12)); items.append(("n", b[1], 26))
    total = sum(h for _, _, h in items)
    y = (y0 + y1) / 2 - total / 2
    layer = Image.new("RGBA", (1080 * S, 1350 * S), (0, 0, 0, 0))
    sh = Image.new("RGBA", (1080 * S, 1350 * S), (0, 0, 0, 0))
    d, sd = ImageDraw.Draw(layer), ImageDraw.Draw(sh)
    X = x0 + pad
    for kind, p, h in items:
        if kind in ("t", "s"):
            txt, f = p
            for dr, col, off in ((sd, (0, 0, 0, 170), 3), (d, (255, 255, 255, 255), 0)):
                dr.text((X * S, (y + off) * S), txt, font=f, fill=col, anchor="la")
        elif kind == "b":
            i, t, f, sz = p
            r = sz * 0.62
            cy = y + sz * 0.62
            d.ellipse([(X) * S, (cy - r) * S, (X + 2 * r) * S, (cy + r) * S], fill=BLUE + (255,))
            d.text(((X + r) * S, (cy + 1) * S), str(i), font=font(FH, sz * 0.9), fill=(255, 255, 255, 255), anchor="mm")
            for dr, col, off in ((sd, (0, 0, 0, 170), 2), (d, (255, 255, 255, 255), 0)):
                dr.text(((X + 2 * r + 18) * S, (cy + off) * S), t, font=f, fill=col, anchor="lm")
        elif kind == "c":
            fc = font(FH, 30)
            w = tw(p, fc) + 56
            d.rounded_rectangle([X * S, y * S, (X + w) * S, (y + 52) * S], radius=26 * S, fill=BLUE + (255,))
            d.text(((X + w / 2) * S, (y + 27) * S), p, font=fc, fill=(255, 255, 255, 255), anchor="mm")
        elif kind == "n":
            fn = font(FM, 24)
            for dr, col, off in ((sd, (0, 0, 0, 170), 2), (d, (255, 255, 255, 255), 0)):
                dr.text((X * S, (y + off) * S), p, font=fn, fill=col, anchor="la")
        y += h
    sh = sh.filter(ImageFilter.GaussianBlur(S * 2))
    comp = Image.alpha_composite(sh.resize((1080, 1350), Image.LANCZOS), layer.resize((1080, 1350), Image.LANCZOS))
    return Image.alpha_composite(img, comp).convert("RGB"), total

Z1 = (54, 1038, 1026, 1330)
Z2 = (39, 981, 1040, 1308)
Z3 = (54, 978, 1026, 1298)

out = {}
out["01_cover.png"] = render("67a2efc2-image.png", Z1, [
    ("title", ["СВОБОДНАЯ ШАЙБА:", "ВЫИГРЫВАЕТ НЕ ВСЕГДА", "САМЫЙ СИЛЬНЫЙ"], 56),
    ("sub", "Часто эпизод решается за шаг до контакта.", 30)])
out["02_three.png"] = render("c4ab2391-image.png", Z2, [
    ("title", ["ТРИ ВЕЩИ РЕШАЮТ БОРЬБУ"], 54),
    ("bullets", ["Первый шаг: читай, куда покатится шайба",
                 "Корпус между шайбой и соперником",
                 "Партнёр рядом, чтобы забрать шайбу"], 30)])
out["03_cta.png"] = render("a17fa483-image.png", Z3, [
    ("title", ["ПРОВЕРЬ СВОЮ СМЕНУ"], 54),
    ("sub", "Кто первым достал шайбу? Чем её закрыл? Где был партнёр?", 28),
    ("cta", "НАПИШИ «ШАЙБА» В ДИРЕКТ"),
    ("nick", "@alex__analytics")])
for n, (im, tot) in out.items():
    im.save(os.path.join(OUT, n), "PNG")
    print(n, im.size, "text_h", round(tot))
