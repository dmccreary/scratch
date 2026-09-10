#!/usr/bin/env python3
"""Generate the seven mascot poses for Cody the CoderDojo Turtle as SVG.

All poses share one geometry definition so the character stays identical
across the set.  Rasterised to transparent PNG by headless Chrome.
"""
import math
import os
import sys

OUT = sys.argv[1]

W = H = 512

# ---- Palette (CoderDojo purple #642580 / teal #41BAC1) -------------------
SHELL      = "#642580"
SHELL_DK   = "#43164F"
SCUTE      = "#8E44AD"
TEAL       = "#41BAC1"
TEAL_DK    = "#2A7F86"
SKIN       = "#8BC34A"
SKIN_DK    = "#55892C"
BELLY      = "#FBEFC8"
BELLY_DK   = "#DCC48A"
INK        = "#26323F"
BLUSH      = "#F48FB1"
MOUTH_IN   = "#5D2A33"
TONGUE     = "#F48FB1"
BULB       = "#FFE082"
BULB_DK    = "#F9A825"

# ---- Geometry ------------------------------------------------------------
HEAD_CX, HEAD_CY, HEAD_RX, HEAD_RY = 256, 150, 80, 74
BODY_CX, BODY_CY, BODY_RX, BODY_RY = 256, 305, 112, 100
BELLY_RX, BELLY_RY = 68, 62
SH_L = (182, 252)      # screen-left shoulder
SH_R = (330, 252)      # screen-right shoulder
HAND_L_DOWN = (112, 348)
HAND_R_DOWN = (400, 348)

EYE_L = (222, 144)
EYE_R = (290, 144)
EYE_RX, EYE_RY = 26, 28


def d(v):
    return f"{v:.1f}"


# ---- Primitives ----------------------------------------------------------
def limb(p0, ctrl, p1, w=34, hand_r=22):
    """Arm/leg: dark outline pass, then coloured pass, so joints have no seams."""
    path = f'M{d(p0[0])} {d(p0[1])} Q{d(ctrl[0])} {d(ctrl[1])} {d(p1[0])} {d(p1[1])}'
    return (
        f'<path d="{path}" fill="none" stroke="{SKIN_DK}" stroke-width="{w+12}" stroke-linecap="round"/>'
        f'<circle cx="{d(p1[0])}" cy="{d(p1[1])}" r="{hand_r+6}" fill="{SKIN_DK}"/>'
        f'<path d="{path}" fill="none" stroke="{SKIN}" stroke-width="{w}" stroke-linecap="round"/>'
        f'<circle cx="{d(p1[0])}" cy="{d(p1[1])}" r="{hand_r}" fill="{SKIN}"/>'
    )


def nub(p0, p1, w=14):
    """A finger / thumb capsule."""
    path = f'M{d(p0[0])} {d(p0[1])} L{d(p1[0])} {d(p1[1])}'
    return (
        f'<path d="{path}" fill="none" stroke="{SKIN_DK}" stroke-width="{w+12}" stroke-linecap="round"/>'
        f'<path d="{path}" fill="none" stroke="{SKIN}" stroke-width="{w}" stroke-linecap="round"/>'
    )


def hexagon(cx, cy, r, rot=0.0):
    pts = []
    for k in range(6):
        a = math.radians(rot + k * 60)
        pts.append(f"{d(cx + r*math.cos(a))},{d(cy + r*math.sin(a))}")
    return " ".join(pts)


def pen(hand, angle_deg, length=58):
    """Cody's teal marker, held in whichever hand is free."""
    a = math.radians(angle_deg)
    dx, dy = math.cos(a), math.sin(a)
    bx, by = hand[0] - dx * 12, hand[1] - dy * 12          # butt end
    tx, ty = hand[0] + dx * (length - 14), hand[1] + dy * (length - 14)  # body end
    nx, ny = hand[0] + dx * length, hand[1] + dy * length  # nib
    band = (hand[0] + dx * (length * 0.52), hand[1] + dy * (length * 0.52))
    px, py = -dy, dx                                        # perpendicular
    body = f'M{d(bx)} {d(by)} L{d(tx)} {d(ty)}'
    return (
        f'<path d="{body}" fill="none" stroke="{TEAL_DK}" stroke-width="23" stroke-linecap="round"/>'
        f'<path d="{body}" fill="none" stroke="{TEAL}" stroke-width="15" stroke-linecap="round"/>'
        f'<path d="M{d(band[0]-px*9)} {d(band[1]-py*9)} L{d(band[0]+px*9)} {d(band[1]+py*9)}" '
        f'fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" opacity="0.9"/>'
        f'<circle cx="{d(nx)}" cy="{d(ny)}" r="10" fill="{INK}"/>'
        # fist wrapped around the barrel
        f'<path d="M{d(hand[0]-px*21)} {d(hand[1]-py*21)} L{d(hand[0]+px*21)} {d(hand[1]+py*21)}" '
        f'fill="none" stroke="{SKIN_DK}" stroke-width="30" stroke-linecap="round"/>'
        f'<path d="M{d(hand[0]-px*21)} {d(hand[1]-py*21)} L{d(hand[0]+px*21)} {d(hand[1]+py*21)}" '
        f'fill="none" stroke="{SKIN}" stroke-width="22" stroke-linecap="round"/>'
    )


# ---- Body parts ----------------------------------------------------------
def legs(spread=0):
    lx, rx = 214 - spread, 298 + spread
    lfx, rfx = 196 - spread * 2, 316 + spread * 2
    out = limb((lx, 372), (lx - 4, 408), (lfx + 10, 434), w=40, hand_r=0)
    out += limb((rx, 372), (rx + 4, 408), (rfx - 10, 434), w=40, hand_r=0)
    out += (
        f'<ellipse cx="{d(lfx)}" cy="446" rx="46" ry="26" fill="{SKIN_DK}"/>'
        f'<ellipse cx="{d(lfx)}" cy="443" rx="40" ry="21" fill="{SKIN}"/>'
        f'<ellipse cx="{d(rfx)}" cy="446" rx="46" ry="26" fill="{SKIN_DK}"/>'
        f'<ellipse cx="{d(rfx)}" cy="443" rx="40" ry="21" fill="{SKIN}"/>'
    )
    return out


def tail():
    return (
        f'<path d="M292 384 Q352 386 372 414 Q336 404 288 408 Z" fill="{SKIN_DK}"/>'
        f'<path d="M294 388 Q346 390 364 412 Q332 404 290 406 Z" fill="{SKIN}"/>'
    )


def shell():
    out = (
        f'<ellipse cx="{BODY_CX}" cy="{BODY_CY}" rx="{BODY_RX+6}" ry="{BODY_RY+6}" fill="{SHELL_DK}"/>'
        f'<ellipse cx="{BODY_CX}" cy="{BODY_CY}" rx="{BODY_RX}" ry="{BODY_RY}" fill="{SHELL}"/>'
    )
    # ring of scutes
    for k in range(8):
        a = math.radians(-90 + k * 45)
        cx = BODY_CX + 90 * math.cos(a)
        cy = BODY_CY + 80 * math.sin(a)
        out += (
            f'<polygon points="{hexagon(cx, cy, 24, 30)}" fill="{SCUTE}" '
            f'stroke="{TEAL}" stroke-width="4" stroke-linejoin="round"/>'
        )
    # plastron (belly plate)
    out += (
        f'<ellipse cx="{BODY_CX}" cy="312" rx="{BELLY_RX+5}" ry="{BELLY_RY+5}" fill="{BELLY_DK}"/>'
        f'<ellipse cx="{BODY_CX}" cy="312" rx="{BELLY_RX}" ry="{BELLY_RY}" fill="{BELLY}"/>'
        f'<path d="M204 300 Q256 286 308 300" fill="none" stroke="{BELLY_DK}" '
        f'stroke-width="5" stroke-linecap="round"/>'
        f'<path d="M200 330 Q256 344 312 330" fill="none" stroke="{BELLY_DK}" '
        f'stroke-width="5" stroke-linecap="round"/>'
    )
    # gloss highlight on the shell
    out += (
        f'<ellipse cx="176" cy="252" rx="30" ry="17" fill="#FFFFFF" opacity="0.18" '
        f'transform="rotate(-32 176 252)"/>'
    )
    return out


def head(eyes="open", mouth="smile", brows=None, look=(0, 0)):
    out = (
        f'<ellipse cx="{HEAD_CX}" cy="{HEAD_CY}" rx="{HEAD_RX+6}" ry="{HEAD_RY+6}" fill="{SKIN_DK}"/>'
        f'<ellipse cx="{HEAD_CX}" cy="{HEAD_CY}" rx="{HEAD_RX}" ry="{HEAD_RY}" fill="{SKIN}"/>'
    )
    if eyes == "happy":
        for (ex, ey) in (EYE_L, EYE_R):
            out += (
                f'<path d="M{d(ex-24)} {d(ey+8)} Q{d(ex)} {d(ey-22)} {d(ex+24)} {d(ey+8)}" '
                f'fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
            )
    else:
        for (ex, ey) in (EYE_L, EYE_R):
            px, py = ex + look[0], ey + look[1]
            out += (
                f'<ellipse cx="{ex}" cy="{ey}" rx="{EYE_RX}" ry="{EYE_RY}" fill="#FFFFFF" '
                f'stroke="{INK}" stroke-width="4"/>'
                f'<circle cx="{d(px)}" cy="{d(py)}" r="13" fill="{INK}"/>'
                f'<circle cx="{d(px-5)}" cy="{d(py-6)}" r="5" fill="#FFFFFF"/>'
            )
    if brows:
        # (inner_dy) negative = raised inner brow (concerned)
        for side, (ex, _) in (("l", EYE_L), ("r", EYE_R)):
            inner = 1 if side == "l" else -1
            x0, x1 = ex - 26 * inner, ex + 26 * inner   # x0 outer, x1 inner
            y0, y1 = 108, 108 + brows
            out += (
                f'<path d="M{d(x0)} {d(y0)} Q{d((x0+x1)/2)} {d((y0+y1)/2 - 5)} {d(x1)} {d(y1)}" '
                f'fill="none" stroke="{SKIN_DK}" stroke-width="8" stroke-linecap="round"/>'
            )
    # cheeks
    out += (
        f'<ellipse cx="190" cy="184" rx="17" ry="10" fill="{BLUSH}" opacity="0.55"/>'
        f'<ellipse cx="322" cy="184" rx="17" ry="10" fill="{BLUSH}" opacity="0.55"/>'
    )
    if mouth == "smile":
        out += (f'<path d="M230 190 Q256 214 282 190" fill="none" stroke="{INK}" '
                f'stroke-width="7" stroke-linecap="round"/>')
    elif mouth == "open":
        out += (f'<path d="M226 186 Q256 234 286 186 Z" fill="{MOUTH_IN}"/>'
                f'<ellipse cx="256" cy="207" rx="16" ry="9" fill="{TONGUE}"/>')
    elif mouth == "big":
        out += (f'<path d="M218 182 Q256 244 294 182 Z" fill="{MOUTH_IN}"/>'
                f'<ellipse cx="256" cy="212" rx="19" ry="11" fill="{TONGUE}"/>')
    elif mouth == "oh":
        out += f'<ellipse cx="256" cy="199" rx="14" ry="17" fill="{MOUTH_IN}"/>'
    elif mouth == "grin":
        out += (f'<path d="M226 188 Q256 220 286 188" fill="none" stroke="{INK}" '
                f'stroke-width="7" stroke-linecap="round"/>'
                f'<path d="M226 188 L286 188" fill="none" stroke="{INK}" '
                f'stroke-width="7" stroke-linecap="round"/>')
    return out


# ---- Props ---------------------------------------------------------------
def lightbulb(cx, cy):
    return (
        f'<g stroke="{BULB_DK}" stroke-width="6" stroke-linecap="round">'
        f'<line x1="{cx}" y1="{cy-52}" x2="{cx}" y2="{cy-40}"/>'
        f'<line x1="{cx-42}" y1="{cy-30}" x2="{cx-33}" y2="{cy-22}"/>'
        f'<line x1="{cx+42}" y1="{cy-30}" x2="{cx+33}" y2="{cy-22}"/>'
        f'</g>'
        f'<circle cx="{cx}" cy="{cy}" r="30" fill="{BULB}" stroke="{BULB_DK}" stroke-width="6"/>'
        f'<rect x="{cx-13}" y="{cy+24}" width="26" height="17" rx="6" fill="{BULB_DK}"/>'
        f'<path d="M{cx-10} {cy+6} Q{cx} {cy-14} {cx+10} {cy+6}" fill="none" '
        f'stroke="{BULB_DK}" stroke-width="5" stroke-linecap="round"/>'
    )


def star(cx, cy, r):
    pts = []
    for k in range(8):
        a = math.radians(-90 + k * 45)
        rr = r if k % 2 == 0 else r * 0.38
        pts.append(f"{d(cx + rr*math.cos(a))},{d(cy + rr*math.sin(a))}")
    return (f'<polygon points="{" ".join(pts)}" fill="{BULB}" stroke="{BULB_DK}" '
            f'stroke-width="5" stroke-linejoin="round"/>')


def bang(cx, cy):
    s = 40
    return (
        f'<path d="M{cx} {cy-s} L{cx+s*0.92} {cy+s*0.62} Q{cx+s*1.06} {cy+s*0.88} '
        f'{cx+s*0.78} {cy+s*0.88} L{cx-s*0.78} {cy+s*0.88} Q{cx-s*1.06} {cy+s*0.88} '
        f'{cx-s*0.92} {cy+s*0.62} Z" fill="{BULB}" stroke="{BULB_DK}" '
        f'stroke-width="6" stroke-linejoin="round"/>'
        f'<rect x="{cx-5}" y="{cy-14}" width="10" height="26" rx="5" fill="{INK}"/>'
        f'<circle cx="{cx}" cy="{cy+24}" r="6" fill="{INK}"/>'
    )


CONFETTI = [
    (108, 70, 18, "#FFD54F", 20), (168, 34, 15, "#4FC3F7", -35),
    (238, 52, 17, "#FF8A65", 55), (312, 30, 14, "#AED581", -20),
    (386, 66, 18, "#F06292", 40), (452, 116, 15, "#FFFFFF", -50),
    (74, 148, 16, "#4FC3F7", 30), (446, 208, 17, "#FFD54F", -15),
    (60, 236, 14, "#F06292", 65), (140, 118, 13, "#FFFFFF", -40),
    (350, 122, 14, "#AED581", 25), (470, 300, 15, "#4FC3F7", 45),
    (44, 328, 16, "#FFD54F", -25), (410, 386, 14, "#FF8A65", 35),
]


def confetti():
    out = ""
    for (cx, cy, s, col, rot) in CONFETTI:
        out += (f'<rect x="{cx-s/2}" y="{cy-s/2.6}" width="{s}" height="{s/1.3:.1f}" rx="3" '
                f'fill="{col}" transform="rotate({rot} {cx} {cy})"/>')
    return out


def motion_arcs(cx, cy):
    return (
        f'<g fill="none" stroke="{TEAL}" stroke-width="7" stroke-linecap="round" opacity="0.85">'
        f'<path d="M{cx-6} {cy-30} Q{cx+10} {cy-40} {cx+24} {cy-32}"/>'
        f'<path d="M{cx-14} {cy-48} Q{cx+10} {cy-62} {cx+36} {cy-50}"/>'
        f'</g>'
    )


# ---- Pose assembly -------------------------------------------------------
def build(pose):
    arms = ""
    props = ""
    penart = ""
    spread = 0
    shift = 0
    face = dict(eyes="open", mouth="smile", brows=None, look=(0, 0))

    if pose == "neutral":
        arms = (limb(SH_L, (118, 292), HAND_L_DOWN)
                + limb(SH_R, (394, 292), HAND_R_DOWN))
        penart = pen(HAND_R_DOWN, -72)

    elif pose == "welcome":
        arms = (limb(SH_L, (96, 214), (104, 120))
                + limb(SH_R, (394, 292), HAND_R_DOWN))
        face.update(mouth="open")
        props = motion_arcs(104, 120)
        penart = pen(HAND_R_DOWN, -72)

    elif pose == "thinking":
        arms = (limb(SH_L, (118, 292), HAND_L_DOWN)
                + limb(SH_R, (400, 246), (352, 188)))
        face.update(look=(2, -9))
        props = lightbulb(392, 84)
        penart = pen(HAND_L_DOWN, -108)

    elif pose == "tip":
        arms = limb(SH_L, (118, 292), HAND_L_DOWN) + limb(SH_R, (406, 212), (392, 132))
        arms += nub((392, 122), (392, 84), w=15)
        face.update(mouth="grin")
        props = star(434, 62, 24) + star(462, 116, 13)
        penart = pen(HAND_L_DOWN, -108)

    elif pose == "warning":
        arms = limb(SH_L, (118, 292), HAND_L_DOWN) + limb(SH_R, (408, 242), (392, 186), hand_r=26)
        for fx in (370, 392, 414):
            arms += nub((fx, 178), (fx + (fx - 392) * 0.18, 148), w=12)
        face.update(mouth="oh", brows=-13)
        props = bang(452, 98)
        penart = pen(HAND_L_DOWN, -108)

    elif pose == "encouraging":
        arms = limb(SH_L, (118, 292), HAND_L_DOWN) + limb(SH_R, (402, 296), (392, 244))
        arms += nub((392, 230), (392, 196), w=17)
        face.update(mouth="open")
        penart = pen(HAND_L_DOWN, -108)

    elif pose == "celebration":
        arms = (limb(SH_L, (100, 200), (116, 96))
                + limb(SH_R, (412, 200), (396, 96)))
        for fx, fy in ((100, 84), (116, 76), (132, 84)):
            arms += nub((fx, fy), (fx + (fx - 116) * 0.22, fy - 26), w=12)
        face.update(eyes="happy", mouth="big")
        props = confetti()
        spread = 14
        shift = -12
        penart = pen((396, 96), -62)

    body = (tail() + legs(spread) + arms + shell() + head(**face) + penart)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}">'
        f'{props}'
        f'<g transform="translate(0 {shift})">{body}</g>'
        f'</svg>'
    )


POSES = ["neutral", "welcome", "thinking", "tip", "warning", "encouraging", "celebration"]

os.makedirs(OUT, exist_ok=True)
for p in POSES:
    with open(os.path.join(OUT, f"{p}.svg"), "w") as f:
        f.write(build(p))
    print("wrote", p + ".svg")
