# mater2026

CNC work for a brass astrolabe mater plate. Machine: Carvera Air (no official software — G-code uploaded via web interface).

The design is mostly carried over from a 2023 laser-cut version (`rete2023`).
The laser version emulated depth by stacking sheets; this version mills a single
brass piece, so the back side has a real pocketed cavity instead of a glued-in
PCB-thickness inlay.

---

## Files

### Design

- `mater-plate-back-12-3mm.svg` — **front side** design (Inkscape, units in mm)
- `mater-plate-back-12-3mm-circles.txt` — measured positions and sizes of all registration holes
- `dial-plate-path.svg` — **back side**: outer outline, tab outline, cavity outline (PCB-depth), tick marks on the outer rim
- `mater-plate-sator-3mm-path2.svg` — **back side**: SATOR letter outlines that engrave into the pocketed cavity floor
- `carvera-air-bed-holes.txt` — Carvera Air bed hole positions extracted from STEP file

### Fixtures

- `fixture-plate.scad` — 3D-printed fixture plate (replaces acrylic jig + sacrificial MDF)
- `registration-pin.scad` — 3D-printed registration pins for 6mm tab holes

### G-code

- `gcode/acrylic-01-holes.nc` — registration holes in 6mm acrylic (test run)
- `gcode/brass-01-holes.nc` — registration holes in 3/16" brass
- `gcode/brass-02-engrave-front.nc` — front side engraving *(toolpaths not yet generated)*
- `gcode/brass-03-pocket-back.nc` — back side cavity pocket, PCB depth
- `gcode/brass-04-engrave-back-ticks.nc` — back side tick marks on the outer rim
- `gcode/brass-05-engrave-back-letters.nc` — SATOR letters engraved in the cavity floor
- `gcode/brass-06-profile-back.nc` — outer perimeter cut (releases the part)

### Code

- `gen_back_gcode.py` — generator for `brass-03`..`brass-06`. Parses SVG paths, applies the back-side coordinate transform (X negated, Y flipped, origin at plate centre), flattens curves and arcs to line segments, and offsets the outline outward by the tool radius for the perimeter cut.

---

## Materials

| Role | Material | Thickness |
|---|---|---|
| Fixture plate (jig) | PLA/PETG print | 2mm |
| Test workpiece | Acrylic | 6mm |
| Final workpiece | Brass | 3/16" (4.7625mm) |

The fixture plate bolts to the Carvera Air bed via three M5 holes and stays in place between sessions. Re-probe Z0 at the start of each session; X0 Y0 is re-established by probing the center registration hole.

---

## Bits

- **2mm single flute spiral, 12mm** — acrylic holes
- **1mm carbide end mill, 1/8" shank** — brass holes (uxcell TiN coat, PCB-grade, on order)
- **30° × 0.2mm single flute engraving bit for metal** — brass engraving

The center hole (3.3mm) needs a 0.65mm orbit with the 2mm bit, or a 1.15mm orbit with the 1mm bit.

---

## Registration holes

Zero point: X0 Y0 = plate center, Z0 = top surface of workpiece.

| Hole | Diameter | Position | Purpose |
|---|---|---|---|
| Center | 3.3mm | X0 Y0 | M3 clevis pin (rotates freely) |
| Tab center | 6mm | X0 Y+50.864 | M6 dowel pin |
| Tab right | 6mm | X+6.35 Y+44.514 | M6 dowel pin |
| Tab left | 6mm | X−6.35 Y+44.514 | M6 dowel pin |

The two side tab holes are X-symmetric, which matters for the flip (see below).

The plate body is 82.55mm diameter. The tab holes sit inside three rounded tab features that protrude past the main circle edge.

---

## Cutting parameters

### Acrylic holes (2mm single flute)
- RPM: 20,000
- Feed: 700 mm/min orbital, 250 mm/min plunge
- Pass depth: 1.5mm
- Total depth: 6.5mm (through 6mm acrylic + 0.5mm into fixture plate)

### Brass holes (1mm carbide end mill)
- RPM: 12,000
- Feed: 120 mm/min orbital, 60 mm/min plunge
- Pass depth: 0.15mm (34 passes)
- Total depth: 5.0mm (through brass + ~0.25mm into fixture plate)
- **Apply WD-40 before each hole and mid-cut**

---

## Order of operations

1. **Print fixture plate** — bolt to Carvera Air bed using three M5 screws, probe to set X0 Y0.

2. **Test run in acrylic** — place 6mm acrylic on fixture plate, run `acrylic-01-holes.nc`. Insert pins to verify registration.

3. **Cut brass holes** — place brass on fixture plate, run `brass-01-holes.nc`. Insert pins.

4. **Engrave front side** — run `brass-02-engrave-front.nc` (toolpaths TBD).

5. **Flip the brass left-right** (rotate around the vertical axis). The hole pattern is X-symmetric so the tab pins still register correctly after the flip. Do not flip top-to-bottom — the tab holes would end up at the bottom where the fixture plate has none. After the flip, all the back-side G-code already accounts for the flip (X coordinates negated by the generator).

6. **Remove the centre pin.** It sticks up through the part right where the cavity is about to be milled. The three tab pins still hold the brass down for the rest of the back-side work, and `brass-06-profile-back.nc` after them.

7. **Pocket the cavity** — `brass-03-pocket-back.nc`. 2mm bit, spirals out from centre, 1.6mm deep (standard PCB thickness).

8. **Engrave the rim ticks** — `brass-04-engrave-back-ticks.nc`. 30° engraver, ~0.1mm deep into the original brass surface (the rim is untouched by the pocket cut).

9. **Engrave the SATOR letters** — `brass-05-engrave-back-letters.nc`. Same engraver, reaches down into the pocket floor (Z reference is unchanged — the file targets ‑1.7mm absolute).

10. **Profile cut the perimeter** — `brass-06-profile-back.nc`. 2mm bit, traces the outline offset outward by 1mm so the part lands at design size. The three tab pins keep the part registered while it separates from the surrounding stock.

### Regenerating back-side G-code

```sh
python3 gen_back_gcode.py
```

Re-runs the converter and overwrites the four `brass-0[3-6]*.nc` files. Edit
constants near the top of `gen_back_gcode.py` to change feeds, speeds, depths
or pass counts.
