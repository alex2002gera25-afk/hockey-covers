from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os, random

S = 2
W, H = 1080, 1350
OUT = "/mnt/user-data/outputs/alex_analytics_carousel_06"
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



def badge(d, c, n, r=19):
    d.ellipse([P((c[0]-r, c[1]-r)), P((c[0]+r, c[1]+r))], fill=BLUE, outline=WHITE, width=sc(2))
    text(d, c, str(n), font(FH, int(r * 1.35)), WHITE, "mm")

K = 9.8
def F(x, y, k=K, y0=262):
    return (540 + x * k, y0 + 11 * k + y * k)

def scene(img, y0, k, with_badges=False, cover=False):
    d = rink(img, y0, k)
    f = lambda x, y: F(x, y, k, y0)
    r = 14 if k < 10.3 else 15
    # opponents (white) facing down toward our players / in zone
    opp = [((22, 16.4), 90), ((37, 13), 110), ((7, 13), 70), ((31, 52), 100), ((-14, 52), 80)]
    for (x, y), a in opp:
        player(d, f(x, y), a, "white", r)
    # our team (blue)
    ours = [((22, 23.8), 270), ((37, 27), 255), ((7, 27), 285), ((30, 57), 235), ((-14, 57), 300)]
    for (x, y), a in ours:
        player(d, f(x, y), a, "blue", r)
    puck_at(d, f(22, 19.6), 270, 6)
    return d, f

# ================= 1: cover =================
img, d = new_canvas()
d, f = scene(img, 95, 10.0)
arrow(d, [f(22, 24), f(27, 40), f(30, 53)], BLUE2, 6, head=26)
arrow(d, [f(30, 56), f(15, 30), f(3, 3)], "#FFFFFF", 6, head=26, dash=False)
d = ring(img, f(30, 57), 40)
player(d, f(30, 57), 235, "blue", 15)
ramp(img, 830, 880, 0, 255)
d = ImageDraw.Draw(img, "RGBA")
brand(d)
f1, s1 = fit(["ВЫИГРАЛИ ВБРАСЫВАНИЕ.", "ЧТО ДАЛЬШЕ?"], FH, 920, 112)
y = 905
text(d, (80, y), "ВЫИГРАЛИ ВБРАСЫВАНИЕ.", f1, WHITE)
text(d, (80, y + int(s1 * 1.05)), "ЧТО ДАЛЬШЕ?", f1, BLUE2)
para(d, 80, y + int(s1 * 2.3), "Разбор стандарта в зоне атаки: что происходит в первые секунды после вбрасывания.",
     font(FB, 30), GREY, 920, 40)
d.line([P((80, 1252)), P((200, 1252))], fill=BLUE, width=sc(6))
text(d, (80, 1268), "Листай — разберём схему розыгрыша", font(FBB, 28), WHITE)
text(d, (1000, 1262), "→", font(FH, 44), BLUE2, "ra")
save(img, "01_cover.png")

# ================= 2: scheme =================
img, d = new_canvas()
brand(d)
text(d, (80, 120), "СХЕМА РОЗЫГРЫША", font(FH, 66), WHITE)
text(d, (80, 200), "Условная схема: вбрасывание в правом круге. Синие атакуют.", font(FB, 26), GREY)
d, f = scene(img, 262, K)
# 1: puck back to D1
arrow(d, [f(22, 25), f(26, 42), f(29, 54)], BLUE2, 6, head=24)
# 2: strong-side winger to the net front
arrow(d, [f(36, 24), f(22, 12), f(5, 6)], BLUE2, 6, head=24)
# 3: weak-side winger to the weak-side slot
arrow(d, [f(7, 24), f(-2, 16), f(-8, 9)], BLUE2, 6, head=24)
# 5: shot
arrow(d, [f(27, 55), f(15, 30), f(4, 2)], "#FFFFFF", 6, head=24, dash=False)
d = ring(img, f(-14, 57), 38)
player(d, f(-14, 57), 300, "blue", 14)
for n, p in ((1, f(27, 38)), (2, f(24, 17)), (3, f(-5, 17)), (4, f(-24, 62)), (5, f(13, 40))):
    badge(d, p, n, 19)
ramp(img, 985, 1030, 0, 255)
d = ImageDraw.Draw(img, "RGBA")
rows = ["Вбрасывающий выигрывает шайбу назад, на защитника",
        "Крайний нападающий идёт на пятак и закрывает обзор вратарю",
        "Дальний нападающий готов к добиванию",
        "Второй защитник держит синюю линию: это страховка",
        "Бросок по воротам, пока соперник не перестроился"]
y = 1040
for i, s in enumerate(rows, 1):
    badge(d, (100, y + 21), i, 17)
    text(d, (134, y + 4), s, font(FBB, 26), WHITE)
    y += 50
save(img, "02_scheme.png")

# ================= 3: key details =================
img, d = new_canvas()
c1, c2 = hexrgb_pair = ((5, 7, 13), (11, 31, 58))
g = ImageDraw.Draw(img)
for yy in range(sc(H)):
    t = (yy / sc(H)) ** 2.0 * 0.9
    g.line([(0, yy), (sc(W), yy)], fill=tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3)))
d = ImageDraw.Draw(img, "RGBA")
brand(d)
fa, sa = fit(["ТРИ ДЕТАЛИ, КОТОРЫЕ", "РЕШАЮТ РОЗЫГРЫШ"], FH, 920, 82)
text(d, (80, 140), "ТРИ ДЕТАЛИ, КОТОРЫЕ", fa, WHITE)
text(d, (80, 140 + int(sa * 1.08)), "РЕШАЮТ РОЗЫГРЫШ", fa, BLUE2)
items = [("ДО ВБРАСЫВАНИЯ", "Каждый знает свою задачу и запасной вариант на случай, если шайбу проиграли."),
         ("ПЕРВЫЙ ПАС", "Шайба быстро доходит до бросающего, пока соперник не занял позицию."),
         ("СТРАХОВКА", "Один игрок остаётся на синей линии, иначе потеря шайбы превращается в контратаку.")]
y = 440
for i, (t, s) in enumerate(items, 1):
    h = 235 if i == 3 else 205
    d.rounded_rectangle([P((80, y)), P((1000, y + h))], radius=sc(18), fill=(8, 18, 40, 200), outline=BLUE, width=sc(3))
    d.rounded_rectangle([P((112, y + 30)), P((178, y + 96))], radius=sc(14), fill=BLUE)
    text(d, (145, y + 64), str(i), font(FH, 46), WHITE, "mm")
    text(d, (206, y + 30), t, font(FH, 44), WHITE)
    para(d, 206, y + 92, s, font(FB, 30), GREY, 740, 40)
    y += 235
para(d, 80, 1170, "Схема подбирается под игроков, сторону вбрасывания и соперника. Это пример, а не готовый рецепт.",
     font(FBB, 28), WHITE, 920, 38)
save(img, "03_details.png")

# ================= 4: CTA =================
img, d = new_canvas()
d, f4 = scene(img, -60, 9.8)
arrow(d, [f4(22, 26), f4(26, 42), f4(29, 54)], BLUE2, 6, head=24)
d = ring(img, f4(22, 23.8), 36)
player(d, f4(22, 23.8), 270, "blue", 14)
ramp_top(img, 90, 190, 255, 0)
ramp(img, 700, 790, 0, 255)
d = ImageDraw.Draw(img, "RGBA")
brand(d)
fa, sa = fit(["КАК ВЫ РАЗЫГРЫВАЕТЕ", "СТАНДАРТЫ?"], FH, 920, 100)
text(d, (80, 800), "КАК ВЫ РАЗЫГРЫВАЕТЕ", fa, WHITE)
text(d, (80, 800 + int(sa * 1.04)), "СТАНДАРТЫ?", fa, BLUE2)
para(d, 80, 800 + int(sa * 2.3), "Отправь короткий отрезок с вбрасыванием в зоне атаки: посмотрим, кто занял позицию, куда пошла шайба и кто страховал.",
     font(FB, 29), GREY, 920, 40)
d.rounded_rectangle([P((80, 1120)), P((1000, 1190))], radius=sc(35), fill=BLUE)
text(d, (540, 1155), "НАПИШИ «СТАНДАРТ» В ДИРЕКТ", font(FH, 38), WHITE, "mm")
text(d, (540, 1222), "Разбор помогает точнее понять игру, но не гарантирует результат", font(FB, 21), GREY, "ma")
text(d, (540, 1290), "@alex__analytics", font(FM, 26), WHITE, "ma")
save(img, "04_cta.png")
print("done")
