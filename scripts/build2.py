from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os, random

S = 2
W, H = 1080, 1350
OUT = "/mnt/user-data/outputs/alex_analytics_carousel_02"
BG = (5, 7, 13)
BLUE = "#2D6BFF"; BLUE2 = "#3F82FF"; WHITE = "#FFFFFF"; GREY = "#9AA3B2"; GREYBLUE = "#8FA3BF"
RED = (176, 48, 64)

FH = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"
FB = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FBB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FM = "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"

def font(p, size): return ImageFont.truetype(p, int(size * S))
def sc(v): return int(round(v * S))
def P(pt): return (sc(pt[0]), sc(pt[1]))
def tw(t, f): return f.getlength(t)

def wrap(text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(t, f) <= sc(maxw): cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def para(d, x, y, s, f, fill, maxw, lh):
    for ln in wrap(s, f, maxw):
        d.text(P((x, y)), ln, font=f, fill=fill, anchor="la"); y += lh
    return y

def text(d, xy, s, f, fill, anchor="la"): d.text(P(xy), s, font=f, fill=fill, anchor=anchor)

def fit(strs, path, maxw, start, minsize=36):
    size = start
    while size > minsize and max(tw(s, font(path, size)) for s in strs) > sc(maxw): size -= 2
    return font(path, size), size

def brand(d):
    d.rectangle([P((80, 72)), P((98, 90))], fill=BLUE)
    text(d, (112, 66), "ALEX ANALYTICS", font(FM, 26), WHITE)

def new_canvas():
    img = Image.new("RGB", (sc(W), sc(H)), BG)
    return img, ImageDraw.Draw(img, "RGBA")

def ramp(img, ya, yb, a0, a1):
    """BG-coloured vertical alpha ramp; constant a1 below yb, nothing above ya."""
    m = Image.new("L", (sc(W), sc(H)), 0)
    md = ImageDraw.Draw(m)
    for y in range(sc(ya), sc(H)):
        t = min(1, (y - sc(ya)) / max(1, sc(yb - ya)))
        md.line([(0, y), (sc(W), y)], fill=int(a0 + (a1 - a0) * t))
    img.paste(Image.new("RGB", img.size, BG), (0, 0), m)

def ramp_top(img, ya, yb, a0, a1):
    """alpha a0 at/above ya, ramping to a1 at yb, nothing below."""
    m = Image.new("L", (sc(W), sc(H)), 0)
    md = ImageDraw.Draw(m)
    for y in range(0, sc(yb)):
        t = min(1, max(0, (y - sc(ya)) / max(1, sc(yb - ya))))
        md.line([(0, y), (sc(W), y)], fill=int(a0 + (a1 - a0) * t))
    img.paste(Image.new("RGB", img.size, BG), (0, 0), m)

def rink(img, y0, k=10.6, cx=540):
    Wr, Lr = 85 * k, 100 * k
    x0, x1 = cx - Wr / 2, cx + Wr / 2
    ybot = y0 + Lr
    rad = 28 * k
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([P((x0, y0)), P((x1, ybot + 400))], radius=sc(rad),
                                           corners=(True, True, False, False), fill=255)
    ice = Image.new("RGB", img.size)
    idr = ImageDraw.Draw(ice)
    ca, cb = (16, 44, 82), (9, 22, 44)
    for y in range(img.size[1]):
        t = min(1, max(0, (y - sc(y0)) / sc(Lr)))
        idr.line([(0, y), (img.size[0], y)], fill=tuple(int(ca[i] + (cb[i] - ca[i]) * t) for i in range(3)))
    glow = Image.new("L", img.size, 0)
    ImageDraw.Draw(glow).ellipse([P((cx - 420, y0 + 200)), P((cx + 420, y0 + 800))], fill=110)
    glow = glow.filter(ImageFilter.GaussianBlur(sc(120)))
    ice.paste(Image.new("RGB", img.size, (70, 125, 200)), (0, 0), glow)
    sd = ImageDraw.Draw(ice, "RGBA")
    random.seed(11)
    for _ in range(90):
        ax, ay = random.uniform(x0, x1), random.uniform(y0, ybot)
        bx, by = ax + random.uniform(-380, 380), ay + random.uniform(-260, 260)
        mx, my = (ax + bx) / 2 + random.uniform(-80, 80), (ay + by) / 2 + random.uniform(-80, 80)
        pts = [((1-t)**2*ax + 2*(1-t)*t*mx + t*t*bx, (1-t)**2*ay + 2*(1-t)*t*my + t*t*by) for t in [i/24 for i in range(25)]]
        sd.line([P(p) for p in pts], fill=(255, 255, 255, random.randint(8, 22)), width=sc(1.5))
    img.paste(ice, (0, 0), mask)
    d = ImageDraw.Draw(img, "RGBA")
    gy = y0 + 11 * k; by = y0 + 75 * k
    # trapezoid
    for sx in (-1, 1):
        d.line([P((cx + sx * 14 * k, gy)), P((cx + sx * 11 * k, y0 + 1))], fill=RED + (200,), width=sc(4))
    # goal line + crease
    d.line([P((x0 + 6, gy)), P((x1 - 6, gy))], fill=RED + (235,), width=sc(5))
    r = 6 * k
    d.pieslice([P((cx - r, gy - r)), P((cx + r, gy + r))], 0, 180, fill=(63, 130, 255, 70))
    d.arc([P((cx - r, gy - r)), P((cx + r, gy + r))], 0, 180, fill=RED + (240,), width=sc(4))
    d.rectangle([P((cx - 3 * k, gy - 4 * k)), P((cx + 3 * k, gy))], fill=(210, 220, 240, 40), outline=(235, 240, 250, 255), width=sc(3))
    # faceoff circles
    fy = gy + 20 * k
    for sx in (-1, 1):
        fx = cx + sx * 22 * k
        rr = 15 * k
        d.ellipse([P((fx - rr, fy - rr)), P((fx + rr, fy + rr))], outline=RED + (225,), width=sc(4))
        d.ellipse([P((fx - 1 * k, fy - 1 * k)), P((fx + 1 * k, fy + 1 * k))], fill=RED + (240,))
        for sy in (-1, 1):
            for sxx in (-1, 1):
                hx = fx + sxx * 2 * k
                hy0 = fy + sy * rr
                d.line([P((hx, hy0)), P((hx, hy0 + sy * 2 * k))], fill=RED + (225,), width=sc(4))
    # blue line, neutral dots, centre line + circle
    d.line([P((x0 + 6, by)), P((x1 - 6, by))], fill=(45, 107, 255, 255), width=sc(14))
    for sx in (-1, 1):
        d.ellipse([P((cx + sx * 22 * k - 11, by + 5 * k - 11)), P((cx + sx * 22 * k + 11, by + 5 * k + 11))], fill=RED + (230,))
    yc = y0 + 100 * k
    d.arc([P((cx - 15 * k, yc - 15 * k)), P((cx + 15 * k, yc + 15 * k))], 180, 360, fill=(45, 107, 255, 220), width=sc(4))
    d.line([P((x0 + 6, yc)), P((x1 - 6, yc))], fill=RED + (240,), width=sc(8))
    # boards
    d.rounded_rectangle([P((x0, y0)), P((x1, ybot + 400))], radius=sc(rad), corners=(True, True, False, False),
                        outline=(201, 214, 234, 255), width=sc(9))
    d.rounded_rectangle([P((x0 + 9, y0 + 9)), P((x1 - 9, ybot + 400))], radius=sc(rad - 9), corners=(True, True, False, False),
                        outline=(120, 140, 175, 120), width=sc(3))
    return d

def poly_ellipse(c, a, b, perp, face):
    pts = []
    for i in range(28):
        t = 2 * math.pi * i / 28
        pts.append((c[0] + a * math.cos(t) * perp[0] + b * math.sin(t) * face[0],
                    c[1] + a * math.cos(t) * perp[1] + b * math.sin(t) * face[1]))
    return pts

def player(d, c, ang, team, r=15):
    th = math.radians(ang)
    face = (math.cos(th), math.sin(th)); perp = (-face[1], face[0])
    fill = (45, 107, 255, 255) if team == "blue" else (232, 238, 248, 255)
    dark = (120, 138, 170, 255) if team == "white" else (14, 40, 120, 255)
    sh = [P((x + 3, y + 5)) for x, y in poly_ellipse(c, r * 1.35, r * 0.8, perp, face)]
    d.polygon(sh, fill=(0, 0, 0, 100))
    hand = (c[0] + face[0] * r * 0.9 + perp[0] * r * 1.1, c[1] + face[1] * r * 0.9 + perp[1] * r * 1.1)
    tip = (hand[0] + face[0] * r * 2.1, hand[1] + face[1] * r * 2.1)
    d.line([P(hand), P(tip)], fill=(215, 225, 240, 255), width=sc(2.6))
    d.line([P(tip), P((tip[0] + perp[0] * r * 0.55, tip[1] + perp[1] * r * 0.55))], fill=(215, 225, 240, 255), width=sc(2.6))
    d.polygon([P(p) for p in poly_ellipse(c, r * 1.35, r * 0.8, perp, face)], fill=fill, outline=(255, 255, 255, 220))
    hc = (c[0] + face[0] * r * 0.1, c[1] + face[1] * r * 0.1)
    d.ellipse([P((hc[0] - r * 0.42, hc[1] - r * 0.42)), P((hc[0] + r * 0.42, hc[1] + r * 0.42))], fill=dark)

def puck_at(d, c, ang, r=15):
    th = math.radians(ang)
    p = (c[0] + math.cos(th) * r * 3.6 + (-math.sin(th)) * r * 1.1, c[1] + math.sin(th) * r * 3.6 + math.cos(th) * r * 1.1)
    d.ellipse([P((p[0] - 6, p[1] - 6)), P((p[0] + 6, p[1] + 6))], fill=(0, 0, 0, 255), outline=(255, 255, 255, 255), width=sc(2))

def arrow(d, pts, color, w=6, head=24, dash=True):
    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    ang = math.atan2(y2 - y1, x2 - x1)
    end = (x2 - head * 0.8 * math.cos(ang), y2 - head * 0.8 * math.sin(ang))
    seq = pts[:-1] + [end]
    for a, b in zip(seq[:-1], seq[1:]):
        L = math.dist(a, b); aa = math.atan2(b[1] - a[1], b[0] - a[0]); t = 0
        while t < L:
            t2 = min(t + 16, L)
            d.line([P((a[0] + t * math.cos(aa), a[1] + t * math.sin(aa))), P((a[0] + t2 * math.cos(aa), a[1] + t2 * math.sin(aa)))], fill=color, width=sc(w))
            t += 26 if dash else 16
    hl, hw = head, head * 0.55
    l = (x2 - hl * math.cos(ang) + hw * math.sin(ang), y2 - hl * math.sin(ang) - hw * math.cos(ang))
    r = (x2 - hl * math.cos(ang) - hw * math.sin(ang), y2 - hl * math.sin(ang) + hw * math.cos(ang))
    d.polygon([P((x2, y2)), P(l), P(r)], fill=color)

def ring(img, c, R=48):
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).ellipse([P((c[0] - R, c[1] - R)), P((c[0] + R, c[1] + R))], outline=255, width=sc(12))
    m = m.filter(ImageFilter.GaussianBlur(sc(10)))
    img.paste(Image.new("RGB", img.size, (63, 130, 255)), (0, 0), m)
    d = ImageDraw.Draw(img, "RGBA")
    d.ellipse([P((c[0] - R, c[1] - R)), P((c[0] + R, c[1] + R))], outline=BLUE2, width=sc(4))
    return d

def tag(d, xy, s, target=None):
    f = font(FM, 24)
    w = tw(s, f) / S + 36; h = 46
    x, y = xy
    if target:
        cxm = x + w / 2
        d.line([P((cxm, y + h / 2)), P(target)], fill=(63, 130, 255, 230), width=sc(3))
    d.rounded_rectangle([P((x, y)), P((x + w, y + h))], radius=sc(10), fill=(5, 7, 13, 235), outline=BLUE, width=sc(3))
    text(d, (x + w / 2, y + h / 2 + 1), s, f, WHITE, "mm")

def save(img, name):
    img.resize((W, H), Image.LANCZOS).save(os.path.join(OUT, name), "PNG")

# ===================== SLIDE 1 =====================
img, d = new_canvas()
d = rink(img, 125)
player(d, (540, 290), 90, "white", 18)
player(d, (610, 540), 80, "white"); player(d, (420, 505), 95, "white")
player(d, (780, 630), 250, "blue"); puck_at(d, (780, 590), 250)
player(d, (300, 720), 285, "blue"); player(d, (560, 730), 265, "blue")
arrow(d, [(768, 560), (700, 460), (610, 360), (560, 275)], BLUE2, 5)
d = ring(img, (300, 720), 52)
player(d, (300, 720), 285, "blue")
tag(d, (110, 600), "ГДЕ ОН В ЭТОТ МОМЕНТ?", (300, 670))
ramp(img, 745, 840, 0, 255)
d = ImageDraw.Draw(img, "RGBA")
brand(d)
f1, s1 = fit(["НЕ ИГРАЕТ?"], FH, 900, 140)
text(d, (80, 790), "ВАШ СЫН", f1, WHITE)
text(d, (80, 790 + int(s1 * 1.0)), "НЕ ИГРАЕТ?", f1, WHITE)
y = 790 + int(s1 * 2.0) + 14
f2, s2 = fit(["ПРИЧИНА НЕ ВСЕГДА ТАМ,", "ГДЕ ВЫ ЕЁ ИЩЕТЕ"], FH, 900, 54)
text(d, (80, y), "ПРИЧИНА НЕ ВСЕГДА ТАМ,", f2, BLUE2)
text(d, (80, y + int(s2 * 1.1)), "ГДЕ ВЫ ЕЁ ИЩЕТЕ", f2, BLUE2)
d.line([P((80, 1232)), P((200, 1232))], fill=BLUE, width=sc(6))
text(d, (80, 1250), "Листайте — покажу, что видно в игре", font(FBB, 30), WHITE)
text(d, (1000, 1240), "→", font(FH, 46), BLUE2, "ra")
text(d, (1000, 1304), "условная схема", font(FM, 22), GREY, "ra")
save(img, "01_cover.png")

# ===================== SLIDE 2 =====================
img, d = new_canvas()
d = rink(img, 305)
player(d, (540, 478), 90, "white", 18)
player(d, (420, 625), 90, "white"); player(d, (650, 610), 95, "white")
player(d, (700, 835), 30, "white")
player(d, (790, 880), 250, "blue"); puck_at(d, (790, 880), 250)
player(d, (330, 800), 285, "blue"); player(d, (520, 935), 270, "blue")
d = ring(img, (330, 800), 50); player(d, (330, 800), 285, "blue")
d = ring(img, (790, 880), 50); player(d, (790, 880), 250, "blue"); puck_at(d, (790, 880), 250)
d = ring(img, (520, 935), 50); player(d, (520, 935), 270, "blue")
tag(d, (130, 690), "БЕЗ ШАЙБЫ", (330, 750))
tag(d, (700, 970), "ПОД ДАВЛЕНИЕМ", (790, 930))
tag(d, (230, 1000), "ПОДДЕРЖКА", (480, 960))
ramp(img, 1050, 1120, 0, 255)
d = ImageDraw.Draw(img, "RGBA")
brand(d)
fa, sa = fit(["ВСЕ СМОТРЯТ НА ШАЙБУ.", "РЕШАЕТ ТО, ЧТО ВНЕ КАДРА."], FH, 920, 80)
text(d, (80, 135), "ВСЕ СМОТРЯТ НА ШАЙБУ.", fa, WHITE)
text(d, (80, 135 + int(sa * 1.1)), "РЕШАЕТ ТО, ЧТО ВНЕ КАДРА.", fa, BLUE2)
para(d, 80, 1140, "На решения тренера влияют разные факторы: позиция без шайбы, дисциплина смен, выбор под давлением и роль в звене.",
     font(FBB, 31), WHITE, 920, 43)
text(d, (1000, 1296), "условная схема", font(FM, 22), GREY, "ra")
save(img, "02_situation.png")

# ===================== SLIDE 3 =====================
img, d = new_canvas()
d = rink(img, 300)
player(d, (540, 470), 90, "white", 18)
player(d, (420, 545), 90, "white"); player(d, (660, 530), 95, "white")
player(d, (800, 600), 250, "blue"); puck_at(d, (800, 600), 250)
player(d, (330, 610), 285, "blue"); player(d, (560, 640), 265, "blue")
d = ring(img, (330, 610), 48); player(d, (330, 610), 285, "blue")
ramp(img, 655, 735, 0, 255)
d = ImageDraw.Draw(img, "RGBA")
brand(d)
fa, sa = fit(["ЧТО МЫ СМОТРИМ НА ВИДЕО"], FH, 920, 84)
text(d, (80, 135), "ЧТО МЫ СМОТРИМ НА ВИДЕО", fa, WHITE)
text(d, (80, 135 + int(sa * 1.3)), "Это возможные факторы, а не приговор игроку", font(FB, 31), GREY)
cards = [("Игра без шайбы", "где игрок находится, пока шайба у партнёра"),
         ("Решения под давлением", "что он выбирает за секунду до потери"),
         ("Роль в звене", "чем он полезен команде в своих эпизодах")]
y = 745
for i, (t, s) in enumerate(cards, 1):
    d.rounded_rectangle([P((80, y)), P((1000, y + 138))], radius=sc(16), fill=(11, 31, 58, 215), outline=BLUE, width=sc(3))
    text(d, (118, y + 69), str(i), font(FH, 70), BLUE2, "lm")
    text(d, (190, y + 26), t, font(FBB, 37), WHITE)
    text(d, (190, y + 80), s, font(FB, 29), GREY)
    y += 158
save(img, "03_analysis.png")

# ===================== SLIDE 4 =====================
img, d = new_canvas()
d = rink(img, -220)
player(d, (520, 595), 90, "white"); player(d, (690, 565), 95, "white")
player(d, (560, 710), 270, "blue"); puck_at(d, (560, 710), 270)
player(d, (330, 750), 280, "blue"); player(d, (810, 690), 265, "blue")
d = ring(img, (560, 710), 50); player(d, (560, 710), 270, "blue"); puck_at(d, (560, 710), 270)
arrow(d, [(560, 640), (550, 540), (520, 450)], BLUE2, 5)
ramp_top(img, 380, 520, 255, 0)
ramp(img, 840, 940, 0, 255)
d = ImageDraw.Draw(img, "RGBA")
brand(d)
fa, sa = fit(["ХОТИТЕ ПОНЯТЬ,", "ЧТО ВИДНО В ИГРЕ", "ВАШЕГО СЫНА?"], FH, 920, 100)
text(d, (80, 135), "ХОТИТЕ ПОНЯТЬ,", fa, WHITE)
text(d, (80, 135 + int(sa * 1.05)), "ЧТО ВИДНО В ИГРЕ", fa, WHITE)
text(d, (80, 135 + int(sa * 2.1)), "ВАШЕГО СЫНА?", fa, BLUE2)
steps = ["Отправьте короткий отрезок игры", "Напишите в директ слово «СМЕНА»", "Обсудим, что видно в его эпизодах"]
y = 930
for i, s in enumerate(steps, 1):
    d.ellipse([P((80, y)), P((120, y + 40))], fill=BLUE)
    text(d, (100, y + 21), str(i), font(FH, 26), WHITE, "mm")
    text(d, (140, y + 3), s, font(FBB, 33), WHITE)
    y += 56
d.rounded_rectangle([P((80, 1115)), P((1000, 1195))], radius=sc(40), fill=BLUE)
text(d, (540, 1156), "НАПИШИТЕ «СМЕНА» В ДИРЕКТ", font(FH, 40), WHITE, "mm")
text(d, (540, 1226), "Разбор помогает точнее понять игру, но не гарантирует место в составе", font(FB, 22), GREY, "ma")
text(d, (540, 1286), "@alex__analytics", font(FM, 26), WHITE, "ma")
save(img, "04_cta.png")
print("done")
