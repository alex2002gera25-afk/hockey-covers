import sys, json, os, textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S=2; W,H=1080,1350
FH="/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"
FB="/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FBB="/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FM="/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"
BLUE=(63,130,255); WHITE=(255,255,255); GREY=(154,163,178)
def f(p,s): return ImageFont.truetype(p,int(s*S))
def bg():
    im=Image.new("RGB",(W*S,H*S),(5,7,13)); d=ImageDraw.Draw(im)
    for y in range(H*S):
        t=y/(H*S); d.line([(0,y),(W*S,y)],fill=(int(5+6*t),int(7+14*t*(1-t)*4),int(13+30*t*(1-t)*4)))
    return im
def wrap(d,txt,font,maxw):
    out=[];line=""
    for w in txt.split():
        t=(line+" "+w).strip()
        if d.textlength(t,font=font)<=maxw*S: line=t
        else: out.append(line); line=w
    if line: out.append(line)
    return out
def text(d,x,y,txt,font,fill,maxw=920,lh=1.22):
    for l in wrap(d,txt,font,maxw):
        d.text((x*S,y*S),l,font=font,fill=fill); y+=font.size/S*lh
    return y
def brand(d):
    d.rectangle([80*S,70*S,98*S,88*S],fill=BLUE); d.text((112*S,66*S),"ALEX ANALYTICS",font=f(FM,26),fill=WHITE)
def finish(im,path): im.resize((W,H),Image.LANCZOS).save(path)
def player(d,x,y,col,stick=1):
    d.ellipse([(x-20)*S,(y-11)*S,(x+20)*S,(y+11)*S],fill=col)
    d.ellipse([(x-6)*S,(y-6)*S,(x+6)*S,(y+4)*S],fill=(10,20,50) if col==BLUE else (120,130,150))
    d.line([(x+22*stick)*S,(y-18)*S,(x+30*stick)*S,(y+14)*S],fill=(220,225,235),width=3*S)
def boards(d,y0,y1):
    d.rounded_rectangle([60*S,y0*S,W*S-60*S,y1*S],radius=40*S,fill=(14,38,78),outline=(190,205,235),width=5*S)
    d.line([(60*S,(y1-70)*S),(W*S-60*S,(y1-70)*S)],fill=(40,95,220),width=14*S)
    for x in (230,540,850): d.line([(x*S,(y0+10)*S),(x*S,(y1-80)*S)],fill=(120,40,55),width=4*S)
def pill(d,x,y,txt):
    fnt=f(FBB,38); w=d.textlength(txt,font=fnt)/S
    d.rounded_rectangle([x*S,y*S,(x+w+80)*S,(y+84)*S],radius=42*S,fill=BLUE)
    d.text(((x+40)*S,(y+17)*S),txt,font=fnt,fill=WHITE)

def cover(p,c):
    im=bg(); d=ImageDraw.Draw(im); brand(d)
    boards(d,130,820)
    # bench gate on the boards + players
    d.rectangle([400*S,738*S,680*S,758*S],fill=(11,31,58))
    d.text((440*S,780*S),'СКАМЕЙКА',font=f(FM,26),fill=(150,170,210))
    for x,y,col,s in [(300,330,WHITE,1),(520,430,BLUE,1),(760,300,WHITE,-1),(640,620,BLUE,1),(400,560,WHITE,1),(560,760,BLUE,1)]: player(d,x,y,col,s)
    d.ellipse([(515)*S,(748)*S,(605)*S,(772)*S],outline=BLUE,width=4*S)
    d.line([(560*S),(745*S),(540*S),(560*S)],fill=BLUE,width=5*S)
    y=text(d,80,860,c["t1"],f(FH,84),WHITE,920,1.08)
    y=text(d,80,y,c["t2"],f(FH,84),BLUE,920,1.08)
    text(d,80,y+14,c["sub"],f(FB,36),GREY,900,1.3)
    d.rectangle([80*S,1250*S,200*S,1254*S],fill=BLUE)
    d.text((80*S,1268*S),c["foot"],font=f(FBB,32),fill=WHITE); d.text((970*S,1268*S),"→",font=f(FBB,40),fill=BLUE)
    finish(im,p)
def rich(d,x,y,txt,font,maxw,lh,base,hi):
    import re
    toks=[]  # (word, highlighted, space_before)
    prev_trail=False
    for i,part in enumerate(txt.split("**")):
        first=True
        for m in re.finditer(r'(\s*)(\S+)',part):
            sb = bool(m.group(1)) or (first and prev_trail and bool(toks))
            toks.append([m.group(2), i%2==1, sb]); first=False
        if part: prev_trail = part[-1].isspace()
    # glue: a token directly after a marker (no whitespace) has no space before
    sp=d.textlength(" ",font=font)/S
    lines=[];cur=[];curw=0
    for w,h,sb in toks:
        ww=d.textlength(w,font=font)/S; add=(sp if (sb and cur) else 0)
        if cur and sb and curw+add+ww>maxw: lines.append(cur);cur=[];curw=0;add=0
        cur.append((w,h,add)); curw+=add+ww
    if cur: lines.append(cur)
    for ln in lines:
        xx=x
        for w,h,add in ln:
            xx+=add; d.text((xx*S,y*S),w,font=font,fill=hi if h else base); xx+=d.textlength(w,font=font)/S
        y+=lh
    return y
def cards(p,c):
    im=bg(); d=ImageDraw.Draw(im); brand(d)
    y=text(d,80,170,c["title"],f(FH,72),WHITE,920,1.1)
    text(d,80,y+8,c["sub"],f(FB,34),GREY,920,1.3)
    y=430
    for i,(h,b) in enumerate(c["items"],1):
        d.rounded_rectangle([80*S,y*S,1000*S,(y+262)*S],radius=28*S,fill=(11,31,58),outline=(40,70,130),width=2*S)
        d.ellipse([110*S,(y+28)*S,170*S,(y+88)*S],fill=BLUE); d.text((128*S,(y+34)*S),str(i),font=f(FH,40),fill=WHITE)
        text(d,200,y+28,h,f(FBB,38),WHITE,770,1.15)
        rich(d,200,y+92,b,f(FB,31),770,42,(190,200,218),(63,130,255))
        y+=286
    finish(im,p)
def cta(p,c):
    im=bg(); d=ImageDraw.Draw(im); brand(d)
    for k in range(3):
        d.arc([(140+k*60)*S,(200+k*40)*S,(940-k*60)*S,(1100-k*40)*S],200,340,fill=(30,60,120),width=3*S)
    y=text(d,80,560,c["t1"],f(FH,78),WHITE,920,1.1)
    y=text(d,80,y,c["t2"],f(FH,78),BLUE,920,1.1)
    y=text(d,80,y+20,c["sub"],f(FB,36),GREY,900,1.3)
    pill(d,80,y+50,c["btn"])
    d.text((80*S,1250*S),"@alex__analytics",font=f(FBB,34),fill=GREY)
    finish(im,p)
if __name__=="__main__":
    spec=json.load(open(sys.argv[1])); out=sys.argv[2]; os.makedirs(out,exist_ok=True)
    cover(f"{out}/01_cover.png",spec["cover"]); cards(f"{out}/02_video.png",spec["s2"])
    cards(f"{out}/03_moments.png",spec["s3"]); cta(f"{out}/04_cta.png",spec["cta"])
