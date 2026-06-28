# mater2026

CNC work for a brass astrolabe mater plate. Machine: Carvera Air (no official software — G-code uploaded via web interface).

Only the front side design is in this repo so far.

---

## Files

- `mater-plate-back-12-3mm.svg` — front side design (Inkscape, units in mm)
- `mater-plate-back-12-3mm-circles.txt` — measured positions and sizes of all registration holes
- `gcode/acrylic-jig.nc` — cuts the jig from 6mm acrylic
- `gcode/brass-plate.nc` — cuts registration holes in 3/16" brass

---

## Materials

| Layer | Material | Thickness |
|---|---|---|
| Sacrificial | MDF | 1/4" (6.35mm) |
| Jig | Acrylic | 6mm |
| Workpiece | Brass | 3/16" (4.7625mm) |

---

## Registration holes

Zero point: X0 Y0 = plate center, Z0 = top surface of workpiece.

| Hole | Diameter | Position |
|---|---|---|
| Center | 3mm | X0 Y0 |
| Tab center | 6mm | X0 Y+50.864 |
| Tab right | 6mm | X+6.35 Y+44.514 |
| Tab left | 6mm | X−6.35 Y+44.514 |

The two side tab holes are X-symmetric, which matters for the flip (see below).

The plate body is 82.55mm diameter. The tab holes are inside three rounded tab features that protrude past the main circle edge.

---

## Bits

- **2mm carbide end mill, 1/8" shank** — acrylic jig
- **1mm carbide end mill, 1/8" shank** — brass plate (uxcell titanium coat, PCB-grade)
- V-bit (not yet ordered) — engraving, later

The center hole (3mm) is tight for a 2mm bit (only 0.5mm orbital radius). The 1mm bit gives a comfortable 1.0mm orbit for the same hole.

---

## Cutting parameters

### Acrylic jig (2mm end mill)
- RPM: 20,000
- Feed: 700 mm/min orbital, 250 mm/min plunge
- Pass depth: 1.5mm
- Total depth: 6.5mm (through acrylic + 0.5mm into MDF)

### Brass plate (1mm end mill)
- RPM: 12,000
- Feed: 120 mm/min orbital, 60 mm/min plunge
- Pass depth: 0.15mm (34 passes)
- Total depth: 5.0mm (through brass + ~0.25mm into MDF)
- **Apply WD-40 before each hole and mid-cut**

---

## Order of operations

1. **Cut the acrylic jig** — acrylic on sacrificial MDF, run `acrylic-jig.nc`

2. **Cut brass holes in the same setup** — place brass on top of the acrylic jig without moving or re-zeroing, run `brass-plate.nc`. Holes cut through brass into the already-cut jig holes, guaranteeing alignment.

3. **Insert dowel pins** through brass and jig.

4. **Engrave front side.**

5. **Flip the brass left-right** (rotate around vertical axis). The hole pattern is X-symmetric so the pins still register correctly after the flip. Do not flip top-to-bottom — the tab holes would end up at the bottom where the jig has none.

6. **Re-pin and engrave back side** using mirrored G-code (negate all X coordinates). Back side design not yet in this repo.
