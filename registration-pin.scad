// Registration pin for 6mm tab holes
//
// Pin shaft length is sized so that when the pin is fully inserted, its
// bottom is flush with the underside of the fixture plate (i.e. touching
// the Carvera Air bed) AND the flange just lands on top of the workpiece.
// That way the flange actually clamps the work down, not floats above it.
//
// shaft_length = fixture_t + workpiece_t
//
// Set workpiece_t below for whichever stock you're cutting and re-export.
// Oriented flange-down for printing — no supports needed.

// ----- Parameters -----

fixture_t      = 2.0;        // your printed fixture plate thickness
workpiece_t    = 4.7625;     // 3/16" brass.  For the acrylic test, use 6.0.

hole_diameter  = 6.0;
tolerance      = -0.15;      // make more negative if loose, toward 0 if too tight

shaft_d        = hole_diameter + tolerance;
shaft_length   = fixture_t + workpiece_t;

flange_d       = 9.0;        // wide enough to rest on top of brass
flange_h       = 2.0;
chamfer_h      = 0.8;        // lead-in taper at insertion tip

$fn = 64;

// ----- Geometry -----

// flange on the print bed, shaft pointing up
rotate([180, 0, 0])
translate([0, 0, -(shaft_length + flange_h)]) {
    // flange (sits on top surface of workpiece)
    translate([0, 0, shaft_length])
        cylinder(d=flange_d, h=flange_h);

    // shaft with chamfered tip
    difference() {
        cylinder(d=shaft_d, h=shaft_length);
        // chamfer: cone wider than shaft at z=0, narrowing to shaft_d at chamfer_h
        translate([0, 0, -0.01])
            cylinder(d1=shaft_d + 1, d2=shaft_d, h=chamfer_h + 0.01);
    }
}
