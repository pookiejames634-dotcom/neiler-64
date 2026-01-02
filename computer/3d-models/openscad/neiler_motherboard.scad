// Neiler-64 Motherboard - 3D Model
// ATX form factor motherboard
// Sockets for CPU, GPU, 4x RAM slots, expansion slots

// Include component models (when rendering separately)
// use <neiler_cpu_chip.scad>;
// use <neiler_gpu_chip.scad>;
// use <neiler_ram_module.scad>;

// Parameters
mobo_width = 305;     // ATX width (12")
mobo_depth = 244;     // ATX depth (9.6")
mobo_thickness = 1.6;

module neiler_motherboard() {
    // Main PCB
    color("DarkSlateBlue") {
        difference() {
            cube([mobo_width, mobo_depth, mobo_thickness], center=true);

            // Mounting holes (ATX standard)
            mounting_holes();

            // I/O shield cutout
            translate([-mobo_width/2, mobo_depth/2 - 44, 0])
                cube([45, 1, mobo_thickness + 2], center=true);
        }
    }

    // CPU Socket (PLCC-68)
    translate([-50, 40, mobo_thickness/2])
        cpu_socket();

    // GPU Socket (TQFP-100)
    translate([60, 40, mobo_thickness/2])
        gpu_socket();

    // RAM slots (4x DIMM)
    for(i = [0:3]) {
        translate([-80 + i*45, -40, mobo_thickness/2])
            ram_slot();
    }

    // Chipset
    translate([0, -80, mobo_thickness/2])
        chipset();

    // BIOS/ROM chip
    translate([-100, -100, mobo_thickness/2])
        rom_chip();

    // Power connectors
    translate([mobo_width/2 - 25, 80, mobo_thickness/2])
        power_connector_24pin();
    translate([mobo_width/2 - 25, 50, mobo_thickness/2])
        power_connector_8pin();

    // Expansion slots (ISA-style for Neiler peripherals)
    for(i = [0:3]) {
        translate([20, -120 + i*25, mobo_thickness/2])
            expansion_slot();
    }

    // I/O ports on back panel
    translate([-mobo_width/2 + 15, mobo_depth/2 - 20, mobo_thickness/2])
        io_panel();

    // CMOS battery
    translate([100, -100, mobo_thickness/2])
        cmos_battery();

    // Capacitors scattered around
    capacitor_array();

    // Motherboard labels
    motherboard_labels();
}

module mounting_holes() {
    // ATX mounting hole positions
    holes = [
        [-mobo_width/2 + 6.35, -mobo_depth/2 + 6.35],
        [-mobo_width/2 + 6.35, mobo_depth/2 - 6.35],
        [mobo_width/2 - 6.35, -mobo_depth/2 + 6.35],
        [mobo_width/2 - 6.35, mobo_depth/2 - 6.35],
        [0, -mobo_depth/2 + 6.35],
        [0, mobo_depth/2 - 6.35],
    ];

    for(hole = holes) {
        translate([hole[0], hole[1], 0])
            cylinder(r=3, h=mobo_thickness + 2, center=true, $fn=20);
    }
}

module cpu_socket() {
    color("White") {
        cube([30, 30, 5], center=true);

        // Socket pins
        color("Gold")
        translate([0, 0, -2])
            cylinder(r=12, h=1, center=true, $fn=60);
    }

    // Label
    color("Black")
    translate([0, 0, 2.6])
        linear_extrude(height=0.05)
        text("CPU", size=3, halign="center", valign="center", font="Liberation Sans:style=Bold");
}

module gpu_socket() {
    color("Black") {
        cube([25, 25, 3], center=true);

        // Socket contacts
        color("Gold")
        for(i = [0:3]) {
            translate([0, 0, -1])
                rotate([0, 0, i*90])
                translate([10, 0, 0])
                cube([8, 0.5, 0.3], center=true);
        }
    }

    color("White")
    translate([0, 0, 1.6])
        linear_extrude(height=0.05)
        text("GPU", size=2.5, halign="center", valign="center", font="Liberation Sans:style=Bold");
}

module ram_slot() {
    color("White") {
        cube([140, 12, 8], center=true);

        // Retention clips
        color("LightGray")
        for(x = [-65, 65]) {
            translate([x, 0, 0])
                cube([5, 12, 12], center=true);
        }
    }

    color("Black")
    translate([0, 0, 4.1])
        linear_extrude(height=0.05)
        text("DDR-NEILER", size=1.8, halign="center", valign="center");
}

module chipset() {
    color("Black") {
        cube([25, 25, 3], center=true);

        color("Silver")
        translate([0, 0, 3])
            cube([20, 20, 0.2], center=true);
    }

    color("Cyan")
    translate([0, 0, 1.6])
        linear_extrude(height=0.05)
        text("N64", size=4, halign="center", valign="center", font="Liberation Sans:style=Bold");
}

module rom_chip() {
    color("Black") {
        cube([12, 8, 3], center=true);
    }

    color("White")
    translate([0, 0, 1.6])
        linear_extrude(height=0.05)
        text("BIOS", size=1.5, halign="center", valign="center");
}

module power_connector_24pin() {
    color("White") {
        cube([60, 20, 12], center=true);

        // Pins
        color("Yellow")
        for(i = [0:23]) {
            x = -28 + (i % 12) * 4.5;
            y = (i < 12) ? -5 : 5;
            translate([x, y, -4])
                cube([0.8, 0.8, 8], center=true);
        }
    }
}

module power_connector_8pin() {
    color("Yellow") {
        cube([25, 15, 12], center=true);

        color("Black")
        for(i = [0:7]) {
            x = -12 + i * 3.5;
            translate([x, 0, -4])
                cube([0.8, 0.8, 8], center=true);
        }
    }
}

module expansion_slot() {
    color("Brown") {
        cube([120, 8, 10], center=true);

        // Gold fingers area
        color("Gold")
        translate([0, 0, -3])
            cube([100, 5, 2], center=true);
    }
}

module io_panel() {
    spacing = 12;

    // Serial ports
    for(i = [0:1]) {
        translate([i*spacing, 0, 0])
            db9_connector("COM");
    }

    // Parallel port
    translate([2*spacing, 0, 0])
        db25_connector("LPT");

    // PS/2 ports
    for(i = [0:1]) {
        translate([3*spacing + i*7, 0, 0])
            ps2_connector();
    }

    // Audio jacks
    for(i = [0:2]) {
        translate([4*spacing + i*6, 0, 0])
            audio_jack();
    }
}

module db9_connector(label) {
    color("Silver") {
        cube([15, 8, 10], center=true);
    }
}

module db25_connector(label) {
    color("Pink") {
        cube([20, 8, 10], center=true);
    }
}

module ps2_connector() {
    color("Purple") {
        cylinder(r=4, h=8, center=true, $fn=20);
    }
}

module audio_jack() {
    color("Lime") {
        cylinder(r=3, h=8, center=true, $fn=20);
    }
}

module cmos_battery() {
    color("Silver") {
        cylinder(r=10, h=3, center=false, $fn=30);
    }

    color("Blue")
    translate([0, 0, 3])
        cylinder(r=9, h=0.5, center=false, $fn=30);
}

module capacitor_array() {
    positions = [
        [-40, 90], [-20, 90], [0, 90],
        [80, 90], [100, 90], [120, 90],
        [-120, 0], [-100, 0],
        [40, -40], [60, -40],
        [-60, -120], [-40, -120], [-20, -120]
    ];

    for(pos = positions) {
        translate([pos[0], pos[1], mobo_thickness/2])
            small_capacitor();
    }
}

module small_capacitor() {
    color("Black") {
        cylinder(r=3, h=7, center=false, $fn=20);

        color("Gold")
        translate([0, 0, 7])
            cylinder(r=2.5, h=0.5, center=false, $fn=20);
    }
}

module motherboard_labels() {
    color("White") {
        // Main title
        translate([0, mobo_depth/2 - 30, mobo_thickness/2 + 0.01])
            linear_extrude(height=0.05)
            text("NEILER-64 MOTHERBOARD", size=5, halign="center", valign="center", font="Liberation Sans:style=Bold");

        // Model number
        translate([0, mobo_depth/2 - 38, mobo_thickness/2 + 0.01])
            linear_extrude(height=0.05)
            text("Model: NM-001 Rev 1.0", size=2.5, halign="center", valign="center");

        // Specifications
        translate([-130, mobo_depth/2 - 80, mobo_thickness/2 + 0.01])
            linear_extrude(height=0.05)
            text("• Neiler-8/16 CPU", size=1.8, halign="left", valign="center");

        translate([-130, mobo_depth/2 - 85, mobo_thickness/2 + 0.01])
            linear_extrude(height=0.05)
            text("• NeilerGPU Graphics", size=1.8, halign="left", valign="center");

        translate([-130, mobo_depth/2 - 90, mobo_thickness/2 + 0.01])
            linear_extrude(height=0.05)
            text("• Up to 32MB RAM", size=1.8, halign="left", valign="center");

        translate([-130, mobo_depth/2 - 95, mobo_thickness/2 + 0.01])
            linear_extrude(height=0.05)
            text("• 4x Expansion Slots", size=1.8, halign="left", valign="center");
    }
}

// Render motherboard
neiler_motherboard();
