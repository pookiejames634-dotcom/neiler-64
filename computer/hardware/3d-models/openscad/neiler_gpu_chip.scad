// NeilerGPU Chip 3D Model
// Custom graphics processor with sprite engine
// 128-pin TQFP package with integrated video DAC

// Chip dimensions (TQFP-128 package)
chip_width = 20.0;   // mm (body size)
chip_depth = 20.0;   // mm
chip_height = 1.4;   // mm (body thickness)
pin_count = 128;
pins_per_side = 32;

// Pin specifications (TQFP gull-wing)
pin_width = 0.22;    // mm
pin_length = 0.65;   // mm (exposed length)
pin_pitch = 0.5;     // mm (0.5mm pitch for high density)
pin_thickness = 0.15; // mm

// Colors
chip_color = [0.15, 0.15, 0.15];     // Dark gray epoxy
pin_color = [0.85, 0.85, 0.8];       // Tin/lead
label_color = [1.0, 1.0, 1.0];       // White
die_color = [0.2, 0.25, 0.3];        // Silicon die (visible in cutaway)

module neilergpu_chip() {
    union() {
        // Main chip body
        color(chip_color) {
            difference() {
                // Chip body
                cube([chip_width, chip_depth, chip_height]);

                // Pin 1 indicator chamfer
                translate([-0.1, -0.1, chip_height - 0.3])
                    rotate([0, 0, 0])
                    cube([1.5, 1.5, 0.4]);
            }
        }

        // All 128 pins (TQFP gull-wing leads)
        color(pin_color) {
            // Top side (pins 1-32)
            for (i = [0:pins_per_side-1]) {
                translate([chip_width/2 - (pins_per_side-1)*pin_pitch/2 + i*pin_pitch,
                          chip_depth,
                          0]) {
                    tqfp_pin();
                }
            }

            // Right side (pins 33-64)
            for (i = [0:pins_per_side-1]) {
                translate([chip_width,
                          chip_depth/2 + (pins_per_side-1)*pin_pitch/2 - i*pin_pitch,
                          0]) {
                    rotate([0, 0, 90])
                        tqfp_pin();
                }
            }

            // Bottom side (pins 65-96)
            for (i = [0:pins_per_side-1]) {
                translate([chip_width/2 + (pins_per_side-1)*pin_pitch/2 - i*pin_pitch,
                          0,
                          0]) {
                    rotate([0, 0, 180])
                        tqfp_pin();
                }
            }

            // Left side (pins 97-128)
            for (i = [0:pins_per_side-1]) {
                translate([0,
                          chip_depth/2 - (pins_per_side-1)*pin_pitch/2 + i*pin_pitch,
                          0]) {
                    rotate([0, 0, -90])
                        tqfp_pin();
                }
            }
        }

        // Chip labeling and markings
        color(label_color) {
            // Main chip name
            translate([chip_width/2, chip_depth/2 + 2, chip_height - 0.01]) {
                linear_extrude(height = 0.02) {
                    text("NEILERGPU", size = 2, halign = "center", valign = "center",
                         font = "Liberation Sans:style=Bold");
                }
            }

            // Specifications
            translate([chip_width/2, chip_depth/2 - 0.5, chip_height - 0.01]) {
                linear_extrude(height = 0.02) {
                    text("640x480", size = 1.3, halign = "center", valign = "center");
                }
            }

            translate([chip_width/2, chip_depth/2 - 2, chip_height - 0.01]) {
                linear_extrude(height = 0.02) {
                    text("65K COLOR", size = 1.1, halign = "center", valign = "center");
                }
            }

            // Part number
            translate([chip_width/2, 2.5, chip_height - 0.01]) {
                linear_extrude(height = 0.02) {
                    text("NLR-GPU-16", size = 0.9, halign = "center", valign = "center");
                }
            }

            // Manufacturing info
            translate([chip_width/2, 1.2, chip_height - 0.01]) {
                linear_extrude(height = 0.02) {
                    text("2025 WEEK 01", size = 0.7, halign = "center", valign = "center");
                }
            }

            // Pin 1 dot
            translate([1.5, chip_depth - 1.5, chip_height - 0.01]) {
                cylinder(h = 0.02, r = 0.4, $fn = 20);
            }

            // Laser code (QR-like pattern)
            translate([chip_width - 3, 2, chip_height - 0.01]) {
                for (x = [0:4]) {
                    for (y = [0:4]) {
                        if ((x + y) % 2 == 0) {
                            translate([x * 0.3, y * 0.3, 0])
                                cube([0.2, 0.2, 0.02]);
                        }
                    }
                }
            }
        }

        // Exposed thermal pad (center bottom)
        color([0.7, 0.7, 0.65]) {
            translate([chip_width/2 - 3.5, chip_depth/2 - 3.5, -0.1])
                cube([7, 7, 0.1]);
        }
    }
}

// TQFP gull-wing pin module
module tqfp_pin() {
    // Gull-wing lead profile
    hull() {
        // Inner part (connected to chip)
        translate([-pin_width/2, 0, 0.2])
            cube([pin_width, 0.1, pin_thickness]);

        // Bend down
        translate([-pin_width/2, 0.3, 0])
            cube([pin_width, 0.1, pin_thickness]);

        // Outer flat part (solderable)
        translate([-pin_width/2, 0.4, 0])
            cube([pin_width, pin_length - 0.4, pin_thickness]);
    }
}

// Render the GPU chip
neilergpu_chip();

// Cutaway view showing internal die (for documentation)
module neilergpu_cutaway() {
    difference() {
        neilergpu_chip();

        // Cut away top half
        translate([-5, -5, chip_height/2])
            cube([chip_width + 10, chip_depth + 10, chip_height]);
    }

    // Show internal die
    color(die_color, 0.8) {
        translate([chip_width/2 - 7, chip_depth/2 - 7, 0.2])
            cube([14, 14, 0.4]);
    }

    // Bond wires (fine gold wires from die to pins)
    color([1.0, 0.84, 0], 0.9) {
        for (angle = [0:45:315]) {
            rotate([0, 0, angle]) {
                translate([0, chip_depth/2 - 7, 0.6])
                    cylinder(h = 0.1, r1 = 0.05, r2 = 0.02, $fn = 8);
            }
        }
    }
}

// Uncomment to see cutaway view
// neilergpu_cutaway();
