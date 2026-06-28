// Registration pin for 6mm jig holes
// Oriented flange-down for printing (no supports needed)
// Adjust tolerance until you get a snug slip fit — try -0.15 first

hole_diameter  = 6.0;
tolerance      = -0.15;  // make more negative if loose, toward 0 if too tight

shaft_d        = hole_diameter + tolerance;
shaft_length   = 12.0;   // brass 4.76mm + acrylic 6mm + a little past
flange_d       = 9.0;    // wide enough to rest on top of brass
flange_h       = 2.0;
chamfer_h      = 0.8;    // lead-in taper at insertion tip

$fn = 64;

// flange on floor, shaft pointing up
rotate([180, 0, 0])
translate([0, 0, -(shaft_length + flange_h)]) {
    // flange (sits on top surface of brass)
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
