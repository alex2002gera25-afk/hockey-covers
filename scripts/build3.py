from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random, os

S = 2
W, H = 1080, 1350
OUT = "/mnt/user-data/outputs/alex_analytics_carousel_03"
BG = (5, 7, 13)
BLUE = "#2D6BFF"; BLUE2 = "#3F82FF"; WHITE = "#FFFFFF"; GREY = "#9AA3B2"

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

def atmosphere(seed, glow_xy, beam=True):
    """Dark arena atmosphere: cold glow, soft bokeh lights, light haze, ice shimmer at the bottom."""
    random.seed(seed)
    img = Image.new("RGB", (sc(W), sc(H)), BG)
    # vertical base gradient toward deep navy
    g = ImageDraw.Draw(img)
    for y in range(sc(H)):
        t = (y / sc(H))
        c = (int(5 + 6 * t), int(7 + 20 * t), int(13 + 42 * t))
        g.line([(0, y), (sc(W), y)], fill=c)
    # main cold glow
    glow = Image.new("L", img.size, 0)
    gd = ImageDraw.Draw(glow)
    gx, gy = glow_xy
    gd.ellipse([P((gx - 420, gy - 300)), P((gx + 420, gy + 300))], fill=170)
    glow = glow.filter(ImageFilter.GaussianBlur(sc(170)))
    img.paste(Image.new("RGB", img.size, (45, 107, 255)), (0, 0), glow)
    # light beams from above
    if beam:
        bm = Image.new("L", img.size, 0)
        bd = ImageDraw.Draw(bm)
        for bx, w, a in ((gx - 260, 70, 60), (gx, 100, 80), (gx + 270, 60, 50)):
            bd.polygon([P((bx - 12, -20)), P((bx + 12, -20)), P((bx + w * 2.2, 900)), P((bx - w * 2.2, 900))], fill=a)
        bm = bm.filter(ImageFilter.GaussianBlur(sc(36)))
        img.paste(Image.new("RGB", img.size, (140, 180, 255)), (0, 0), bm)
    # bokeh
    bk = Image.new("RGBA", img.size, (0, 0, 0, 0))
    bd = ImageDraw.Draw(bk)
    for _ in range(26):
        x, y = random.uniform(0, W), random.uniform(0, H * 0.55)
        r = random.uniform(10, 46)
        a = random.randint(18, 60)
        col = random.choice([(120, 170, 255), (63, 130, 255), (200, 220, 255)])
        bd.ellipse([P((x - r, y - r)), P((x + r, y + r))], fill=col + (a,))
    bk = bk.filter(ImageFilter.GaussianBlur(sc(5)))
    img.paste(bk, (0, 0), bk)
    # ice shimmer lines near bottom
    sh = ImageDraw.Draw(img, "RGBA")
    for _ in range(70):
        x = random.uniform(-100, W + 100); y = random.uniform(H * 0.62, H)
        L = random.uniform(120, 520); dy = random.uniform(-40, 40)
        sh.line([P((x, y)), P((x + L, y + dy))], fill=(190, 215, 255, random.randint(6, 20)), width=sc(1.5))
    # vignette
    vg = Image.new("L", img.size, 0)
    vd = ImageDraw.Draw(vg)
    vd.rectangle([0, 0, sc(W), sc(H)], fill=0)
    vd.ellipse([P((-260, -200)), P((W + 260, H + 200))], fill=255)
    vg = vg.filter(ImageFilter.GaussianBlur(sc(160)))
    dark = Image.new("RGB", img.size, BG)
    img = Image.composite(img, dark, vg)
    return img

def brand(d):
    d.rectangle([P((80, 72)), P((98, 90))], fill=BLUE)
    text(d, (112, 66), "ALEX ANALYTICS", font(FM, 26), WHITE)

def darken(img, ya, yb, amax):
    """Darken the lower part so text stays readable."""
    m = Image.new("L", img.size, 0)
    md = ImageDraw.Draw(m)
    for y in range(sc(ya), sc(H)):
        t = min(1, (y - sc(ya)) / max(1, sc(yb - ya)))
        md.line([(0, y), (sc(W), y)], fill=int(amax * t))
    img.paste(Image.new("RGB", img.size, BG), (0, 0), m)

def save(img, name):
    img.resize((W, H), Image.LANCZOS).save(os.path.join(OUT, name), "PNG")

def card(d, x0, y0, x1, y1):
    d.rounded_rectangle([P((x0, y0)), P((x1, y1))], radius=sc(18), fill=(8, 18, 40, 200), outline=BLUE, width=sc(3))

# ================= 1: cover =================
img = atmosphere(3, (540, 420))
darken(img, 520, 880, 235)
d = ImageDraw.Draw(img, "RGBA")
brand(d)
f1, s1 = fit(["ТЫ ОТКРЫЛСЯ.", "ПАРТНЁР НЕ ОТДАЛ."], FH, 920, 128)
y = 700
text(d, (80, y), "ТЫ ОТКРЫЛСЯ.", f1, WHITE)
text(d, (80, y + int(s1 * 1.02)), "ПАРТНЁР НЕ ОТДАЛ.", f1, WHITE)
f2, s2 = fit(["ПОЧЕМУ ТАК ПРОИСХОДИТ?"], FH, 920, 74)
text(d, (80, y + int(s1 * 2.12)), "ПОЧЕМУ ТАК ПРОИСХОДИТ?", f2, BLUE2)
yy = y + int(s1 * 2.12) + int(s2 * 1.6)
para(d, 80, yy, "Чаще всего дело не в партнёре, а в моменте, когда ты открылся.", font(FB, 36), GREY, 900, 48)
d.line([P((80, 1232)), P((200, 1232))], fill=BLUE, width=sc(6))
text(d, (80, 1250), "Листай — разберём момент открывания", font(FBB, 30), WHITE)
text(d, (1000, 1240), "→", font(FH, 46), BLUE2, "ra")
save(img, "01_cover.png")

# ================= 2: mechanics =================
img = atmosphere(8, (860, 300), beam=False)
darken(img, 0, 1350, 120)
d = ImageDraw.Draw(img, "RGBA")
brand(d)
fa, sa = fit(["ОТКРЫТЬСЯ — НЕ ЗНАЧИТ", "ПРОСТО ПРИЙТИ В ТОЧКУ"], FH, 920, 76)
text(d, (80, 140), "ОТКРЫТЬСЯ — НЕ ЗНАЧИТ", fa, WHITE)
text(d, (80, 140 + int(sa * 1.08)), "ПРОСТО ПРИЙТИ В ТОЧКУ", fa, BLUE2)
para(d, 80, 140 + int(sa * 2.5), "У партнёра с шайбой на решение секунды. За это время он проверяет три вещи.",
     font(FB, 33), GREY, 900, 44)
rows = [("Видит ли он тебя", "корпус развёрнут к шайбе, клюшка подставлена под передачу"),
        ("Свободен ли коридор", "между вами нет клюшки или корпуса соперника"),
        ("Успеет ли шайба", "ты в точке, куда передача дойдёт вовремя")]
y = 520
for i, (t, s) in enumerate(rows, 1):
    card(d, 80, y, 1000, y + 200)
    text(d, (124, y + 100), str(i), font(FH, 96), BLUE2, "lm")
    text(d, (230, y + 38), t, font(FBB, 41), WHITE)
    para(d, 230, y + 100, s, font(FB, 30), GREY, 720, 40)
    y += 230
text(d, (80, 1240), "Если хотя бы одно «нет», передачи не будет.", font(FH, 36), WHITE)
save(img, "02_mechanics.png")

# ================= 3: three reasons =================
img = atmosphere(21, (260, 380), beam=False)
darken(img, 0, 1350, 120)
d = ImageDraw.Draw(img, "RGBA")
brand(d)
fa, sa = fit(["ТРИ ПРИЧИНЫ, ПОЧЕМУ", "ПЕРЕДАЧА НЕ ПРИХОДИТ"], FH, 920, 78)
text(d, (80, 140), "ТРИ ПРИЧИНЫ, ПОЧЕМУ", fa, WHITE)
text(d, (80, 140 + int(sa * 1.08)), "ПЕРЕДАЧА НЕ ПРИХОДИТ", fa, BLUE2)
items = [("СЛИШКОМ РАНО", "Пока партнёр обрабатывает шайбу, защитник успевает закрыть коридор."),
         ("СЛИШКОМ ПОЗДНО", "Партнёр уже выбрал другой вариант и не ждёт передачи на тебя."),
         ("БЕЗ СИГНАЛА", "Ты в нужной точке, но партнёр не понял, что открылся: нет подставленной клюшки и развёрнутого корпуса.")]
y = 440
for i, (t, s) in enumerate(items, 1):
    card(d, 80, y, 1000, y + (250 if i == 3 else 205))
    d.rounded_rectangle([P((112, y + 30)), P((178, y + 96))], radius=sc(14), fill=BLUE)
    text(d, (145, y + 64), str(i), font(FH, 46), WHITE, "mm")
    text(d, (206, y + 30), t, font(FH, 46), WHITE)
    para(d, 206, y + 92, s, font(FB, 30), GREY, 740, 40)
    y += 235 if i < 3 else 0
para(d, 80, 1180, "Причин в эпизоде бывает несколько. Что именно сработало, видно только при разборе развития момента.",
     font(FBB, 28), WHITE, 920, 38)
save(img, "03_reasons.png")

# ================= 4: CTA =================
img = atmosphere(33, (540, 380))
darken(img, 430, 780, 235)
d = ImageDraw.Draw(img, "RGBA")
brand(d)
fa, sa = fit(["КАК ПОНЯТЬ,", "В ЧЁМ ТВОЯ ПРИЧИНА?"], FH, 920, 112)
text(d, (80, 690), "КАК ПОНЯТЬ,", fa, WHITE)
text(d, (80, 690 + int(sa * 1.04)), "В ЧЁМ ТВОЯ ПРИЧИНА?", fa, BLUE2)
para(d, 80, 690 + int(sa * 2.4), "Поставь смену на паузу в момент, когда ты открылся, и проверь: видел ли тебя партнёр, был ли свободен коридор, вовремя ли ты пришёл в точку.",
     font(FB, 31), GREY, 920, 42)
d.rounded_rectangle([P((80, 1100)), P((1000, 1180))], radius=sc(40), fill=BLUE)
text(d, (540, 1141), "НАПИШИ «ОТКРЫВАНИЕ» В ДИРЕКТ", font(FH, 40), WHITE, "mm")
text(d, (540, 1212), "Отправь короткий отрезок смены, и разберём момент вместе", font(FB, 27), WHITE, "ma")
text(d, (540, 1256), "Разбор помогает точнее понять игру, но не гарантирует результат", font(FB, 21), GREY, "ma")
text(d, (540, 1296), "@alex__analytics", font(FM, 26), WHITE, "ma")
save(img, "04_cta.png")
print("done")
