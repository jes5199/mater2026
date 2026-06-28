; Acrylic jig - center hole + 3 tab holes
; Tool: 2mm carbide end mill (1/8" shank)
; Material: 6mm acrylic over sacrificial MDF
; X0 Y0 = plate center, Z0 = top surface of acrylic
; Depth: 6.5mm (through acrylic, 0.5mm into MDF)
; Center hole 3.3mm (clearance fit for M3 clevis pin)

G21       ; metric
G90       ; absolute
G17       ; XY plane for arcs
M3 S20000 ; spindle on, 20000 RPM
G4 P2     ; wait for spindle spin-up

; ====================================================
; CENTER HOLE  3.3mm diameter  orbit radius 0.65mm
; center: X0 Y0
; ====================================================
G0 Z5.0
G0 X0 Y0
G0 X0.65 Y0
G1 Z-1.500 F250  ; pass 1
G2 I-0.65 J0 F700
G1 Z-3.000 F250  ; pass 2
G2 I-0.65 J0 F700
G1 Z-4.500 F250  ; pass 3
G2 I-0.65 J0 F700
G1 Z-6.000 F250  ; pass 4
G2 I-0.65 J0 F700
G1 Z-6.500 F250  ; pass 5
G2 I-0.65 J0 F700
G2 I-0.65 J0 F700  ; spring pass
G0 Z5.0

; ====================================================
; TAB CENTER  6.0mm diameter  orbit radius 2.0mm
; center: X0 Y50.864
; ====================================================
G0 Z5.0
G0 X0 Y50.864
G0 X2.0 Y50.864
G1 Z-1.500 F250  ; pass 1
G2 I-2.0 J0 F700
G1 Z-3.000 F250  ; pass 2
G2 I-2.0 J0 F700
G1 Z-4.500 F250  ; pass 3
G2 I-2.0 J0 F700
G1 Z-6.000 F250  ; pass 4
G2 I-2.0 J0 F700
G1 Z-6.500 F250  ; pass 5
G2 I-2.0 J0 F700
G2 I-2.0 J0 F700  ; spring pass
G0 Z5.0

; ====================================================
; TAB RIGHT  6.0mm diameter  orbit radius 2.0mm
; center: X6.35 Y44.514
; ====================================================
G0 Z5.0
G0 X6.35 Y44.514
G0 X8.35 Y44.514
G1 Z-1.500 F250  ; pass 1
G2 I-2.0 J0 F700
G1 Z-3.000 F250  ; pass 2
G2 I-2.0 J0 F700
G1 Z-4.500 F250  ; pass 3
G2 I-2.0 J0 F700
G1 Z-6.000 F250  ; pass 4
G2 I-2.0 J0 F700
G1 Z-6.500 F250  ; pass 5
G2 I-2.0 J0 F700
G2 I-2.0 J0 F700  ; spring pass
G0 Z5.0

; ====================================================
; TAB LEFT  6.0mm diameter  orbit radius 2.0mm
; center: X-6.35 Y44.514
; ====================================================
G0 Z5.0
G0 X-6.35 Y44.514
G0 X-4.35 Y44.514
G1 Z-1.500 F250  ; pass 1
G2 I-2.0 J0 F700
G1 Z-3.000 F250  ; pass 2
G2 I-2.0 J0 F700
G1 Z-4.500 F250  ; pass 3
G2 I-2.0 J0 F700
G1 Z-6.000 F250  ; pass 4
G2 I-2.0 J0 F700
G1 Z-6.500 F250  ; pass 5
G2 I-2.0 J0 F700
G2 I-2.0 J0 F700  ; spring pass
G0 Z5.0

M5          ; spindle off
G0 X0 Y0    ; return home
