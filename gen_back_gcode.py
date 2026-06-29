#!/usr/bin/env python3
"""
Generate G-code for the back side of the brass mater plate.

Produces four files under gcode/:
    brass-03-pocket-back.nc         spiral pocket the central cavity
    brass-04-engrave-back-ticks.nc  ticks on the outer rim
    brass-05-engrave-back-letters.nc SATOR letters on the pocket floor
    brass-06-profile-back.nc        through-cut the outer perimeter

Coordinate transform (the brass is flipped left-right after the front-side
operations, so X is negated):
    machine_x = -(svg_x - 66.675)
    machine_y = -(svg_y - 66.675)

Run from the repo root:
    python3 gen_back_gcode.py
"""

import math
import os
import re

REPO = os.path.dirname(os.path.abspath(__file__))
GCODE = os.path.join(REPO, "gcode")

# Plate centre in SVG units (mm)
CX, CY = 66.675, 66.675

# Cavity radius (from dial-plate-path.svg green circle)
CAVITY_R = 35.052

# Plate radius
PLATE_R = 41.275

# PCB-thickness cavity depth
POCKET_DEPTH = 1.6

# Brass stock thickness
BRASS_T = 4.7625  # 3/16"

# Engrave depth at the surface (rim ticks) and inside the pocket (letters)
ENGRAVE_DEPTH = 0.10

# Cutters
BIT2_R = 1.0      # 2mm flat end mill -> radius
STEPOVER = 1.0    # 50% of 2mm tool

# Feeds/speeds (brass)
RPM_MILL = 10000
RPM_ENGRAVE = 12000
FEED_POCKET = 200       # mm/min, 2mm bit roughing brass
FEED_PROFILE = 180
FEED_PLUNGE = 60
FEED_ENGRAVE = 150
DEPTH_PER_PASS_MILL = 0.25
DEPTH_PER_PASS_PROFILE = 0.20
PROFILE_TOTAL = BRASS_T + 0.25   # through brass + into fixture

# Acrylic-test parameters
ACR_T               = 6.0
ACR_TOTAL           = 6.5      # through 6mm acrylic + 0.5mm into spoiler
ACR_RPM             = 20000
ACR_FEED_ORBIT      = 700
ACR_FEED_PROFILE    = 600
ACR_FEED_PLUNGE     = 250
ACR_DEPTH_PER_PASS  = 1.5

SAFE_Z = 5.0          # rapid clearance during the job
POST_JOB_Z = 25.0     # higher lift at end-of-job, in case workpiece moved

# Engraving inter-contour motion.  ENGRAVE_HOP is an ABSOLUTE retract height
# above the stock top (Z0) used when hopping between the many engrave contours
# — small, because the engraving face is flat and nothing protrudes above the
# stock in the tool path (fixturing is the 3 tab pins + perimeter waste).  It
# also clears the shallow back-side pocket (1.6mm deep) when reaching in for
# the letters.  Raise it if a clamp is ever placed over the engraving field.
# ENGRAVE_PLUNGE_CLEAR: rapid (G0) down to this height above the *local*
# feature surface, then feed (G1) only the final approach — so we no longer
# creep the whole 5mm of air down at the slow plunge feed.
ENGRAVE_HOP = 1.0
ENGRAVE_PLUNGE_CLEAR = 0.5


# ---------------------------------------------------------------------------
# Coordinate transform
# ---------------------------------------------------------------------------

def xy(svg_x, svg_y):
    """SVG coords -> machine coords for the *back* (flipped) side."""
    return (-(svg_x - CX), -(svg_y - CY))


def xy_front(svg_x, svg_y):
    """SVG coords -> machine coords for the *front* side (no X flip)."""
    return (svg_x - CX, -(svg_y - CY))


# ---------------------------------------------------------------------------
# SVG path tokenizer
# ---------------------------------------------------------------------------

_NUM = re.compile(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?')

def tokenize_path(d):
    """Yield (cmd, [floats]) tuples following SVG semantics for the commands
    used in this project's files: M m L l H h V v Q q A a Z z."""
    i = 0
    n = len(d)
    last_cmd = None
    while i < n:
        ch = d[i]
        if ch.isspace() or ch == ',':
            i += 1
            continue
        if ch.isalpha():
            cmd = ch
            i += 1
        else:
            cmd = last_cmd
            if cmd is None:
                raise ValueError("path begins without a command: %r" % d[:20])
        # how many args this command consumes per "step"
        nargs = {
            'M': 2, 'm': 2,
            'L': 2, 'l': 2,
            'H': 1, 'h': 1,
            'V': 1, 'v': 1,
            'Q': 4, 'q': 4,
            'T': 2, 't': 2,
            'A': 7, 'a': 7,
            'C': 6, 'c': 6,
            'Z': 0, 'z': 0,
        }[cmd]
        if nargs == 0:
            yield (cmd, [])
            last_cmd = cmd
            continue
        # consume one tuple
        args = []
        while len(args) < nargs:
            while i < n and d[i] in ' ,\t\n':
                i += 1
            m = _NUM.match(d, i)
            if not m:
                raise ValueError("expected number at %d in %r" % (i, d[max(0,i-10):i+10]))
            args.append(float(m.group()))
            i = m.end()
        yield (cmd, args)
        # After the first M, subsequent implicit commands are L (for M) or l (for m)
        if cmd == 'M':
            last_cmd = 'L'
        elif cmd == 'm':
            last_cmd = 'l'
        else:
            last_cmd = cmd


def flatten_path(d, step=0.1):
    """Convert an SVG path 'd' into a list of polylines (each a list of (x,y)
    points in SVG coordinates).  Lines pass straight through; quadratic
    Beziers and arcs are approximated by short line segments of size 'step'.
    """
    polylines = []
    poly = []
    cx, cy = 0.0, 0.0
    start_x, start_y = 0.0, 0.0   # start of current subpath
    last_ctrl = None              # last quadratic control point (for T)

    def emit(x, y):
        nonlocal cx, cy
        poly.append((x, y))
        cx, cy = x, y

    def start_subpath(x, y):
        nonlocal start_x, start_y, poly
        if poly:
            polylines.append(poly)
        poly = [(x, y)]
        start_x, start_y = x, y

    for cmd, args in tokenize_path(d):
        c = cmd
        if c in ('M', 'm'):
            x, y = args
            if c == 'm' and poly:
                x += cx; y += cy
            start_subpath(x, y)
            cx, cy = x, y
        elif c in ('L', 'l'):
            x, y = args
            if c == 'l':
                x += cx; y += cy
            emit(x, y)
            last_ctrl = None
        elif c == 'H':
            emit(args[0], cy); last_ctrl = None
        elif c == 'h':
            emit(cx + args[0], cy); last_ctrl = None
        elif c == 'V':
            emit(cx, args[0]); last_ctrl = None
        elif c == 'v':
            emit(cx, cy + args[0]); last_ctrl = None
        elif c in ('Q', 'q'):
            x1, y1, x2, y2 = args
            if c == 'q':
                x1 += cx; y1 += cy
                x2 += cx; y2 += cy
            # quadratic Bezier (cx,cy) -> (x2,y2) control (x1,y1)
            # approximate length and pick step count
            length = (math.hypot(x1-cx, y1-cy) +
                      math.hypot(x2-x1, y2-y1))
            n = max(2, int(math.ceil(length / step)))
            for k in range(1, n+1):
                t = k / n
                u = 1 - t
                px = u*u*cx + 2*u*t*x1 + t*t*x2
                py = u*u*cy + 2*u*t*y1 + t*t*y2
                poly.append((px, py))
            cx, cy = x2, y2
            last_ctrl = (x1, y1)
        elif c in ('T', 't'):
            x2, y2 = args
            if c == 't':
                x2 += cx; y2 += cy
            if last_ctrl is None:
                x1, y1 = cx, cy
            else:
                # reflect previous control point about current point
                x1 = 2*cx - last_ctrl[0]
                y1 = 2*cy - last_ctrl[1]
            length = math.hypot(x1-cx, y1-cy) + math.hypot(x2-x1, y2-y1)
            n = max(2, int(math.ceil(length / step)))
            for k in range(1, n+1):
                t = k / n
                u = 1 - t
                px = u*u*cx + 2*u*t*x1 + t*t*x2
                py = u*u*cy + 2*u*t*y1 + t*t*y2
                poly.append((px, py))
            cx, cy = x2, y2
            last_ctrl = (x1, y1)
        elif c in ('A', 'a'):
            rx, ry, rot, large, sweep, x, y = args
            if c == 'a':
                x += cx; y += cy
            for px, py in _arc_to_points(cx, cy, rx, ry, rot, large, sweep, x, y, step):
                poly.append((px, py))
            cx, cy = x, y
            last_ctrl = None
        elif c in ('Z', 'z'):
            poly.append((start_x, start_y))
            cx, cy = start_x, start_y
            last_ctrl = None
        else:
            raise ValueError("unsupported path command: %s" % c)
    if poly:
        polylines.append(poly)
    return polylines


def _arc_to_points(x1, y1, rx, ry, phi_deg, large, sweep, x2, y2, step):
    """Flatten an SVG arc to a sequence of points (excluding the starting
    point).  Implementation of the endpoint-to-centre conversion from the
    SVG spec."""
    if x1 == x2 and y1 == y2:
        return
    if rx == 0 or ry == 0:
        yield (x2, y2)
        return
    rx = abs(rx); ry = abs(ry)
    phi = math.radians(phi_deg)
    cos_p = math.cos(phi); sin_p = math.sin(phi)

    # Step 1: transform to (x1', y1')
    dx = (x1 - x2) / 2.0
    dy = (y1 - y2) / 2.0
    x1p =  cos_p*dx + sin_p*dy
    y1p = -sin_p*dx + cos_p*dy

    # Step 2: ensure radii are large enough
    rad_check = (x1p**2)/(rx**2) + (y1p**2)/(ry**2)
    if rad_check > 1:
        s = math.sqrt(rad_check)
        rx *= s; ry *= s

    # Step 3: compute centre (cx', cy')
    sign = -1 if large == sweep else 1
    num = rx*rx*ry*ry - rx*rx*y1p*y1p - ry*ry*x1p*x1p
    den = rx*rx*y1p*y1p + ry*ry*x1p*x1p
    factor = math.sqrt(max(0.0, num / den)) if den else 0.0
    cxp = sign * factor * (rx * y1p / ry)
    cyp = sign * factor * (-ry * x1p / rx)

    # Step 4: compute centre in original coordinates
    cx_o = cos_p*cxp - sin_p*cyp + (x1 + x2) / 2.0
    cy_o = sin_p*cxp + cos_p*cyp + (y1 + y2) / 2.0

    # Step 5: compute start and delta angles
    def ang(ux, uy, vx, vy):
        dot = ux*vx + uy*vy
        n = math.hypot(ux, uy) * math.hypot(vx, vy)
        if n == 0: return 0.0
        c = max(-1.0, min(1.0, dot / n))
        a = math.acos(c)
        if ux*vy - uy*vx < 0: a = -a
        return a

    theta1 = ang(1, 0, (x1p - cxp)/rx, (y1p - cyp)/ry)
    dtheta = ang((x1p - cxp)/rx, (y1p - cyp)/ry,
                 (-x1p - cxp)/rx, (-y1p - cyp)/ry)
    if sweep == 0 and dtheta > 0:
        dtheta -= 2*math.pi
    elif sweep == 1 and dtheta < 0:
        dtheta += 2*math.pi

    # arc length estimate
    arc_len = abs(dtheta) * (rx + ry) / 2.0
    n = max(2, int(math.ceil(arc_len / step)))

    for k in range(1, n + 1):
        t = theta1 + dtheta * k / n
        x =  cos_p * rx * math.cos(t) - sin_p * ry * math.sin(t) + cx_o
        y =  sin_p * rx * math.cos(t) + cos_p * ry * math.sin(t) + cy_o
        yield (x, y)


# ---------------------------------------------------------------------------
# SVG path extraction
# ---------------------------------------------------------------------------

def signed_area(poly):
    """Standard shoelace.  In a Y-up coordinate system: positive area
    means the vertices wind CCW, negative means CW."""
    n = len(poly)
    if n < 3:
        return 0.0
    s = 0.0
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        s += x1 * y2 - x2 * y1
    return s / 2.0


def offset_polyline_outward(poly, distance):
    """Outward offset of a closed polygon by `distance` using Shapely.

    The polygon is buffered with round joins, i.e. the Minkowski sum of the
    part region with a disc of radius `distance` (the bit radius).  This is
    plunge-safe by construction: convex corners get a clean bit-radius arc,
    and the tool is never sent into a concave valley narrower than the bit,
    so no separate corner pre-rounding of the source outline is required."""
    from shapely.geometry import Polygon

    eps = 1e-4
    verts = []
    for p in poly:
        if not verts or math.hypot(p[0] - verts[-1][0],
                                   p[1] - verts[-1][1]) > eps:
            verts.append(p)
    if len(verts) > 1 and math.hypot(verts[0][0] - verts[-1][0],
                                     verts[0][1] - verts[-1][1]) < eps:
        verts.pop()
    if len(verts) < 3:
        return list(poly)

    src = Polygon(verts)
    if not src.is_valid:
        src = src.buffer(0)

    expanded = src.buffer(distance, join_style=1, resolution=8)
    if expanded.geom_type == "MultiPolygon":
        expanded = max(expanded.geoms, key=lambda g: g.area)
    return list(expanded.exterior.coords)


def paths_with_stroke(svg_path, color):
    """Return the d-attributes of every <path> whose style includes the
    given stroke colour, in document order, deduped by id."""
    with open(svg_path) as f:
        s = f.read()
    blocks = re.findall(r'<path\b[^>]*?>', s, re.DOTALL)
    out = []
    seen = set()
    for b in blocks:
        if 'stroke:' + color not in b:
            continue
        m = re.search(r'\bid="([^"]+)"', b)
        if m:
            if m.group(1) in seen:
                continue
            seen.add(m.group(1))
        d = re.search(r'\bd="([^"]+)"', b)
        if d:
            out.append(d.group(1))
    return out


def paths_excluding_stroke(svg_path, color):
    """Return the d-attributes of every <path> whose style does NOT include
    the given stroke colour (in document order, deduped by id).  Used for the
    front engraving: take all the line-art but skip the cut/drill features,
    which carry the olive #808000 stroke.  <circle> elements (the holes /
    registration marks) are not <path>s and so are excluded automatically."""
    with open(svg_path) as f:
        s = f.read()
    blocks = re.findall(r'<path\b[^>]*?>', s, re.DOTALL)
    out = []
    seen = set()
    for b in blocks:
        if 'stroke:' + color in b:
            continue
        m = re.search(r'\bid="([^"]+)"', b)
        if m:
            if m.group(1) in seen:
                continue
            seen.add(m.group(1))
        d = re.search(r'\bd="([^"]+)"', b)
        if d:
            out.append(d.group(1))
    return out


# ---------------------------------------------------------------------------
# G-code emitters
# ---------------------------------------------------------------------------

def header(title, tool, mat, z0, rpm,
           origin="plate center (BACK SIDE - brass flipped left-right)"):
    return [
        f"; {title}",
        f"; Tool: {tool}",
        f"; Material: {mat}",
        f"; X0 Y0 = {origin}",
        f"; Z0 = {z0}",
        "",
        "G21       ; metric",
        "G90       ; absolute",
        "G17       ; XY plane for arcs",
        f"M3 S{rpm} ; spindle on",
        "G4 P2     ; spin-up dwell",
        "",
    ]


def footer():
    return [
        "",
        "M5          ; spindle off",
        f"G0 Z{POST_JOB_Z}    ; high lift in case the workpiece moved",
        "G0 X0 Y0",
        "",
    ]


def emit_engrave_polylines(lines, polylines_svg, z_top, z_engrave,
                           feed_engrave=FEED_ENGRAVE,
                           feed_plunge=FEED_PLUNGE,
                           transform=xy):
    """Add engrave moves for a list of polylines (in SVG coords).
    Transforms to machine coords (via `transform`, default the back/flipped
    `xy`; pass `xy_front` for natural front-side orientation) and emits a
    single down-pass per polyline.

    Between contours the tool hops to ENGRAVE_HOP (a small absolute clearance
    above the stock top), rapids in XY, then rapids straight down to
    ENGRAVE_PLUNGE_CLEAR above the *local* feature surface and only feeds
    (G1 at feed_plunge) the final approach to z_engrave.  The feature surface
    is one ENGRAVE_DEPTH above the cut depth (Z0 for surface engraving, the
    pocket floor for the letters), so the slow plunge is ~the engrave depth +
    the clearance instead of the full retract height.
    Emits modal G-code: feed only when it changes."""
    approach_z = z_engrave + ENGRAVE_DEPTH + ENGRAVE_PLUNGE_CLEAR
    last_feed = None
    for poly in polylines_svg:
        if len(poly) < 2:
            continue
        x0, y0 = transform(*poly[0])
        lines.append(f"G0 Z{ENGRAVE_HOP}")
        lines.append(f"G0 X{x0:.4f} Y{y0:.4f}")
        lines.append(f"G0 Z{approach_z:.4f}")
        if last_feed != feed_plunge:
            lines.append(f"G1 Z{z_engrave:.4f} F{feed_plunge}")
            last_feed = feed_plunge
        else:
            lines.append(f"G1 Z{z_engrave:.4f}")
        first = True
        for px, py in poly[1:]:
            mx, my = transform(px, py)
            if first and last_feed != feed_engrave:
                lines.append(f"G1 X{mx:.4f} Y{my:.4f} F{feed_engrave}")
                last_feed = feed_engrave
            else:
                lines.append(f"X{mx:.4f} Y{my:.4f}")
            first = False
    lines.append(f"G0 Z{ENGRAVE_HOP}")


# ---------------------------------------------------------------------------
# brass-03  spiral pocket
# ---------------------------------------------------------------------------

def gen_pocket():
    out = header(
        title="Back side cavity pocket",
        tool="2mm single flute spiral end mill",
        mat="3/16\" brass on fixture plate",
        z0="top of brass",
        rpm=RPM_MILL,
    )
    out += [
        f"; Cavity: circle r={CAVITY_R}mm centred on plate centre",
        f"; Depth: {POCKET_DEPTH}mm (standard PCB thickness)",
        f"; Bit radius {BIT2_R}mm, stepover {STEPOVER}mm",
        f"; Center pin must be REMOVED before this op (the 3 tab pins still hold the part)",
        "",
    ]

    # final cut radius for a 2mm bit pocketing a CAVITY_R hole
    r_max = CAVITY_R - BIT2_R
    # number of orbital passes per depth level
    radii = []
    r = STEPOVER
    while r < r_max:
        radii.append(r)
        r += STEPOVER
    radii.append(r_max)

    # depth levels (downcutting through POCKET_DEPTH)
    z_levels = []
    z = -DEPTH_PER_PASS_MILL
    while z > -POCKET_DEPTH:
        z_levels.append(round(z, 4))
        z -= DEPTH_PER_PASS_MILL
    z_levels.append(-POCKET_DEPTH)

    out.append(f"G0 Z{SAFE_Z}")
    out.append(f"G0 X0 Y0")
    for z in z_levels:
        out.append("")
        out.append(f"; ---- depth Z{z} ----")
        out.append(f"G1 Z{z:.4f} F{FEED_PLUNGE}")
        for rr in radii:
            # ramp out to radius rr, then a full orbit
            out.append(f"G1 X{rr:.4f} Y0 F{FEED_POCKET}")
            out.append(f"G2 I-{rr:.4f} J0 F{FEED_POCKET}")
        # return to centre so next plunge is at X0 Y0
        out.append(f"G1 X0 Y0 F{FEED_POCKET}")

    out += footer()
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# brass-04  ticks on the rim
# ---------------------------------------------------------------------------

def gen_ticks():
    svg = os.path.join(REPO, "dial-plate-path.svg")
    paths = paths_with_stroke(svg, "#000000")
    # Each tick path is short; flatten with a generous step.
    polylines = []
    for d in paths:
        polylines += flatten_path(d, step=0.2)

    out = header(
        title="Back side tick marks",
        tool="30 deg x 0.2mm engraving bit",
        mat="3/16\" brass on fixture plate",
        z0="top of brass (original surface, BEFORE the pocket cut)",
        rpm=RPM_ENGRAVE,
    )
    out += [
        f"; {len(paths)} tick paths from dial-plate-path.svg",
        f"; Engraving depth {ENGRAVE_DEPTH}mm below original brass surface",
        "",
    ]
    emit_engrave_polylines(out, polylines, z_top=0.0,
                           z_engrave=-ENGRAVE_DEPTH)
    out += footer()
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# brass-05  letters in the pocket floor
# ---------------------------------------------------------------------------

def gen_letters():
    svg = os.path.join(REPO, "mater-plate-sator-3mm-path2.svg")
    paths = paths_with_stroke(svg, "#ff0000")
    polylines = []
    for d in paths:
        polylines += flatten_path(d, step=0.05)

    z_engrave = -(POCKET_DEPTH + ENGRAVE_DEPTH)

    out = header(
        title="Back side SATOR letters (in pocket floor)",
        tool="30 deg x 0.2mm engraving bit",
        mat="3/16\" brass, cavity already pocketed to -" + str(POCKET_DEPTH) + "mm",
        z0="top of brass (unchanged; we are reaching into the pocket)",
        rpm=RPM_ENGRAVE,
    )
    out += [
        f"; {len(paths)} letter outline paths from mater-plate-sator-3mm-path2.svg",
        f"; Engraving floor of the {POCKET_DEPTH}mm-deep cavity at Z={z_engrave}",
        "",
    ]
    emit_engrave_polylines(out, polylines, z_top=0.0,
                           z_engrave=z_engrave)
    out += footer()
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# brass-02  front-side engraving (line-art on the natural-orientation face)
# ---------------------------------------------------------------------------

def gen_front_engrave():
    """Front-side engraving of the dial face.

    This is the FIRST operation on the visible face, done BEFORE the brass is
    flipped left-right for the back-side ops.  It therefore uses the natural,
    *un-mirrored* coordinate frame (`xy_front`, X not negated) — unlike every
    back-side file which uses the flipped `xy`.  Same plate centre (CX,CY) and
    same Inkscape page frame as the back SVGs (identical viewBox), so X0 Y0 is
    the plate centre for both.

    Source: mater-plate-back-12-3mm.svg (the front-side design per README).
    Engrave every line-art path; skip the olive #808000 cut/drill features
    (outer profile + holes) which are produced by brass-01 / brass-06.
    """
    svg = os.path.join(REPO, "mater-plate-back-12-3mm.svg")
    paths = paths_excluding_stroke(svg, "#808000")
    polylines = []
    for d in paths:
        polylines += flatten_path(d, step=0.1)

    out = header(
        title="Front side engraving (dial face)",
        tool="30 deg x 0.2mm single flute engraving bit for metal",
        mat="3/16\" brass (front face, before flip)",
        z0="top of brass",
        rpm=RPM_ENGRAVE,
        origin="plate center (FRONT SIDE - natural orientation, NOT flipped)",
    )
    out += [
        f"; {len(paths)} line-art paths from mater-plate-back-12-3mm.svg",
        f"; (olive #808000 outline/holes skipped — see brass-01 / brass-06)",
        f"; Engraving depth {ENGRAVE_DEPTH}mm below brass surface",
        f"; FRONT orientation: X is NOT mirrored (xy_front); back files are.",
        "",
    ]
    emit_engrave_polylines(out, polylines, z_top=0.0,
                           z_engrave=-ENGRAVE_DEPTH, transform=xy_front)
    out += footer()
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# brass-06  outer perimeter profile cut
# ---------------------------------------------------------------------------

def gen_profile():
    svg = os.path.join(REPO, "dial-plate-path.svg")
    paths = paths_with_stroke(svg, "#808000")
    # The big plate outline is the longest path; the small circles are the
    # registration holes (already cut).  Pick the longest by flattened length.
    best = None
    best_len = 0
    for d in paths:
        polys = flatten_path(d, step=0.25)
        if not polys: continue
        poly = polys[0]
        L = sum(math.hypot(poly[i+1][0]-poly[i][0],
                           poly[i+1][1]-poly[i][1])
                for i in range(len(poly)-1))
        if L > best_len:
            best_len = L
            best = poly

    # depth levels
    z_levels = []
    z = -DEPTH_PER_PASS_PROFILE
    while z > -PROFILE_TOTAL:
        z_levels.append(round(z, 4))
        z -= DEPTH_PER_PASS_PROFILE
    z_levels.append(-PROFILE_TOTAL)

    out = header(
        title="Back side outer profile cut (releases the part)",
        tool="2mm single flute spiral end mill",
        mat="3/16\" brass on fixture plate",
        z0="top of brass",
        rpm=RPM_MILL,
    )
    out += [
        f"; Toolpath is the SVG outline OFFSET OUTWARD by {BIT2_R}mm",
        "; so the finished part lands at the design dimensions.",
        "; Total depth: " + f"{PROFILE_TOTAL:.3f}mm (through brass + into fixture)",
        "; The three tab pins keep the part registered after release.",
        "",
    ]

    # transform polyline to machine coords, then offset outward by bit radius.
    # The outward buffer (Minkowski sum with the bit disc) is plunge-safe by
    # construction — it rounds convex corners with a bit-radius arc and never
    # lets the tool reach into a concave valley narrower than the bit — so no
    # separate corner pre-rounding is needed.
    mx_my = [xy(p[0], p[1]) for p in best]
    mx_my = offset_polyline_outward(mx_my, BIT2_R)

    # rapid to start
    sx, sy = mx_my[0]
    out.append(f"G0 Z{SAFE_Z}")
    out.append(f"G0 X{sx:.4f} Y{sy:.4f}")
    last_feed = None
    for z in z_levels:
        out.append("")
        out.append(f"; ---- depth Z{z} ----")
        if last_feed != FEED_PLUNGE:
            out.append(f"G1 Z{z:.4f} F{FEED_PLUNGE}")
            last_feed = FEED_PLUNGE
        else:
            out.append(f"G1 Z{z:.4f}")
        first = True
        for x, y in mx_my[1:]:
            if first and last_feed != FEED_PROFILE:
                out.append(f"G1 X{x:.4f} Y{y:.4f} F{FEED_PROFILE}")
                last_feed = FEED_PROFILE
            else:
                out.append(f"X{x:.4f} Y{y:.4f}")
            first = False
        # last point should be near first; if not, close it explicitly
        if (mx_my[-1][0]-sx)**2 + (mx_my[-1][1]-sy)**2 > 1e-6:
            out.append(f"X{sx:.4f} Y{sy:.4f}")

    out += footer()
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# acrylic-02-full  one-shot test cut: holes + perimeter, 2mm bit only
# ---------------------------------------------------------------------------

def gen_acrylic_full():
    """Single-file test cut for 6mm acrylic: drills all four registration
    holes and then cuts the outer perimeter, all with the 2mm bit and a
    single Z reference at the top of the acrylic.

    No flip — the part comes out in the natural design orientation.
    Assumes the acrylic is clamped from above onto something that protects
    the bed for the final 0.5mm of each cut (the printed fixture plate
    placed loose underneath works fine).
    """
    out = header(
        title="Acrylic test piece: 4 registration holes + outer perimeter",
        tool="2mm single flute spiral end mill",
        mat="6mm acrylic clamped from above",
        z0="top of acrylic",
        rpm=ACR_RPM,
    )
    # Override the back-side comment from header() (no flip on this file)
    out[3] = "; X0 Y0 = plate center (no flip)"
    out += [
        f"; Total cut depth: {ACR_TOTAL}mm (through 6mm acrylic + 0.5mm into spoiler)",
        f"; Reduce ACR_TOTAL to ~5.8 in gen_back_gcode.py if you have NO spoiler",
        f"; under the acrylic, to leave a thin web that protects the bed.",
        ";",
        f"; Hole orbits (2mm bit, 1mm radius):",
        f";   center 3.3mm hole -> orbit radius 0.65mm",
        f";   tab    6.0mm hole -> orbit radius 2.00mm",
        ";",
        f"; Perimeter is offset OUTWARD by {BIT2_R}mm so the part lands at design size.",
        f"; After perimeter releases, the part is loose — your clamps must NOT be",
        f"; over the part itself, but anchored to the surrounding waste.",
        "",
    ]

    def hole(cx, cy, orbit_r, label):
        out.append(f"; ---- {label}: X{cx} Y{cy}, orbit r={orbit_r}mm ----")
        out.append(f"G0 Z{SAFE_Z}")
        out.append(f"G0 X{cx} Y{cy}")
        out.append(f"G0 X{cx + orbit_r} Y{cy}")
        z = -ACR_DEPTH_PER_PASS
        pass_n = 1
        while z > -ACR_TOTAL + 1e-9:
            out.append(f"G1 Z{z:.4f} F{ACR_FEED_PLUNGE}  ; pass {pass_n}")
            out.append(f"G2 I-{orbit_r} J0 F{ACR_FEED_ORBIT}")
            z -= ACR_DEPTH_PER_PASS
            pass_n += 1
        out.append(f"G1 Z-{ACR_TOTAL} F{ACR_FEED_PLUNGE}  ; final depth")
        out.append(f"G2 I-{orbit_r} J0 F{ACR_FEED_ORBIT}")
        out.append(f"G2 I-{orbit_r} J0 F{ACR_FEED_ORBIT}  ; spring pass")
        out.append(f"G0 Z{SAFE_Z}")
        out.append("")

    hole(   0.000,  0.000, 0.65, "CENTER 3.3mm")
    hole(   0.000, 50.864, 2.0,  "TAB CENTER 6.0mm")
    hole(   6.350, 44.514, 2.0,  "TAB RIGHT 6.0mm")
    hole(  -6.350, 44.514, 2.0,  "TAB LEFT 6.0mm")

    # Outer perimeter
    out.append("; ---- OUTER PERIMETER (releases the part) ----")
    svg = os.path.join(REPO, "dial-plate-path.svg")
    paths = paths_with_stroke(svg, "#808000")
    best, best_len = None, 0
    for d in paths:
        polys = flatten_path(d, step=0.25)
        if not polys: continue
        poly = polys[0]
        L = sum(math.hypot(poly[i+1][0]-poly[i][0],
                           poly[i+1][1]-poly[i][1])
                for i in range(len(poly)-1))
        if L > best_len:
            best_len, best = L, poly

    # Plunge-safe outward offset (see gen_profile): the buffer already rounds
    # convex corners and limits the tool at concave valleys, so no separate
    # corner pre-rounding is needed.
    mx_my = [xy_front(p[0], p[1]) for p in best]
    mx_my = offset_polyline_outward(mx_my, BIT2_R)

    # depth levels
    z_levels = []
    z = -ACR_DEPTH_PER_PASS
    while z > -ACR_TOTAL + 1e-9:
        z_levels.append(round(z, 4))
        z -= ACR_DEPTH_PER_PASS
    z_levels.append(-ACR_TOTAL)

    sx, sy = mx_my[0]
    out.append(f"G0 Z{SAFE_Z}")
    out.append(f"G0 X{sx:.4f} Y{sy:.4f}")
    last_feed = None
    for z in z_levels:
        out.append("")
        out.append(f"; ---- depth Z{z} ----")
        if last_feed != ACR_FEED_PLUNGE:
            out.append(f"G1 Z{z:.4f} F{ACR_FEED_PLUNGE}")
            last_feed = ACR_FEED_PLUNGE
        else:
            out.append(f"G1 Z{z:.4f}")
        first = True
        for x, y in mx_my[1:]:
            if first and last_feed != ACR_FEED_PROFILE:
                out.append(f"G1 X{x:.4f} Y{y:.4f} F{ACR_FEED_PROFILE}")
                last_feed = ACR_FEED_PROFILE
            else:
                out.append(f"X{x:.4f} Y{y:.4f}")
            first = False
        if (mx_my[-1][0]-sx)**2 + (mx_my[-1][1]-sy)**2 > 1e-6:
            out.append(f"X{sx:.4f} Y{sy:.4f}")

    out += footer()
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    os.makedirs(GCODE, exist_ok=True)
    files = {
        "acrylic-02-full.nc":                 gen_acrylic_full(),
        "brass-02-engrave-front.nc":          gen_front_engrave(),
        "brass-03-pocket-back.nc":            gen_pocket(),
        "brass-04-engrave-back-ticks.nc":     gen_ticks(),
        "brass-05-engrave-back-letters.nc":   gen_letters(),
        "brass-06-profile-back.nc":           gen_profile(),
    }
    for name, body in files.items():
        path = os.path.join(GCODE, name)
        with open(path, "w") as f:
            f.write(body)
        # quick stats
        lines = body.count("\n")
        print(f"wrote {name:38s} {lines:6d} lines, {len(body):8d} bytes")


if __name__ == "__main__":
    main()
