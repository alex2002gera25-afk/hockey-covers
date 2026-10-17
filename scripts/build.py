from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os

S = 2
W, H = 1080, 1350
OUT = "/mnt/user-data/outputs/alex_analytics_carousel_01"

BG = "#05070D"; BG2 = "#0B0B0F"; NAVY = "#0B1F3A"
BLUE = "#2D6BFF"; BLUE2 = "#3F82FF"
WHITE = "#FFFFFF"; GREY = "#9AA3B2"; GREYBLUE = "#8FA3BF"

FH = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"
FB = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FBB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FM = "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"

def font(p, size): return ImageFont.truetype(p, int(size * S))
def sc(v): return int(round(v * S))
def P(pt): return (sc(pt[0]), sc(pt[1]))

def hexrgb(h): h = h.lstrip("#"); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def new_canvas():
    img = Image.new("RGB", (sc(W), sc(H)), BG)
    px = Image.new("RGB", (1, sc(H)))
    c1, c2 = hexrgb(BG), hexrgb(NAVY)
    grad = Image.new("RGB", (sc(W), sc(H)))
    gd = ImageDraw.Draw(grad)
    for y in range(sc(H)):
        t = (y / sc(H)) ** 2.2 * 0.85
        gd.line([(0, y), (sc(W), y)], fill=tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3)))
    img = grad
    d = ImageDraw.Draw(img, "RGBA")
    for x in range(0, W + 1, 90):
        d.line([P((x, 0)), P((x, H))], fill=(45, 107, 255, 14), width=1)
    for y in range(0, H + 1, 90):
        d.line([P((0, y)), P((W, y))], fill=(45, 107, 255, 14), width=1)
    return img, d

def tw(text, f): 
    return f.getlength(text)

def wrap(text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(t, f) <= sc(maxw): cur = t
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def text(d, xy, s, f, fill, anchor="la"):
    d.text(P(xy), s, font=f, fill=fill, anchor=anchor)

def para(d, x, y, s, f, fill, maxw, lh):
    for ln in wrap(s, f, maxw):
        d.text(P((x, y)), ln, font=f, fill=fill, anchor="la"); y += lh
    return y

def fit(s, path, maxw, start, minsize=40):
    size = start
    while size > minsize and tw(s, font(path, size)) > sc(maxw): size -= 2
    return font(path, size), size

def frame(d, n, total=4, note=None):
    d.rectangle([P((80, 72)), P((98, 90))], fill=BLUE)
    text(d, (112, 66), "ALEX ANALYTICS", font(FM, 26), WHITE)
    text(d, (1000, 66), f"{n:02d} / {total:02d}", font(FM, 26), GREYBLUE, "ra")
    d.line([P((80, 112)), P((1000, 112))], fill=(143, 163, 191, 70), width=2)
    text(d, (80, 1288), "@alex__analytics", font(FM, 24), GREY)
    if note: text(d, (1000, 1288), note, font(FM, 24), GREY, "ra")

def arrow(d, pts, color, w=6, dash=False, head=24):
    # polyline with arrowhead on last segment
    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    ang = math.atan2(y2 - y1, x2 - x1)
    end = (x2 - head * 0.8 * math.cos(ang), y2 - head * 0.8 * math.sin(ang))
    seq = pts[:-1] + [end]
    if not dash:
        d.line([P(p) for p in seq], fill=color, width=sc(w), joint="curve")
    else:
        for a, b in zip(seq[:-1], seq[1:]):
            L = math.dist(a, b); a_ = math.atan2(b[1]-a[1], b[0]-a[0]); t = 0
            while t < L:
                t2 = min(t + 16, L)
                d.line([P((a[0]+t*math.cos(a_), a[1]+t*math.sin(a_))), P((a[0]+t2*math.cos(a_), a[1]+t2*math.sin(a_)))], fill=color, width=sc(w))
                t += 26
    hl = head; hw = head * 0.55
    tip = (x2, y2)
    l = (x2 - hl * math.cos(ang) + hw * math.sin(ang), y2 - hl * math.sin(ang) - hw * math.cos(ang))
    r = (x2 - hl * math.cos(ang) - hw * math.sin(ang), y2 - hl * math.sin(ang) + hw * math.cos(ang))
    d.polygon([P(tip), P(l), P(r)], fill=color)

def zone(d, x0, y0, x1, y1):
    Wd, Hd = x1 - x0, y1 - y0
    d.rounded_rectangle([P((x0, y0)), P((x1, y1))], radius=sc(Wd * 0.14), corners=(True, True, False, False),
                        fill=(8, 13, 24, 255), outline=hexrgb(GREYBLUE), width=sc(4))
    cx = (x0 + x1) / 2
    gy = y0 + Hd * 0.12
    by = y0 + Hd * 0.88
    d.line([P((x0 + 3, gy)), P((x1 - 3, gy))], fill=(70, 86, 120, 255), width=sc(3))
    nw = Wd * 0.085
    d.rectangle([P((cx - nw, gy - Hd * 0.05)), P((cx + nw, gy))], outline=WHITE, width=sc(3))
    r = Wd * 0.075
    d.arc([P((cx - r, gy - r)), P((cx + r, gy + r))], 0, 180, fill=BLUE, width=sc(3))
    fy = gy + (by - gy) * 0.42
    for fx in (x0 + Wd * 0.27, x0 + Wd * 0.73):
        rr = Wd * 0.1
        d.ellipse([P((fx - rr, fy - rr)), P((fx + rr, fy + rr))], outline=(52, 68, 100, 255), width=sc(3))
        d.ellipse([P((fx - 5, fy - 5)), P((fx + 5, fy + 5))], fill=(52, 68, 100, 255))
    d.line([P((x0 + 3, by)), P((x1 - 3, by))], fill=BLUE, width=sc(9))
    return dict(cx=cx, gy=gy, by=by, net=(cx, gy - Hd * 0.025))

def wedge(d, c, ang_deg, color, length=62, spread=42):
    a = math.radians(ang_deg)
    p1 = (c[0] + length * math.cos(a - math.radians(spread)), c[1] + length * math.sin(a - math.radians(spread)))
    p2 = (c[0] + length * math.cos(a + math.radians(spread)), c[1] + length * math.sin(a + math.radians(spread)))
    d.polygon([P(c), P(p1), P(p2)], fill=color)

def player(d, c, label, kind, rr=26):
    if kind == "att":
        d.ellipse([P((c[0]-rr, c[1]-rr)), P((c[0]+rr, c[1]+rr))], fill=BLUE, outline=WHITE, width=sc(3))
        col = WHITE
    else:
        d.ellipse([P((c[0]-rr, c[1]-rr)), P((c[0]+rr, c[1]+rr))], fill=WHITE, outline=BLUE2, width=sc(3))
        col = BG
    text(d, c, label, font(FH, 30), col, "mm")

def puck(d, c):
    d.ellipse([P((c[0]-9, c[1]-9)), P((c[0]+9, c[1]+9))], fill="#000000", outline=WHITE, width=sc(2))

def badge(d, c, n, r=19):
    d.ellipse([P((c[0]-r, c[1]-r)), P((c[0]+r, c[1]+r))], fill=BLUE)
    text(d, c, str(n), font(FH, 26), WHITE, "mm")

def save(img, name):
    img = img.resize((W, H), Image.LANCZOS)
    img.save(os.path.join(OUT, name), "PNG")

# ---------------- SLIDE 1 ----------------
img, d = new_canvas()
frame(d, 1)
z = zone(d, 110, 150, 970, 690)
A = (800, 625); D = (640, 450)
arrow(d, [A, (790, 560), (700, 420), (560, z['gy'] + 10)], BLUE2, 6, dash=True)
wedge(d, D, 60, (255, 255, 255, 60))
player(d, D, "Д", "def"); player(d, A, "Н", "att"); puck(d, (A[0] - 34, A[1] - 10))
# fade into background
fade = Image.new("RGBA", (sc(W), sc(160)), (0, 0, 0, 0))
fd = ImageDraw.Draw(fade)
c1, c2 = hexrgb(BG), hexrgb(NAVY)
for yy in range(sc(160)):
    ay = sc(540) + yy
    t = (ay / sc(H)) ** 2.2 * 0.85
    col = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
    a = int(255 * min(1, (yy / sc(160)) ** 1.3))
    fd.line([(0, yy), (sc(W), yy)], fill=col + (a,))
img.paste(fade, (0, sc(540)), fade)
d = ImageDraw.Draw(img, "RGBA")
f1, s1 = fit("ПРОИГРАЛ ЭПИЗОД", FH, 920, 118)
y = 700
text(d, (80, y), "ЗАЩИТНИК", f1, WHITE); y += int(s1 * 1.0)
text(d, (80, y), "ПРОИГРАЛ ЭПИЗОД", f1, WHITE); y += int(s1 * 1.0)
text(d, (80, y), "ДО БРОСКА.", f1, BLUE2); y += int(s1 * 1.12)
f2, _ = fit("ГДЕ НАЧАЛАСЬ ОШИБКА?", FH, 920, 64)
text(d, (80, y), "ГДЕ НАЧАЛАСЬ ОШИБКА?", f2, WHITE); y += 100
text(d, (80, y), "Дистанция, угол и положение корпуса", font(FB, 36), GREY)
d.line([P((80, 1190)), P((200, 1190))], fill=BLUE, width=sc(6))
text(d, (80, 1208), "Листай — разберём эпизод", font(FBB, 30), WHITE)
text(d, (1000, 1200), "→", font(FH, 44), BLUE2, "ra")
text(d, (80, 1288), "@alex__analytics", font(FM, 24), GREY)
text(d, (1000, 1288), "условный эпизод", font(FM, 24), GREY, "ra")
save(img, "01_cover.png")

# ---------------- SLIDE 2 ----------------
img, d = new_canvas()
frame(d, 2, note="условный эпизод")
fh, _ = fit("ЧТО ПРОИСХОДИТ НА ЛЬДУ", FH, 920, 86)
text(d, (80, 135), "ЧТО ПРОИСХОДИТ НА ЛЬДУ", fh, WHITE)
para(d, 80, 232, "Нападающий входит в зону с шайбой по флангу. Защитник один против него, партнёры ещё возвращаются.",
     font(FB, 33), GREY, 920, 44)
z = zone(d, 110, 395, 970, 880)
A = (810, 790); Dp = (640, 610)
# angle lines
d.line([P(Dp), P(z['net'])], fill=(63, 130, 255, 150), width=sc(3))
d.line([P(Dp), P(A)], fill=(63, 130, 255, 150), width=sc(3))
arrow(d, [A, (815, 640), (790, 520)], BLUE2, 6, dash=True)
wedge(d, Dp, 50, (255, 255, 255, 70))
player(d, Dp, "Д", "def"); player(d, A, "Н", "att"); puck(d, (A[0] - 34, A[1] - 10))
badge(d, (742, 700), 1); text(d, (770, 688), "ДИСТАНЦИЯ", font(FM, 24), WHITE)
badge(d, (470, 540), 2); text(d, (498, 528), "УГОЛ", font(FM, 24), WHITE)
badge(d, (548, 672), 3); text(d, (576, 660), "КОРПУС", font(FM, 24), WHITE)
rows = [("Дистанция", "от неё зависит время нападающего на решение"),
        ("Угол", "он определяет, какой путь к воротам открыт"),
        ("Корпус", "положение плеч задаёт, куда защитник ведёт игрока")]
y = 915
for i, (t, s) in enumerate(rows, 1):
    badge(d, (110, y + 30), i, 22)
    text(d, (152, y), t, font(FBB, 36), WHITE)
    text(d, (152, y + 46), s, font(FB, 29), GREY)
    y += 112
save(img, "02_situation.png")

# ---------------- SLIDE 3 ----------------
img, d = new_canvas()
frame(d, 3, note="условный эпизод")
fh, _ = fit("ГДЕ ПРОИГРАН ЭПИЗОД", FH, 920, 86)
text(d, (80, 135), "ГДЕ ПРОИГРАН ЭПИЗОД", fh, WHITE)
text(d, (80, 232), "Один и тот же вход в зону — два разных решения", font(FB, 33), GREY)
# left panel
x0, y0, x1, y1 = 90, 340, 520, 790
text(d, (x0, 298), "А. СДАЛ ДИСТАНЦИЮ", font(FBB, 30), GREYBLUE)
zl = zone(d, x0, y0, x1, y1)
A = (x0 + 335, 735 - 40); D1 = (x0 + 195, 520)
arrow(d, [A, (x0 + 270, 600), (x0 + 215, 470), (zl['cx'], zl['gy'] + 10)], BLUE2, 5, dash=True, head=20)
wedge(d, D1, 90, (255, 255, 255, 70), 56, 44)
player(d, D1, "Д", "def", 22); player(d, A, "Н", "att", 22); puck(d, (A[0] - 29, A[1] - 8))
# right panel
x0b, x1b = 560, 990
text(d, (x0b, 298), "Б. ДЕРЖИТ КОНТРОЛЬ", font(FBB, 30), BLUE2)
zr = zone(d, x0b, y0, x1b, y1)
A2 = (x0b + 335, 735 - 40); D2 = (x0b + 285, 635)
arrow(d, [A2, (x0b + 392, 600), (x0b + 392, 500), (zr['cx'] + 20, zr['gy'] + 10)], BLUE2, 5, dash=True, head=20)
wedge(d, D2, 20, (63, 130, 255, 130), 58, 44)
player(d, D2, "Д", "def", 22); player(d, A2, "Н", "att", 22); puck(d, (A2[0] - 29, A2[1] - 8))
# bullets
def bullets(x, y, items, col):
    f = font(FB, 29)
    for it in items:
        d.rectangle([P((x, y + 11)), P((x + 12, y + 23))], fill=col)
        y = para(d, x + 28, y, it, f, WHITE, 400, 38) + 8
    return y
bullets(90, 820, ["Далеко от нападающего: у него время на выбор",
                  "Плечи прямо: обводка в любую сторону",
                  "Центр к воротам открыт"], GREYBLUE)
bullets(560, 820, ["Близко: в пределах досягаемости клюшки",
                   "Полуоборот ведёт игрока к борту",
                   "Центр закрыт, бросок с острого угла"], BLUE2)
d.rounded_rectangle([P((80, 1112)), P((1000, 1250))], radius=sc(14), outline=BLUE, width=sc(3), fill=(11, 31, 58, 150))
para(d, 110, 1130, "Главное — расстояние в момент входа. От ситуации зависят скорость нападающего и помощь партнёров.",
     font(FBB, 31), WHITE, 860, 42)
save(img, "03_analysis.png")

# ---------------- SLIDE 4 ----------------
img, d = new_canvas()
frame(d, 4)
fh, sh = fit("ЧТО ПРОВЕРИТЬ В СВОЕЙ СМЕНЕ", FH, 920, 80)
text(d, (80, 135), "ЧТО ПРОВЕРИТЬ", fh, WHITE)
text(d, (80, 135 + int(sh * 1.02)), "В СВОЕЙ СМЕНЕ", fh, BLUE2)
y = 135 + int(sh * 2.05) + 30
para(d, 80, y, "Поставь видео на паузу на входе в зону и ответь на четыре вопроса.", font(FB, 32), GREY, 920, 42)
rows = [("Расстояние", "Насколько близко защитник к нападающему?"),
        ("Корпус", "Куда повёрнуты плечи: к шайбе или к борту?"),
        ("Коридор", "Что закрыто: центр к воротам или фланг?"),
        ("Помощь", "Где партнёры и успевают ли подключиться?")]
y = 430
for i, (t, s) in enumerate(rows, 1):
    text(d, (80, y - 8), f"{i}", font(FH, 74), BLUE2)
    text(d, (150, y), t, font(FBB, 37), WHITE)
    text(d, (150, y + 48), s, font(FB, 30), GREY)
    d.line([P((150, y + 96)), P((1000, y + 96))], fill=(143, 163, 191, 40), width=2)
    y += 118
y = 925
para(d, 80, y, "Бросок — это последствие. Ошибка часто начинается раньше.", font(FH, 48), WHITE, 920, 58)
d.rounded_rectangle([P((80, 1070)), P((1000, 1250))], radius=sc(14), outline=BLUE, width=sc(3), fill=(11, 31, 58, 170))
para(d, 110, 1092, "Напиши в директ слово «ЗАЩИТА» и отправь короткий отрезок, если хочешь обсудить эпизод, где защитник потерял позицию.",
     font(FBB, 31), WHITE, 860, 42)
save(img, "04_cta.png")
print("done")
