#!/usr/bin/env python3
"""Original broadsheet renderer for news-image-20261122.
Written in-session 2026-11-22. PIL + Noto Serif / DejaVu Serif TTF.
Deterministic: no clock, no randomness. Output entry.png 1024x1024.
"""
from PIL import Image, ImageDraw, ImageFont
import textwrap, os

W = H = 1024
PAPER = (247, 243, 232)
INK = (18, 18, 18)
RED = (178, 24, 24)
GREY = (90, 90, 90)
RULE = (40, 40, 40)
LIGHT = (235, 229, 214)
BLUE = (30, 64, 110)
TEAL = (18, 110, 100)
GOLD = (184, 134, 11)

SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-BoldItalic.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def F(path, size):
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def wrap(text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def draw_wrap(x, y, text, font, max_w, fill=INK, leading=2, max_lines=4):
    lines = wrap(text, font, max_w)[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += font.size + leading
    return y

def badge(x, y, n):
    d.ellipse([x, y, x+22, y+22], fill=RED)
    f = F(SANS_B, 11)
    t = str(n)
    tw = d.textlength(t, font=f)
    d.text((x + (22-tw)/2, y+4), t, font=f, fill=(255,255,255))

def rule(x1, y, x2, wdt=1, col=RULE):
    d.line([x1, y, x2, y], fill=col, width=wdt)

# ---------- masthead ----------
d.rectangle([0,0,W,6], fill=RED)
f_kick = F(SANS_B, 10)
d.text((18,12), "THE DAY IN WORLD NEWS  ·  ONE PICTURE  ·  SUNDAY EDITION", font=f_kick, fill=RED)
d.text((760,12), "52 STORIES · 7 REGIONS", font=f_kick, fill=INK)
f_date = F(SERIF_B, 38)
d.text((18,28), "Sunday 22 November 2026", font=f_date, fill=INK)
f_sub = F(SERIF_I, 12)
d.text((18,72), "Every story here happened or was first reported on this Sunday, in some time zone.", font=f_sub, fill=GREY)
f_cnt = F(SANS_B, 11)
d.text((640,74), "EVERY ONE FROM THIS SUNDAY", font=f_cnt, fill=RED)
rule(18, 92, 1006, 2)
rule(18, 96, 1006, 1)

# ---------- UTC timeline ----------
y0 = 102
d.text((18,y0), "THE DAY SO FAR IN UTC", font=F(SANS_B,9), fill=RED)
d.text((210,y0), "first reports, Sunday 00:00-02:00 UTC  ·  Europe & the Americas still to come", font=F(SANS,8), fill=GREY)
axis_y = y0+28
d.line([30,axis_y,990,axis_y], fill=INK, width=1)
for hr in range(0,25,4):
    x = 30 + hr/24*960
    d.line([x,axis_y-4,x,axis_y+4], fill=INK, width=1)
    d.text((x-10,axis_y+6), f"{hr:02d}:00", font=F(SANS,7), fill=GREY)
events = [
    (0.27, "00:16 Trump: permanent\nIran deal"),
    (0.68, "00:41 Pant 100,\nIndia 629-6"),
    (0.95, "00:57 BBC world\nlist published"),
    (1.05, "01:03 Gaza strikes\nreported"),
    (1.17, "01:10 Hegseth on\nCanada defence"),
]
label_x = [18, 150, 280, 410, 540]
for idx,(hr, label) in enumerate(events):
    x = 30 + hr/24*960
    if hr < 3:
        d.ellipse([x-4,axis_y-4,x+4,axis_y+4], fill=RED)
        lx = label_x[idx]
        d.line([x,axis_y+4,lx+20,y0+40], fill=GREY, width=1)
        yy = y0+42
        for ln in label.split("\n"):
            d.text((lx, yy), ln, font=F(SANS,7), fill=INK); yy+=9
    else:
        d.ellipse([x-4,axis_y-4,x+4,axis_y+4], outline=RED, width=1)
        d.text((x-30, y0+42), "09:00 Miliband", font=F(SANS,7), fill=GREY)
        d.text((x-30, y0+51), "Sunday interview*", font=F(SANS,7), fill=GREY)
d.text((720, y0+42), "Later Sunday: Miliband Sunday interview (09:00 UTC)*", font=F(SANS,7), fill=GREY)
rule(18, 168, 1006, 1)

# ---------- heroes ----------
heroes = [
    (1, "GLOBAL · CLIMATE", "COP31 in Antalya deadlocked past its deadline",
     "Nearly 200 countries, no deal. EU's Hoekstra: \"good deal or no deal.\" Draft dropped fossil-fuel language and a $120bn adaptation target. Talks in overtime.",
     "CONFIRMED · BBC / REUTERS", "earth"),
    (2, "MIDDLE EAST · GULF", "Bahrain says Iranian attack set industrial site ablaze",
     "Interior Ministry: fire, material damage, no injuries; smoke over Sitra. IRGC claims missile-drone strike on US bases, 2 Patriot radars destroyed.",
     "REPORTED · REUTERS / AFP", "flame"),
    (3, "MIDDLE EAST · IRAN", "Trump wants a \"permanent\" Iran nuclear deal",
     "Fox interview, 22 Nov 00:16 UTC. Araghchi: Hormuz can reopen on Iran's \"reasonable conditions\"; uranium stays in Iran. 2 tankers hit near Oman.",
     "CONFIRMED · FOX / UKMTO", "ship"),
    (4, "OCEANIA · CRICKET", "Pant's 9th Test hundred powers India to 629-6",
     "Wellington, Day 4 lunch: India lead NZ by 261, highest India tally in NZ (beat 520, 2009). Pant 100 with a six; Duffy 1-201. NZ made 368.",
     "CONFIRMED · REUTERS", "bat"),
]

def icon(kind, x, y, w, h):
    # simple flat original drawings
    if kind == "earth":
        d.ellipse([x+30,y+5,x+30+70,y+5+52], fill=(120,180,220), outline=INK)
        d.ellipse([x+45,y+15,x+75,y+35], fill=(90,170,90))
        d.ellipse([x+70,y+30,x+95,y+48], fill=(90,170,90))
        d.line([x+10,y+62,x+120,y+62], fill=RED, width=3)
    elif kind == "flame":
        d.rectangle([x+20,y+35,x+110,y+62], fill=(120,120,120), outline=INK)
        d.rectangle([x+85,y+15,x+100,y+35], fill=(100,100,100), outline=INK)
        for dx in (35,55,75):
            d.polygon([(x+dx,y+35),(x+dx+8,y+12),(x+dx+16,y+35)], fill=(230,120,20))
            d.polygon([(x+dx+4,y+35),(x+dx+8,y+22),(x+dx+12,y+35)], fill=(250,200,40))
    elif kind == "ship":
        d.rectangle([x+15,y+40,x+115,y+58], fill=BLUE)
        d.polygon([(x+115,y+40),(x+130,y+58),(x+115,y+58)], fill=BLUE)
        d.rectangle([x+40,y+22,x+90,y+40], fill=(200,60,40), outline=INK)
        d.line([x+10,y+64,x+130,y+64], fill=TEAL, width=3)
    elif kind == "bat":
        d.ellipse([x+55,y+8,x+85,y+38], fill=(200,40,40), outline=INK)
        d.rectangle([x+30,y+30,x+45,y+62], fill=(210,180,120), outline=INK)
        d.text((x+88,y+18), "100", font=F(SERIF_B,16), fill=RED)
    elif kind == "bridge":
        d.line([x+5,y+45,x+125,y+45], fill=INK, width=3)
        d.line([x+20,y+45,x+20,y+15], fill=INK, width=2); d.line([x+110,y+45,x+110,y+15], fill=INK, width=2)
        d.line([x+20,y+15,x+110,y+15], fill=RED, width=2)
        d.line([x+5,y+60,x+125,y+60], fill=TEAL, width=3)
    elif kind == "radar":
        d.ellipse([x+35,y+5,x+95,y+55], outline=INK, width=2)
        d.ellipse([x+50,y+15,x+80,y+45], outline=GREY, width=1)
        d.line([x+65,y+30,x+90,y+12], fill=RED, width=2)
        d.ellipse([x+62,y+27,x+68,y+33], fill=RED)
    elif kind == "chart":
        for i,hh in enumerate([45,35,25,12]):
            d.rectangle([x+15+i*28, y+62-hh, x+35+i*28, y+62], fill=RED if i>1 else BLUE)
        d.line([x+10,y+62,x+125,y+62], fill=INK, width=2)
    elif kind == "flag":
        d.line([x+30,y+5,x+30,y+62], fill=INK, width=3)
        d.rectangle([x+30,y+8,x+90,y+32], fill=(30,80,160))
        d.text((x+38,y+13), "EU", font=F(SANS_B,12), fill=(255,255,255))
    elif kind == "ship2":
        d.rectangle([x+15,y+38,x+110,y+56], fill=(60,60,60))
        for dx in (40,60,80):
            d.polygon([(x+dx,y+38),(x+dx+6,y+18),(x+dx+12,y+38)], fill=(230,120,20))
        d.line([x+10,y+62,x+125,y+62], fill=TEAL, width=3)
    elif kind == "mask":
        d.ellipse([x+35,y+8,x+95,y+55], fill=(240,220,180), outline=INK)
        d.ellipse([x+50,y+25,x+60,y+35], fill=INK); d.ellipse([x+72,y+25,x+82,y+35], fill=INK)
    elif kind == "march":
        for dx in (20,45,70,95):
            d.ellipse([x+dx,y+18,x+dx+14,y+32], fill=INK)
            d.line([x+dx+7,y+32,x+dx+7,y+55], fill=INK, width=3)
        d.rectangle([x+15,y+5,x+115,y+16], fill=RED)
    elif kind == "bridge2":
        d.arc([x+10,y+10,x+120,y+70], 180, 360, fill=INK, width=3)
        d.line([x+10,y+45,x+120,y+45], fill=INK, width=3)
        d.line([x+10,y+62,x+120,y+62], fill=TEAL, width=3)
    else:
        d.rectangle([x+20,y+15,x+110,y+55], outline=INK, width=2)
        d.text((x+45,y+28), "NEWS", font=F(SANS_B,12), fill=RED)

hx = 18
hy = 176
hw = 242
for (n, tag, head, dek, verif, ic) in heroes:
    d.rectangle([hx,hy,hx+hw,hy+188], outline=RULE, width=1)
    badge(hx+6, hy+6, n)
    d.text((hx+34, hy+9), tag, font=F(SANS_B,8), fill=RED)
    icon(ic, hx+55, hy+28, 130, 70)
    yy = hy+102
    yy = draw_wrap(hx+8, yy, head, F(SERIF_B,13), hw-16, leading=1, max_lines=2)
    yy = draw_wrap(hx+8, yy+2, dek, F(SERIF,8), hw-16, fill=(40,40,40), leading=1, max_lines=4)
    d.text((hx+8, hy+172), verif, font=F(SANS_B,7), fill=BLUE)
    hx += hw + 7

# ---------- panels ----------
panels = [
    (5,"EUROPE · UKRAINE","Zelensky: bridge strikes a \"fair response\"","Kyiv acted after 109 Russian attacks on Ukrainian bridges, he told BBC, meeting UK's Streeting in Kyiv.","CONFIRMED · BBC","bridge"),
    (6,"EUROPE · BALTIC","Sparta II hit by 2 drones in Gulf of Finland","Russian cargo ship ablaze, drifted into Finnish waters; 16 crew evacuated. Finland: likely Ukraine.","REPORTED · REUTERS","ship2"),
    (7,"N. AMERICA · CYBER","FBI probes apparent hack of NCIC crime database","2nd breach in months. NCIC shares warrants & records with local, state, federal police. FBI declined comment.","REPORTED · AP / CNN","radar"),
    (8,"LATIN AMERICA · MEXICO","\"El Chapo Isidro\" captured in Sinaloa shoot-out","FBI Top 10, $5m reward. Fausto Isidro Meza-Flores, 44, taken with 2 lieutenants; 8 arrested, gunfire in Guasave.","CONFIRMED · REUTERS","flag"),
    (9,"MIDDLE EAST · GAZA","Gaza strikes reported despite Oct 2025 ceasefire","Civil defence: 6 killed Fri near Bureij, Deir al-Balah, Nuseirat (AFP). Board of Peace warns truce risks collapse.","CLAIM · AFP / AP","flame"),
    (10,"EUROPE · UKRAINE","Kryvyi Rih missile attack kills 2, wounds 60","Ballistic strike on Zelensky's hometown; a 7-year-old boy among dead, BBC/NY Post report overnight.","REPORTED · BBC","bridge"),
    (11,"MARKETS · TECH","Nasdaq -5.28% wipes out all its 2026 gains","S&P -3.7% (7th down day), Dow -950. Anthropic -8.5% to $88.91 after $83 IPO; Nvidia -14% Friday.","CONFIRMED · CNN","chart"),
    (12,"EUROPE · UK-EU","Miliband: EU deal not hostage to tuition fees","Sunday interview: 100,000 youth visas/yr (18-31); fees row £38,000 vs £9,970 separate. Deal from 2028.","CONFIRMED · BBC","flag"),
    (13,"EUROPE · DENMARK","Denmark accuses Russia of plot to kill rapper","PET: plot vs Kyivstoner foiled 25 Sep; 2 charged. Defence attaché expelled in 7 days. Russia denies.","CLAIM · PET / BBC","mask"),
    (14,"EUROPE · PORTUGAL","Thousands march in Lisbon over living costs","CGTP union march in heavy rain Saturday; wages, pensions, housing. Earnings 37% below EU average.","CONFIRMED · REUTERS","march"),
    (15,"SOUTH ASIA · INDIA","Modi opens 19.7 km Nitish Setu over the Ganga","Six-lane Patna-Vaishali bridge, ₹4,280 crore; ₹34,470 crore Bihar projects launched in Vaishali.","CONFIRMED · NDTV / IANS","bridge2"),
    (16,"MIDDLE EAST · ISRAEL","Eisenkot invites Likud to coalition talks","Ex-PM backs Gadi Eisenkot for PM, says he won't serve under Netanyahu, India Today reported Sun 01:13 IST.","REPORTED · INDIA TODAY","flag"),
]
px, py = 18, 372
pw, ph = 242, 100
for i,(n,tag,head,dek,verif,ic) in enumerate(panels):
    col = i % 4; row = i // 4
    x = px + col*(pw+7); y = py + row*(ph+5)
    d.rectangle([x,y,x+pw,y+ph], outline=RULE, width=1)
    badge(x+5,y+5,n)
    d.text((x+32,y+8), tag, font=F(SANS_B,7), fill=RED)
    # small coloured rule instead of a drawing, to keep text clean
    d.rectangle([x+7,y+22,x+60,y+25], fill=RED)
    yy = y+28
    yy = draw_wrap(x+7, yy, head, F(SERIF_B,10), pw-14, leading=1, max_lines=2)
    yy = draw_wrap(x+7, yy+1, dek, F(SERIF,7), pw-14, fill=(45,45,45), leading=1, max_lines=3)
    d.text((x+7, y+ph-13), verif, font=F(SANS_B,6), fill=BLUE)

# ---------- map + date check ----------
my = 372 + 3*(100+5) + 6
d.text((18,my), "WHERE IT HAPPENED", font=F(SANS_B,9), fill=RED)
# simple world map: continents as blobs
mx, myy, mw, mh = 18, my+14, 490, 100
d.rectangle([mx,myy,mx+mw,myy+mh], fill=(220,232,240), outline=RULE)
# continents (rough original shapes)
d.polygon([(mx+30,myy+25),(mx+110,myy+18),(mx+125,myy+55),(mx+85,myy+70),(mx+45,myy+60)], fill=(180,200,160), outline=GREY) # N America
d.polygon([(mx+95,myy+75),(mx+130,myy+72),(mx+135,myy+115),(mx+110,myy+122)], fill=(180,200,160), outline=GREY) # S America
d.polygon([(mx+215,myy+20),(mx+265,myy+18),(mx+270,myy+45),(mx+230,myy+50)], fill=(180,200,160), outline=GREY) # Europe
d.polygon([(mx+225,myy+55),(mx+275,myy+52),(mx+285,myy+95),(mx+250,myy+115),(mx+230,myy+90)], fill=(210,190,140), outline=GREY) # Africa
d.polygon([(mx+280,myy+20),(mx+400,myy+18),(mx+430,myy+55),(mx+360,myy+70),(mx+300,myy+60)], fill=(180,200,160), outline=GREY) # Asia
d.polygon([(mx+395,myy+85),(mx+445,myy+82),(mx+450,myy+108),(mx+410,myy+112)], fill=(210,190,140), outline=GREY) # Oceania
pins = [(1,300,35),(2,320,55),(3,315,48),(4,435,95),(5,255,30),(6,250,22),(7,70,38),(8,55,62),(9,295,52),(11,75,42),(12,235,28),(15,355,55)]
for n,dx,dy in pins:
    x,y = mx+dx, myy+dy
    d.ellipse([x-7,y-7,x+7,y+7], fill=RED, outline=(255,255,255))
    f=F(SANS_B,7); t=str(n); tw=d.textlength(t,font=f)
    d.text((x-tw/2,y-4), t, font=f, fill=(255,255,255))
d.text((mx+8,myy+mh-14), "Pins = panel numbers  ·  1 Antalya  2 Bahrain  4 Wellington  6 Gulf of Finland  8 Sinaloa  15 Bihar", font=F(SANS,7), fill=INK)

# date check
dx0 = 520
d.text((dx0,my), "DATE CHECK — deliberately excluded as older news", font=F(SANS_B,9), fill=RED)
d.rectangle([dx0,my+14,1006,my+14+100], fill=LIGHT, outline=RULE)
excluded = [
    "Peru M6.9 quake, Junin — Fri 20 Nov 19:09 Lima",
    "Iran hits Kuwait Ali Al Salem base — Wed 18 Nov",
    "Crimean Bridge arch destroyed — Tue 17 Nov",
    "Kyiv: 110 missiles + 400 drones, 3 bridges — Fri 20 Nov",
    "Voyager 1 reaches 1 light-day — Wed 18 Nov 10:16 UTC",
    "Virginia measles child death announced — Fri 20 Nov",
    "India-Japan 2+2 live-fire deal, Tokyo — Thu 19 Nov",
    "Estonia to shut Russia border from 1 Dec — decided Fri 20 Nov",
    "Palisades fire arson conviction, LA — verdict Fri 20 Nov",
]
yy = my+19
for e in excluded:
    d.text((dx0+8,yy), "×  "+e, font=F(SERIF,8), fill=INK); yy+=12

# ---------- briefs ----------
by = my+14+100+8
d.text((18,by), "ALSO ON SUNDAY 22 NOVEMBER — 36 briefs, grouped by region", font=F(SANS_B,9), fill=RED)
rule(18,by+14,1006,1)
brief_cols = [
    [("AMERICAS", [
        (17,"Judge OKs $7.25bn Bayer Roundup settlement"),
        (18,"Washington lock of hair sells for $4,000"),
        (19,"Teen gamer Tresp, 16, helps FBI rescue girl"),
        (20,"Hegseth sets US-Canada defence limits"),
        (21,"US measles >5,800 cases, most since 1991"),
        (22,"S. Korea repeats $75,000 exam-cheat bounty"),
    ]), ("EUROPE", [
        (23,"French police sentenced, Zecler beating"),
        (24,"Italy 24h general strike (CGIL), Rome"),
        (25,"Real Madrid 2-1 Celta; Newcastle 2-2 Arsenal"),
        (26,"Napoli 1-0 Torino; Lyon 1-0 at Lille"),
        (27,"France 45-17 Argentina, Nations final"),
        (28,"Anthropic: AI proof of Riemann claimed"),
    ])],
    [("AFRICA · MIDDLE EAST", [
        (29,"ANC 30.8% (was 45.6%) fights for SA cities"),
        (30,"Nigeria youth voter sign-ups fall vs 2023"),
        (31,"UNIFIL: S. Lebanon still bears war toll"),
        (32,"Lieberman: oust Netanyahu, top objective"),
        (33,"Two tankers hit off Oman, UKMTO says"),
        (34,"Crude futures -3%+ to Rs 7,842/barrel"),
    ]), ("ASIA-PACIFIC", [
        (35,"Cyclone Akvan: 14 Ranchi flights cancelled"),
        (36,"Air India Jeddah flights off to 24 Nov"),
        (37,"Philippines pet-cremation livestream row"),
        (38,"Australia 191/7 beat England 187/9 (T20I)"),
        (39,"Pakistan beat Sri Lanka by 8 wkts, Test"),
        (40,"Sri Lanka A 284/9 beat Hong Kong 260/9"),
    ])],
    [("SOUTH ASIA · INDIA", [
        (41,"Chahal joins BJP, OBC Morcha invitee"),
        (42,"ICMR: 100 tech transfers, 20 licences"),
        (43,"Prince William: cover for 10,000 forest staff"),
        (44,"Pakistan's Malik at SCO dialogue, Delhi"),
        (45,"UP cops mistake Owaisi for SC judge"),
        (46,"Chennai Book Fair 2027: 16-18 January"),
    ]), ("SPORT · CULTURE", [
        (47,"Cummins unanimously backed as captain"),
        (48,"Hockey coach Bhangu dies at 86"),
        (49,"Advani, Ramachandran win snooker openers"),
        (50,"MI Emirates 174/8 beat Vipers 122"),
        (51,"Ramayana Part 1: Day 17 box office"),
        (52,"US UFO files: 8th tranche, clips to 2026"),
    ])],
]
def draw_briefs(x, y, groups, colw=320):
    for title, items in groups:
        d.text((x,y), title, font=F(SANS_B,8), fill=RED); y+=12
        for n,t in items:
            d.text((x,y), f"{n}.", font=F(SANS_B,8), fill=INK)
            d.text((x+24,y), t, font=F(SERIF,8), fill=INK)
            y+=10
        y+=4
    return y
draw_briefs(18, by+20, brief_cols[0])
draw_briefs(352, by+20, brief_cols[1])
draw_briefs(686, by+20, brief_cols[2])

# ---------- footer ----------
rule(18, 995, 1006, 1)
d.text((18,1000), "Every story here happened or was first reported on Sunday 22 November 2026. CLAIM = one side's account, not independently confirmed.", font=F(SERIF,7), fill=INK)
d.text((18,1010), "Sources: BBC, Reuters, AP, AFP, CNN, NDTV, The Hindu, India Today, UKMTO, CDC. Original drawings. No photographs.", font=F(SERIF,7), fill=GREY)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, format="PNG", optimize=True)
print(out, os.path.getsize(out))
