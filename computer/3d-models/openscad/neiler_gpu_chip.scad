// Neiler GPU Chip - 3D Model
// 100-pin TQFP package with heatsink
// High-performance graphics processor for Neiler-64

// Parameters
chip_width = 20.0;   // 20mm square body
chip_height = 1.4;   // Body thickness
pin_count = 100;     // 100-pin TQFP
pin_width = 0.22;
pin_length = 0.75;
pin_pitch = 0.5;
pin_thickness = 0.15;
heatsink_size = 25.0;
heatsink_height = 10.0;

module neiler_gpu_chip() {
    color("DarkSlateGray") {
        // Main chip body
        difference() {
            cube([chip_width, chip_width, chip_height], center=true);

            // Pin 1 indicator
            translate([-chip_width/2 + 1.5, -chip_width/2 + 1.5, chip_height/2 - 0.2])
                cylinder(r=0.5, h=0.4, center=true, $fn=20);
        }
    }

    // Top surface with markings
    color("Black")
    translate([0, 0, chip_height/2 + 0.01])
        cube([chip_width - 0.3, chip_width - 0.3, 0.05], center=true);

    // GPU markings
    color("Cyan") {
        translate([0, 5, chip_height/2 + 0.06])
            linear_extrude(height=0.05)
            text("NEILER", size=2.5, halign="center", valign="center", font="Liberation Sans:style=Bold");

        translate([0, 1.5, chip_height/2 + 0.06])
            linear_extrude(height=0.05)
            text("GPU-64", size=3, halign="center", valign="center", font="Liberation Sans:style=Bold");

        translate([0, -2, chip_height/2 + 0.06])
            linear_extrude(height=0.05)
            text("320x200/640x480", size=1.2, halign="center", valign="center");

        translate([0, -4, chip_height/2 + 0.06])
            linear_extrude(height=0.05)
            text("NG-001", size=1.5, halign="center", valign="center");
    }

    // Generate TQFP pins (gull-wing style)
    color("Silver") {
        pins_per_side = pin_count / 4;
        for(i = [0 : pins_per_side - 1]) {
            offset = -chip_width/2 + (chip_width - (pins_per_side-1)*pin_pitch)/2 + i*pin_pitch;

            // Bottom edge
            translate([offset, -chip_width/2, 0])
                tqfp_pin();
            // Top edge
            translate([offset, chip_width/2, 0])
                rotate([0, 0, 180])
                tqfp_pin();
            // Left edge
            translate([-chip_width/2, offset, 0])
                rotate([0, 0, -90])
                tqfp_pin();
            // Right edge
            translate([chip_width/2, offset, 0])
                rotate([0, 0, 90])
                tqfp_pin();
        }
    }

    // Optional heatsink
    color("Silver", 0.7)
    translate([0, 0, chip_height/2 + heatsink_height/2])
        heatsink();
}

module tqfp_pin() {
    // Gull-wing pin profile
    translate([0, -chip_width/2 - pin_length/2, 0])
        cube([pin_width, pin_length, pin_thickness], center=true);
}

module heatsink() {
    fin_count = 8;
    fin_thickness = 1.0;
    fin_spacing = (heatsink_size - fin_count*fin_thickness) / (fin_count - 1);

    // Base plate
    translate([0, 0, -heatsink_height/2 + 0.5])
        cube([heatsink_size, heatsink_size, 1], center=true);

    // Fins
    for(i = [0 : fin_count - 1]) {
        translate([- heatsink_size/2 + i*(fin_thickness + fin_spacing), 0, 0])
            cube([fin_thickness, heatsink_size, heatsink_height], center=true);
    }
}

// Render GPU
neiler_gpu_chip();
