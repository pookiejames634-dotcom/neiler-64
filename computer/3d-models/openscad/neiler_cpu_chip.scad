// Neiler-8 CPU Chip - 3D Model
// 64-pin PLCC package with custom pinout
// Designed for the Neiler-64 computer system

// Parameters
chip_width = 24.13;  // 24.13mm square PLCC package
chip_height = 4.57;  // Total height
body_height = 4.06;  // Body height
pin_count = 68;      // 68-pin PLCC
pin_width = 0.38;
pin_length = 1.27;
pin_pitch = 1.27;

module neiler_cpu_chip() {
    color("DimGray") {
        // Main chip body
        difference() {
            // Main package body
            translate([0, 0, 0])
                cube([chip_width, chip_width, body_height], center=true);

            // Pin 1 indicator (beveled corner)
            translate([-chip_width/2 + 2, -chip_width/2 + 2, body_height/2 - 0.5])
                rotate([0, 0, 45])
                cube([2, 2, 1], center=true);
        }

        // Top label surface
        color("Black")
        translate([0, 0, body_height/2 + 0.01])
            cube([chip_width - 0.5, chip_width - 0.5, 0.1], center=true);
    }

    // Chip markings
    color("White") {
        translate([0, 6, body_height/2 + 0.06])
            linear_extrude(height=0.05)
            text("NEILER-8", size=3, halign="center", valign="center", font="Liberation Sans:style=Bold");

        translate([0, 2, body_height/2 + 0.06])
            linear_extrude(height=0.05)
            text("CPU", size=2.5, halign="center", valign="center");

        translate([0, -2, body_height/2 + 0.06])
            linear_extrude(height=0.05)
            text("N8-001", size=2, halign="center", valign="center");

        translate([0, -5, body_height/2 + 0.06])
            linear_extrude(height=0.05)
            text("2025", size=1.8, halign="center", valign="center");
    }

    // Generate PLCC pins (J-lead style)
    color("Gold") {
        // Bottom pins
        for(i = [0 : pin_count/4 - 1]) {
            // Bottom edge
            translate([-chip_width/2 + 2 + i*pin_pitch, -chip_width/2, -body_height/2])
                plcc_pin();
            // Top edge
            translate([-chip_width/2 + 2 + i*pin_pitch, chip_width/2, -body_height/2])
                rotate([0, 0, 180])
                plcc_pin();
            // Left edge
            translate([-chip_width/2, -chip_width/2 + 2 + i*pin_pitch, -body_height/2])
                rotate([0, 0, -90])
                plcc_pin();
            // Right edge
            translate([chip_width/2, -chip_width/2 + 2 + i*pin_pitch, -body_height/2])
                rotate([0, 0, 90])
                plcc_pin();
        }
    }
}

module plcc_pin() {
    // J-lead pin profile
    hull() {
        translate([0, 0, 0])
            cube([pin_width, pin_length, 0.2], center=true);
        translate([0, pin_length/2 - 0.3, -0.5])
            cube([pin_width, 0.6, 0.2], center=true);
    }
}

// Render the chip
neiler_cpu_chip();
