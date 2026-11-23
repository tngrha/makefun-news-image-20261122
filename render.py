#!/usr/bin/env python3
"""Broadsheet renderer: 'Sunday 22 November 2026' one-image world news summary.

Original code written for make.fun competition news-image-20261122 (revision 2).
Draws a 1024x1024 front page with PIL and real serif type (Noto Serif):
masthead, UTC timeline, 4 hero panels, 12 small panels, a pinned world map,
36 one-line briefs, a date-check box and a footer. 52 stories, 7 regions.

Run:  python3 render.py [output.png]
"""
import math
import sys

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 18
CW = W - 2 * MARGIN  # content width

PAPER = (247, 243, 234)
INK = (26, 23, 19)
MUTED = (96, 90, 80)
RED = (176, 32, 48)
GREEN = (28, 110, 60)
AMBER = (166, 106, 8)
RULE = (60, 56, 50)
PANEL_BG = (255, 253, 248)

SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_BLACK = "/usr/share/fonts/truetype/noto/NotoSerif-Black.ttf"
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, s, f, max_w):
    """Greedy word wrap; returns list of lines."""
    lines, cur = [], ""
    for word in s.split():
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, f, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=f, fill=fill)
        y += leading
    return y


def badge(draw, cx, cy, r, num):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    f = font(SANS_B, int(r * 1.15))
    s = str(num)
    tw = text_w(draw, s, f)
    draw.text((cx - tw / 2, cy - r * 0.62), s, font=f, fill=(255, 255, 255))


def star(draw, cx, cy, r_out, r_in, fill, points=5, rot=-math.pi / 2):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = rot + i * math.pi / points
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def burst(draw, cx, cy, r, fill):
    """Explosion starburst."""
    star(draw, cx, cy, r, r * 0.45, fill, points=8)


def dashed_line(draw, p0, p1, fill, width=2, dash=6, gap=5):
    x0, y0 = p0
    x1, y1 = p1
    dist = math.hypot(x1 - x0, y1 - y0)
    if dist == 0:
        return
    ux, uy = (x1 - x0) / dist, (y1 - y0) / dist
    t = 0.0
    while t < dist:
        t2 = min(t + dash, dist)
        draw.line([(x0 + ux * t, y0 + uy * t), (x0 + ux * t2, y0 + uy * t2)],
                  fill=fill, width=width)
        t = t2 + gap


# ---------------------------------------------------------------- illustrations
# Each takes (draw, x, y, w, h) and paints a flat scene inside that box.

def illo_thermo(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(252, 236, 205))
    # sun
    sx, sy = x + w * 0.16, y + h * 0.34
    d.ellipse([sx - 13, sy - 13, sx + 13, sy + 13], fill=(240, 160, 40))
    for a in range(0, 360, 45):
        r1, r2 = 17, 24
        d.line([(sx + r1 * math.cos(math.radians(a)), sy + r1 * math.sin(math.radians(a))),
                (sx + r2 * math.cos(math.radians(a)), sy + r2 * math.sin(math.radians(a)))],
               fill=(240, 160, 40), width=3)
    # thermometer
    tx = x + w * 0.42
    d.rounded_rectangle([tx - 7, y + 8, tx + 7, y + h - 22], 7, fill=(255, 255, 255),
                        outline=(90, 90, 90), width=2)
    d.rectangle([tx - 3, y + h * 0.42, tx + 3, y + h - 24], fill=RED)
    d.ellipse([tx - 11, y + h - 26, tx + 11, y + h - 4], fill=RED, outline=(90, 90, 90), width=2)
    # crossed-out pact paper
    px, py = x + w * 0.62, y + 10
    d.rectangle([px, py, px + w * 0.3, py + h - 20], fill=(255, 255, 255), outline=(120, 120, 120), width=2)
    for i in range(4):
        ly = py + 10 + i * 9
        d.line([(px + 6, ly), (px + w * 0.3 - 6, ly)], fill=(170, 170, 170), width=2)
    d.line([(px + 2, py + 2), (px + w * 0.3 - 2, py + h - 22)], fill=RED, width=4)
    d.line([(px + w * 0.3 - 2, py + 2), (px + 2, py + h - 22)], fill=RED, width=4)


def illo_building(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 238))
    bx, bw = x + w * 0.18, w * 0.55
    by, bh = y + 10, h - 18
    d.rectangle([bx, by, bx + bw, by + bh], fill=(196, 178, 150), outline=(110, 96, 74), width=2)
    # collapsed corner
    d.polygon([(bx + bw * 0.62, by), (bx + bw, by + bh * 0.45), (bx + bw, by + bh),
               (bx + bw * 0.62, by + bh)], fill=(150, 132, 104))
    d.polygon([(bx + bw * 0.62, by), (bx + bw, by + bh * 0.45), (bx + bw * 0.7, by + bh * 0.5)],
              fill=(214, 226, 238))
    for r in range(4):
        for c in range(3):
            wx = bx + 8 + c * (bw * 0.28)
            wy = by + 8 + r * (bh * 0.22)
            if c == 2 and r < 2:
                continue
            d.rectangle([wx, wy, wx + 12, wy + 10], fill=(70, 84, 100))
    # rubble + drone
    d.polygon([(bx + bw * 0.55, by + bh), (bx + bw * 1.25, by + bh), (bx + bw * 0.9, by + bh - 12)],
              fill=(120, 108, 88))
    dx, dy = x + w * 0.82, y + h * 0.22
    d.line([(dx - 12, dy), (dx + 12, dy)], fill=(40, 40, 40), width=3)
    d.ellipse([dx - 4, dy - 4, dx + 4, dy + 4], fill=(40, 40, 40))
    for s in (-1, 1):
        d.ellipse([dx + s * 12 - 5, dy - 3, dx + s * 12 + 5, dy + 1], outline=(40, 40, 40), width=2)
    burst(d, bx + bw * 0.78, by + bh * 0.3, 12, (240, 120, 40))


def illo_tanker(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(206, 228, 240))
    sea = y + h * 0.68
    d.rectangle([x, sea, x + w, y + h], fill=(70, 130, 170))
    # tanker hull
    hx = x + w * 0.12
    d.polygon([(hx, sea - 8), (hx + w * 0.62, sea - 8), (hx + w * 0.56, sea + 8), (hx + w * 0.06, sea + 8)],
              fill=(52, 58, 66))
    d.rectangle([hx + w * 0.46, sea - 22, hx + w * 0.56, sea - 8], fill=(240, 240, 240))
    for i in range(3):
        cx = hx + w * (0.1 + i * 0.13)
        d.rectangle([cx, sea - 14, cx + w * 0.09, sea - 8], fill=(120, 130, 140))
    burst(d, hx + w * 0.3, sea - 14, 13, (245, 130, 40))
    d.ellipse([hx + w * 0.3 - 4, sea - 18, hx + w * 0.3 + 4, sea - 10], fill=(200, 60, 30))
    # incoming dashed arc
    dashed_line(d, (x + w * 0.92, y + 8), (hx + w * 0.32, sea - 16), RED, width=2)
    # smoke
    for i, r in enumerate((6, 9, 12)):
        d.ellipse([hx + w * 0.3 - r + i * 6, sea - 30 - i * 8, hx + w * 0.3 + r + i * 6, sea - 30 - i * 8 + r],
                  fill=(150, 150, 150))


def illo_mercury(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 22, 48))
    for (sx, sy) in [(0.08, 0.2), (0.3, 0.12), (0.55, 0.25), (0.8, 0.15), (0.92, 0.4), (0.15, 0.6), (0.7, 0.7)]:
        d.ellipse([x + w * sx - 1.5, y + h * sy - 1.5, x + w * sx + 1.5, y + h * sy + 1.5], fill=(255, 255, 255))
    # Mercury
    mx, my, mr = x + w * 0.34, y + h * 0.55, h * 0.3
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(176, 160, 140))
    for (ox, oy, r) in [(-0.3, -0.2, 0.16), (0.25, 0.3, 0.2), (0.1, -0.45, 0.12)]:
        d.ellipse([mx + ox * mr - r * mr, my + oy * mr - r * mr, mx + ox * mr + r * mr, my + oy * mr + r * mr],
                  fill=(150, 134, 114))
    # orbit + probe
    d.ellipse([mx - mr * 1.9, my - mr * 0.75, mx + mr * 1.9, my + mr * 0.75], outline=(140, 180, 230), width=2)
    px, py = mx + mr * 1.55, my - mr * 0.55
    d.rectangle([px - 5, py - 4, px + 5, py + 4], fill=(230, 230, 230))
    d.rectangle([px - 16, py - 2, px - 6, py + 2], fill=(90, 140, 220))
    d.rectangle([px + 6, py - 2, px + 16, py + 2], fill=(90, 140, 220))
    f = font(SANS_B, 11)
    d.text((x + w * 0.62, y + h * 0.62), "8-YEAR JOURNEY", font=f, fill=(255, 220, 120))


def illo_warship(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 232, 244))
    sea = y + h * 0.66
    d.rectangle([x, sea, x + w, y + h], fill=(64, 122, 164))
    hx = x + w * 0.14
    d.polygon([(hx, sea - 6), (hx + w * 0.66, sea - 6), (hx + w * 0.6, sea + 7), (hx + w * 0.05, sea + 7)],
              fill=(88, 96, 104))
    d.rectangle([hx + w * 0.2, sea - 18, hx + w * 0.34, sea - 6], fill=(110, 118, 126))
    d.rectangle([hx + w * 0.44, sea - 14, hx + w * 0.52, sea - 6], fill=(110, 118, 126))
    burst(d, hx + w * 0.27, sea - 16, 11, (245, 130, 40))
    # sea drone wake
    dashed_line(d, (x + w * 0.94, sea + 6), (hx + w * 0.62, sea + 4), (255, 255, 255), width=2)


def illo_capitol(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 234, 246))
    bx, bw = x + w * 0.1, w * 0.52
    base = y + h - 8
    d.polygon([(bx, y + 16), (bx + bw / 2, y + 4), (bx + bw, y + 16)], fill=(120, 128, 140))
    for i in range(5):
        cx = bx + 6 + i * (bw - 18) / 4
        d.rectangle([cx, y + 18, cx + 5, base - 6], fill=(150, 158, 170))
    d.rectangle([bx - 3, base - 6, bx + bw + 3, base], fill=(120, 128, 140))
    f = font(SERIF_BLACK, 22)
    d.text((x + w * 0.66, y + h * 0.3), "258", font=f, fill=RED)
    f2 = font(SANS_B, 8)
    d.text((x + w * 0.66, y + h * 0.3 + 24), "SEATS", font=f2, fill=MUTED)


def illo_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 240, 244))
    pts = [(0.06, 0.25), (0.3, 0.35), (0.5, 0.5), (0.72, 0.68), (0.92, 0.82)]
    xy = [(x + w * a, y + h * b) for a, b in pts]
    d.line(xy, fill=RED, width=3)
    for (px, py) in xy:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED)
    d.polygon([(xy[-1][0] + 2, xy[-1][1] + 8), (xy[-1][0] - 8, xy[-1][1] - 2), (xy[-1][0] + 8, xy[-1][1] - 4)],
              fill=RED)
    f = font(SERIF_BLACK, 16)
    d.text((x + 8, y + 4), "-3.7%", font=f, fill=RED)
    f2 = font(SANS_B, 7.5)
    d.text((x + 8, y + 24), "S&P 500", font=f2, fill=MUTED)


def illo_star(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 236, 220))
    cx, cy = x + w * 0.36, y + h * 0.52
    d.ellipse([cx - h * 0.34, cy - h * 0.34, cx + h * 0.34, cy + h * 0.34], fill=(212, 168, 60),
              outline=(150, 112, 30), width=2)
    star(d, cx, cy, h * 0.24, h * 0.1, (150, 112, 30))
    f = font(SANS_B, 9)
    d.text((x + w * 0.62, y + h * 0.3), "FBI TOP 10", font=f, fill=(120, 84, 20))
    d.text((x + w * 0.62, y + h * 0.3 + 12), "CAPTURED", font=f, fill=RED)


def illo_factory(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(244, 230, 214))
    base = y + h - 6
    bx = x + w * 0.12
    d.rectangle([bx, y + h * 0.45, bx + w * 0.55, base], fill=(150, 140, 128))
    d.rectangle([bx + w * 0.06, y + h * 0.2, bx + w * 0.13, y + h * 0.45], fill=(120, 110, 98))
    d.polygon([(bx, y + h * 0.45), (bx + w * 0.18, y + h * 0.3), (bx + w * 0.36, y + h * 0.45),
               (bx + w * 0.55, y + h * 0.45)], fill=(170, 158, 142))
    # flames
    for fx in (0.2, 0.32, 0.44):
        cx = bx + w * fx
        d.polygon([(cx - 6, base - 4), (cx, y + h * 0.42), (cx + 6, base - 4)], fill=(240, 110, 30))
        d.polygon([(cx - 3, base - 4), (cx, y + h * 0.55), (cx + 3, base - 4)], fill=(250, 190, 60))
    for i, r in enumerate((5, 7, 9)):
        d.ellipse([bx + w * 0.1 - r + i * 5, y + 2 + i * 2, bx + w * 0.1 + r + i * 5, y + 2 + i * 2 + r],
                  fill=(140, 140, 140))


def illo_car_fire(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 222))
    base = y + h - 10
    cx = x + w * 0.16
    d.rounded_rectangle([cx, base - 16, cx + w * 0.6, base], 4, fill=(70, 74, 82))
    d.polygon([(cx + w * 0.14, base - 16), (cx + w * 0.24, base - 26), (cx + w * 0.42, base - 26),
               (cx + w * 0.5, base - 16)], fill=(70, 74, 82))
    for wx in (0.12, 0.48):
        d.ellipse([cx + w * wx - 6, base - 6, cx + w * wx + 6, base + 6], fill=(30, 30, 34))
    for fx in (0.2, 0.34, 0.48):
        px = cx + w * fx
        d.polygon([(px - 6, base - 12), (px, y + 6), (px + 6, base - 12)], fill=(240, 110, 30))
        d.polygon([(px - 3, base - 12), (px, y + h * 0.35), (px + 3, base - 12)], fill=(250, 190, 60))


def illo_exam(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 238, 230))
    px, py = x + w * 0.18, y + 6
    pw, ph = w * 0.44, h - 12
    d.rectangle([px, py, px + pw, py + ph], fill=(255, 255, 255), outline=(140, 140, 140), width=2)
    for i in range(4):
        ly = py + 8 + i * 8
        d.line([(px + 6, ly), (px + pw - 6, ly)], fill=(180, 180, 180), width=2)
    f = font(SERIF_BLACK, 15)
    d.text((px + pw * 0.3, py + ph * 0.55), "AI", font=f, fill=RED)
    # red pen slash
    d.line([(px + pw * 0.2, py + ph * 0.85), (px + pw * 0.8, py + ph * 0.5)], fill=RED, width=3)
    f2 = font(SANS_B, 8.5)
    d.text((x + w * 0.68, y + h * 0.38), "MINISTER", font=f2, fill=MUTED)
    d.text((x + w * 0.68, y + h * 0.38 + 11), "RESIGNS", font=f2, fill=RED)


def illo_moto(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(252, 240, 214))
    base = y + h - 10
    for wx in (0.22, 0.62):
        cx = x + w * wx
        d.ellipse([cx - 11, base - 22, cx + 11, base], outline=(40, 40, 44), width=4)
    d.line([(x + w * 0.22, base - 11), (x + w * 0.42, base - 26), (x + w * 0.62, base - 11)],
           fill=(200, 40, 40), width=5)
    d.line([(x + w * 0.42, base - 26), (x + w * 0.52, base - 34)], fill=(200, 40, 40), width=5)
    d.ellipse([x + w * 0.5, base - 42, x + w * 0.58, base - 34], fill=(240, 200, 60))
    f = font(SERIF_BLACK, 20)
    d.text((x + w * 0.78, y + h * 0.18), "8", font=f, fill=RED)
    f2 = font(SANS_B, 7)
    d.text((x + w * 0.78, y + h * 0.18 + 22), "TITLES", font=f2, fill=MUTED)


def illo_tennis(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 240, 220))
    cx, cy = x + w * 0.36, y + h * 0.44
    d.ellipse([cx - 20, cy - 24, cx + 20, cy + 24], outline=(90, 60, 30), width=4)
    for i in (-12, -6, 0, 6, 12):
        d.line([(cx + i, cy - 20), (cx + i, cy + 20)], fill=(160, 160, 160), width=1)
        d.line([(cx - 16, cy + i), (cx + 16, cy + i)], fill=(160, 160, 160), width=1)
    d.line([(cx + 8, cy + 20), (cx + 26, cy + 40)], fill=(90, 60, 30), width=5)
    d.ellipse([x + w * 0.72 - 8, y + h * 0.3 - 8, x + w * 0.72 + 8, y + h * 0.3 + 8], fill=(196, 214, 60))
    d.arc([x + w * 0.72 - 8, y + h * 0.3 - 8, x + w * 0.72 + 8, y + h * 0.3 + 8], 300, 120, fill=(255, 255, 255), width=2)
    f = font(SANS_B, 8)
    d.text((x + w * 0.6, y + h * 0.66), "FIRST TITLE", font=f, fill=(40, 100, 40))


def illo_f1(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(26, 28, 44))
    # checkered strip
    sq = 8
    for i in range(int(w / sq)):
        for j in range(2):
            if (i + j) % 2 == 0:
                d.rectangle([x + i * sq, y + 4 + j * sq, x + (i + 1) * sq, y + 4 + (j + 1) * sq],
                            fill=(255, 255, 255))
    base = y + h - 12
    cx = x + w * 0.14
    d.polygon([(cx, base - 8), (cx + w * 0.5, base - 10), (cx + w * 0.68, base - 6), (cx + w * 0.68, base)],
              fill=(210, 40, 40))
    d.rectangle([cx + w * 0.3, base - 20, cx + w * 0.42, base - 10], fill=(210, 40, 40))
    d.rectangle([cx + w * 0.02, base - 16, cx + w * 0.06, base - 8], fill=(160, 30, 30))
    for wx in (0.14, 0.56):
        d.ellipse([cx + w * wx - 8, base - 10, cx + w * wx + 8, base + 6], fill=(20, 20, 24),
                  outline=(200, 200, 200), width=2)
    f = font(SANS_B, 9)
    d.text((x + w * 0.72, y + h * 0.42), "0.639s", font=f, fill=(255, 220, 120))


def illo_robot(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(230, 232, 240))
    cx, cy = x + w * 0.32, y + h * 0.5
    d.rounded_rectangle([cx - 22, cy - 18, cx + 22, cy + 18], 6, fill=(120, 128, 142),
                        outline=(70, 76, 90), width=2)
    d.ellipse([cx - 13, cy - 8, cx - 4, cy + 1], fill=(255, 90, 90))
    d.ellipse([cx + 4, cy - 8, cx + 13, cy + 1], fill=(255, 90, 90))
    d.line([(cx - 10, cy + 9), (cx + 10, cy + 9)], fill=(50, 54, 66), width=3)
    d.line([(cx, cy - 18), (cx, cy - 28)], fill=(70, 76, 90), width=3)
    d.ellipse([cx - 4, cy - 33, cx + 4, cy - 25], fill=RED)
    # gavel-ish "no rules" sign
    f = font(SANS_B, 9)
    d.text((x + w * 0.58, y + h * 0.3), "NO BINDING", font=f, fill=MUTED)
    d.text((x + w * 0.58, y + h * 0.3 + 12), "RULES", font=f, fill=RED)


def illo_drone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 234, 246))
    cx, cy = x + w * 0.4, y + h * 0.42
    for sx, sy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
        ex, ey = cx + sx * 26, cy + sy * 14
        d.line([(cx, cy), (ex, ey)], fill=(50, 54, 60), width=3)
        d.ellipse([ex - 9, ey - 3, ex + 9, ey + 3], outline=(50, 54, 60), width=2)
    d.rounded_rectangle([cx - 12, cy - 7, cx + 12, cy + 7], 4, fill=(50, 54, 60))
    d.ellipse([cx - 3, cy + 5, cx + 3, cy + 11], fill=RED)
    # rooftops below
    base = y + h - 6
    for i, rx in enumerate((0.08, 0.34, 0.6)):
        bx = x + w * rx
        d.polygon([(bx, base - 12), (bx + w * 0.11, base - 22), (bx + w * 0.22, base - 12)],
                  fill=(150, 120, 96))
        d.rectangle([bx + 2, base - 12, bx + w * 0.22 - 2, base], fill=(190, 168, 138))
    burst(d, x + w * 0.8, y + h * 0.3, 10, (245, 130, 40))


ILLOS = {
    "thermo": illo_thermo, "building": illo_building, "tanker": illo_tanker,
    "mercury": illo_mercury, "warship": illo_warship, "capitol": illo_capitol,
    "chart": illo_chart, "star": illo_star, "factory": illo_factory,
    "car_fire": illo_car_fire, "exam": illo_exam, "moto": illo_moto,
    "tennis": illo_tennis, "f1": illo_f1, "robot": illo_robot, "drone": illo_drone,
}


# ---------------------------------------------------------------- story data
# panel: (num, tag, headline, dek, verify, source, illo, map_xy or None)
HEROES = [
    (1, "GLOBAL · CLIMATE", "COP31 talks collapse with no deal on fossil fuels",
     "The longest UN climate summit on record ends in Antalya; about 130 countries reject a draft silent on fossil fuels.",
     "CONFIRMED", "Reuters", "thermo", (0.575, 0.30)),
    (2, "EUROPE · UKRAINE WAR", "Russian drone hits Kyiv flats; 14 missing",
     "A five-storey block partly collapses in Dymer; at least six killed across the region, Zelensky says.",
     "CONFIRMED", "BBC", "building", (0.545, 0.22)),
    (3, "MIDDLE EAST · IRAN WAR", "Iran strikes Bahrain; tankers hit near Hormuz",
     "Bahrain says a civilian site was hit, two wounded; Iran says it targeted US air defences. Gulf states condemn it.",
     "CLAIM", "Iran · Bahrain", "tanker", (0.605, 0.36)),
    (4, "SPACE · SCIENCE", "BepiColombo in orbit at Mercury, ESA confirms",
     "The Europe–Japan probe ends an eight-year journey — only the second mission to orbit Mercury. A glitch cut its burn short.",
     "CONFIRMED", "ESA", "mercury", None),
]

SMALL = [
    (5, "AFRICA · LIBYA WAR", "Russian warship hit at Benghazi",
     "Eastern Libyan authorities blame a suspected Ukrainian sea drone; a second ship was later targeted.",
     "REPORTED", "France 24", "warship", (0.52, 0.33)),
    (6, "N. AMERICA · POLITICS", "Democrats reach 258 House seats, most since 1992",
     "A North Carolina recount seals the tally; four races still undecided.",
     "CONFIRMED", "BBC", "capitol", (0.20, 0.30)),
    (7, "GLOBAL · MARKETS", "AI sell-off deepens: S&P -3.7%, Nikkei -5.1%",
     "Friday closes reported through Sunday; Nvidia faces an SEC inquiry after Huang quit.",
     "REPORTED", "AP", "chart", (0.16, 0.28)),
    (8, "S. AMERICA · JUSTICE", "Mexico captures cartel boss ‘El Chapo Isidro’",
     "FBI top-10 fugitive seized in Sinaloa; four soldiers and 16 gunmen killed.",
     "CONFIRMED", "NPR", "star", (0.13, 0.42)),
    (9, "ASIA · DISASTER", "Candy factory fire: 3 dead, 36 missing",
     "Rescuers pull six body bags from the Cikande ruins on Sunday.",
     "CONFIRMED", "AP", "factory", (0.78, 0.58)),
    (10, "MIDDLE EAST · WEST BANK", "Settlers torch vehicles in West Bank villages",
     "Twelve vehicles and several homes burned near Ramallah; Israel opens an inquiry.",
     "CONFIRMED", "France 24", "car_fire", (0.585, 0.35)),
    (11, "ASIA · POLITICS", "S. Korea education minister quits over AI cheating",
     "Choi Kyo-jin resigns after an exam top-scorer admits using AI.",
     "CONFIRMED", "BBC", "exam", (0.845, 0.30)),
    (12, "EUROPE · SPORT", "Márquez takes 8th MotoGP title, ties Agostini",
     "Eighth place at Portimão is enough; Bezzecchi wins the race.",
     "CONFIRMED", "Reuters", "moto", (0.465, 0.27)),
    (13, "EUROPE · SPORT", "Alcaraz beats Zverev for first ATP Finals title",
     "6–2, 7–6 in Turin completes his set of big hard-court crowns.",
     "CONFIRMED", "BBC Sport", "tennis", (0.50, 0.25)),
    (14, "N. AMERICA · SPORT", "Verstappen wins Las Vegas GP by 0.639s",
     "Lights out at 04:00 UTC; Norris second, Piastri third.",
     "CONFIRMED", "AP", "f1", (0.11, 0.30)),
    (15, "EUROPE · TECHNOLOGY", "UN talks on AI weapons end without binding rules",
     "Nations agree only to more discussion; the Red Cross warns time is running out.",
     "CONFIRMED", "CBC", "robot", (0.49, 0.24)),
    (16, "AFRICA · SUDAN WAR", "Drones hit Khartoum homes and a UN building",
     "Early-Sunday strikes; Sudan's army accuses Ethiopia of launching them.",
     "REPORTED", "France 24", "drone", (0.555, 0.44)),
]

# briefs: (region, [(lead, text), ...]) — numbered from 17 in order
BRIEFS = [
    ("NORTH AMERICA", [
        ("US:", "Trump orders contractors to report Congress asks"),
        ("FBI:", "probes reported breach of crime database"),
        ("Seattle:", "ICE airport arrests draw governor's fury"),
        ("Baseball:", "Skubal reportedly agrees $450m Mets deal"),
        ("Golf:", "Thitikul wins LPGA finale 3rd year running"),
        ("NWSL:", "KC Current win first title, beat Spirit 2–1"),
        ("NBA:", "Wembanyama scores 50 in Spurs win"),
    ]),
    ("SOUTH AMERICA", [
        ("Argentina:", "approves $50bn LNG export project"),
        ("Brazil:", "Bolsonaro stable in intensive care"),
        ("Haiti:", "agrees with El Salvador to build 3 prisons"),
        ("Football:", "Boca Juniors win Copa Sudamericana 2–0"),
    ]),
    ("EUROPE", [
        ("UK:", "May tells PM Burnham to move on from Brexit"),
        ("Denmark:", "expels Russian attaché over alleged plot"),
        ("France:", "6th weekend of cost protests; 144 arrests"),
        ("Istanbul:", "thousands protest media takeover"),
        ("Darts:", "Gerwyn Price wins Grand Slam 16–11"),
        ("Football:", "Leeds win at Chelsea 4–1, first since 1999"),
        ("Rugby:", "England beat All Blacks at Twickenham"),
        ("Chess:", "Gukesh–Sindarov world title match starts"),
    ]),
    ("MIDDLE EAST", [
        ("Gaza:", "Israeli strikes kill 2+ despite truce framework"),
        ("Israel:", "Likud–Eisenkot talks end without a deal"),
        ("Lebanon:", "Aoun blames Israel and Iran on independence day"),
        ("Iran:", "begins rationing electricity as cold season starts"),
        ("Houthis:", "claim hit on Saudi refinery; Saudi intercepts"),
    ]),
    ("AFRICA", [
        ("Nigeria:", "funeral boat capsizes, 24 dead"),
        ("S. Africa:", "ex-deputy president Mlambo-Ngcuka dies at 71"),
        ("Zimbabwe:", "author cleared of using AI for prize story"),
        ("U17 Cup:", "Tanzania draw 2–2 with Costa Rica on debut"),
    ]),
    ("ASIA", [
        ("Trade:", "EU–Indonesia deal signed; 98.5% of tariffs go"),
        ("Bangladesh:", "garment strikes clash with police"),
        ("Hong Kong:", "Election Committee vote draws ~99% turnout"),
        ("Mongolia:", "parliament accepts president's resignation"),
        ("Japan:", "Shuri Castle hall restored 7 years after fire"),
        ("K-pop:", "Ateez earn 4th No. 1 on Billboard 200"),
    ]),
    ("OCEANIA", [
        ("Cook Is.:", "Cyclone Xavier weakens; all safe on Nassau"),
        ("Australia:", "Molly Meldrum, Countdown host, dies at 83"),
    ]),
]

TIMELINE = [
    (0.04, "Overnight", "ESA confirms BepiColombo at Mercury"),
    (0.17, "04:00", "Las Vegas GP: Verstappen wins"),
    (0.27, "Early", "Drones hit Khartoum, UN building"),
    (0.44, "Sunday", "Drone hits Dymer flats"),
    (0.56, "13:00", "MotoGP: Márquez seals 8th title"),
    (0.70, "Afternoon", "COP31 collapses in Antalya"),
    (0.87, "Evening", "Alcaraz wins ATP Finals"),
]

DATE_CHECK = [
    ("Xi–Trump–Putin summit, Shenzhen", "Thu 19 Nov"),
    ("ICJ: Myanmar committed genocide", "Thu 19 Nov"),
    ("Voyager 1 one light-day out", "Wed 18 Nov"),
    ("Pilotless air-taxi flight, Japan", "Fri 20 Nov"),
    ("BepiColombo burn (confirmed Sun)", "Sat 21 Nov"),
    ("Jensen Huang quits Nvidia", "12–13 Nov"),
    ("Not yet: Spain election", "Sun 29 Nov"),
    ("Not yet: Belgian air strike", "Mon 23 Nov"),
]

REGION_COLORS = {
    "NORTH AMERICA": (52, 96, 164), "SOUTH AMERICA": (30, 140, 110),
    "EUROPE": (96, 120, 60), "MIDDLE EAST": (200, 120, 30),
    "AFRICA": (170, 60, 40), "ASIA": (130, 60, 140), "OCEANIA": (40, 150, 160),
}


def verify_color(v):
    return {"CONFIRMED": GREEN, "REPORTED": AMBER, "CLAIM": RED}.get(v, MUTED)


def panel(d, x, y, w, story, hero=False):
    """Draw one story panel; returns bottom y."""
    num, tag, head, dek, verify, source, illo, _ = story
    illo_h = 72 if hero else 40
    ILLOS[illo](d, x, y, w, illo_h)
    d.rectangle([x, y, x + w, y + illo_h], outline=(120, 112, 100), width=1)
    cy = y + illo_h + 6
    badge(d, x + 9, cy + 8, 9 if hero else 8, num)
    f_tag = font(SANS_B, 9.5 if hero else 8)
    d.text((x + 24, cy + 2), tag, font=f_tag, fill=RED)
    cy += 20 if hero else 17
    f_head = font(SERIF_B, 19 if hero else 13.5)
    lines = wrap(d, head, f_head, w - 4)
    cy = draw_lines(d, x, cy, lines, f_head, INK, 22 if hero else 15.5)
    cy += 2
    if hero:
        f_dek = font(SERIF, 11)
        lines = wrap(d, dek, f_dek, w - 4)
        cy = draw_lines(d, x, cy, lines[:3], f_dek, (60, 56, 50), 13.5)
        cy += 3
    f_v = font(SANS_B, 8.5 if hero else 7.5)
    d.text((x, cy), verify, font=f_v, fill=verify_color(verify))
    vw = text_w(d, verify, f_v)
    d.text((x + vw + 5, cy), source.upper(), font=f_v, fill=MUTED)
    return cy + (13 if hero else 11)


# coarse world landmass as rows of lon cells (each char ~ 7.2 degrees)
WORLD = [
    "        NNNN        EEEEEEEEEE  AAAAAAAA                      ",
    "      NNNNNNNN     EEEEEEEEE  AAAAAAAAAAAAAA                  ",
    "     NNNNNNNNNN   EEEEEEE   AAAAAAAAAAAAAAAAAAA               ",
    "      NNNNNNNN    EEEE     AAAAAAAAAAAAAAAAAAAAA              ",
    "       NNNNNN     EE  M   AAAAAAAAAAAAAAAAAAAA                ",
    "        NNNN       MMMMM  AAAAAAAAAAAAAAAAAA                  ",
    "         NN     FFFFFFFFF  AAAAAAAAAAAAAAAAA                   ",
    "        SSS    FFFFFFFFFF   AAAAAAAAAAAAAAA                   ",
    "       SSSS    FFFFFFFFF    AAAAAAAAAAAAA                    ",
    "       SSSSS    FFFFFFF      AAAAAAAAAAA                     ",
    "        SSSS     FFFFF        AAAAAAAA      OO                ",
    "        SSS      FFFF          AAAAAA     OOOO                ",
    "         SS       FF            AAAA       OOO                ",
    "         S         F             AA         OO                ",
]


def draw_map(d, x, y, w, h, pins):
    d.rectangle([x, y, x + w, y + h], fill=(216, 232, 244), outline=(120, 112, 100), width=1)
    rows = len(WORLD)
    cols = max(len(r) for r in WORLD)
    cw, ch = w / cols, h / rows
    cmap = {"N": (52, 96, 164), "S": (30, 140, 110), "E": (96, 120, 60),
            "M": (200, 120, 30), "F": (170, 60, 40), "A": (130, 60, 140), "O": (40, 150, 160)}
    for ri, row in enumerate(WORLD):
        for ci, ch_ in enumerate(row):
            if ch_ in cmap:
                cx = x + (ci + 0.5) * cw
                cy = y + (ri + 0.5) * ch
                r = min(cw, ch) * 0.42
                d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=cmap[ch_])
    for num, fx, fy in pins:
        px, py = x + fx * w, y + fy * h
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=(255, 255, 255), outline=RED, width=2)
        f = font(SANS_B, 8)
        s = str(num)
        d.text((px - text_w(d, s, f) / 2, py - 5), s, font=f, fill=RED)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0 = MARGIN

    # ---- masthead
    f_kick = font(SANS_B, 11)
    d.text((x0, 12), "THE WORLD'S NEWS OF ONE DAY", font=f_kick, fill=RED)
    counts = "52 STORIES · 7 REGIONS · ALL FROM THIS SUNDAY"
    d.text((x0 + CW - text_w(d, counts, f_kick), 12), counts, font=f_kick, fill=INK)
    f_date = font(SERIF_BLACK, 60)
    d.text((x0, 28), "Sunday 22 November 2026", font=f_date, fill=INK)
    d.line([(x0, 100), (x0 + CW, 100)], fill=RULE, width=2)

    # ---- timeline
    ty = 106
    f_tl = font(SANS_B, 10)
    d.rectangle([x0, ty + 14, x0 + 62, ty + 44], fill=RED)
    d.text((x0 + 7, ty + 17), "THE DAY", font=f_tl, fill=(255, 255, 255))
    d.text((x0 + 7, ty + 30), "IN UTC", font=f_tl, fill=(255, 255, 255))
    ax0, ax1 = x0 + 78, x0 + CW - 4
    ay = ty + 40
    d.line([(ax0, ay), (ax1, ay)], fill=RULE, width=2)
    f_time = font(SANS_B, 9)
    f_ev = font(SERIF, 9.5)
    for i, (frac, when, what) in enumerate(TIMELINE):
        px = ax0 + frac * (ax1 - ax0)
        d.ellipse([px - 3, ay - 3, px + 3, ay + 3], fill=RED)
        above = i % 2 == 0
        lines = wrap(d, what, f_ev, 150)
        tw = max(text_w(d, ln, f_ev) for ln in lines)
        tx = min(max(px - tw / 2, ax0), ax1 - tw)
        if above:
            ly = ay - 10 - len(lines) * 11
            d.text((tx, ly - 11), when, font=f_time, fill=RED)
            draw_lines(d, tx, ly, lines, f_ev, INK, 11)
        else:
            d.text((tx, ay + 6), when, font=f_time, fill=RED)
            draw_lines(d, tx, ay + 17, lines, f_ev, INK, 11)
    d.line([(x0, ty + 80), (x0 + CW, ty + 80)], fill=RULE, width=1)

    # ---- heroes
    hy = ty + 88
    gap = 12
    hw = (CW - 3 * gap) / 4
    bottoms = []
    for i, story in enumerate(HEROES):
        bottoms.append(panel(d, x0 + i * (hw + gap), hy, hw, story, hero=True))
    hy2 = max(bottoms) + 8
    d.line([(x0, hy2), (x0 + CW, hy2)], fill=RULE, width=1)

    # ---- small panels, 2 rows of 6
    sy = hy2 + 8
    sw = (CW - 5 * 10) / 6
    row_bottoms = []
    for r in range(2):
        bs = []
        for c in range(6):
            story = SMALL[r * 6 + c]
            bs.append(panel(d, x0 + c * (sw + 10), sy, sw, story, hero=False))
        row_bottoms.append(max(bs))
        sy = max(bs) + 10
        if r == 0:
            d.line([(x0, sy - 5), (x0 + CW, sy - 5)], fill=(190, 184, 172), width=1)
    by = sy + 2
    d.line([(x0, by), (x0 + CW, by)], fill=RULE, width=1)

    # ---- bottom: map + date check (left), briefs (right, 2 columns)
    by += 8
    left_w = 302
    f_h = font(SANS_B, 10)
    d.text((x0, by), "WHERE IT HAPPENED", font=f_h, fill=INK)
    note = "4: MERCURY"
    d.text((x0 + left_w - text_w(d, note, f_h), by), note, font=f_h, fill=RED)
    pins = [(s[0], s[7][0], s[7][1]) for s in HEROES + SMALL if s[7]]
    draw_map(d, x0, by + 16, left_w, 118, pins)
    # legend (one row, short labels)
    lx = x0
    ly = by + 16 + 122
    f_leg = font(SANS, 7.5)
    for name, col in REGION_COLORS.items():
        label = {"NORTH AMERICA": "N. Am", "SOUTH AMERICA": "S. Am", "EUROPE": "Europe",
                 "MIDDLE EAST": "Mid East", "AFRICA": "Africa", "ASIA": "Asia",
                 "OCEANIA": "Oceania"}[name]
        d.ellipse([lx, ly + 2, lx + 7, ly + 9], fill=col)
        d.text((lx + 10, ly), label, font=f_leg, fill=MUTED)
        lx += 10 + text_w(d, label, f_leg) + 8
    # date check box
    dy = ly + 15
    d.rectangle([x0, dy, x0 + left_w, dy + 112], outline=RED, width=2)
    d.rectangle([x0, dy, x0 + left_w, dy + 16], fill=(250, 232, 230))
    d.text((x0 + 6, dy + 3), "DATE CHECK — LEFT OUT AS NOT SUNDAY'S NEWS", font=font(SANS_B, 8), fill=RED)
    f_dc = font(SERIF, 9.5)
    f_dcd = font(SANS_B, 8.5)
    yy = dy + 21
    for what, when in DATE_CHECK:
        d.text((x0 + 6, yy), what, font=f_dc, fill=INK)
        d.text((x0 + left_w - 6 - text_w(d, when, f_dcd), yy), when, font=f_dcd, fill=RED)
        yy += 11

    # briefs in two columns
    bx0 = x0 + left_w + 16
    col_w = (x0 + CW - bx0 - 14) / 2
    f_reg = font(SANS_B, 9.5)
    f_lead = font(SERIF_B, 9)
    f_txt = font(SERIF, 9)
    # split regions: col1 = first 3 groups (19 items), col2 = last 4 (17 items)
    num = 17
    cols = [BRIEFS[:3], BRIEFS[3:]]
    for ci, groups in enumerate(cols):
        cx = bx0 + ci * (col_w + 14)
        cy = by
        for region, items in groups:
            d.ellipse([cx, cy + 2, cx + 8, cy + 10], fill=REGION_COLORS[region])
            d.text((cx + 12, cy), region, font=f_reg, fill=INK)
            cnt = str(len(items))
            d.text((cx + col_w - text_w(d, cnt, f_reg), cy), cnt, font=f_reg, fill=MUTED)
            cy += 13
            for lead, txt in items:
                badge(d, cx + 6, cy + 5.5, 6.5, num)
                num += 1
                tx = cx + 16
                d.text((tx, cy), lead, font=f_lead, fill=INK)
                lw = text_w(d, lead + " ", f_lead)
                lines = wrap(d, txt, f_txt, col_w - 16 - lw)
                # first line continues after lead; rest wrap full width
                if lines:
                    d.text((tx + lw, cy), lines[0], font=f_txt, fill=(50, 46, 40))
                    cy += 10.5
                    for ln in lines[1:]:
                        d.text((tx, cy), ln, font=f_txt, fill=(50, 46, 40))
                        cy += 10.5
                cy += 1
            cy += 4

    # ---- footer
    fy = H - 26
    d.line([(x0, fy - 6), (x0 + CW, fy - 6)], fill=RULE, width=1)
    f_foot = font(SERIF, 9)
    foot = ("Every story here happened or was first reported on Sunday 22 November 2026. "
            "CLAIM = one side's account, not independently confirmed. "
            "Sources: Reuters, AP, AFP, BBC, Guardian, Al Jazeera, France 24 and others. Original drawings.")
    lines = wrap(d, foot, f_foot, CW)
    draw_lines(d, x0, fy, lines[:2], f_foot, MUTED, 11)

    img.save(out, "PNG", optimize=True)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
