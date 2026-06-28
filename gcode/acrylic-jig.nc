; Acrylic jig - center hole + 3 tab holes
; Tool: 2mm carbide end mill (1/8" shank)
; Material: 6mm acrylic over sacrificial MDF
; X0 Y0 = plate center, Z0 = top surface of acrylic
; Depth: 6.5mm (through acrylic, 0.5mm into MDF)
; Passes: 1.5mm each, spring pass at full depth

G21       ; metric
G90       ; absolute
G17       ; XY plane for arcs
M3 S20000 ; spindle on, 20000 RPM
G4 P2     ; wait for spindle spin-up

; -----------------------------------------------
; CENTER HOLE  3mm diameter  orbit radius 0.5mm
; -----------------------------------------------
G0 Z5
G0 X0 Y0
G1 Z-1.5 F250
G1 X0.5 F700
G2 I-0.5 J0
G1 X0
G1 Z-3.0 F250
G1 X0.5 F700
G2 I-0.5 J0
G1 X0
G1 Z-4.5 F250
G1 X0.5 F700
G2 I-0.5 J0
G1 X0
G1 Z-6.5 F250
G1 X0.5 F700
G2 I-0.5 J0
G2 I-0.5 J0   ; spring pass
G1 X0
G0 Z5

; -----------------------------------------------
; TAB CENTER HOLE  6mm diameter  orbit radius 2mm
; position: X0 Y50.864
; -----------------------------------------------
G0 X0 Y50.864
G1 Z-1.5 F250
G1 X2 F700
G2 I-2 J0
G1 X0
G1 Z-3.0 F250
G1 X2 F700
G2 I-2 J0
G1 X0
G1 Z-4.5 F250
G1 X2 F700
G2 I-2 J0
G1 X0
G1 Z-6.5 F250
G1 X2 F700
G2 I-2 J0
G2 I-2 J0     ; spring pass
G1 X0
G0 Z5

; -----------------------------------------------
; TAB RIGHT HOLE  6mm diameter  orbit radius 2mm
; position: X6.35 Y44.514
; -----------------------------------------------
G0 X6.35 Y44.514
G1 Z-1.5 F250
G1 X8.35 F700
G2 I-2 J0
G1 X6.35
G1 Z-3.0 F250
G1 X8.35 F700
G2 I-2 J0
G1 X6.35
G1 Z-4.5 F250
G1 X8.35 F700
G2 I-2 J0
G1 X6.35
G1 Z-6.5 F250
G1 X8.35 F700
G2 I-2 J0
G2 I-2 J0     ; spring pass
G1 X6.35
G0 Z5

; -----------------------------------------------
; TAB LEFT HOLE  6mm diameter  orbit radius 2mm
; position: X-6.35 Y44.514
; -----------------------------------------------
G0 X-6.35 Y44.514
G1 Z-1.5 F250
G1 X-4.35 F700
G2 I-2 J0
G1 X-6.35
G1 Z-3.0 F250
G1 X-4.35 F700
G2 I-2 J0
G1 X-6.35
G1 Z-4.5 F250
G1 X-4.35 F700
G2 I-2 J0
G1 X-6.35
G1 Z-6.5 F250
G1 X-4.35 F700
G2 I-2 J0
G2 I-2 J0     ; spring pass
G1 X-6.35
G0 Z5

M5          ; spindle off
G0 X0 Y0    ; return home
