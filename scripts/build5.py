import sys
sys.argv = ["x"]
exec(open('/home/claude/build3.py').read().split("# ================= 1: cover =================")[0].replace('OUT = "/mnt/user-data/outputs/alex_analytics_carousel_03"', 'OUT = "/mnt/user-data/outputs/alex_analytics_carousel_04"'))
import math, random
from PIL import ImageChops

def spray(img, origin, ang_deg, spread_deg, n, lmin, lmax, seed=5, glow=True):
    random.seed(seed)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ox, oy = origin
    for _ in range(n):
        a = math.radians(ang_deg + random.gauss(0, spread_deg / 2.4))
        dist = (lmin + (lmax - lmin) * random.random() ** 1.6)
        x = ox + math.cos(a) * dist
        y = oy + math.sin(a) * dist - 0.0006 * dist * dist
        size = random.choice([2, 3, 4, 5, 7, 10]) * (1.2 - 0.6 * dist / lmax)
        alpha = int(random.randint(110, 255) * (1 - 0.55 * dist / lmax))
        col = random.choice([(255, 255, 255), (230, 241, 255), (200, 222, 255)])
        if random.random() < 0.35:
            L = random.uniform(10, 38)
            ld.line([P((x, y)), P((x - math.cos(a) * L, y - math.sin(a) * L))], fill=col + (alpha,), width=sc(max(2, size * 0.6)))
        else:
            ld.ellipse([P((x - size, y - size)), P((x + size, y + size))], fill=col + (alpha,))
    cloud = Image.new("RGBA", img.size, (0, 0, 0, 0))
    cd = ImageDraw.Draw(cloud)
    for _ in range(26):
        a = math.radians(ang_deg + random.gauss(0, spread_deg / 3))
        dist = random.uniform(lmin, lmax * 0.7)
        x = ox + math.cos(a) * dist; y = oy + math.sin(a) * dist
        r = random.uniform(30, 90)
        cd.ellipse([P((x - r, y - r)), P((x + r, y + r))], fill=(220, 236, 255, random.randint(18, 46)))
    cloud = cloud.filter(ImageFilter.GaussianBlur(sc(22)))
    img.paste(cloud, (0, 0), cloud)
    soft = layer.filter(ImageFilter.GaussianBlur(sc(2.2)))
    if glow:
        g = layer.filter(ImageFilter.GaussianBlur(sc(14)))
        img.paste(g, (0, 0), g)
    img.paste(soft, (0, 0), soft)
    img.paste(layer, (0, 0), layer)

def puck(img, c, r=92, tilt=0.42):
    cx, cy = c
    th = r * 0.55
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    sd.ellipse([P((cx - r * 1.15, cy + th * 0.55)), P((cx + r * 1.15, cy + th * 1.5))], fill=(0, 0, 0, 190))
    sh = sh.filter(ImageFilter.GaussianBlur(sc(16)))
    img.paste(sh, (0, 0), sh)
    d = ImageDraw.Draw(img, "RGBA")
    ry = r * tilt
    # side
    for i in range(int(th)):
        t = i / th
        col = (int(18 - 8 * t), int(20 - 8 * t), int(26 - 8 * t))
        d.ellipse([P((cx - r, cy + i - ry)), P((cx + r, cy + i + ry))], fill=col + (255,))
    # top
    d.ellipse([P((cx - r, cy - ry)), P((cx + r, cy + ry))], fill=(26, 28, 36, 255))
    d.ellipse([P((cx - r * 0.93, cy - ry * 0.93)), P((cx + r * 0.93, cy + ry * 0.93))], fill=(12, 13, 18, 255))
    # rim light
    d.arc([P((cx - r, cy - ry)), P((cx + r, cy + ry))], 200, 340, fill=(140, 180, 255, 220), width=sc(3))
    d.arc([P((cx - r, cy + th - ry)), P((cx + r, cy + th + ry))], 20, 160, fill=(70, 110, 190, 150), width=sc(3))
    # specular band on top
    sp = Image.new("RGBA", img.size, (0, 0, 0, 0))
    spd = ImageDraw.Draw(sp)
    spd.ellipse([P((cx - r * 0.55, cy - ry * 0.7)), P((cx + r * 0.2, cy - ry * 0.05))], fill=(150, 190, 255, 70))
    sp = sp.filter(ImageFilter.GaussianBlur(sc(6)))
    img.paste(sp, (0, 0), sp)
    return ImageDraw.Draw(img, "RGBA")

def motion_streaks(img, c, n=26, length=420, ang=190, seed=3):
    random.seed(seed)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    for _ in range(n):
        dy = random.uniform(-26, 26)
        L = random.uniform(120, length)
        x0, y0 = c[0] + random.uniform(60, 110), c[1] + dy
        a = math.radians(ang + random.uniform(-4, 4))
        ld.line([P((x0, y0)), P((x0 + math.cos(a) * L, y0 + math.sin(a) * L))], fill=(170, 205, 255, random.randint(40, 120)), width=sc(random.choice([2, 3, 4])))
    layer = layer.filter(ImageFilter.GaussianBlur(sc(2)))
    img.paste(layer, (0, 0), layer)

def ice_floor(img, y_top):
    m = Image.new("L", img.size, 0)
    md = ImageDraw.Draw(m)
    for y in range(sc(y_top - 260), sc(H)):
        t = (y - sc(y_top - 260)) / sc(H - y_top + 260)
        md.line([(0, y), (sc(W), y)], fill=int(95 * math.sin(min(1, t * 1.6) * math.pi / 2) * (1 - t) ** 0.6))
    img.paste(Image.new("RGB", img.size, (60, 110, 190)), (0, 0), m)

def blade(img, tipx, tipy):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    pts = [(tipx - 360, tipy + 30), (tipx, tipy - 18), (tipx + 40, tipy - 4), (tipx + 40, tipy + 28), (tipx - 360, tipy + 120)]
    ld.polygon([P(p) for p in pts], fill=(18, 20, 28, 255))
    ld.line([P((tipx - 360, tipy + 34)), P((tipx, tipy - 14))], fill=(120, 165, 240, 230), width=sc(3))
    ld.rectangle([P((tipx - 190, tipy + 10)), P((tipx - 120, tipy + 74))], fill=(235, 240, 250, 200))
    img.paste(layer, (0, 0), layer)

def chain(dr, pts, widths, fill):
    for (a, b, w) in zip(pts[:-1], pts[1:], widths):
        dr.line([P(a), P(b)], fill=fill, width=sc(w))
    for p, w in zip(pts, widths + [widths[-1]]):
        dr.ellipse([P((p[0] - w / 2, p[1] - w / 2)), P((p[0] + w / 2, p[1] + w / 2))], fill=fill)

def skater(dr, o, fill, head, shoulders, hips, near_leg, far_leg, near_arm, far_arm, stick, torso_w=88, face=1):
    ox, oy = o
    T = lambda p: (p[0] + ox, p[1] + oy)
    # far limbs first
    chain(dr, [T(p) for p in far_leg], [34, 28, 22], fill)
    chain(dr, [T(p) for p in far_arm], [26, 22, 20], fill)
    # stick
    dr.line([P(T(stick[0])), P(T(stick[1]))], fill=fill, width=sc(7))
    bl = T(stick[1]); dr.line([P(bl), P((bl[0] + 52 * face, bl[1] + 4))], fill=fill, width=sc(10))
    # torso
    chain(dr, [T(shoulders), T(hips)], [torso_w], fill)
    # near limbs
    chain(dr, [T(p) for p in near_leg], [38, 30, 24], fill)
    chain(dr, [T(p) for p in near_arm], [30, 25, 22], fill)
    # head + helmet
    hx, hy = T(head)
    dr.ellipse([P((hx - 31, hy - 33)), P((hx + 31, hy + 31))], fill=fill)
    # skates
    for leg in (near_leg, far_leg):
        ax, ay = T(leg[-1])
        dr.polygon([P((ax - 26 * face, ay - 14)), P((ax + 36 * face, ay - 10)), P((ax + 40 * face, ay + 14)), P((ax - 30 * face, ay + 14))], fill=fill)
        dr.line([P((ax - 40 * face, ay + 20)), P((ax + 50 * face, ay + 20))], fill=fill, width=sc(5))

def silhouettes_scene(img):
    layer_rim = Image.new("RGBA", img.size, (0, 0, 0, 0))
    layer_dark = Image.new("RGBA", img.size, (0, 0, 0, 0))
    rd, dd = ImageDraw.Draw(layer_rim), ImageDraw.Draw(layer_dark)
    # attacker (left, leaning back, being hit)
    att = dict(o=(-10, 0), head=(412, 330), shoulders=(418, 395), hips=(398, 520),
               near_leg=[(412, 520), (452, 600), (410, 692)], far_leg=[(388, 522), (340, 610), (300, 690)],
               near_arm=[(440, 392), (505, 432), (548, 462)], far_arm=[(392, 400), (350, 455), (470, 470)],
               stick=[(470, 445), (628, 690)], face=1)
    # defender (right, driving shoulder into contact)
    dfn = dict(o=(-40, 0), head=(600, 362), shoulders=(612, 420), hips=(668, 530),
               near_leg=[(672, 535), (622, 612), (590, 692)], far_leg=[(690, 530), (740, 610), (775, 692)],
               near_arm=[(588, 424), (548, 462), (528, 438)], far_arm=[(645, 424), (700, 470), (720, 430)],
               stick=[(720, 440), (790, 690)], face=-1)
    for cfg in (att, dfn):
        skater(rd, fill=(150, 195, 255, 255), **cfg)
    for cfg in (att, dfn):
        skater(dd, fill=(6, 9, 16, 255), **cfg)
    # rim light = blurred lit copy offset up-left, silhouette on top
    glow = layer_rim.filter(ImageFilter.GaussianBlur(sc(5)))
    shifted = Image.new("RGBA", img.size, (0, 0, 0, 0))
    shifted.paste(glow, (sc(-5), sc(-4)))
    img.paste(shifted, (0, 0), shifted)
    img.paste(layer_dark, (0, 0), layer_dark)
    # reflection on ice (flipped, faded)
    refl = layer_dark.transpose(Image.FLIP_TOP_BOTTOM)
    refl = refl.filter(ImageFilter.GaussianBlur(sc(7)))
    ice_y = 712
    rf = Image.new("RGBA", img.size, (0, 0, 0, 0))
    rf.paste(refl, (0, sc(2 * ice_y) - sc(H)))
    a = rf.split()[3].point(lambda v: int(v * 0.35))
    fade = Image.new("L", img.size, 0)
    fd = ImageDraw.Draw(fade)
    for y in range(sc(ice_y), sc(ice_y + 190)):
        fd.line([(0, y), (sc(W), y)], fill=int(255 * (1 - (y - sc(ice_y)) / sc(190))))
    from PIL import ImageChops
    a = ImageChops.multiply(a, fade)
    rf.putalpha(a)
    img.paste(rf, (0, 0), rf)

# ================= 1: cover =================
img = atmosphere(41, (560, 340), beam=False)
# bright arena light behind the action
bg = Image.new("L", img.size, 0)
bgd = ImageDraw.Draw(bg)
bgd.ellipse([P((200, 120)), P((920, 620))], fill=215)
bg = bg.filter(ImageFilter.GaussianBlur(sc(120)))
img.paste(Image.new("RGB", img.size, (120, 170, 250)), (0, 0), bg)
# ice floor
fl = Image.new("L", img.size, 0)
fld = ImageDraw.Draw(fl)
for y in range(sc(700), sc(H)):
    t = (y - sc(700)) / sc(H - 700)
    fld.line([(0, y), (sc(W), y)], fill=int(200 * (1 - t) ** 0.9))
img.paste(Image.new("RGB", img.size, (35, 70, 130)), (0, 0), fl)
# boards with glass top-right
d0 = ImageDraw.Draw(img, "RGBA")
d0.polygon([P((0, 706)), P((W, 706)), P((W, 760)), P((0, 760))], fill=(10, 18, 36, 255))
d0.line([P((0, 706)), P((W, 706))], fill=(150, 195, 255, 230), width=sc(4))
# arena lights (flares)
for fx, fy, fr in ((470, 60, 26), (810, 70, 30), (980, 130, 22), (640, 40, 34), (260, 210, 18)):
    fg = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(fg).ellipse([P((fx - fr, fy - fr)), P((fx + fr, fy + fr))], fill=(255, 255, 255, 235))
    fgb = fg.filter(ImageFilter.GaussianBlur(sc(16)))
    img.paste(fgb, (0, 0), fgb); img.paste(fg.filter(ImageFilter.GaussianBlur(sc(3))), (0, 0), fg.filter(ImageFilter.GaussianBlur(sc(3))))
silhouettes_scene(img)
# ice spray at the stop
spray(img, (640, 700), -158, 40, 900, 30, 380, seed=9)
spray(img, (640, 700), -20, 30, 260, 30, 260, seed=14, glow=False)
darken(img, 700, 930, 238)
d = ImageDraw.Draw(img, "RGBA")
brand(d)
f1, s1 = fit(["СИЛОВОЙ:", "ЗА ИЛИ ПРОТИВ?"], FH, 920, 150)
y = 800
text(d, (80, y), "СИЛОВОЙ:", f1, WHITE)
text(d, (80, y + int(s1 * 1.02)), "ЗА ИЛИ ПРОТИВ?", f1, BLUE2)
para(d, 80, y + int(s1 * 2.2), "Один и тот же контакт: в одном эпизоде он выигрывает шайбу, в другом оставляет дыру в позиции.",
     font(FB, 31), GREY, 900, 42)
d.line([P((80, 1252)), P((200, 1252))], fill=BLUE, width=sc(6))
text(d, (80, 1268), "Листай — когда силовой оправдан", font(FBB, 28), WHITE)
text(d, (1000, 1262), "→", font(FH, 44), BLUE2, "ra")
save(img, "01_cover.png")

# ================= 2: for =================
img = atmosphere(52, (860, 320), beam=False)
darken(img, 0, 1350, 120)
d = ImageDraw.Draw(img, "RGBA")
brand(d)
fa, sa = fit(["КОГДА СИЛОВОЙ", "РАБОТАЕТ НА КОМАНДУ"], FH, 920, 82)
text(d, (80, 140), "КОГДА СИЛОВОЙ", fa, WHITE)
text(d, (80, 140 + int(sa * 1.08)), "РАБОТАЕТ НА КОМАНДУ", fa, BLUE2)
para(d, 80, 140 + int(sa * 2.5), "Цель контакта — вернуть шайбу или вывести соперника из эпизода. Не сам удар.",
     font(FB, 33), GREY, 900, 44)
rows = [("Шайба у соперника", "контакт приходится на игрока, который владеет шайбой или принимает передачу"),
        ("Ты в зоне досягаемости", "ты подошёл так близко, что не нужно срываться и терять позицию"),
        ("Партнёры страхуют", "если контакт не сработает, место за тобой занимает партнёр")]
y = 500
for i, (t, s) in enumerate(rows, 1):
    card(d, 80, y, 1000, y + 215)
    text(d, (124, y + 108), str(i), font(FH, 96), BLUE2, "lm")
    text(d, (230, y + 34), t, font(FBB, 41), WHITE)
    para(d, 230, y + 96, s, font(FB, 30), GREY, 720, 40)
    y += 245
save(img, "02_for.png")

# ================= 3: against =================
img = atmosphere(63, (260, 360), beam=False)
darken(img, 0, 1350, 120)
d = ImageDraw.Draw(img, "RGBA")
brand(d)
fa, sa = fit(["КОГДА СИЛОВОЙ", "ВЫВОДИТ ИЗ ИГРЫ"], FH, 920, 82)
text(d, (80, 140), "КОГДА СИЛОВОЙ", fa, WHITE)
text(d, (80, 140 + int(sa * 1.08)), "ВЫВОДИТ ИЗ ИГРЫ", fa, BLUE2)
items = [("ПРОМАХ", "Игрок прошёл мимо, а за его спиной остался открытый коридор."),
         ("КОНТАКТ ВМЕСТО ПОЗИЦИИ", "Вместо закрытия линии передачи игрок ушёл за контактом."),
         ("ШТРАФ", "Неточный или запоздалый контакт может закончиться удалением. Критерии зависят от лиги и судьи.")]
y = 430
for i, (t, s) in enumerate(items, 1):
    h = 250 if i == 3 else 205
    card(d, 80, y, 1000, y + h)
    d.rounded_rectangle([P((112, y + 30)), P((178, y + 96))], radius=sc(14), fill=BLUE)
    text(d, (145, y + 64), str(i), font(FH, 46), WHITE, "mm")
    text(d, (206, y + 30), t, font(FH, 42), WHITE)
    para(d, 206, y + 92, s, font(FB, 30), GREY, 740, 40)
    y += 235
para(d, 80, 1180, "Один и тот же контакт может быть и верным, и ошибочным. Это зависит от ситуации в эпизоде.",
     font(FBB, 28), WHITE, 920, 38)
save(img, "03_against.png")

# ================= 4: CTA =================
img = atmosphere(74, (540, 330))
ice_floor(img, 420)
spray(img, (820, 470), -155, 46, 1300, 40, 620, seed=21)
darken(img, 440, 760, 238)
d = ImageDraw.Draw(img, "RGBA")
brand(d)
fa, sa = fit(["ОЦЕНИ СИЛОВОЙ", "ПО РЕЗУЛЬТАТУ ЭПИЗОДА"], FH, 920, 92)
text(d, (80, 690), "ОЦЕНИ СИЛОВОЙ", fa, WHITE)
text(d, (80, 690 + int(sa * 1.04)), "ПО РЕЗУЛЬТАТУ ЭПИЗОДА", fa, BLUE2)
para(d, 80, 690 + int(sa * 2.35), "Не по самому удару. Посмотри, вернулась ли шайба, остался ли игрок в позиции и закрыт ли коридор после контакта.",
     font(FB, 31), GREY, 920, 42)
d.rounded_rectangle([P((80, 1100)), P((1000, 1180))], radius=sc(40), fill=BLUE)
text(d, (540, 1141), "НАПИШИ «СИЛОВОЙ» В ДИРЕКТ", font(FH, 40), WHITE, "mm")
text(d, (540, 1212), "Отправь эпизод с контактом, и разберём его вместе", font(FB, 27), WHITE, "ma")
text(d, (540, 1256), "Разбор помогает точнее понять игру, но не гарантирует результат", font(FB, 21), GREY, "ma")
text(d, (540, 1296), "@alex__analytics", font(FM, 26), WHITE, "ma")
save(img, "04_cta.png")
print("done")
