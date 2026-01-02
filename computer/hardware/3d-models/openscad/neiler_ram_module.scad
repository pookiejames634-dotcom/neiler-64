// Neiler RAM Module 3D Model
// 64MB SDRAM-style memory module
// Custom 168-pin DIMM form factor

// Module dimensions
pcb_length = 133.35;  // mm (standard DIMM length)
pcb_height = 30.0;    // mm
pcb_thickness = 1.6;  // mm
pin_count = 168;

// RAM chip dimensions (TSOP-II 54-pin)
chip_width = 22.22;   // mm
chip_depth = 10.16;   // mm
chip_height = 1.2;    // mm
chips_per_side = 8;   // 8 chips per side = 16 total

// Pin specifications
pin_width = 0.3;      // mm
pin_length = 2.0;     // mm
pin_pitch = 0.762;    // mm (30 mil)
pin_thickness = 0.2;  // mm

// Colors
pcb_color = [0.1, 0.3, 0.1];         // Green FR4
chip_color = [0.15, 0.15, 0.15];     // Black epoxy
pin_color = [0.83, 0.69, 0.22];      // Gold plated
label_color = [1.0, 1.0, 1.0];       // White silkscreen
heatspreader_color = [0.7, 0.7, 0.7]; // Aluminum

module neiler_ram_module() {
    union() {
        // PCB base
        color(pcb_color) {
            difference() {
                // Main PCB
                cube([pcb_length, pcb_height, pcb_thickness]);

                // Notch for keying (offset from center)
                notch_pos = pcb_length/2 - 5;
                translate([notch_pos, pcb_height - 10, -0.1])
                    cube([3, 10.1, pcb_thickness + 0.2]);

                // Mounting holes
                translate([5, 5, -0.1])
                    cylinder(h = pcb_thickness + 0.2, r = 1.5, $fn = 20);
                translate([pcb_length - 5, 5, -0.1])
                    cylinder(h = pcb_thickness + 0.2, r = 1.5, $fn = 20);
            }
        }

        // RAM chips on top side
        for (i = [0:chips_per_side-1]) {
            translate([10 + i * 15, 5, pcb_thickness]) {
                ram_chip();
            }
        }

        // RAM chips on bottom side
        for (i = [0:chips_per_side-1]) {
            translate([10 + i * 15, 5, 0]) {
                rotate([180, 0, 0])
                    ram_chip();
            }
        }

        // Edge connector pins
        color(pin_color) {
            pin_spacing = pcb_length / (pin_count / 2);

            for (i = [0:(pin_count/2)-1]) {
                // Front side pins
                translate([i * pin_spacing + 1, pcb_height, 0]) {
                    dimm_pin();
                }

                // Back side pins
                translate([i * pin_spacing + 1, pcb_height, pcb_thickness]) {
                    dimm_pin();
                }
            }
        }

        // Module labeling
        color(label_color) {
            translate([pcb_length/2, pcb_height/2, pcb_thickness + chip_height + 0.01]) {
                rotate([0, 0, 0])
                    linear_extrude(height = 0.05) {
                        text("NEILER RAM", size = 3, halign = "center", valign = "center",
                             font = "Liberation Sans:style=Bold");
                    }
            }

            translate([pcb_length/2, pcb_height/2 - 4, pcb_thickness + chip_height + 0.01]) {
                rotate([0, 0, 0])
                    linear_extrude(height = 0.05) {
                        text("64MB SDRAM", size = 2, halign = "center", valign = "center");
                    }
            }

            translate([pcb_length/2, pcb_height/2 + 4, pcb_thickness + chip_height + 0.01]) {
                rotate([0, 0, 0])
                    linear_extrude(height = 0.05) {
                        text("PC-133", size = 2, halign = "center", valign = "center");
                    }
            }

            // Serial number
            translate([10, 2, pcb_thickness + 0.01]) {
                linear_extrude(height = 0.05) {
                    text("S/N: NLR2025010001", size = 1, halign = "left");
                }
            }

            // Part number
            translate([pcb_length - 10, 2, pcb_thickness + 0.01]) {
                linear_extrude(height = 0.05) {
                    text("P/N: NLR-RAM-64M", size = 1, halign = "right");
                }
            }
        }

        // Optional heatspreader version
        if (false) {  // Set to true to add heatspreader
            color(heatspreader_color, 0.8) {
                translate([5, 3, pcb_thickness + chip_height])
                    cube([pcb_length - 10, pcb_height - 6, 2]);
            }
        }
    }
}

// Individual RAM chip module (TSOP-II package)
module ram_chip() {
    union() {
        // Chip body
        color(chip_color) {
            cube([chip_width, chip_depth, chip_height]);
        }

        // Pins (27 pins per side for TSOP-II 54)
        color(pin_color) {
            pins_per_side = 27;

            // Left side pins
            for (i = [0:pins_per_side-1]) {
                translate([0, 1 + i * 0.3, 0])
                    tsop_pin();
            }

            // Right side pins
            for (i = [0:pins_per_side-1]) {
                translate([chip_width, 1 + i * 0.3, 0])
                    rotate([0, 0, 180])
                        tsop_pin();
            }
        }

        // Chip label
        color(label_color) {
            translate([chip_width/2, chip_depth/2, chip_height - 0.01]) {
                linear_extrude(height = 0.02) {
                    text("64M", size = 1.2, halign = "center", valign = "center",
                         font = "Liberation Mono:style=Bold");
                }
            }

            // Pin 1 dot
            translate([1, chip_depth - 1, chip_height - 0.01]) {
                cylinder(h = 0.02, r = 0.3, $fn = 12);
            }
        }
    }
}

// TSOP gull-wing pin
module tsop_pin() {
    hull() {
        cube([pin_width, pin_thickness, 0.1]);
        translate([-pin_length + pin_width, 0, -0.3])
            cube([pin_length - pin_width, pin_thickness, 0.1]);
    }
}

// DIMM edge connector pin
module dimm_pin() {
    cube([pin_width, pin_length, pin_thickness]);
}

// Render the module
neiler_ram_module();

// Alternative: Render multiple modules showing capacity
module ram_bank_4x64mb() {
    for (i = [0:3]) {
        translate([0, 0, i * 5])
            neiler_ram_module();
    }

    // Capacity label
    color([1, 1, 1])
        translate([pcb_length/2, -10, 10])
            linear_extrude(height = 1)
                text("256MB TOTAL", size = 5, halign = "center",
                     font = "Liberation Sans:style=Bold");
}

// Uncomment to see 4x64MB bank
// ram_bank_4x64mb();
