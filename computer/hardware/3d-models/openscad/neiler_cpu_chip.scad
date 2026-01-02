// Neiler-8 CPU Chip 3D Model
// Custom 8-bit CPU in 64-pin PLCC package
// Physically buildable as ASIC or FPGA module

// Chip dimensions (PLCC-64 package)
chip_width = 24.13;  // mm
chip_depth = 24.13;  // mm
chip_height = 4.57;  // mm
pin_count = 64;
corner_cut = 3.0;    // mm diagonal cut

// Pin specifications
pin_width = 0.46;    // mm
pin_length = 1.27;   // mm
pin_spacing = 1.27;  // mm
pin_height = 0.5;    // mm

// Materials and colors
chip_color = [0.1, 0.1, 0.1];        // Black epoxy
pin_color = [0.8, 0.8, 0.7];         // Tin/Lead
label_color = [0.9, 0.9, 0.9];       // White silkscreen
heatsink_color = [0.3, 0.3, 0.35];   // Aluminum

module neiler_cpu_chip() {
    union() {
        // Main chip body
        color(chip_color) {
            difference() {
                // Chip body with chamfered top
                hull() {
                    translate([0, 0, 0])
                        cube([chip_width, chip_depth, chip_height - 0.5]);
                    translate([0.5, 0.5, chip_height - 0.5])
                        cube([chip_width - 1, chip_depth - 1, 0.5]);
                }

                // Pin 1 indicator (corner cut)
                translate([-1, -1, -0.1])
                    rotate([0, 0, 45])
                    cube([corner_cut, corner_cut, chip_height + 0.2]);
            }
        }

        // Pins (PLCC J-lead style)
        color(pin_color) {
            pins_per_side = 16;

            // Top side pins
            for (i = [0:pins_per_side-1]) {
                translate([chip_width/2 - (pins_per_side-1)*pin_spacing/2 + i*pin_spacing,
                          chip_depth,
                          pin_height]) {
                    j_lead_pin();
                }
            }

            // Bottom side pins
            for (i = [0:pins_per_side-1]) {
                translate([chip_width/2 - (pins_per_side-1)*pin_spacing/2 + i*pin_spacing,
                          0,
                          pin_height]) {
                    rotate([0, 0, 180])
                        j_lead_pin();
                }
            }

            // Left side pins
            for (i = [0:pins_per_side-1]) {
                translate([0,
                          chip_depth/2 - (pins_per_side-1)*pin_spacing/2 + i*pin_spacing,
                          pin_height]) {
                    rotate([0, 0, -90])
                        j_lead_pin();
                }
            }

            // Right side pins
            for (i = [0:pins_per_side-1]) {
                translate([chip_width,
                          chip_depth/2 - (pins_per_side-1)*pin_spacing/2 + i*pin_spacing,
                          pin_height]) {
                    rotate([0, 0, 90])
                        j_lead_pin();
                }
            }
        }

        // Chip labeling
        color(label_color) {
            translate([chip_width/2, chip_depth/2, chip_height - 0.01]) {
                linear_extrude(height = 0.02) {
                    text("NEILER-8", size = 2.5, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");
                }
            }

            translate([chip_width/2, chip_depth/2 - 3, chip_height - 0.01]) {
                linear_extrude(height = 0.02) {
                    text("CPU", size = 2, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");
                }
            }

            translate([chip_width/2, chip_depth/2 + 3, chip_height - 0.01]) {
                linear_extrude(height = 0.02) {
                    text("8MHz", size = 1.5, halign = "center", valign = "center");
                }
            }

            // Part number
            translate([chip_width/2, 2, chip_height - 0.01]) {
                linear_extrude(height = 0.02) {
                    text("NLR8-CPU-01", size = 1.2, halign = "center", valign = "center");
                }
            }

            // Pin 1 dot indicator
            translate([2, chip_depth - 2, chip_height - 0.01]) {
                cylinder(h = 0.02, r = 0.5, $fn = 20);
            }
        }

        // Optional integrated heatsink/slug
        color(heatsink_color) {
            translate([chip_width/2 - 4, chip_depth/2 - 4, chip_height]) {
                cube([8, 8, 1]);
            }
        }
    }
}

// J-lead pin module
module j_lead_pin() {
    hull() {
        cube([pin_width, pin_length, 0.1]);
        translate([0, pin_length - 0.5, -pin_height])
            cube([pin_width, 0.5, 0.1]);
    }
}

// Render the chip
neiler_cpu_chip();

// Alternative: Render with socket
module neiler_cpu_with_socket() {
    // Chip
    translate([0, 0, 5])
        neiler_cpu_chip();

    // Socket
    socket_height = 5;
    socket_color = [0.2, 0.15, 0.1];  // Brown plastic

    color(socket_color) {
        difference() {
            // Socket body
            cube([chip_width + 2, chip_depth + 2, socket_height]);

            // Chip cavity
            translate([1, 1, 1])
                cube([chip_width, chip_depth, socket_height]);
        }

        // Socket pins (through-hole)
        color(pin_color) {
            pins_per_side = 16;

            for (side = [0:3]) {
                for (i = [0:pins_per_side-1]) {
                    rotate([0, 0, side * 90])
                        translate([chip_width/2 - (pins_per_side-1)*pin_spacing/2 + i*pin_spacing + 1,
                                  chip_depth + 1,
                                  0]) {
                            cylinder(h = socket_height, r = 0.3, $fn = 12);
                            translate([0, 0, -2])
                                cylinder(h = 2, r = 0.3, $fn = 12);
                        }
                }
            }
        }
    }
}

// Uncomment to render with socket instead
// neiler_cpu_with_socket();
