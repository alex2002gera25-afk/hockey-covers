import sys
sys.argv = ["x"]
exec(open('/home/claude/build3.py').read().split("# ================= 1: cover =================")[0].replace('OUT = "/mnt/user-data/outputs/alex_analytics_carousel_03"', 'OUT = "/home/claude/hockey-covers/posts/2026-10-17_smena"'))
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


def skater2(dr, hip, d, lean, k, stride, fill, stick_blade=True, stance="skate"):
    hx, hy = hip
    L = 105 * k
    sh = (hx + d * math.sin(lean) * L, hy - math.cos(lean) * L)
    head = (sh[0] + d * 20 * k, sh[1] - 40 * k)
    if stance == "skate":
        legs_near = [(hx, hy), (hx + d * 52 * k * stride, hy + 58 * k), (hx + d * 28 * k * stride, hy + 122 * k)]
        legs_far = [(hx, hy), (hx - d * 42 * k * stride, hy + 62 * k), (hx - d * 100 * k * stride, hy + 116 * k)]
    else:  # backward / wide defensive stance
        legs_near = [(hx, hy), (hx + 44 * k, hy + 60 * k), (hx + 60 * k, hy + 122 * k)]
        legs_far = [(hx, hy), (hx - 44 * k, hy + 60 * k), (hx - 60 * k, hy + 122 * k)]
    chain(dr, legs_far, [34 * k, 28 * k, 22 * k], fill)
    elbow_f = (sh[0] + d * 12 * k, sh[1] + 48 * k)
    hand_f = (sh[0] + d * 58 * k, sh[1] + 62 * k)
    chain(dr, [sh, elbow_f, hand_f], [26 * k, 22 * k, 20 * k], fill)
    ground = hy + 122 * k
    hand = (sh[0] + d * 70 * k, sh[1] + 70 * k)
    blade = (hand[0] + d * 70 * k, ground + 6 * k)
    dr.line([P(hand), P(blade)], fill=fill, width=sc(7 * k))
    dr.line([P(blade), P((blade[0] + d * 46 * k, blade[1]))], fill=fill, width=sc(9 * k))
    chain(dr, [hip, sh], [84 * k], fill)
    chain(dr, legs_near, [38 * k, 30 * k, 24 * k], fill)
    elbow_n = (sh[0] + d * 40 * k, sh[1] + 42 * k)
    chain(dr, [sh, elbow_n, hand], [30 * k, 25 * k, 22 * k], fill)
    dr.ellipse([P((head[0] - 31 * k, head[1] - 33 * k)), P((head[0] + 31 * k, head[1] + 31 * k))], fill=fill)
    for leg in (legs_near, legs_far):
        ax, ay = leg[-1]
        dr.polygon([P((ax - 26 * k * d, ay - 14 * k)), P((ax + 36 * k * d, ay - 10 * k)), P((ax + 40 * k * d, ay + 14 * k)), P((ax - 30 * k * d, ay + 14 * k))], fill=fill)
        dr.line([P((ax - 42 * k * d, ay + 20 * k)), P((ax + 52 * k * d, ay + 20 * k))], fill=fill, width=sc(5 * k))
    return blade

def rush_scene(img):
    rim = Image.new("RGBA", img.size, (0, 0, 0, 0)); dark = Image.new("RGBA", img.size, (0, 0, 0, 0))
    rd, dd = ImageDraw.Draw(rim), ImageDraw.Draw(dark)
    # (hip_x, hip_y, dir, lean, size, stride, stance)
    cast = [
        (720, 0, 0, 0, 0, 0, 0),
    ]
    G = lambda g, k: g - 122 * k
    players = [
        (610, G(612, 0.62), +1, 0.40, 0.62, 1.0, "skate"),   # far winger
        (440, G(676, 0.82), +1, 0.46, 0.82, 1.0, "skate"),   # puck carrier
        (920, G(616, 0.64), -1, 0.10, 0.64, 1.0, "def"),     # defender 2 (far)
        (775, G(706, 0.88), -1, 0.14, 0.88, 1.0, "def"),     # defender 1
        (250, G(730, 0.92), +1, 0.46, 0.92, 1.0, "skate"),   # near winger
        (95, G(640, 0.74), +1, 0.66, 0.74, 1.0, "skate"),   # backchecker (trailing)
    ]
    blades = []
    for hx, hy, d, lean, k, stride, st in players:
        for dr, col in ((rd, (150, 195, 255, 255)),):
            skater2(dr, (hx, hy), d, lean, k, stride, col, stance="def" if st == "def" else "skate")
    for hx, hy, d, lean, k, stride, st in players:
        b = skater2(dd, (hx, hy), d, lean, k, stride, (6, 9, 16, 255), stance="def" if st == "def" else "skate")
        blades.append(b)
    glow = rim.filter(ImageFilter.GaussianBlur(sc(5)))
    shifted = Image.new("RGBA", img.size, (0, 0, 0, 0)); shifted.paste(glow, (sc(-5), sc(-4)))
    img.paste(shifted, (0, 0), shifted)
    img.paste(dark, (0, 0), dark)
    return blades


# ================= 1: cover =================
img = atmosphere(77, (540, 330), beam=False)
bg = Image.new("L", img.size, 0)
ImageDraw.Draw(bg).ellipse([P((120, 120)), P((960, 640))], fill=215)
bg = bg.filter(ImageFilter.GaussianBlur(sc(120)))
img.paste(Image.new("RGB", img.size, (120, 170, 250)), (0, 0), bg)
fl = Image.new("L", img.size, 0)
fld = ImageDraw.Draw(fl)
for y in range(sc(560), sc(H)):
    t = (y - sc(560)) / sc(H - 560)
    fld.line([(0, y), (sc(W), y)], fill=int(205 * (1 - t) ** 0.8))
img.paste(Image.new("RGB", img.size, (35, 70, 130)), (0, 0), fl)
for fx, fy, fr in ((470, 60, 26), (810, 70, 30), (980, 130, 22), (640, 40, 34), (260, 190, 18)):
    fg = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(fg).ellipse([P((fx - fr, fy - fr)), P((fx + fr, fy + fr))], fill=(255, 255, 255, 235))
    fgb = fg.filter(ImageFilter.GaussianBlur(sc(16))); img.paste(fgb, (0, 0), fgb)
    fgs = fg.filter(ImageFilter.GaussianBlur(sc(3))); img.paste(fgs, (0, 0), fgs)
# soft ice shadows under skaters
shd = Image.new("RGBA", img.size, (0, 0, 0, 0))
sdd = ImageDraw.Draw(shd)
for cx, gy, w in ((610, 612, 100), (440, 676, 130), (920, 616, 100), (775, 706, 145), (250, 730, 150), (95, 640, 115)):
    sdd.ellipse([P((cx - w, gy - 12)), P((cx + w, gy + 16))], fill=(0, 0, 0, 120))
shd = shd.filter(ImageFilter.GaussianBlur(sc(9))); img.paste(shd, (0, 0), shd)
blades = rush_scene(img)
spray(img, (270, 735), -170, 34, 420, 30, 220, seed=8)
spray(img, (800, 712), 20, 28, 380, 30, 200, seed=15, glow=False)
spray(img, (60, 650), 175, 24, 200, 20, 150, seed=19, glow=False)
darken(img, 700, 930, 238)
d = ImageDraw.Draw(img, "RGBA")
brand(d)
f1, s1 = fit(["ВЫШЕЛ НА СМЕНЕ.", "ЧТО ВИДИШЬ ПЕРВЫМ?"], FH, 920, 150)
y = 800
text(d, (80, y), "ВЫШЕЛ НА СМЕНЕ.", f1, WHITE)
text(d, (80, y + int(s1 * 1.02)), "ЧТО ВИДИШЬ ПЕРВЫМ?", f1, BLUE2)
para(d, 80, y + int(s1 * 2.2), "Первые секунды на льду решают, закрыт ли твой игрок.",
     font(FB, 31), GREY, 900, 42)
d.line([P((80, 1252)), P((200, 1252))], fill=BLUE, width=sc(6))
text(d, (80, 1268), "Листай — что делать на смене", font(FBB, 28), WHITE)
text(d, (1000, 1262), "→", font(FH, 44), BLUE2, "ra")
save(img, "01_cover.png")



# ===== CTA =====
img = atmosphere(91, (540, 380), beam=False)
bgm = Image.new("L", img.size, 0)
ImageDraw.Draw(bgm).ellipse([P((140, 100)), P((940, 700))], fill=200)
bgm = bgm.filter(ImageFilter.GaussianBlur(sc(130)))
img.paste(Image.new("RGB", img.size, (95, 150, 240)), (0, 0), bgm)
fl = Image.new("L", img.size, 0); fld = ImageDraw.Draw(fl)
for y in range(sc(640), sc(H)):
    t = (y - sc(640)) / sc(H - 640); fld.line([(0, y), (sc(W), y)], fill=int(190 * (1 - t) ** 0.8))
img.paste(Image.new("RGB", img.size, (35, 70, 130)), (0, 0), fl)
motion_streaks(img, (540, 470), n=30, length=460, ang=190, seed=4)
spray(img, (700, 520), 10, 30, 300, 30, 220, seed=21)
puck(img, (540, 470), r=120)
darken(img, 640, 900, 240)
d = ImageDraw.Draw(img, "RGBA")
brand(d)
f1, s1 = fit(["ХОЧЕШЬ РАЗОБРАТЬ", "СВОИ СМЕНЫ?"], FH, 920, 110)
y = 700
text(d, (80, y), "ХОЧЕШЬ РАЗОБРАТЬ", f1, WHITE)
text(d, (80, y + int(s1 * 1.02)), "СВОИ СМЕНЫ?", f1, BLUE2)
para(d, 80, y + int(s1 * 2.2), "Покажем, где в твоей игре на смене образуются дыры.", font(FB, 31), GREY, 900, 42)
bx = 80; by = 1060
fb = font(FBB, 36); tw = d.textlength("Напиши «АНАЛИТИКА» в директ", font=fb) / S
d.rounded_rectangle([P((bx, by)), P((bx + tw + 80, by + 84))], radius=sc(42), fill=BLUE)
text(d, (bx + 40, by + 17), "Напиши «АНАЛИТИКА» в директ", fb, WHITE)
text(d, (80, 1262), "@alex__analytics", font(FBB, 30), GREY)
save(img, "04_cta.png")
