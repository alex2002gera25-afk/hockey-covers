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

# ================= 1: cover =================
img = atmosphere(41, (600, 380))
ice_floor(img, 640)
spray(img, (250, 650), -34, 50, 1700, 40, 720, seed=7)
motion_streaks(img, (700, 620), n=14, length=300)
d = puck(img, (700, 625), 104)
darken(img, 640, 900, 238)
d = ImageDraw.Draw(img, "RGBA")
brand(d)
f1, s1 = fit(["СИЛОВОЙ:", "ЗА ИЛИ ПРОТИВ?"], FH, 920, 150)
y = 790
text(d, (80, y), "СИЛОВОЙ:", f1, WHITE)
text(d, (80, y + int(s1 * 1.02)), "ЗА ИЛИ ПРОТИВ?", f1, BLUE2)
para(d, 80, y + int(s1 * 2.2), "Один и тот же контакт: в одном эпизоде он выигрывает шайбу, в другом оставляет дыру в позиции.",
     font(FB, 33), GREY, 900, 44)
d.line([P((80, 1232)), P((200, 1232))], fill=BLUE, width=sc(6))
text(d, (80, 1250), "Листай — когда силовой оправдан", font(FBB, 30), WHITE)
text(d, (1000, 1240), "→", font(FH, 46), BLUE2, "ra")
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
