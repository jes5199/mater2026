// Carvera Air fixture plate
// Replaces acrylic jig + MDF sacrificial board
// Origin (0,0,0) = workpiece center = CNC machine X0 Y0, top surface
//
// Bolt this to the Carvera Air bed using the three M6 mounting holes.
// Then probe the center registration hole to set X0 Y0 for each session.
//
// Mounting holes correspond to Carvera Air bed holes (in bed coordinates):
//   (45, 120), (80, 30), (125, 75)
// ...assuming workpiece center at bed position (75, 80).
// If you position the plate differently on the bed, update mount_holes below.
//
// Print flat (largest face down). No supports needed.

// ----- Parameters -----

plate_t   = 4;     // plate thickness (mm)
tolerance = 0.1;   // added to all hole diameters to account for FDM shrinkage
                   // increase toward 0.2 if holes print tight

// Plate extents relative to workpiece center (0,0)
x_min = -55;
x_max =  60;
y_min = -60;
y_max =  65;

// Work registration holes [x, y, nominal_diameter]
// These match the G-code zeros exactly
work_holes = [
    [  0.000,  0.000, 3.3],  // center — M3 clevis pin
    [  0.000, 50.864, 6.0],  // tab top center
    [  6.350, 44.514, 6.0],  // tab right
    [ -6.350, 44.514, 6.0],  // tab left
];

// Bed mounting holes [x, y] relative to workpiece center — M6 clearance
mount_holes = [
    [-30,  40],   // bed hole (45, 120)
    [  5, -50],   // bed hole (80,  30)
    [ 50,  -5],   // bed hole (125, 75)
];

// ----- Geometry -----

$fn = 64;

difference() {
    // plate body
    translate([(x_min + x_max) / 2, (y_min + y_max) / 2, 0])
        cube([x_max - x_min, y_max - y_min, plate_t], center = true);

    // work registration holes (through)
    for (h = work_holes)
        translate([h[0], h[1], -0.5])
            cylinder(d = h[2] + tolerance, h = plate_t + 1);

    // bed mounting holes (through, M6 clearance)
    for (h = mount_holes)
        translate([h[0], h[1], -0.5])
            cylinder(d = 6.5, h = plate_t + 1);

    // orientation notch: corner cut at bottom-left so you can't mount it backwards
    translate([x_min, y_min, -0.5])
        cylinder(r = 8, h = plate_t + 1, $fn = 4);
}
