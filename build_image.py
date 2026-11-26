#!/usr/bin/env python3
"""Render the news-image-20261126 entry: one picture of Thursday 26 November 2026.

Flat editorial illustration drawn with PIL shapes only. No photos, no network,
no timestamps: the output is deterministic, so two runs are byte-identical.
"""
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 10  # outer margin

PAPER = (248, 244, 236)
INK = (26, 26, 26)
GREY = (107, 107, 107)
RULE = (26, 26, 26)
RED = (179, 39, 30)
NAVY = (31, 58, 95)
TEAL = (14, 124, 123)
GOLD = (201, 162, 39)
LIGHT = (233, 227, 214)
PANEL = (255, 253, 247)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


F_DATE = font(SERIF_B, 34)
F_STRIP = font(SANS_B, 12)
F_COUNTS = font(SANS, 11)
F_SEC = font(SANS_B, 10)
F_UTC_T = font(SANS_B, 10)
F_UTC = font(SANS, 8)
F_NUM = font(SANS_B, 20)
F_NUM_L = font(SANS, 8)
F_BANNER = font(SANS_B, 20)
F_LEAD_H = font(SERIF_B, 15)
F_LEAD_B = font(SANS, 11)
F_BADGE = font(SANS_B, 8)
F_TILE_H = font(SANS_B, 10)
F_TILE_B = font(SANS, 9)
F_IDX_H = font(SANS_B, 9)
F_IDX_F = font(SANS, 8)
F_MAP_L = font(SANS, 7)
F_DC_T = font(SANS_B, 10)
F_DC = font(SANS, 9)

REGION_COLORS = {
    "East Asia": (192, 57, 43),
    "South Asia": (230, 126, 34),
    "Central Asia": (125, 60, 152),
    "Middle East": (183, 149, 11),
    "Europe": (31, 78, 121),
    "North America": (14, 124, 123),
    "Latin America": (34, 153, 84),
    "Africa": (147, 81, 22),
    "Oceania": (46, 134, 193),
    "Global": (93, 109, 126),
}

BADGE_FILL = {
    "OFFICIAL": (30, 122, 52),
    "CONFIRMED": (31, 78, 121),
    "REPORTED": (154, 107, 0),
}


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap measured with the real font."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill=INK, leading=None):
    if leading is None:
        leading = fnt.size + 3
    lines = wrap(draw, text, fnt, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def fit_font(draw, text, fnt_path, size, max_w, min_size=7):
    """Largest size <= `size` at which `text` fits `max_w` on one line."""
    s = size
    while s > min_size:
        f = font(fnt_path, s)
        if draw.textlength(text, font=f) <= max_w:
            return f
        s -= 1
    return font(fnt_path, min_size)


def draw_wrapped_max(draw, x, y, text, fnt, max_w, max_lines, fill=INK, leading=None):
    """Wrapped text truncated to at most `max_lines` (ellipsis on the last)."""
    if leading is None:
        leading = fnt.size + 3
    lines = wrap(draw, text, fnt, max_w)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and draw.textlength(lines[-1] + "\u2026", font=fnt) > max_w:
            lines[-1] = lines[-1][:-1].rstrip()
        lines[-1] += "\u2026"
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def badge(draw, x, y, kind):
    w = int(draw.textlength(kind, font=F_BADGE)) + 12
    h = 13
    draw.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=BADGE_FILL[kind])
    draw.text((x + 6, y + 2), kind, font=F_BADGE, fill=(255, 255, 255))
    return w


def grain(img):
    """Deterministic print grain on the paper, drawn before any content."""
    rnd = random.Random(26112026)
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for _ in range(7000):
        x = rnd.randint(0, W - 1)
        y = rnd.randint(0, H - 1)
        d.point((x, y), fill=(60, 50, 30, 18))
    img.alpha_composite(ov)


# ---------------------------------------------------------------- data

LEADS = [
    {
        "banner": "7 WARHEAD TYPES",
        "banner_bg": (123, 30, 30),
        "headline": "Kim orders tactical nukes spread wider",
        "body": "KCNA says Kim Jong Un inspected new Hwasan warheads and urged tactical nuclear weapons deployed across more domains.",
        "badge": "CONFIRMED",
        "region": "East Asia",
        "field": "Conflict",
        "illo": "nukes",
    },
    {
        "banner": "+3.05%",
        "banner_bg": (20, 90, 50),
        "headline": "Asia rebounds as tariff fears fade",
        "body": "Taiex leads the rally at +3.05%; Kospi +1.88% and Nikkei +1.85% climb back after days of heavy selling.",
        "badge": "CONFIRMED",
        "region": "East Asia",
        "field": "Economy",
        "illo": "markets",
    },
    {
        "banner": "60 MPH",
        "banner_bg": (31, 78, 121),
        "headline": "Nor'easter slams New York on Thanksgiving",
        "body": "National Weather Service warns of gusts to 60 mph and 1\u20133 inches of rain from 10 a.m. as the storm hits the city.",
        "badge": "OFFICIAL",
        "region": "North America",
        "field": "Weather",
        "illo": "storm",
    },
]

TILES = [
    {
        "headline": "Houthis claim hit on Saudi's biggest refinery",
        "body": "Crude rallies as Houthis say they hit the largest refinery.",
        "badge": "REPORTED", "region": "Middle East", "field": "Conflict", "illo": "refinery",
    },
    {
        "headline": "King tides flood California coast",
        "body": "Peak at 11:38 a.m. in Marin County; waves 20\u201330 ft, Bay floods.",
        "badge": "CONFIRMED", "region": "North America", "field": "Weather", "illo": "tides",
    },
    {
        "headline": "Thanksgiving NFL: Bears\u2013Lions for the North",
        "body": "Both 8\u20132 in the biggest early-window game ever.",
        "badge": "CONFIRMED", "region": "North America", "field": "Sport", "illo": "nfl",
    },
    {
        "headline": "Four nations demand Gaza aid access",
        "body": "Four nations call for immediate, unrestricted aid amid Gaza floods.",
        "badge": "CONFIRMED", "region": "Middle East", "field": "Humanitarian", "illo": "aid",
    },
    {
        "headline": "Second US judge blocks birthright order",
        "body": "Judge Cooper: no new exceptions to US-born citizenship.",
        "badge": "CONFIRMED", "region": "North America", "field": "Law", "illo": "court",
    },
    {
        "headline": "US details $12bn in Venezuelan oil revenue",
        "body": "State Dept tracks oil, mineral money a year after Maduro's capture.",
        "badge": "OFFICIAL", "region": "Latin America", "field": "Economy", "illo": "oil",
    },
    {
        "headline": "Tanker hit by unknown projectile off Dubai",
        "body": "UK agency reports an explosion west of Dubai; no casualties so far.",
        "badge": "REPORTED", "region": "Middle East", "field": "Conflict", "illo": "tanker",
    },
    {
        "headline": "Deir al-Balah apartment hit; 2 killed",
        "body": "Al Jazeera reports a strike on a residential apartment in central Gaza.",
        "badge": "REPORTED", "region": "Middle East", "field": "Conflict", "illo": "apartment",
    },
    {
        "headline": "Ramaphosa wins Farmgate reprieve",
        "body": "President escapes impeachment probe over the Farmgate scandal.",
        "badge": "CONFIRMED", "region": "Africa", "field": "Politics", "illo": "saflag",
    },
    {
        "headline": "Tech stocks swing as AI faith weakens",
        "body": "Tech shares swing wildly as faith in the AI trade weakens.",
        "badge": "CONFIRMED", "region": "Global", "field": "Markets", "illo": "tech",
    },
]

INDEX = [
    ("Greer: new tariffs \u2018months away\u2019", "USTR chief says India duties won't bite for months", "North America", "Trade", "CONFIRMED"),
    ("Spain heads to snap polls Sunday", "39m voters; PP 31.5%, PSOE 29%, Vox 17.9%", "Europe", "Politics", "CONFIRMED"),
    ("Trump proposes fresh tariffs, incl. China", "NYT front page: new tariff push after midterms", "North America", "Trade", "REPORTED"),
    ("Saudi intercepts Houthi missiles", "Over Riyadh, after Jeddah and Jazan attacks", "Middle East", "Conflict", "REPORTED"),
    ("Houthis hit Saudi PIF tower a 2nd time", "Two Indians hurt in Riyadh financial-district strike", "Middle East", "Conflict", "REPORTED"),
    ("Europeans \u2018ready to talk again to Putin\u2019", "Le Monde front page on Ukraine diplomacy", "Europe", "Politics", "REPORTED"),
    ("Argentina enters recession", "El Pa\u00eds: economy contracts as Milei era bites", "Latin America", "Economy", "REPORTED"),
    ("Thousands protest gender violence", "Marches across Spain on eve of Sunday vote", "Europe", "Society", "REPORTED"),
    ("Helsing weighs mega-acquisition", "Handelsblatt: defence startup eyes big deal", "Europe", "Tech", "REPORTED"),
    ("Perfumers fined for colluding", "FT: fragrance houses penalised over price-fixing", "Europe", "Business", "REPORTED"),
    ("Bid to block NYC rent freeze dismissed", "NYT: challenge to rent freeze rejected", "North America", "Law", "REPORTED"),
    ("India food costs keep rising", "BBC: putting food on the table gets pricier", "South Asia", "Economy", "REPORTED"),
    ("Mexico probes CIA-aiding prosecutor", "Cartel links alleged against prosecutor", "Latin America", "Law", "REPORTED"),
    ("Rojava Kurds rally behind Kurdistan", "Amid conflict with Iraq, Kurds unite", "Middle East", "Politics", "REPORTED"),
    ("Riner: Ukraine \u2018not our conflict\u2019", "Judoka-turned-candidate breaks with consensus", "Europe", "Politics", "REPORTED"),
    ("Report: Iran advances hybrid missiles", "Cluster warheads among new stockpile, report says", "Middle East", "Conflict", "REPORTED"),
    ("Iraq: US troop decisions \u2018independent\u2019", "Baghdad pushes back on stationing claims", "Middle East", "Politics", "REPORTED"),
    ("Israeli troops raid homes in S. Syria", "Civilian detained in cross-border operation", "Middle East", "Conflict", "REPORTED"),
    ("Puigdemont to return to Spain Dec 12", "Catalan separatist sets date after Sunday's vote", "Europe", "Politics", "REPORTED"),
    ("Ukraine helps Norway harden air defences", "Kyiv aids Oslo on the Russia border", "Europe", "Conflict", "REPORTED"),
    ("Germany rebuilds Hitler's Eagle's Nest", "Nazi retreat restored after fire damage", "Europe", "Culture", "REPORTED"),
    ("Gaza winter aid \u2018out of reach\u2019", "Needy families can't get survival items", "Middle East", "Humanitarian", "REPORTED"),
    ("Titanic postcard sells at auction", "Sent days before the doomed voyage", "Europe", "Culture", "REPORTED"),
    ("France faces backlash over Ukraine troops", "Troop deployment plan draws fire at home", "Europe", "Politics", "REPORTED"),
    ("Extreme El Ni\u00f1o stokes Amazon fears", "Weeks of severe weather fuel worry", "Latin America", "Climate", "REPORTED"),
    ("UK won't extend EU student tuition rates", "Burnham: no equal fees for EU students", "Europe", "Education", "REPORTED"),
    ("RAF shelters jets amid drone threat", "Planes moved into hangars overnight", "Europe", "Conflict", "REPORTED"),
    ("Jordan sentences man to death", "For killing a police officer in attack", "Middle East", "Law", "REPORTED"),
    ("Zimbabwe issues warrant for Mugabe's son", "After he misses court appearance", "Africa", "Law", "REPORTED"),
    ("Russian ship \u2018blocking GPS\u2019 near UK", "Several passenger jets affected, reports say", "Europe", "Conflict", "REPORTED"),
    ("Lithuania backs easier EU visas", "For Azerbaijanis, ahead of 2027 presidency", "Europe", "Politics", "REPORTED"),
    ("Ukraine claims Smolensk site destroyed", "Russian aerospace recon site hit, Kyiv says", "Europe", "Conflict", "REPORTED"),
    ("Peru closes dozens of ports", "Powerful currents batter the coastline", "Latin America", "Weather", "REPORTED"),
    ("Australia passes online safety law", "Tech firms face fines up to 5% of revenue", "Oceania", "Tech", "REPORTED"),
    ("Kazakhstan \u2018secretly\u2019 moving activist", "Chechen Mansur Movlaev faces extradition to Russia", "Central Asia", "Law", "REPORTED"),
    ("Fiji closes schools early in drought", "El Ni\u00f1o drought shuts classes Nov 30\u2013Dec 4", "Oceania", "Climate", "REPORTED"),
    ("\u2018700 Israelis in West Bank attacks\u2019", "Israeli army radio figure, reported Thursday", "Middle East", "Conflict", "REPORTED"),
]

UTC_EVENTS = [
    ("00:52", "Kospi hits intraday high, +2.07%, in Seoul"),
    ("03:35", "Bitcoin $60,564 \u00b7 gold $3,604 in early Asia trade"),
    ("04:22", "Israeli radio: 700 Israelis in W. Bank attacks"),
    ("15:00", "NWS wind warning takes effect in New York"),
    ("18:00", "Bears\u2013Lions kick off in Detroit, both 8\u20132"),
    ("19:38", "King tide peaks in Marin County, California"),
    ("21:30", "Eagles\u2013Cowboys kick off in Dallas"),
]

NUMBERS = [
    ("+3.05%", "TAIEX, ASIA'S BEST DAY"),
    ("$94.71", "BRENT CRUDE, EARLY ASIA"),
    ("$60,564", "BITCOIN, 03:35 UTC"),
    ("$3,604", "GOLD, 03:35 UTC"),
    ("60 MPH", "NYC WIND GUSTS, NWS"),
    ("$12BN", "VENEZUELA OIL REVENUE"),
]

PINS = [
    ("PYONGYANG", 39.0, 125.8),
    ("TAIPEI", 25.0, 121.6),
    ("NEW YORK", 40.7, -74.0),
    ("SAN FRANCISCO", 37.8, -122.4),
    ("DETROIT", 42.3, -83.0),
    ("GAZA", 31.5, 34.5),
    ("RIYADH", 24.7, 46.7),
    ("DUBAI", 25.2, 55.3),
    ("CARACAS", 10.5, -66.9),
    ("JOBURG", -26.2, 28.0),
    ("MADRID", 40.4, -3.7),
    ("CANBERRA", -35.3, 149.1),
]

DATE_CHECK_OUT = (
    "Cairo tanker fire kills 30 \u00b7 Shenzhou-24 docks, first Pakistani astronaut \u00b7 "
    "Macy's parade moved to Saturday \u00b7 USTR proposes 25% India tariffs \u00b7 CIA hack first "
    "reported \u00b7 Shanghai chief Chen probe announced \u00b7 NATO space vow \u00b7 Jolie\u2013Pitt "
    "winery settlement \u2014 all Wed 25 Nov or earlier."
)
DATE_CHECK_NOT_YET = (
    "Spain votes Sun 29 Nov \u00b7 Macy's parade Sat 28 Nov \u00b7 Estonia's Russia border shuts "
    "Dec 1 \u00b7 USTR tariff hearings Jan 25, 2027."
)

# land boxes (lat_min, lat_max, lon_min, lon_max) for the dotted world map
LAND_BOXES = [
    (60, 72, -168, -140), (58, 71, -140, -95), (50, 70, -95, -55),
    (45, 60, -125, -66), (30, 45, -125, -66), (25, 32, -117, -80),
    (15, 25, -105, -86), (8, 18, -92, -79), (60, 70, -25, -12),
    (55, 70, 5, 30), (50, 60, -5, 30), (43, 55, -10, 30),
    (36, 45, -10, 28), (36, 44, 28, 45), (58, 72, 30, 60),
    (50, 70, 60, 180), (40, 58, 40, 75), (30, 50, 75, 135),
    (20, 35, 68, 90), (8, 28, 75, 100), (20, 30, 100, 122),
    (8, 23, 98, 110), (0, 15, 95, 110), (-5, 8, 95, 120),
    (-10, 0, 110, 141), (30, 42, 130, 142), (35, 45, 138, 145),
    (15, 35, -17, -5), (5, 30, -5, 35), (0, 15, -15, 45),
    (-5, 5, 8, 42), (-18, 0, 12, 40), (-30, -18, 12, 33),
    (-35, -30, 18, 28), (5, 12, -75, -60), (-5, 10, -80, -60),
    (-15, -2, -80, -40), (-25, -15, -70, -35), (-35, -25, -70, -55),
    (-40, -35, -73, -62), (-10, -25, 113, 150), (-25, -38, 113, 153),
    (-38, -47, 145, 150), (-34, -42, 166, 178), (-46, -34, 166, 178),
    (30, 38, 30, 36), (12, 30, 32, 45), (12, 18, 42, 52),
    (24, 30, 50, 58), (10, 15, -15, -10),
]


# ---------------------------------------------------------------- illustrations

def illo_nukes(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(22, 35, 58))
    d.ellipse([x + w - 78, y + 8, x + w - 18, y + 68], fill=(179, 39, 30))
    d.polygon([(x + 8, y + h), (x + 60, y + h - 42), (x + 120, y + h),
               (x + 180, y + h - 30), (x + 250, y + h), (x + w, y + h - 18),
               (x + w, y + h), (x, y + h)], fill=(12, 20, 34))
    for i in range(7):
        mx = x + 22 + i * 42
        mh = 58 + (i % 3) * 10
        my = y + h - 26 - mh
        d.rectangle([mx, my + 14, mx + 12, y + h - 26], fill=(220, 222, 226))
        d.polygon([(mx, my + 16), (mx + 6, my), (mx + 12, my + 16)], fill=(220, 222, 226))
        d.rectangle([mx - 3, y + h - 30, mx + 15, y + h - 24], fill=(90, 96, 104))
        d.ellipse([mx + 3, my + 22, mx + 9, my + 28], fill=(179, 39, 30))
    d.text((x + 12, y + 8), "HWASAN-14 \u00b7 21 \u00b7 22 \u00b7 23 \u00b7 24 \u00b7 25",
           font=font(SANS_B, 9), fill=(255, 255, 255))
    for sx, sy in [(30, 20), (120, 14), (200, 22), (280, 16), (90, 30), (250, 34)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(200, 210, 230))


def illo_markets(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 240, 222))
    for gy in range(5):
        yy = y + 12 + gy * (h - 24) // 4
        d.line([x + 8, yy, x + w - 8, yy], fill=(190, 215, 198), width=1)
    bars = [(30, 34), (72, 52), (114, 46), (156, 74), (198, 66), (240, 96), (282, 88)]
    for bx, bh in bars:
        d.rectangle([x + bx, y + h - 14 - bh, x + bx + 26, y + h - 14],
                    fill=(20, 120, 70) if bh > 60 else (46, 160, 100))
    d.line([(x + 30, y + h - 48), (x + 100, y + h - 66), (x + 160, y + h - 88),
            (x + 230, y + h - 96), (x + 300, y + h - 116)],
           fill=(123, 30, 30), width=3)
    d.polygon([(x + 300, y + h - 116), (x + 288, y + h - 110), (x + 296, y + h - 100)],
              fill=(123, 30, 30))
    d.text((x + 12, y + 8), "KOSPI +1.88%  \u00b7  NIKKEI +1.85%  \u00b7  TAIEX +3.05%",
           font=font(SANS_B, 9), fill=(20, 90, 50))


def illo_storm(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 74, 96))
    d.ellipse([x + 18, y + 6, x + 118, y + 46], fill=(38, 54, 72))
    d.ellipse([x + 80, y + 2, x + 180, y + 40], fill=(44, 62, 82))
    d.ellipse([x + 150, y + 10, x + 250, y + 48], fill=(38, 54, 72))
    d.ellipse([x + 230, y + 4, x + 310, y + 42], fill=(44, 62, 82))
    for bx, bw, bh in [(10, 34, 60), (48, 26, 84), (78, 30, 66), (112, 24, 92),
                       (140, 36, 58), (180, 26, 78), (210, 30, 64), (244, 28, 88),
                       (276, 34, 56)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(24, 34, 46))
    for wx in (60, 120, 180, 240, 300):
        for wy in (58, 82, 106):
            d.line([x + wx, y + wy, x + wx - 8, y + wy + 14], fill=(180, 200, 220), width=2)
    d.arc([x + w - 66, y + h - 52, x + w - 6, y + h - 2], 200, 340,
          fill=(255, 255, 255), width=3)


def illo_refinery(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(248, 196, 120))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(90, 60, 30))
    for tx, th in [(16, 20), (52, 16), (88, 24), (124, 18), (156, 22)]:
        top = y + h - 12 - th
        d.rectangle([x + tx, top, x + tx + 16, y + h - 12], fill=(70, 70, 78))
        d.rectangle([x + tx + 5, top - 6, x + tx + 11, top], fill=(70, 70, 78))
        d.ellipse([x + tx + 2, top - 14, x + tx + 14, top - 2],
                  fill=(230, 230, 230))
    d.polygon([(x + w - 34, y + 8), (x + w - 22, y + 24), (x + w - 10, y + 8),
               (x + w - 16, y + 30), (x + w - 30, y + 30)], fill=(230, 120, 20))
    d.polygon([(x + w - 28, y + 26), (x + w - 22, y + 38), (x + w - 16, y + 26)],
              fill=(255, 200, 40))


def illo_tides(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(183, 219, 238))
    d.rectangle([x, y, x + w, y + 16], fill=(240, 244, 248))
    d.polygon([(x, y + h), (x + 60, y + 18), (x + 130, y + h)], fill=(46, 134, 193))
    d.polygon([(x + 60, y + h), (x + 130, y + 18), (x + 194, y + h)], fill=(31, 110, 170))
    d.arc([x + 96, y + 10, x + 150, y + 40], 180, 360, fill=(255, 255, 255), width=3)
    d.rectangle([x + 14, y + 26, x + 54, y + 40], fill=(140, 90, 50))
    d.polygon([(x + 10, y + 26), (x + 34, y + 14), (x + 58, y + 26)], fill=(123, 30, 30))
    d.rectangle([x + 150, y + 30, x + 182, y + 42], fill=(140, 90, 50))
    d.polygon([(x + 146, y + 30), (x + 166, y + 18), (x + 186, y + 30)], fill=(123, 30, 30))


def illo_nfl(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(46, 139, 87))
    for i in range(5):
        yy = y + 8 + i * (h - 16) // 4
        d.line([x, yy, x + w, yy], fill=(255, 255, 255), width=1)
    d.line([x + 18, y + 6, x + 18, y + h - 6], fill=(255, 214, 0), width=3)
    d.line([x + w - 18, y + 6, x + w - 18, y + h - 6], fill=(255, 214, 0), width=3)
    d.ellipse([x + w // 2 - 34, y + h // 2 - 13, x + w // 2 + 34, y + h // 2 + 13],
              fill=(139, 90, 43))
    d.line([x + w // 2 - 24, y + h // 2, x + w // 2 + 24, y + h // 2],
           fill=(255, 255, 255), width=2)
    for lx in (-12, -4, 4, 12):
        d.line([x + w // 2 + lx, y + h // 2 - 5, x + w // 2 + lx, y + h // 2 + 5],
               fill=(255, 255, 255), width=2)


def illo_aid(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 232, 240))
    for tx in (12, 78, 144):
        d.rectangle([x + tx, y + 22, x + tx + 40, y + 38], fill=(255, 255, 255))
        d.rectangle([x + tx + 40, y + 26, x + tx + 52, y + 38], fill=(220, 222, 226))
        d.rectangle([x + tx + 14, y + 26, x + tx + 26, y + 34], fill=(179, 39, 30))
        d.ellipse([x + tx + 8, y + 38, x + tx + 16, y + 46], fill=(26, 26, 26))
        d.ellipse([x + tx + 36, y + 38, x + tx + 44, y + 46], fill=(26, 26, 26))
    d.polygon([(x + 150, y + h - 4), (x + 172, y + h - 22), (x + 194, y + h - 4)],
              fill=(240, 240, 230))
    d.polygon([(x + 20, y + h - 4), (x + 40, y + h - 18), (x + 60, y + h - 4)],
              fill=(240, 240, 230))
    for rx in (30, 90, 150, 180):
        d.line([x + rx, y + 8, x + rx - 3, y + 16], fill=(100, 140, 180), width=2)


def illo_court(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 210))
    d.polygon([(x + 20, y + 10), (x + w // 2, y + 2), (x + w - 20, y + 10)],
              fill=(140, 120, 90))
    for cx in (30, 66, 102, 138, 168):
        d.rectangle([x + cx, y + 14, x + cx + 10, y + h - 12], fill=(255, 255, 255))
    d.rectangle([x + 12, y + h - 12, x + w - 12, y + h - 6], fill=(140, 120, 90))
    d.rectangle([x + 84, y + 26, x + 98, y + h - 12], fill=(60, 60, 66))


def illo_oil(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 226, 160))
    d.polygon([(x + 20, y + h - 8), (x + 44, y + 6), (x + 68, y + h - 8)], fill=(40, 40, 40))
    d.line([x + 32, y + h - 8, x + 50, y + 12], fill=(40, 40, 40), width=2)
    d.line([x + 56, y + h - 8, x + 38, y + 12], fill=(40, 40, 40), width=2)
    for cy in (34, 28, 22):
        d.ellipse([x + 120, y + h - 8 - cy, x + 150, y + h - 2 - cy + 10],
                  fill=(201, 162, 39))
    d.ellipse([x + 120, y + h - 42, x + 150, y + h - 32], fill=(230, 190, 60))
    d.rectangle([x + 158, y + h - 26, x + 182, y + h - 8], fill=(60, 60, 66))
    d.rectangle([x + 158, y + h - 32, x + 182, y + h - 26], fill=(40, 40, 44))


def illo_tanker(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(183, 219, 238))
    d.polygon([(x + 120, y + 6), (x + 132, y + 20), (x + 144, y + 6), (x + 138, y + 26),
               (x + 150, y + 26), (x + 136, y + 34), (x + 142, y + 44), (x + 128, y + 38),
               (x + 118, y + 46), (x + 122, y + 34), (x + 110, y + 28), (x + 124, y + 24)],
              fill=(230, 120, 20))
    d.ellipse([x + 108, y + 2, x + 128, y + 16], fill=(120, 120, 120))
    d.ellipse([x + 140, y + 10, x + 158, y + 24], fill=(120, 120, 120))
    d.rectangle([x + 12, y + 30, x + 150, y + 44], fill=(40, 40, 44))
    d.rectangle([x + 130, y + 18, x + 152, y + 30], fill=(255, 255, 255))
    d.rectangle([x + 150, y + 34, x + 182, y + 44], fill=(90, 60, 30))


def illo_apartment(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(220, 205, 180))
    d.rectangle([x + 20, y + 8, x + 90, y + h - 6], fill=(240, 228, 200))
    d.rectangle([x + 100, y + 16, x + 160, y + h - 6], fill=(228, 212, 182))
    for wx in (30, 54, 78):
        for wy in (16, 30):
            d.rectangle([x + wx, y + wy, x + wx + 12, y + wy + 10], fill=(90, 110, 140))
    for wx in (112, 134):
        for wy in (24, 38):
            d.rectangle([x + wx, y + wy, x + wx + 10, y + wy + 8], fill=(90, 110, 140))
    d.ellipse([x + 150, y + 2, x + 176, y + 20], fill=(140, 140, 140))
    d.ellipse([x + 164, y + 12, x + 190, y + 30], fill=(120, 120, 120))
    d.rectangle([x + 54, y + 16, x + 66, y + 26], fill=(26, 26, 26))


def illo_saflag(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 240, 235))
    d.rectangle([x + 12, y + 6, x + w - 12, y + h - 6], fill=(0, 122, 77))
    d.polygon([(x + 12, y + 6), (x + 12, y + h - 6), (x + 70, y + h // 2 + 2)],
              fill=(0, 0, 0))
    d.polygon([(x + 12, y + 6), (x + w - 12, y + 6), (x + 70, y + h // 2 - 2),
               (x + 12, y + h // 2 - 2)], fill=(222, 56, 44))
    d.polygon([(x + 12, y + h - 6), (x + w - 12, y + h - 6), (x + 70, y + h // 2 + 2),
               (x + 12, y + h // 2 + 2)], fill=(0, 58, 150))
    d.polygon([(x + 12, y + 6), (x + 84, y + h // 2), (x + 12, y + h - 6),
               (x + 12, y + h // 2 + 6), (x + 66, y + h // 2), (x + 12, y + h // 2 - 6)],
              fill=(255, 255, 255))
    d.polygon([(x + 12, y + 6), (x + 78, y + h // 2), (x + 12, y + h - 6),
               (x + 12, y + h // 2 + 4), (x + 62, y + h // 2), (x + 12, y + h // 2 - 4)],
              fill=(0, 122, 77))


def illo_tech(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(22, 35, 58))
    pts = [(x + 8, y + 34), (x + 40, y + 18), (x + 70, y + 30), (x + 100, y + 12),
           (x + 130, y + 26), (x + 160, y + 10), (x + 186, y + 20)]
    d.line(pts, fill=(255, 214, 0), width=2)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 214, 0))
    d.rectangle([x + 12, y + h - 22, x + 34, y + h - 4], fill=(60, 90, 130))
    d.rectangle([x + 12, y + h - 22, x + 34, y + h - 4], outline=(180, 200, 220))
    for i in range(3):
        d.line([x + 14 + i * 7, y + h - 22, x + 14 + i * 7, y + h - 26],
               fill=(180, 200, 220), width=2)
    d.rectangle([x + 44, y + h - 16, x + 62, y + h - 4], fill=(90, 60, 120))
    d.rectangle([x + 44, y + h - 16, x + 62, y + h - 4], outline=(180, 200, 220))


ILLOS = {
    "nukes": illo_nukes, "markets": illo_markets, "storm": illo_storm,
    "refinery": illo_refinery, "tides": illo_tides, "nfl": illo_nfl,
    "aid": illo_aid, "court": illo_court, "oil": illo_oil,
    "tanker": illo_tanker, "apartment": illo_apartment, "saflag": illo_saflag,
    "tech": illo_tech,
}


# ---------------------------------------------------------------- map

def in_land(lat, lon):
    for la0, la1, lo0, lo1 in LAND_BOXES:
        if la0 <= lat <= la1 and lo0 <= lon <= lo1:
            return True
    return False


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 232, 240))
    cell = 6
    for gy in range(h // cell):
        for gx in range(w // cell):
            lon = -180 + (gx + 0.5) * cell / w * 360
            lat = 90 - (gy + 0.5) * cell / h * 180
            if in_land(lat, lon):
                cx = x + gx * cell + 2
                cy = y + gy * cell + 2
                d.ellipse([cx, cy, cx + 2, cy + 2], fill=(90, 110, 130))
    for name, lat, lon in PINS:
        px = x + int((lon + 180) / 360 * w)
        py = y + int((90 - lat) / 180 * h)
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(179, 39, 30),
                  outline=(255, 255, 255))
        d.ellipse([px - 1, py - 1, px + 1, py + 1], fill=(255, 255, 255))
        lx = px + 6 if lon < 120 else px - 6 - int(d.textlength(name, font=F_MAP_L))
        ly = py - 9
        if name in ("GAZA", "RIYADH"):
            ly = py + 6
        if name == "DUBAI":
            lx = px + 6
            ly = py - 9
        d.text((lx, ly), name, font=F_MAP_L, fill=(26, 26, 26))


# ---------------------------------------------------------------- build

def build():
    img = Image.new("RGBA", (W, H), PAPER + (255,))
    grain(img)
    d = ImageDraw.Draw(img)

    # ---- masthead
    date = "THURSDAY 26 NOVEMBER 2026"
    dw = d.textlength(date, font=F_DATE)
    d.text(((W - dw) / 2, 8), date, font=F_DATE, fill=INK)
    strip = "ONE DAY OF WORLD NEWS, ONE PICTURE"
    sw = d.textlength(strip, font=F_STRIP)
    d.line([M + 40, 56, (W - sw) / 2 - 14, 56], fill=RED, width=2)
    d.line([(W + sw) / 2 + 14, 56, W - M - 40, 56], fill=RED, width=2)
    d.text(((W - sw) / 2, 48), strip, font=F_STRIP, fill=RED)
    regions = sorted({s["region"] for s in LEADS + TILES} |
                     {r for _, _, r, _, _ in INDEX})
    fields = sorted({s["field"] for s in LEADS + TILES} |
                    {f for _, _, _, f, _ in INDEX})
    total = len(LEADS) + len(TILES) + len(INDEX)
    counts = (f"{total} STORIES \u00b7 {len(regions)} REGIONS \u00b7 {len(fields)} FIELDS "
              "\u00b7 EVERY ONE FROM THIS THURSDAY")
    cw = d.textlength(counts, font=F_COUNTS)
    d.text(((W - cw) / 2, 66), counts, font=F_COUNTS, fill=INK)
    d.line([M, 82, W - M, 82], fill=RULE, width=2)

    # ---- UTC strip
    y = 88
    d.text((M, y), "THE DAY IN UTC", font=F_SEC, fill=RED)
    y += 14
    col_w = (W - 2 * M - 6 * 6) / 7
    for i, (t, ev) in enumerate(UTC_EVENTS):
        cx = M + i * (col_w + 6)
        d.text((cx, y), t, font=F_UTC_T, fill=NAVY)
        draw_wrapped(d, cx, y + 12, ev, F_UTC, col_w, leading=10)
        if i < 6:
            d.line([cx + col_w + 3, y, cx + col_w + 3, y + 34], fill=(200, 192, 176), width=1)
    d.line([M, 132, W - M, 132], fill=(200, 192, 176), width=1)

    # ---- numbers strip
    y = 138
    d.text((M, y), "THE DAY IN NUMBERS", font=F_SEC, fill=RED)
    y += 14
    cell_w = (W - 2 * M - 5 * 6) / 6
    for i, (num, lab) in enumerate(NUMBERS):
        cx = M + i * (cell_w + 6)
        nf = fit_font(d, num, SANS_B, 20, cell_w, min_size=14)
        d.text((cx, y), num, font=nf, fill=NAVY)
        draw_wrapped(d, cx, y + 22, lab, F_NUM_L, cell_w, fill=GREY, leading=10)
    d.line([M, 176, W - M, 176], fill=RULE, width=2)

    # ---- leads
    y0 = 184
    lead_w = (W - 2 * M - 2 * 10) / 3
    illo_h = 124
    for i, lead in enumerate(LEADS):
        lx = M + i * (lead_w + 10)
        d.rectangle([lx, y0, lx + lead_w, y0 + 30], fill=lead["banner_bg"])
        bw = d.textlength(lead["banner"], font=F_BANNER)
        d.text((lx + (lead_w - bw) / 2, y0 + 4), lead["banner"], font=F_BANNER,
               fill=(255, 255, 255))
        iy = y0 + 30
        ILLOS[lead["illo"]](d, int(lx), iy, int(lead_w), illo_h)
        hy = iy + illo_h + 8
        hy = draw_wrapped(d, int(lx), hy, lead["headline"], F_LEAD_H, lead_w,
                          leading=18)
        hy += 2
        hy = draw_wrapped(d, int(lx), hy, lead["body"], F_LEAD_B, lead_w, leading=14)
        by = y0 + 30 + illo_h + 8 + 36 + 56
        bw2 = badge(d, int(lx), int(by), lead["badge"])
        reg = f"{lead['region'].upper()} \u00b7 {lead['field'].upper()}"
        d.text((lx + bw2 + 8, by + 2), reg, font=F_BADGE, fill=GREY)
    leads_bottom = y0 + 30 + illo_h + 8 + 36 + 56 + 13

    # ---- tiles (5 x 2)
    ty0 = leads_bottom + 6
    tile_w = (W - 2 * M - 4 * 8) / 5
    tile_h = 116
    for i, tile in enumerate(TILES):
        row, col = divmod(i, 5)
        tx = M + col * (tile_w + 8)
        ty = ty0 + row * (tile_h + 6)
        ILLOS[tile["illo"]](d, int(tx), int(ty), int(tile_w), 50)
        hy = draw_wrapped_max(d, int(tx), int(ty + 54), tile["headline"], F_TILE_H,
                              tile_w, 2, leading=12)
        draw_wrapped_max(d, int(tx), int(hy + 2), tile["body"], F_TILE_B, tile_w, 2,
                         fill=(60, 60, 60), leading=11)
        badge(d, int(tx), int(ty + tile_h - 13), tile["badge"])
    tiles_bottom = ty0 + 2 * tile_h + 6

    # ---- bottom band: map + index
    by0 = tiles_bottom + 6
    d.line([M, by0 - 4, W - M, by0 - 4], fill=RULE, width=2)
    map_w = 286
    map_x = M
    idx_x = M + map_w + 8
    idx_w = W - M - idx_x
    d.text((map_x, by0), "WHERE IT HAPPENED", font=F_SEC, fill=RED)
    d.text((idx_x, by0), f"THE DAY IN BRIEF \u2014 {len(INDEX)} MORE STORIES",
           font=F_SEC, fill=RED)
    my = by0 + 16
    map_h = 956 - my
    draw_map(d, map_x, my, map_w, map_h)
    # index: 3 columns
    cols = 3
    per_col = (len(INDEX) + cols - 1) // cols
    col_w = (idx_w - 2 * 10) / cols
    row_h = (956 - (by0 + 16)) / per_col
    for ci in range(cols):
        cx = idx_x + ci * (col_w + 10)
        for ri in range(per_col):
            k = ci * per_col + ri
            if k >= len(INDEX):
                break
            head, fact, region, field, bdg = INDEX[k]
            ry = by0 + 16 + ri * row_h
            d.ellipse([cx, ry + 2, cx + 6, ry + 8], fill=REGION_COLORS[region])
            tx = cx + 10
            hf = fit_font(d, head, SANS_B, 9, col_w - 10, min_size=7)
            d.text((tx, ry), head, font=hf, fill=INK)
            ff = fit_font(d, fact, SANS, 8, col_w - 10, min_size=7)
            d.text((tx, ry + 9), fact, font=ff, fill=GREY)

    # ---- date check
    dy = 962
    d.rectangle([M, dy, W - M, 1018], outline=RULE, width=1, fill=PANEL)
    d.text((M + 10, dy + 6), "DATE CHECK \u2014 WHAT WE LEFT OUT, AND WHAT HAS NOT HAPPENED YET",
           font=F_DC_T, fill=RED)
    ty = dy + 20
    ty = draw_wrapped(d, M + 10, ty, "NOT THIS DAY: " + DATE_CHECK_OUT, F_DC,
                      W - 2 * M - 20, leading=11)
    draw_wrapped(d, M + 10, ty + 1, "NOT YET: " + DATE_CHECK_NOT_YET, F_DC,
                 W - 2 * M - 20, leading=11)

    return img.convert("RGB")


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    build().save(out, "PNG", optimize=True)
    print("saved", out)
