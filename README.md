# mater2026

CNC work for a brass astrolabe mater plate. Machine: Carvera Air (no official software — G-code uploaded via web interface).

Only the front side design is in this repo so far.

---

## Files

- `mater-plate-back-12-3mm.svg` — front side design (Inkscape, units in mm)
- `mater-plate-back-12-3mm-circles.txt` — measured positions and sizes of all registration holes
- `carvera-air-bed-holes.txt` — Carvera Air bed hole positions extracted from STEP file
- `fixture-plate.scad` — 3D-printed fixture plate (replaces acrylic jig + sacrificial MDF)
- `registration-pin.scad` — 3D-printed registration pins for 6mm tab holes
- `gcode/acrylic-01-holes.nc` — cuts registration holes in 6mm acrylic (test run)
- `gcode/brass-01-holes.nc` — cuts registration holes in 3/16" brass
- `gcode/brass-02-engrave-front.nc` — front side engraving (toolpaths not yet generated)

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

5. **Flip the brass left-right** (rotate around vertical axis). The hole pattern is X-symmetric so the pins still register correctly after the flip. Do not flip top-to-bottom — the tab holes would end up at the bottom where the fixture plate has none.

6. **Engrave back side** — run `brass-03-engrave-back.nc` with mirrored X coordinates (file and back side design not yet in this repo).
