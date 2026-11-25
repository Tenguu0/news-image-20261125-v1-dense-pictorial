#!/usr/bin/env python3
"""Build the 25 November 2026 one-page newspaper image.

Reads the AI-generated pictorial illustrations committed under assets/
and composes a dense 1024x1024 front page: masthead, one big pictured
lead story, a 4x3 grid of pictured stories, an ALSO TODAY strip and a
footer. Fully deterministic: same assets in, same PNG bytes out.
No network access at runtime. Requires Pillow only.

Usage:  python3 main.py            # writes /output/entry.png
        OUTPUT_DIR=/tmp/out python3 main.py
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
OUT_DIR = os.environ.get("OUTPUT_DIR", "/output")
OUT_PATH = os.path.join(OUT_DIR, "entry.png")

PAGE_W, PAGE_H = 1024, 1024
PAPER = (247, 243, 234)
INK = (20, 20, 20)
MUTED = (90, 86, 78)
RED = (179, 32, 44)
NAVY = (27, 42, 74)
RULE = (180, 172, 158)
CARD_BG = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load_font(name, size):
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_I = "DejaVuSans-Oblique.ttf"


def text_width(draw, text, font):
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0]


def wrap_lines(draw, text, font, max_width, max_lines=None):
    """Greedy word wrap; truncates with an ellipsis past max_lines."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if text_width(draw, trial, font) <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and text_width(draw, lines[-1] + " ...", font) > max_width:
            tail = lines[-1].rsplit(" ", 1)
            lines[-1] = tail[0] if len(tail) == 2 else tail[0][:-1]
        lines[-1] = lines[-1].rstrip() + " ..."
    return lines


def draw_wrapped(draw, xy, text, font, color, max_width, line_gap, max_lines=None):
    x, y = xy
    for line in wrap_lines(draw, text, font, max_width, max_lines):
        draw.text((x, y), line, font=font, fill=color)
        y += font.size + line_gap
    return y


def cover_crop(image, target_w, target_h):
    """Centre-crop to the target aspect ratio, then resize (LANCZOS)."""
    src_w, src_h = image.size
    target_ratio = target_w / target_h
    src_ratio = src_w / src_h
    if src_ratio > target_ratio:
        new_w = int(src_h * target_ratio)
        left = (src_w - new_w) // 2
        box = (left, 0, left + new_w, src_h)
    else:
        new_h = int(src_w / target_ratio)
        top = (src_h - new_h) // 2
        box = (0, top, src_w, top + new_h)
    return image.crop(box).resize((target_w, target_h), Image.LANCZOS)


def picture(name, target_w, target_h):
    path = os.path.join(ASSETS, name)
    with Image.open(path) as shot:
        shot = shot.convert("RGB")
        return cover_crop(shot, target_w, target_h)


LEAD = {
    "image": "lead.jpg",
    "kicker": "MIDDLE EAST",
    "headline": "Houthi drone hits Riyadh's tallest tower \u2014 11 wounded",
    "summary": (
        "Saudi civil defence says a Houthi drone struck the PIF Tower in "
        "Riyadh, wounding 11 people, including two Indians and three "
        "Nepalese. It is the second strike on the tower in days."
    ),
}

GRID = [
    {
        "image": "g1-ship.jpg",
        "kicker": "UKRAINE",
        "headline": "Kyiv: we hit a Russian ship in the Gulf of Finland",
        "summary": "Zelenskiy confirms a Ukrainian drone strike; Norway urges caution.",
    },
    {
        "image": "g2-cop.jpg",
        "kicker": "CLIMATE",
        "headline": "COP31 talks collapse with no deal",
        "summary": "Talks in Antalya end with no deal as the fossil-fuel impasse holds.",
    },
    {
        "image": "g3-huawei.jpg",
        "kicker": "TECH",
        "headline": "Huawei guilty on 10 of 12 counts in US trial",
        "summary": "A Brooklyn jury convicts the tech giant after a three-month trial.",
    },
    {
        "image": "g4-cia.jpg",
        "kicker": "USA",
        "headline": "CIA and spy chief's office hit by hack",
        "summary": "The CIA and ODNI suffer a cyberattack on unclassified systems.",
    },
    {
        "image": "g5-mine.jpg",
        "kicker": "INDONESIA",
        "headline": "Dozens feared trapped in flooded Java gold mine",
        "summary": "Rescuers search for around 30 workers stuck 100 m deep in Pongkor, Bogor.",
    },
    {
        "image": "g6-shenzhou.jpg",
        "kicker": "SPACE",
        "headline": "China launches Shenzhou-24 crew to orbit",
        "summary": "The crewed mission lifts off from Jiuquan aboard a Long March 2F rocket.",
    },
    {
        "image": "g7-madrid.jpg",
        "kicker": "FOOTBALL",
        "headline": "Madrid rout PSV 5\u20131",
        "summary": "Bellingham's stunner and a Mbapp\u00e9 brace power Real's comeback.",
    },
    {
        "image": "g8-senegal.jpg",
        "kicker": "AFRICA",
        "headline": "Senegal get AFCON crown back",
        "summary": "CAS overturns CAF's decision and restores Senegal's 1\u20130 final win.",
    },
    {
        "image": "g9-cricket.jpg",
        "kicker": "CRICKET",
        "headline": "Vaibhav, 204 off 53 balls \u2014 a world record",
        "summary": "India A's teenager smashes 28 sixes in the fastest List A double century ever.",
    },
    {
        "image": "g10-markets.jpg",
        "kicker": "MARKETS",
        "headline": "Asia stocks slide as tariff threat returns",
        "summary": "Nikkei falls 2.9%, Seoul 5.3% as the US readies fresh tariff measures.",
    },
    {
        "image": "g11-sarkozy.jpg",
        "kicker": "FRANCE",
        "headline": "Sarkozy and Bruni ordered to trial",
        "summary": "The former president and his wife face trial over the Libya case.",
    },
    {
        "image": "g12-hanoi.jpg",
        "kicker": "VIETNAM",
        "headline": "Hanoi blast kills six, injures 10",
        "summary": "An explosion rips through a residential area; a gas leak is suspected.",
    },
]

ALSO_TODAY = [
    "Trump pardons turkeys Freedom and Feathers",
    "Giuliani gets the Medal of Freedom",
    "Gukesh draws World Chess opener",
]


def build():
    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(page)

    # --- Masthead -------------------------------------------------------
    title_font = load_font(SERIF_B, 46)
    date_font = load_font(SANS_B, 14)
    draw.text((16, 12), "THE WORLD IN ONE PAGE", font=title_font, fill=INK)
    date_text = "WEDNESDAY 25 NOVEMBER 2026"
    date_w = text_width(draw, date_text, date_font)
    draw.text((PAGE_W - 16 - date_w, 30), date_text, font=date_font, fill=NAVY)
    draw.rectangle((16, 66, PAGE_W - 16, 69), fill=RED)
    draw.rectangle((16, 72, PAGE_W - 16, 73), fill=INK)

    # --- Lead story -----------------------------------------------------
    lead_x, lead_y, lead_w, lead_h = 16, 82, 576, 252
    lead_img = picture(LEAD["image"], lead_w, lead_h)
    page.paste(lead_img, (lead_x, lead_y))
    draw.rectangle(
        (lead_x, lead_y, lead_x + lead_w - 1, lead_y + lead_h - 1),
        outline=INK,
        width=1,
    )
    tx = lead_x + lead_w + 16
    tw = PAGE_W - 16 - tx
    y = lead_y + 2
    kicker_font = load_font(SANS_B, 14)
    draw.text((tx, y), LEAD["kicker"], font=kicker_font, fill=RED)
    y += 22
    head_font = load_font(SERIF_B, 29)
    y = draw_wrapped(
        draw, (tx, y), LEAD["headline"], head_font, INK, tw, 6, max_lines=3
    )
    y += 6
    sum_font = load_font(SANS, 14)
    draw_wrapped(
        draw, (tx, y), LEAD["summary"], sum_font, MUTED, tw, 4, max_lines=5
    )

    # --- Grid of pictured stories ---------------------------------------
    grid_top = 348
    card_w, card_h = 242, 184
    gap_x, gap_y = 8, 9
    img_h = 98
    g_kicker = load_font(SANS_B, 11)
    g_head = load_font(SERIF_B, 14)
    g_sum = load_font(SANS, 11)
    for idx, story in enumerate(GRID):
        row, col = divmod(idx, 4)
        cx = 16 + col * (card_w + gap_x)
        cy = grid_top + row * (card_h + gap_y)
        draw.rectangle((cx, cy, cx + card_w - 1, cy + card_h - 1), fill=CARD_BG)
        draw.rectangle(
            (cx, cy, cx + card_w - 1, cy + card_h - 1), outline=RULE, width=1
        )
        shot = picture(story["image"], card_w - 2, img_h)
        page.paste(shot, (cx + 1, cy + 1))
        ix = cx + 8
        iw = card_w - 16
        iy = cy + img_h + 7
        draw.text((ix, iy), story["kicker"], font=g_kicker, fill=RED)
        iy += 16
        iy = draw_wrapped(
            draw, (ix, iy), story["headline"], g_head, INK, iw, 1, max_lines=2
        )
        iy += 2
        draw_wrapped(
            draw, (ix, iy), story["summary"], g_sum, MUTED, iw, 1, max_lines=2
        )

    # --- ALSO TODAY strip ------------------------------------------------
    strip_y = 922
    draw.rectangle((16, strip_y, PAGE_W - 16, strip_y + 1), fill=INK)
    strip_font = load_font(SANS_B, 12)
    item_font = load_font(SANS, 12)
    label = "ALSO TODAY"
    draw.text((16, strip_y + 10), label, font=strip_font, fill=RED)
    lx = 16 + text_width(draw, label, strip_font) + 14
    for item in ALSO_TODAY:
        draw.text((lx, strip_y + 10), item, font=item_font, fill=INK)
        lx += text_width(draw, item, item_font) + 26
        if item is not ALSO_TODAY[-1]:
            draw.text((lx - 16, strip_y + 10), "\u2022", font=item_font, fill=RED)
    draw.rectangle((16, strip_y + 34, PAGE_W - 16, strip_y + 35), fill=INK)

    # --- Footer ----------------------------------------------------------
    foot_font = load_font(SANS_I, 11)
    foot = "Pictures are AI-generated illustrations."
    draw.text((16, 968), foot, font=foot_font, fill=MUTED)
    right = "All stories reported 25 November 2026  \u00b7  make.fun"
    rw = text_width(draw, right, foot_font)
    draw.text((PAGE_W - 16 - rw, 968), right, font=foot_font, fill=MUTED)

    os.makedirs(OUT_DIR, exist_ok=True)
    page.save(OUT_PATH, "PNG")
    print("wrote", OUT_PATH, page.size)
    return 0


if __name__ == "__main__":
    sys.exit(build())
