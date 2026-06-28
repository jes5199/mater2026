; Brass plate - center hole + 3 tab holes
; Tool: 1mm carbide end mill (1/8" shank)
; Material: 3/16" brass (4.7625mm) over sacrificial MDF
; APPLY CUTTING FLUID (WD-40) before each hole and mid-cut
; X0 Y0 = plate center, Z0 = top surface of brass
; 5.0mm total depth, 34 passes x 0.15mm
; Center hole 3.3mm (clearance fit for M3 clevis pin)

G21       ; metric
G90       ; absolute
G17       ; XY plane for arcs
M3 S12000 ; spindle on, 12000 RPM
G4 P2     ; wait for spindle spin-up

; ====================================================
; CENTER HOLE  3.3mm diameter  orbit radius 1.15mm
; center: X0 Y0
; ====================================================
G0 Z5.0
G0 X0 Y0
G0 X1.15 Y0
G1 Z-0.150 F60  ; pass 1
G2 I-1.15 J0 F120
G1 Z-0.300 F60  ; pass 2
G2 I-1.15 J0 F120
G1 Z-0.450 F60  ; pass 3
G2 I-1.15 J0 F120
G1 Z-0.600 F60  ; pass 4
G2 I-1.15 J0 F120
G1 Z-0.750 F60  ; pass 5
G2 I-1.15 J0 F120
G1 Z-0.900 F60  ; pass 6
G2 I-1.15 J0 F120
G1 Z-1.050 F60  ; pass 7
G2 I-1.15 J0 F120
G1 Z-1.200 F60  ; pass 8
G2 I-1.15 J0 F120
G1 Z-1.350 F60  ; pass 9
G2 I-1.15 J0 F120
G1 Z-1.500 F60  ; pass 10
G2 I-1.15 J0 F120
G1 Z-1.650 F60  ; pass 11
G2 I-1.15 J0 F120
G1 Z-1.800 F60  ; pass 12
G2 I-1.15 J0 F120
G1 Z-1.950 F60  ; pass 13
G2 I-1.15 J0 F120
G1 Z-2.100 F60  ; pass 14
G2 I-1.15 J0 F120
G1 Z-2.250 F60  ; pass 15
G2 I-1.15 J0 F120
G1 Z-2.400 F60  ; pass 16
G2 I-1.15 J0 F120
G1 Z-2.550 F60  ; pass 17
G2 I-1.15 J0 F120
G1 Z-2.700 F60  ; pass 18
G2 I-1.15 J0 F120
G1 Z-2.850 F60  ; pass 19
G2 I-1.15 J0 F120
G1 Z-3.000 F60  ; pass 20
G2 I-1.15 J0 F120
G1 Z-3.150 F60  ; pass 21
G2 I-1.15 J0 F120
G1 Z-3.300 F60  ; pass 22
G2 I-1.15 J0 F120
G1 Z-3.450 F60  ; pass 23
G2 I-1.15 J0 F120
G1 Z-3.600 F60  ; pass 24
G2 I-1.15 J0 F120
G1 Z-3.750 F60  ; pass 25
G2 I-1.15 J0 F120
G1 Z-3.900 F60  ; pass 26
G2 I-1.15 J0 F120
G1 Z-4.050 F60  ; pass 27
G2 I-1.15 J0 F120
G1 Z-4.200 F60  ; pass 28
G2 I-1.15 J0 F120
G1 Z-4.350 F60  ; pass 29
G2 I-1.15 J0 F120
G1 Z-4.500 F60  ; pass 30
G2 I-1.15 J0 F120
G1 Z-4.650 F60  ; pass 31
G2 I-1.15 J0 F120
G1 Z-4.800 F60  ; pass 32
G2 I-1.15 J0 F120
G1 Z-4.950 F60  ; pass 33
G2 I-1.15 J0 F120
G1 Z-5.000 F60  ; pass 34
G2 I-1.15 J0 F120
G2 I-1.15 J0 F120  ; spring pass
G0 Z5.0

; ====================================================
; TAB CENTER  6.0mm diameter  orbit radius 2.5mm
; center: X0 Y50.864
; ====================================================
G0 Z5.0
G0 X0 Y50.864
G0 X2.5 Y50.864
G1 Z-0.150 F60  ; pass 1
G2 I-2.5 J0 F120
G1 Z-0.300 F60  ; pass 2
G2 I-2.5 J0 F120
G1 Z-0.450 F60  ; pass 3
G2 I-2.5 J0 F120
G1 Z-0.600 F60  ; pass 4
G2 I-2.5 J0 F120
G1 Z-0.750 F60  ; pass 5
G2 I-2.5 J0 F120
G1 Z-0.900 F60  ; pass 6
G2 I-2.5 J0 F120
G1 Z-1.050 F60  ; pass 7
G2 I-2.5 J0 F120
G1 Z-1.200 F60  ; pass 8
G2 I-2.5 J0 F120
G1 Z-1.350 F60  ; pass 9
G2 I-2.5 J0 F120
G1 Z-1.500 F60  ; pass 10
G2 I-2.5 J0 F120
G1 Z-1.650 F60  ; pass 11
G2 I-2.5 J0 F120
G1 Z-1.800 F60  ; pass 12
G2 I-2.5 J0 F120
G1 Z-1.950 F60  ; pass 13
G2 I-2.5 J0 F120
G1 Z-2.100 F60  ; pass 14
G2 I-2.5 J0 F120
G1 Z-2.250 F60  ; pass 15
G2 I-2.5 J0 F120
G1 Z-2.400 F60  ; pass 16
G2 I-2.5 J0 F120
G1 Z-2.550 F60  ; pass 17
G2 I-2.5 J0 F120
G1 Z-2.700 F60  ; pass 18
G2 I-2.5 J0 F120
G1 Z-2.850 F60  ; pass 19
G2 I-2.5 J0 F120
G1 Z-3.000 F60  ; pass 20
G2 I-2.5 J0 F120
G1 Z-3.150 F60  ; pass 21
G2 I-2.5 J0 F120
G1 Z-3.300 F60  ; pass 22
G2 I-2.5 J0 F120
G1 Z-3.450 F60  ; pass 23
G2 I-2.5 J0 F120
G1 Z-3.600 F60  ; pass 24
G2 I-2.5 J0 F120
G1 Z-3.750 F60  ; pass 25
G2 I-2.5 J0 F120
G1 Z-3.900 F60  ; pass 26
G2 I-2.5 J0 F120
G1 Z-4.050 F60  ; pass 27
G2 I-2.5 J0 F120
G1 Z-4.200 F60  ; pass 28
G2 I-2.5 J0 F120
G1 Z-4.350 F60  ; pass 29
G2 I-2.5 J0 F120
G1 Z-4.500 F60  ; pass 30
G2 I-2.5 J0 F120
G1 Z-4.650 F60  ; pass 31
G2 I-2.5 J0 F120
G1 Z-4.800 F60  ; pass 32
G2 I-2.5 J0 F120
G1 Z-4.950 F60  ; pass 33
G2 I-2.5 J0 F120
G1 Z-5.000 F60  ; pass 34
G2 I-2.5 J0 F120
G2 I-2.5 J0 F120  ; spring pass
G0 Z5.0

; ====================================================
; TAB RIGHT  6.0mm diameter  orbit radius 2.5mm
; center: X6.35 Y44.514
; ====================================================
G0 Z5.0
G0 X6.35 Y44.514
G0 X8.85 Y44.514
G1 Z-0.150 F60  ; pass 1
G2 I-2.5 J0 F120
G1 Z-0.300 F60  ; pass 2
G2 I-2.5 J0 F120
G1 Z-0.450 F60  ; pass 3
G2 I-2.5 J0 F120
G1 Z-0.600 F60  ; pass 4
G2 I-2.5 J0 F120
G1 Z-0.750 F60  ; pass 5
G2 I-2.5 J0 F120
G1 Z-0.900 F60  ; pass 6
G2 I-2.5 J0 F120
G1 Z-1.050 F60  ; pass 7
G2 I-2.5 J0 F120
G1 Z-1.200 F60  ; pass 8
G2 I-2.5 J0 F120
G1 Z-1.350 F60  ; pass 9
G2 I-2.5 J0 F120
G1 Z-1.500 F60  ; pass 10
G2 I-2.5 J0 F120
G1 Z-1.650 F60  ; pass 11
G2 I-2.5 J0 F120
G1 Z-1.800 F60  ; pass 12
G2 I-2.5 J0 F120
G1 Z-1.950 F60  ; pass 13
G2 I-2.5 J0 F120
G1 Z-2.100 F60  ; pass 14
G2 I-2.5 J0 F120
G1 Z-2.250 F60  ; pass 15
G2 I-2.5 J0 F120
G1 Z-2.400 F60  ; pass 16
G2 I-2.5 J0 F120
G1 Z-2.550 F60  ; pass 17
G2 I-2.5 J0 F120
G1 Z-2.700 F60  ; pass 18
G2 I-2.5 J0 F120
G1 Z-2.850 F60  ; pass 19
G2 I-2.5 J0 F120
G1 Z-3.000 F60  ; pass 20
G2 I-2.5 J0 F120
G1 Z-3.150 F60  ; pass 21
G2 I-2.5 J0 F120
G1 Z-3.300 F60  ; pass 22
G2 I-2.5 J0 F120
G1 Z-3.450 F60  ; pass 23
G2 I-2.5 J0 F120
G1 Z-3.600 F60  ; pass 24
G2 I-2.5 J0 F120
G1 Z-3.750 F60  ; pass 25
G2 I-2.5 J0 F120
G1 Z-3.900 F60  ; pass 26
G2 I-2.5 J0 F120
G1 Z-4.050 F60  ; pass 27
G2 I-2.5 J0 F120
G1 Z-4.200 F60  ; pass 28
G2 I-2.5 J0 F120
G1 Z-4.350 F60  ; pass 29
G2 I-2.5 J0 F120
G1 Z-4.500 F60  ; pass 30
G2 I-2.5 J0 F120
G1 Z-4.650 F60  ; pass 31
G2 I-2.5 J0 F120
G1 Z-4.800 F60  ; pass 32
G2 I-2.5 J0 F120
G1 Z-4.950 F60  ; pass 33
G2 I-2.5 J0 F120
G1 Z-5.000 F60  ; pass 34
G2 I-2.5 J0 F120
G2 I-2.5 J0 F120  ; spring pass
G0 Z5.0

; ====================================================
; TAB LEFT  6.0mm diameter  orbit radius 2.5mm
; center: X-6.35 Y44.514
; ====================================================
G0 Z5.0
G0 X-6.35 Y44.514
G0 X-3.85 Y44.514
G1 Z-0.150 F60  ; pass 1
G2 I-2.5 J0 F120
G1 Z-0.300 F60  ; pass 2
G2 I-2.5 J0 F120
G1 Z-0.450 F60  ; pass 3
G2 I-2.5 J0 F120
G1 Z-0.600 F60  ; pass 4
G2 I-2.5 J0 F120
G1 Z-0.750 F60  ; pass 5
G2 I-2.5 J0 F120
G1 Z-0.900 F60  ; pass 6
G2 I-2.5 J0 F120
G1 Z-1.050 F60  ; pass 7
G2 I-2.5 J0 F120
G1 Z-1.200 F60  ; pass 8
G2 I-2.5 J0 F120
G1 Z-1.350 F60  ; pass 9
G2 I-2.5 J0 F120
G1 Z-1.500 F60  ; pass 10
G2 I-2.5 J0 F120
G1 Z-1.650 F60  ; pass 11
G2 I-2.5 J0 F120
G1 Z-1.800 F60  ; pass 12
G2 I-2.5 J0 F120
G1 Z-1.950 F60  ; pass 13
G2 I-2.5 J0 F120
G1 Z-2.100 F60  ; pass 14
G2 I-2.5 J0 F120
G1 Z-2.250 F60  ; pass 15
G2 I-2.5 J0 F120
G1 Z-2.400 F60  ; pass 16
G2 I-2.5 J0 F120
G1 Z-2.550 F60  ; pass 17
G2 I-2.5 J0 F120
G1 Z-2.700 F60  ; pass 18
G2 I-2.5 J0 F120
G1 Z-2.850 F60  ; pass 19
G2 I-2.5 J0 F120
G1 Z-3.000 F60  ; pass 20
G2 I-2.5 J0 F120
G1 Z-3.150 F60  ; pass 21
G2 I-2.5 J0 F120
G1 Z-3.300 F60  ; pass 22
G2 I-2.5 J0 F120
G1 Z-3.450 F60  ; pass 23
G2 I-2.5 J0 F120
G1 Z-3.600 F60  ; pass 24
G2 I-2.5 J0 F120
G1 Z-3.750 F60  ; pass 25
G2 I-2.5 J0 F120
G1 Z-3.900 F60  ; pass 26
G2 I-2.5 J0 F120
G1 Z-4.050 F60  ; pass 27
G2 I-2.5 J0 F120
G1 Z-4.200 F60  ; pass 28
G2 I-2.5 J0 F120
G1 Z-4.350 F60  ; pass 29
G2 I-2.5 J0 F120
G1 Z-4.500 F60  ; pass 30
G2 I-2.5 J0 F120
G1 Z-4.650 F60  ; pass 31
G2 I-2.5 J0 F120
G1 Z-4.800 F60  ; pass 32
G2 I-2.5 J0 F120
G1 Z-4.950 F60  ; pass 33
G2 I-2.5 J0 F120
G1 Z-5.000 F60  ; pass 34
G2 I-2.5 J0 F120
G2 I-2.5 J0 F120  ; spring pass
G0 Z5.0

M5          ; spindle off
G0 X0 Y0    ; return home
