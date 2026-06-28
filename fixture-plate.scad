// Carvera Air fixture plate
// Replaces acrylic jig + MDF sacrificial board
// Origin (0,0,0) = workpiece center = CNC machine X0 Y0, top surface
//
// Bolt this to the Carvera Air bed using the three mounting holes.
// Then probe the center registration hole to set X0 Y0 for each session.
//
// Mounting holes correspond to Carvera Air bed holes (in bed coordinates):
//   (45, 120), (80, 30), (125, 75)
// ...assuming workpiece center at bed position (75, 80).
// If you position the plate differently on the bed, update mount_holes below.
//
// NOTE: mount_d is set for M4 clearance (4.5mm). The Carvera Air bed holes
// appear as 6mm in the STEP model but may be tapped M4 — verify on the machine
// and change mount_d to 6.5 if they are actually M6.
//
// Print flat (largest face down). No supports needed.

// ----- Parameters -----

plate_t   = 4;     // plate thickness (mm)
tolerance = 0.1;   // added to registration hole diameters for FDM shrinkage
                   // increase toward 0.2 if holes print tight

// Plate extents relative to workpiece center (0,0)
x_min = -55;
x_max =  60;
y_min = -60;
y_max =  65;

// Work registration holes [x, y, nominal_diameter]
work_holes = [
    [  0.000,  0.000, 3.3],  // center — M3 clevis pin
    [  0.000, 50.864, 6.0],  // tab top center
    [  6.350, 44.514, 6.0],  // tab right
    [ -6.350, 44.514, 6.0],  // tab left
];

// Bed mounting holes [x, y] relative to workpiece center
mount_holes = [
    [-30,  40],   // bed hole (45, 120)
    [  5, -50],   // bed hole (80,  30)
    [ 50,  -5],   // bed hole (125, 75)
];
mount_d = 4.5;   // M4 clearance — change to 6.5 if bed holes are M6

// ----- Geometry -----

$fn = 64;

// punch a hole all the way through the plate at the current origin
module thru(d, sides = 0) {
    translate([0, 0, -(plate_t / 2 + 1)])
        cylinder(d = d, h = plate_t + 2, $fn = sides > 0 ? sides : $fn);
}

difference() {
    // plate body, centered on Z=0
    translate([(x_min + x_max) / 2, (y_min + y_max) / 2, 0])
        cube([x_max - x_min, y_max - y_min, plate_t], center = true);

    // work registration holes
    for (h = work_holes)
        translate([h[0], h[1], 0])
            thru(h[2] + tolerance);

    // bed mounting holes
    for (h = mount_holes)
        translate([h[0], h[1], 0])
            thru(mount_d);

    // orientation notch at bottom-left corner — makes plate asymmetric
    // so you can't bolt it down rotated 180°
    translate([x_min, y_min, 0])
        thru(16, sides = 4);
}
