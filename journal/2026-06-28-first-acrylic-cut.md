# 2026-06-28 — first end-to-end acrylic cut

First time actually running G-code on the Carvera Air. Cut `acrylic-02-full.nc`
(4 registration holes + outer perimeter, 2mm single-flute spiral, 20000 RPM).

## What worked

- All four registration holes came out **basically perfect** by eye.
- Tool length probe + 3D work probe gave correct Z0/X0/Y0.
- The Carvera auto-probes Z at job start by default — annoying but harmless.
  Swapping back to the cutter after the probe step is part of the standard
  flow.
- Sending the file: ended up downloading the raw URL on the Kindle Fire's
  Silk browser from the GitHub repo, after USB-MTP via OpenMTP failed
  outright. The Carvera Controller app's file picker only ever sees its own
  private app dir, so the file has to be imported via the app's own button.

## What broke / needs fixing

### 1. Bite marks at the tab/circle transitions
At the corners where the main 41.275mm circle meets the 6.35mm tab neck
arcs, the bit cut **inward** by a small amount on both sides — leaving
four little notches per affected tab.

**Hypothesis:** the perimeter generator (`offset_polyline_outward` in
`gen_back_gcode.py`) uses a bisector-of-adjacent-edge-normals method.  At
sharp transitions (concave-to-convex tangent breaks at the tab junctions),
the bisector blows up — the code clamps with `max(dot, 0.05)` which still
allows up to 20× amplification. The result is the toolpath swinging
**inward** at the transition, biting the part.

**Fix candidates for next iteration:**
- Round corners by inserting a bit-radius arc at sharp transitions instead
  of the bisector blowup.
- Or use Shapely / Clipper for the offset (proven algorithms, handles
  this cleanly).
- Or detect transition vertices in the SVG and add intermediate
  bridging points so no single bisector spans a sharp tangent break.

### 2. Workpiece lifted as the perimeter cleared
After the final perimeter pass, the central plate piece was loose and
jumped out of position.  Then the machine's "return to home" rapid moved
the spindle across the (now-misplaced) workpiece and the bit hit it and
**snapped**.

**Hypothesis:** two contributing causes:
1. The acrylic was only held by external clamps on the surrounding waste,
   nothing holding the central piece itself.  The perimeter cut is
   designed to release it, and it released enthusiastically.
2. The post-job `G0 Z5.0` clearance isn't high enough — a dislodged
   workpiece can stick up well above the original 5mm safe Z and put the
   tip of the bit straight into it on the return rapid.

**Fix candidates:**
- **Adhesive under the acrylic**: double-sided carpet tape or 3M VHB
  between the acrylic and the spoiler.  Standard CNC fixturing for thin
  flat stock.  Should keep the centre piece in place after release.
- Bump the post-job `SAFE_Z` to something like 15–20mm so the return-home
  rapid clears a dislodged part.
- Optionally leave a tiny on-cut bridge (skip the last 0.1mm of the
  perimeter and tab the part to the surrounding waste) so it doesn't go
  fully free during the cut.

### 3. Centre hole slightly loose
By eye the centre 3.3mm hole feels a hair larger than it wants to be for
an M3 clevis pin.  Will measure with calipers when home.

**Hypothesis:** orbit radius (0.65mm with a 2mm bit) gives a nominal
3.3mm hole, but the bit cuts slightly oversize due to tool deflection,
runout, and chip clearance.  Acrylic is also forgiving on hole size.

**Fix candidate (after measurement):**
- If the hole is e.g. 3.4mm, reduce orbit radius by 0.05mm.
- For brass with the 1mm bit, the orbit is 1.15mm — same principle, may
  need to reduce to 1.10mm.

## Action items for next session

- [ ] Measure the four holes with calipers; compare to target diameters.
- [ ] Pick a corner-handling strategy for the perimeter offset and reimplement.
- [ ] Bump `SAFE_Z` in `gen_back_gcode.py` to 15–20mm.
- [ ] Order/locate double-sided fixturing tape.
- [ ] Replace the snapped 2mm bit (or count the survivors in the bit box).
