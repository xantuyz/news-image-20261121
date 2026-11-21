#!/usr/bin/env python3
"""Draw the world news of Saturday 21 November 2026 as a one-page
breaking-news broadsheet, 1024x1024 PNG.

Pure Pillow: flat spot illustrations drawn with polygons, arcs and
ellipses, copy set in DejaVu. Run: python3 render.py
Writes entry.png beside this script.

Stories (each verified against live reporting on the morning of
21 Nov 2026; Friday events are dated Friday on the page):
  1. LEAD — Two Russian missiles and a drone come down in Poland
     on Friday night; PM Tusk calls it a deliberate provocation,
     NATO chief Rutte a "grave violation". No casualties.
  2. Wall Street routs on Friday: Nasdaq -5.28% (2026 gains gone),
     S&P 500 -3.70% into correction, Dow -949 points; Nvidia -14%
     after reports of an SEC accounting probe.
  3. UK and EU seal a post-Brexit reset at Friday's Brussels
     summit: food trade, linked carbon markets, youth mobility
     for 100,000 a year.
  4. Trump administration wants a Ukraine-Russia peace deal by
     early January (FT report, Friday); Trump says Putin wants
     diplomacy.
  5. Cyclone Akvan comes ashore near Gopalpur, Odisha, on Friday:
     winds 70-80 km/h, 370,000 evacuated, no major damage.
  6. Denmark expels a Russian diplomat over an alleged plot to
     kill a Ukrainian rapper (reported Saturday).
Left out on purpose (date traps): the ICJ Myanmar verdict
(19 Nov, used in yesterday's edition), the Eisenkot mandate
(8 Nov), the four-nation Gaza aid statement (15 Nov), France's
cost-of-living protests (their fourth weekend was 14-15 Nov).
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
EDGE = 36
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# --- palette: stone paper, charcoal ink, signal red, electric yellow,
#     cobalt, sage (deliberately unlike yesterday's cream/rust/teal) ---
STONE = (231, 232, 227)
PAPER = (247, 247, 243)
INK = (23, 25, 28)
RED = (201, 47, 61)
YELLOW = (228, 184, 63)
COBALT = (36, 87, 166)
SAGE = (108, 139, 114)
GREY = (120, 122, 116)
LINEC = (178, 180, 172)
SKY = (208, 222, 235)
PALE_RED = (244, 214, 212)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def load(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def serif_b(size):
    return load("DejaVuSerif-Bold.ttf", size)


def serif(size):
    return load("DejaVuSerif.ttf", size)


def sans_b(size):
    return load("DejaVuSans-Bold.ttf", size)


def sans(size):
    return load("DejaVuSans.ttf", size)


def wrap_text(draw, text, font, width):
    """Greedy word wrap; returns list of lines that fit `width`."""
    lines = []
    for chunk in text.split("\n"):
        words = chunk.split()
        if not words:
            lines.append("")
            continue
        line = words[0]
        for word in words[1:]:
            trial = line + " " + word
            if draw.textlength(trial, font=font) <= width:
                line = trial
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


class FrontPage:
    def __init__(self):
        self.img = Image.new("RGB", (SIZE, SIZE), STONE)
        self.d = ImageDraw.Draw(self.img)

    def rule(self, x0, y, x1, color=LINEC, width=2):
        self.d.line([(x0, y), (x1, y)], fill=color, width=width)

    def tag(self, x, y, text, fg=PAPER, bg=RED, font=None):
        font = font or sans_b(15)
        pad_x, pad_y = 10, 5
        w = self.d.textlength(text, font=font) + 2 * pad_x
        h = font.size + 2 * pad_y
        self.d.rectangle([x, y, x + w, y + h], fill=bg)
        self.d.text((x + pad_x, y + pad_y), text, font=font, fill=fg)
        return w

    def headline(self, x, y, width, text, size, color=INK, leading=None):
        font = serif_b(size)
        leading = leading or int(size * 1.12)
        lines = wrap_text(self.d, text, font, width)
        for line in lines:
            self.d.text((x, y), line, font=font, fill=color)
            y += leading
        return y

    def deck(self, x, y, width, text, size=17, color=INK, leading=None):
        font = sans(size)
        leading = leading or int(size * 1.32)
        for line in wrap_text(self.d, text, font, width):
            self.d.text((x, y), line, font=font, fill=color)
            y += leading
        return y

    def source(self, x, y, text):
        self.d.text((x, y), text, font=sans_b(12), fill=GREY)

    def panel(self, x, y, w, h, fill=PAPER):
        self.d.rectangle([x, y, x + w, y + h], fill=fill, outline=LINEC, width=2)
        return (x + 16, y + 14, w - 32, h - 28)

    # --- masthead ------------------------------------------------------
    def masthead(self):
        d = self.d
        d.text((EDGE, 26), "THE WORLD", font=serif_b(66), fill=INK)
        d.text((EDGE, 100), "SATURDAY EDITION", font=sans_b(21), fill=RED)
        right = "SATURDAY · 21 NOVEMBER 2026"
        w = d.textlength(right, font=sans_b(21))
        d.text((SIZE - EDGE - w, 100), right, font=sans_b(21), fill=INK)
        sub = "GLOBAL NEWS IN ONE FRAME — MORNING EDITION"
        w2 = d.textlength(sub, font=sans(15))
        d.text((SIZE - EDGE - w2, 44), sub, font=sans(15), fill=GREY)
        self.rule(EDGE, 140, SIZE - EDGE, color=RED, width=5)
        self.rule(EDGE, 148, SIZE - EDGE, color=INK, width=2)

    # --- art: lead, Poland ----------------------------------------------
    def art_poland(self, x, y, w, h):
        d = self.d
        # sky band + ground
        d.rectangle([x, y, x + w, y + h], fill=SKY)
        d.rectangle([x, y + h - 34, x + w, y + h], fill=SAGE)
        # rough Poland silhouette, scaled to the box
        sx = lambda fx: x + int(w * fx)
        sy = lambda fy: y + int(h * fy)
        poly = [(sx(0.10), sy(0.16)), (sx(0.34), sy(0.05)),
                (sx(0.62), sy(0.12)), (sx(0.82), sy(0.34)),
                (sx(0.90), sy(0.58)), (sx(0.76), sy(0.78)),
                (sx(0.56), sy(0.88)), (sx(0.32), sy(0.86)),
                (sx(0.14), sy(0.68)), (sx(0.07), sy(0.40))]
        d.polygon(poly, fill=PAPER, outline=INK)
        # dashed border line across the map, above the ground band
        for i in range(0, int(w * 0.78), 26):
            d.line([(x + 14 + i, sy(0.78)), (x + 28 + i, sy(0.78))],
                   fill=INK, width=3)
        # impact rings
        for fx, fy, r in [(0.56, 0.52, 30), (0.74, 0.40, 23)]:
            cx, cy = sx(fx), sy(fy)
            d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=RED, width=4)
            d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED)
        # two red missiles, diagonal
        for fx, fy, ang in [(0.16, 0.30, -38), (0.28, 0.16, -30)]:
            mx, my = sx(fx), sy(fy)
            rad = math.radians(ang)
            dx, dy = math.cos(rad) * 66, math.sin(rad) * 66
            d.line([(mx, my), (mx + dx, my + dy)], fill=RED, width=12)
            d.polygon([(mx + dx, my + dy),
                       (mx + dx - dy * 0.28, my + dy + dx * 0.28),
                       (mx + dx + dy * 0.28, my + dy - dx * 0.28)],
                      fill=RED)
            d.polygon([(mx, my), (mx - dx * 0.22, my - dy * 0.22 + 11),
                       (mx - dx * 0.22, my - dy * 0.22 - 11)], fill=YELLOW)
        # small yellow drone
        dx0, dy0 = sx(0.80), sy(0.66)
        d.ellipse([dx0 - 15, dy0 - 8, dx0 + 15, dy0 + 8], fill=YELLOW,
                  outline=INK)
        for ox, oy in [(-21, -13), (21, -13), (-21, 13), (21, 13)]:
            d.line([(dx0 + ox - 7, dy0 + oy), (dx0 + ox + 7, dy0 + oy)],
                   fill=INK, width=3)
        d.text((x + 12, y + h - 28), "2 MISSILES + 1 DRONE",
               font=sans_b(16), fill=INK)

    # --- art: Wall Street bars ------------------------------------------
    def art_markets(self, x, y, w, h):
        d = self.d
        d.rectangle([x, y, x + w, y + h], fill=(24, 26, 30))
        # three descending bars on the left
        base = y + h - 8
        bars = [(x + 14, 0.42), (x + 66, 0.60), (x + 118, 0.78)]
        for bx, frac in bars:
            bh = int(h * frac)
            d.rectangle([bx, base - bh, bx + 42, base], fill=RED)
        d.line([(x + 8, base - int(h * 0.86)), (x + 168, base - 6)],
               fill=YELLOW, width=4)
        tx = x + 182
        d.text((tx, y + 4), "NASDAQ", font=sans_b(12), fill=(200, 200, 200))
        d.text((tx, y + 18), "-5.28%", font=sans_b(26), fill=RED)
        d.text((tx, y + 48), "S&P 500  -3.70%", font=sans_b(13), fill=PAPER)
        d.text((tx, y + 66), "DOW  -1.93%", font=sans_b(13), fill=PAPER)
        d.text((tx, y + 84), "NVDA  -14%", font=sans_b(13), fill=YELLOW)

    # --- art: UK-EU bridge (compact strip) ------------------------------
    def art_bridge(self, x, y, w, h):
        d = self.d
        d.rectangle([x, y, x + w, y + h], fill=(232, 236, 240))
        # Union Jack (simplified), left
        fx, fy = x + 6, y + 2
        d.rectangle([fx, fy, fx + 64, fy + 38], fill=COBALT)
        d.line([(fx, fy), (fx + 64, fy + 38)], fill=PAPER, width=7)
        d.line([(fx + 64, fy), (fx, fy + 38)], fill=PAPER, width=7)
        d.line([(fx + 32, fy), (fx + 32, fy + 38)], fill=RED, width=9)
        d.line([(fx, fy + 19), (fx + 64, fy + 19)], fill=RED, width=9)
        # EU flag (simplified), right
        ex, ey = x + w - 70, y + 2
        d.rectangle([ex, ey, ex + 64, ey + 38], fill=COBALT)
        for k in range(12):
            ang = 2 * math.pi * k / 12 - math.pi / 2
            sx = ex + 32 + 12 * math.cos(ang)
            sy = ey + 19 + 12 * math.sin(ang)
            d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=YELLOW)
        # shallow bridge arc between the flags
        d.line([(x + 78, y + 46), (x + w - 84, y + 46)], fill=COBALT, width=4)
        d.ellipse([x + w // 2 - 6, y + 40, x + w // 2 + 6, y + 52],
                  fill=YELLOW, outline=INK)
        label = "100,000 YOUTH / YEAR · FOOD · CARBON"
        lw = d.textlength(label, font=sans_b(13))
        d.text((x + (w - lw) // 2, y + h - 16), label,
               font=sans_b(13), fill=INK)

    # --- art: diplomacy calendar ----------------------------------------
    def art_talks(self, x, y, w, h):
        d = self.d
        d.rectangle([x, y, x + w, y + h], fill=(240, 232, 200))
        # January calendar card, left
        cx, cy = x + 10, y + 4
        ch = h - 22
        d.rectangle([cx, cy, cx + 104, cy + ch], fill=PAPER, outline=INK, width=2)
        d.rectangle([cx, cy, cx + 104, cy + 20], fill=RED)
        d.text((cx + 8, cy + 2), "JANUARY", font=sans_b(12), fill=PAPER)
        d.text((cx + 28, cy + 22), "2027", font=serif_b(20), fill=INK)
        # two speech bubbles, right
        bx = x + 128
        d.ellipse([bx, y + 2, bx + 128, y + 26], fill=PAPER, outline=INK, width=2)
        d.text((bx + 14, y + 8), "KYIV", font=sans_b(13), fill=COBALT)
        d.ellipse([bx, y + 30, bx + 128, y + 54], fill=PAPER, outline=INK, width=2)
        d.text((bx + 8, y + 36), "MOSCOW", font=sans_b(13), fill=RED)
        # nearly-joined dashed line at the bottom
        ly = y + h - 8
        for i in range(0, 108, 16):
            d.line([(x + 10 + i, ly), (x + 20 + i, ly)], fill=INK, width=3)
        d.ellipse([x + 128, ly - 6, x + 140, ly + 6], fill=YELLOW, outline=INK)
        d.text((x + 148, ly - 6), "NOT YET AGREED",
               font=sans_b(11), fill=GREY)

    # --- art: cyclone ----------------------------------------------------
    def art_cyclone(self, x, y, w, h):
        d = self.d
        d.rectangle([x, y, x + w, y + h], fill=SKY)
        # spiral, scaled to the box
        cx, cy = x + 78, y + int(h * 0.42)
        r0 = int(h * 0.36)
        for k, (frac, a0, a1) in enumerate(
                [(1.00, 0, 300), (0.76, 40, 330), (0.52, 90, 350),
                 (0.32, 140, 360)]):
            r = int(r0 * frac)
            d.arc([cx - r, cy - r, cx + r, cy + r], a0, a1, fill=COBALT, width=5)
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=COBALT)
        # rain streaks, right side
        for i, rx in enumerate(range(x + 168, x + w - 8, 20)):
            d.line([(rx, y + 10 + (i % 3) * 6), (rx - 5, y + 34 + (i % 3) * 6)],
                   fill=COBALT, width=3)
        # coastline + three intact houses
        d.rectangle([x, y + h - 20, x + w, y + h], fill=(214, 196, 150))
        for hx in (x + 176, x + 208, x + 240):
            d.rectangle([hx, y + h - 40, hx + 24, y + h - 20], fill=PAPER,
                        outline=INK, width=2)
            d.polygon([(hx - 3, y + h - 40), (hx + 12, y + h - 50),
                       (hx + 27, y + h - 40)], fill=RED)
        d.text((x + 8, y + h - 17), "370,000 EVACUATED",
               font=sans_b(13), fill=INK)

    # --- art: embassy door ----------------------------------------------
    def art_door(self, x, y, w, h):
        d = self.d
        d.rectangle([x, y, x + w, y + h], fill=(238, 232, 220))
        # door, left, scaled to the box
        dx, dy = x + 12, y + 6
        dh = h - 12
        d.rectangle([dx, dy, dx + 92, dy + dh], fill=COBALT, outline=INK, width=2)
        d.rectangle([dx + 10, dy + 10, dx + 82, dy + dh // 2 - 4],
                    fill=PAPER, outline=INK)
        d.rectangle([dx + 10, dy + dh // 2 + 4, dx + 82, dy + dh - 10],
                    fill=PAPER, outline=INK)
        d.ellipse([dx + 70, dy + dh // 2 + 12, dx + 78, dy + dh // 2 + 20],
                  fill=YELLOW)
        # red EXIT sign across the top of the door
        d.rectangle([dx + 12, dy - 2, dx + 80, dy + 18], fill=RED)
        d.text((dx + 24, dy + 1), "EXIT", font=sans_b(13), fill=PAPER)
        # passport, middle
        px, py = x + 128, y + 8
        d.rectangle([px, py, px + 58, py + 54], fill=RED, outline=INK, width=2)
        d.text((px + 4, py + 4), "PASSPORT", font=sans_b(8), fill=PAPER)
        d.ellipse([px + 16, py + 22, px + 38, py + 44], fill=YELLOW, outline=INK)
        # microphone, right
        mx, my = x + 214, y + 22
        d.ellipse([mx - 11, my - 12, mx + 11, my + 12], fill=INK)
        d.rectangle([mx - 3, my + 10, mx + 3, my + 32], fill=INK)
        d.arc([mx - 13, my + 24, mx + 13, my + 48], 0, 180, fill=INK, width=3)

    # --- build -----------------------------------------------------------
    def build(self):
        self.masthead()

        # LEAD — Poland, left, two columns wide
        lx, ly, lw, lh = EDGE, 162, 540, 470
        ix, iy, iw, ih = self.panel(lx, ly, lw, lh)
        self.tag(ix, iy, "LEAD · POLAND — FRIDAY NIGHT")
        y = self.headline(ix, iy + 36, iw,
                          "RUSSIAN MISSILES HIT POLAND", 33)
        y = self.headline(ix, y + 2, iw,
                          "NATO CALLS IT A “GRAVE VIOLATION”", 24,
                          color=RED)
        y = self.deck(ix, y + 8, iw,
                      "Two Kh-101 missiles and a drone came down about "
                      "50 km from the border. PM Tusk called it a "
                      "deliberate provocation; no casualties reported.",
                      size=17)
        self.art_poland(ix, y + 10, iw, ly + lh - 40 - (y + 10))
        self.source(ix, ly + lh - 34, "SOURCE: AP · REUTERS")

        # 2 — Wall Street, right top
        rx = EDGE + 540 + 20
        rw = SIZE - EDGE - rx
        ix, iy, iw, ih = self.panel(rx, 162, rw, 230)
        self.tag(ix, iy, "MARKETS · FRIDAY", bg=INK)
        y = self.headline(ix, iy + 34, iw,
                          "WALL STREET ERASES THE YEAR’S GAINS", 21)
        self.art_markets(ix, y + 6, iw, 162 + 230 - 16 - (y + 6))

        # 3 — UK-EU, right middle
        ix, iy, iw, ih = self.panel(rx, 412, rw, 220)
        self.tag(ix, iy, "LONDON · BRUSSELS", bg=COBALT)
        y = self.headline(ix, iy + 34, iw,
                          "UK AND EU SEAL POST-BREXIT RESET", 21)
        y = self.deck(ix, y + 4, iw,
                      "Food trade, linked carbon markets and youth "
                      "mobility for 100,000 a year.", size=15)
        self.art_bridge(ix, y + 6, iw, 412 + 220 - 16 - (y + 6))

        # bottom row: three panels, y 652..912
        by, bh = 652, 260
        bw = 304
        bx = [EDGE, EDGE + bw + 20, EDGE + 2 * (bw + 20)]

        # 4 — Trump / Ukraine talks
        ix, iy, iw, ih = self.panel(bx[0], by, bw, bh)
        self.tag(ix, iy, "DIPLOMACY", bg=INK, font=sans_b(13))
        y = self.headline(ix, iy + 32, iw,
                          "TRUMP SEEKS UKRAINE DEAL BY JANUARY", 19)
        y = self.deck(ix, y + 4, iw,
                      "Washington wants a Kyiv–Moscow deal by early "
                      "January, the FT reported. Trump says Putin "
                      "wants diplomacy.", size=14)
        self.art_talks(ix, y + 6, iw, by + bh - 16 - (y + 6))

        # 5 — Cyclone Akvan
        ix, iy, iw, ih = self.panel(bx[1], by, bw, bh)
        self.tag(ix, iy, "WEATHER · INDIA", bg=COBALT, font=sans_b(13))
        y = self.headline(ix, iy + 32, iw,
                          "CYCLONE AKVAN HITS ODISHA COAST", 19)
        y = self.deck(ix, y + 4, iw,
                      "The storm crossed near Gopalpur on Friday with "
                      "winds of 70–80 km/h. No major damage reported.",
                      size=14)
        self.art_cyclone(ix, y + 6, iw, by + bh - 16 - (y + 6))

        # 6 — Denmark expels diplomat
        ix, iy, iw, ih = self.panel(bx[2], by, bw, bh)
        self.tag(ix, iy, "COPENHAGEN", bg=RED, font=sans_b(13))
        y = self.headline(ix, iy + 32, iw,
                          "DENMARK EXPELS RUSSIAN DIPLOMAT", 19)
        y = self.deck(ix, y + 4, iw,
                      "Copenhagen cited an alleged plot to kill a "
                      "Ukrainian rapper. The allegation is under "
                      "investigation.", size=14)
        self.art_door(ix, y + 6, iw, by + bh - 16 - (y + 6))

        # footer
        self.rule(EDGE, 928, SIZE - EDGE, color=INK, width=2)
        self.d.text((EDGE, 940),
                    "SOURCES: AP · REUTERS · FINANCIAL TIMES · IMD · AL JAZEERA",
                    font=sans_b(13), fill=GREY)
        tail = "WORLD ROUNDUP — MORNING EDITION — 21 NOV 2026"
        w = self.d.textlength(tail, font=sans_b(13))
        self.d.text((SIZE - EDGE - w, 940), tail, font=sans_b(13), fill=GREY)

        self.img.save(OUT, optimize=True)
        print("wrote %s (%d bytes)" % (OUT, os.path.getsize(OUT)))


if __name__ == "__main__":
    FrontPage().build()
