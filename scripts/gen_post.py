import os, json as _json, sys as _sys
_SPEC=_json.load(open(_sys.argv[1])); _OUTDIR=_sys.argv[2]
_sys.argv=["x"]
exec(open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'build3.py')).read().split("# ================= 1: cover =================")[0].replace('OUT = "/mnt/user-data/outputs/alex_analytics_carousel_03"', 'OUT = _OUTDIR'))
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



import random as _r
THEMES = {"blue": ((60,100,190),(14,32,64)), "deep": ((40,75,160),(10,24,52)),
          "ice": ((95,135,215),(24,50,96)), "steel": ((55,85,150),(14,28,58)),
          "royal": ((45,85,200),(12,30,78))}

def backdrop(R, theme, floor_y, smooth=False):
    gc, fc = THEMES[theme]
    img = atmosphere(R.randint(1, 999), (R.randint(300, 780), R.randint(260, 420)), beam=False)
    gx = R.randint(260, 820); gy = R.randint(220, 420)
    bg = Image.new("L", img.size, 0)
    ImageDraw.Draw(bg).ellipse([P((gx - 420, gy - 260)), P((gx + 420, gy + 260))], fill=R.randint(120, 170))
    bg = bg.filter(ImageFilter.GaussianBlur(sc(120)))
    img.paste(Image.new("RGB", img.size, gc), (0, 0), bg)
    fl = Image.new("L", img.size, 0); fld = ImageDraw.Draw(fl)
    y0 = floor_y - (200 if smooth else 0)
    for y in range(sc(y0), sc(H)):
        t = (y - sc(y0)) / sc(H - y0)
        ramp = min(1.0, t * 4) if smooth else 1.0
        fld.line([(0, y), (sc(W), y)], fill=int(150 * ramp * (1 - t) ** 0.8))
    img.paste(Image.new("RGB", img.size, fc), (0, 0), fl)
    for _ in range(R.randint(3, 6)):
        fx, fy, fr = R.randint(120, 980), R.randint(40, 230), R.randint(16, 34)
        if fy < 120 and fx < 400: fx += 360
        fg = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(fg).ellipse([P((fx - fr, fy - fr)), P((fx + fr, fy + fr))], fill=(255, 255, 255, R.randint(150, 235)))
        img.paste(fg.filter(ImageFilter.GaussianBlur(sc(16))), (0, 0), fg.filter(ImageFilter.GaussianBlur(sc(16))))
        img.paste(fg.filter(ImageFilter.GaussianBlur(sc(3))), (0, 0), fg.filter(ImageFilter.GaussianBlur(sc(3))))
    return img

def draw_cast(img, players):
    shd = Image.new("RGBA", img.size, (0, 0, 0, 0)); sdd = ImageDraw.Draw(shd)
    for hx, hy, d, lean, k, st in players:
        gy = hy + 122 * k; w = 120 * k
        sdd.ellipse([P((hx - w, gy - 12)), P((hx + w, gy + 16))], fill=(0, 0, 0, 120))
    img.paste(shd.filter(ImageFilter.GaussianBlur(sc(9))), (0, 0), shd.filter(ImageFilter.GaussianBlur(sc(9))))
    rim = Image.new("RGBA", img.size, (0, 0, 0, 0)); dark = Image.new("RGBA", img.size, (0, 0, 0, 0))
    rd, dd = ImageDraw.Draw(rim), ImageDraw.Draw(dark)
    for hx, hy, d, lean, k, st in players:
        skater2(rd, (hx, hy), d, lean, k, 1.0, (150, 195, 255, 255), stance=st)
    for hx, hy, d, lean, k, st in players:
        skater2(dd, (hx, hy), d, lean, k, 1.0, (6, 9, 16, 255), stance=st)
    glow = rim.filter(ImageFilter.GaussianBlur(sc(5)))
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0)); sh.paste(glow, (sc(-5), sc(-4)))
    img.paste(sh, (0, 0), sh); img.paste(dark, (0, 0), dark)

def cover_scene(R, kind, theme):
    img = backdrop(R, theme, R.randint(540, 600), smooth=(kind == "puck"))
    players = []
    if kind == "rush":
        n = R.randint(3, 5); dirn = R.choice([1, -1])
        xs = [int(110 + i * (860 / (n - 1))) + R.randint(-25, 25) for i in range(n)]
        for x in xs:
            k = R.uniform(0.6, 0.95); g = 560 + (k - 0.6) * 480
            d = dirn if R.random() > 0.25 else -dirn
            st = "def" if (d != dirn and R.random() > 0.4) else "skate"
            players.append((x, g - 122 * k, d, R.uniform(0.1, 0.62), k, st))
    elif kind == "line":
        dirn = R.choice([1, -1]); k = R.uniform(0.85, 1.0)
        for i, x in enumerate((220, 540, 860)):
            kk = k - 0.06 * abs(i - 1)
            players.append((x + R.randint(-30, 30), 700 - 122 * kk + (R.randint(-30, 30)), dirn, R.uniform(0.25, 0.55), kk, "skate"))
    elif kind == "duel":
        k = R.uniform(1.15, 1.35)
        players = [(R.randint(240, 340), 770 - 122 * k, 1, R.uniform(0.3, 0.55), k, "skate"),
                   (R.randint(740, 840), 770 - 122 * k, -1, R.uniform(0.1, 0.35), k, "def")]
    elif kind == "solo":
        k = R.uniform(1.5, 1.75); d = R.choice([1, -1])
        players = [(R.randint(400, 680), 800 - 122 * k, d, R.uniform(0.3, 0.6), k, "skate")]
    if kind == "puck":
        motion_streaks(img, (540, 450), n=30, length=460, ang=R.choice([190, 175, 200]), seed=R.randint(1, 99))
        spray(img, (R.randint(600, 760), 520), R.choice([10, -10, 25]), 30, 300, 30, 220, seed=R.randint(1, 99))
        puck(img, (R.randint(430, 650), R.randint(400, 480)), r=R.randint(105, 140), tilt=R.uniform(0.36, 0.5))
    else:
        draw_cast(img, players)
        for hx, hy, d, lean, k, st in R.sample(players, min(2, len(players))):
            spray(img, (hx - d * 20, hy + 122 * k + 6), 180 if d > 0 else 0, 30, 380, 30, 220, seed=R.randint(1, 99), glow=R.random() > 0.5)
    return img


_ASSET = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "player_icon.png")

def grad_bg(R, theme):
    top = {"blue": (5, 7, 13), "deep": (5, 7, 13), "ice": (6, 10, 22), "steel": (5, 8, 16), "royal": (5, 8, 18)}[theme]
    bot = {"blue": (11, 31, 58), "deep": (8, 22, 48), "ice": (22, 52, 104), "steel": (14, 30, 62), "royal": (16, 44, 108)}[theme]
    img = Image.new("RGB", (sc(W), sc(H)))
    g = ImageDraw.Draw(img)
    flip = R.random() < 0.5
    for y in range(sc(H)):
        t = y / sc(H)
        if flip: t = 1 - t
        t = t ** 1.1
        g.line([(0, y), (sc(W), y)], fill=tuple(int(top[k] + (bot[k] - top[k]) * t) for k in range(3)))
    # soft diagonal light beams
    bm = Image.new("L", img.size, 0); bd = ImageDraw.Draw(bm)
    for _ in range(R.randint(2, 4)):
        x0 = R.randint(-200, 1100); w = R.randint(60, 200)
        bd.polygon([P((x0, -50)), P((x0 + w, -50)), P((x0 + w - 520, H + 50)), P((x0 - 520, H + 50))], fill=R.randint(8, 20))
    bm = bm.filter(ImageFilter.GaussianBlur(sc(40)))
    img.paste(Image.new("RGB", img.size, (190, 215, 255)), (0, 0), bm)
    # ice trails: thin faint horizontal strokes
    tr = Image.new("RGBA", img.size, (0, 0, 0, 0)); td = ImageDraw.Draw(tr)
    for _ in range(R.randint(10, 18)):
        y = R.randint(120, 1220); x = R.randint(-100, 900); L = R.randint(120, 520)
        td.line([P((x, y)), P((x + L, y + R.randint(-6, 6)))], fill=(150, 190, 255, R.randint(10, 28)), width=sc(R.choice([2, 3, 5])))
    img.paste(tr.filter(ImageFilter.GaussianBlur(sc(1.2))), (0, 0), tr.filter(ImageFilter.GaussianBlur(sc(1.2))))
    # vignette
    vg = Image.new("L", img.size, 0); vd = ImageDraw.Draw(vg)
    vd.rectangle([0, 0, sc(W), sc(H)], fill=170)
    vd.ellipse([P((-180, -120)), P((W + 180, H + 120))], fill=0)
    vg = vg.filter(ImageFilter.GaussianBlur(sc(160)))
    img.paste(Image.new("RGB", img.size, BG), (0, 0), vg)
    return img

def centered_lines(d, y, txt, f_, fill, maxw, lh):
    words, lines, cur = txt.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f_) / S <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    for l in lines:
        d.text((sc(540), sc(y)), l, font=f_, fill=fill, anchor="ma"); y += lh
    return y

def cover_special(R, kind, theme, c):
    img = grad_bg(R, theme)
    if kind == "text":
        # soft bokeh at the top, like the account's text-only covers
        bk = Image.new("RGBA", img.size, (0, 0, 0, 0)); bd = ImageDraw.Draw(bk)
        for _ in range(R.randint(5, 9)):
            x, y, r_ = R.randint(80, 1000), R.randint(40, 520), R.randint(24, 80)
            bd.ellipse([P((x - r_, y - r_)), P((x + r_, y + r_))], fill=(70, 120, 235, R.randint(26, 70)))
        bk = bk.filter(ImageFilter.GaussianBlur(sc(14)))
        img.paste(bk, (0, 0), bk)
    else:
        icon = Image.open(_ASSET).convert("RGBA")
        iw = R.randint(400, 560); ih = int(icon.height * iw / icon.width)
        icon = icon.resize((sc(iw), sc(ih)), Image.LANCZOS)
        if R.random() < 0.5: icon = icon.transpose(Image.FLIP_LEFT_RIGHT)
        icon = icon.rotate(R.uniform(-9, 9), expand=True, resample=Image.BICUBIC)
        half = max(icon.height, icon.width) / S / 2
        cy = R.randint(260, 460); cy = min(max(cy, 160 + half), 760 - half)
        cx = R.randint(380, 700)
        glow = Image.new("RGBA", icon.size, (255, 255, 255, 0)); glow.putalpha(icon.getchannel("A").point(lambda v: int(v * 0.4)))
        gl = Image.new("RGBA", img.size, (0, 0, 0, 0)); gl.paste(glow, (sc(cx) - icon.width // 2, sc(cy) - icon.height // 2))
        gb = gl.filter(ImageFilter.GaussianBlur(sc(14)))
        img.paste(gb, (0, 0), gb)
        img.paste(icon, (sc(cx) - icon.width // 2, sc(cy) - icon.height // 2), icon)
    return img

_c = _SPEC["cover"]; _R = _r.Random(_c.get("seed", 1)); _kind = _c.get("scene", "rush")
if _kind == "center": _kind = "text"
if _kind in ("icon", "text"):
    img = cover_special(_R, _kind, _c.get("theme", "blue"), _c)
else:
    img = cover_scene(_R, _kind, _c.get("theme", "blue"))
darken(img, 700, 930, 238)
d = ImageDraw.Draw(img, "RGBA")
brand(d)
f1, s1 = fit([_c['t1'], _c['t2']], FH, 920, 150)
y = 640 if _kind == "text" else 800
text(d, (80, y), _c['t1'], f1, WHITE)
text(d, (80, y + int(s1 * 1.02)), _c['t2'], f1, BLUE2)
para(d, 80, y + int(s1 * 2.2), _c['sub'], font(FB, 31), GREY, 900, 42)
d.line([P((80, 1252)), P((200, 1252))], fill=BLUE, width=sc(6))
text(d, (80, 1268), _c['foot'], font(FBB, 28), WHITE)
text(d, (1000, 1262), "→", font(FH, 44), BLUE2, "ra")
save(img, "01_cover.png")

# ===== CTA =====
_R2 = _r.Random(_c.get("seed", 1) + 101)
img = backdrop(_R2, _c.get("cta_theme", _R2.choice(list(THEMES))), 640)
motion_streaks(img, (540, 470), n=30, length=460, ang=_R2.choice([190, 175, 205]), seed=_R2.randint(1, 99))
spray(img, (_R2.randint(600, 780), 520), _R2.choice([10, -8, 22]), 30, 300, 30, 220, seed=_R2.randint(1, 99))
puck(img, (_R2.randint(400, 680), _R2.randint(400, 500)), r=_R2.randint(105, 140), tilt=_R2.uniform(0.36, 0.5))
darken(img, 640, 900, 240)
d = ImageDraw.Draw(img, "RGBA")
brand(d)
f1, s1 = fit([_SPEC['cta']['t1'], _SPEC['cta']['t2']], FH, 920, 110)
y = 700
text(d, (80, y), _SPEC['cta']['t1'], f1, WHITE)
text(d, (80, y + int(s1 * 1.02)), _SPEC['cta']['t2'], f1, BLUE2)
para(d, 80, y + int(s1 * 2.2), _SPEC['cta']['sub'], font(FB, 31), GREY, 900, 42)
bx = 80; by = 1060
fb = font(FBB, 36); tw = d.textlength(_SPEC['cta']['btn'], font=fb) / S
d.rounded_rectangle([P((bx, by)), P((bx + tw + 80, by + 84))], radius=sc(42), fill=BLUE)
text(d, (bx + 40, by + 17), _SPEC['cta']['btn'], fb, WHITE)
text(d, (80, 1262), "@alex__analytics", font(FBB, 30), GREY)
save(img, "04_cta.png")
