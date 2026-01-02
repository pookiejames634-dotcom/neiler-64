// Neiler-64 Motherboard 3D Model
// Complete ATX motherboard with custom Neiler CPU, GPU, RAM slots
// Full I/O, expansion slots, and power delivery

// Board dimensions (ATX standard)
board_width = 305;    // mm
board_depth = 244;    // mm
board_thickness = 1.6; // mm

// Component spacing
cpu_socket_pos = [80, 150];
ram_slot_pos = [150, 150];
gpu_slot_pos = [50, 50];

// Colors
pcb_color = [0.05, 0.2, 0.4];        // Blue PCB (high-end look)
copper_color = [0.72, 0.45, 0.2];    // Copper traces
soldermask_color = [0.05, 0.15, 0.25]; // Dark blue soldermask
silkscreen_color = [1, 1, 1];        // White
gold_color = [1.0, 0.84, 0];         // Gold (ENIG finish)

module neiler_motherboard() {
    union() {
        // Main PCB
        color(pcb_color) {
            difference() {
                // PCB outline
                cube([board_width, board_depth, board_thickness]);

                // Mounting holes (ATX standard positions)
                mounting_holes();

                // I/O shield cutout
                translate([0, board_depth - 45, -0.1])
                    cube([45, 45, board_thickness + 0.2]);
            }
        }

        // CPU socket (PLCC-64 or ZIF socket)
        translate([cpu_socket_pos[0], cpu_socket_pos[1], board_thickness])
            cpu_socket_zif();

        // RAM slots (4x DIMM slots)
        for (i = [0:3]) {
            translate([ram_slot_pos[0], ram_slot_pos[1] - i * 20, board_thickness])
                ram_slot_dimm();
        }

        // GPU socket (custom expansion slot)
        translate([gpu_slot_pos[0], gpu_slot_pos[1], board_thickness])
            rotate([0, 0, 90])
                expansion_slot("GPU");

        // Expansion slots (PCIe-style)
        for (i = [0:3]) {
            translate([gpu_slot_pos[0] + 20 * (i + 1), gpu_slot_pos[1], board_thickness])
                rotate([0, 0, 90])
                    expansion_slot("PCIe x1");
        }

        // Chipset with heatsink
        translate([180, 100, board_thickness])
            chipset_with_heatsink("NEILER NCH");

        // VRM (Voltage Regulator Module)
        translate([cpu_socket_pos[0] - 20, cpu_socket_pos[1] + 40, board_thickness])
            vrm_section();

        // BIOS chip
        translate([100, 30, board_thickness])
            bios_chip();

        // CMOS battery
        translate([250, 30, board_thickness])
            cmos_battery();

        // I/O connectors (rear panel)
        translate([0, board_depth - 40, board_thickness])
            io_panel();

        // Front panel headers
        translate([20, 20, board_thickness])
            front_panel_headers();

        // SATA connectors
        for (i = [0:3]) {
            translate([220 + i * 15, 180, board_thickness])
                rotate([0, 0, 90])
                    sata_connector();
        }

        // M.2 slot
        translate([140, 80, board_thickness])
            m2_slot();

        // ATX power connectors
        translate([board_width - 30, 150, board_thickness])
            atx_24pin_header();

        translate([board_width - 30, 200, board_thickness])
            atx_8pin_cpu_header();

        // PCB traces (decorative top layer)
        color(copper_color, 0.3)
            translate([0, 0, board_thickness + 0.01])
                pcb_trace_art();

        // Silkscreen labels
        color(silkscreen_color)
            translate([0, 0, board_thickness + 0.02])
                motherboard_labels();
    }
}

// CPU Socket (ZIF - Zero Insertion Force)
module cpu_socket_zif() {
    socket_size = 30;
    color([0.2, 0.15, 0.1]) {
        difference() {
            cube([socket_size, socket_size, 5]);
            translate([2, 2, 2])
                cube([socket_size - 4, socket_size - 4, 4]);
        }

        // ZIF lever
        translate([socket_size, socket_size/2 - 2, 0])
            cube([8, 4, 2]);
    }

    // Pin grid
    color(gold_color) {
        for (x = [0:7]) {
            for (y = [0:7]) {
                translate([3 + x * 3, 3 + y * 3, -1])
                    cylinder(h = 1, r = 0.3, $fn = 8);
            }
        }
    }
}

// RAM DIMM slot
module ram_slot_dimm() {
    slot_length = 135;
    color([0.15, 0.15, 0.15]) {
        cube([slot_length, 10, 12]);

        // Retention clips
        translate([-2, 5, 0])
            cube([2, 4, 15]);
        translate([slot_length, 5, 0])
            cube([2, 4, 15]);
    }

    // Contacts
    color(gold_color) {
        for (i = [0:83]) {
            translate([i * 1.6, 4, 1])
                cube([0.3, 2, 8]);
        }
    }
}

// Expansion slot
module expansion_slot(label) {
    slot_length = 90;
    color([0.15, 0.15, 0.15]) {
        cube([slot_length, 8, 12]);

        // Bracket mounting
        translate([-5, 0, 0])
            cube([5, 8, 20]);
    }

    color(gold_color) {
        for (i = [0:40]) {
            translate([5 + i * 2, 3, 1])
                cube([0.3, 2, 8]);
        }
    }

    // Label
    color([1, 1, 1])
        translate([slot_length/2, -2, 0])
            rotate([90, 0, 0])
                linear_extrude(height = 0.1)
                    text(label, size = 2, halign = "center");
}

// Chipset with heatsink
module chipset_with_heatsink(label) {
    // Chip
    color([0.1, 0.1, 0.1])
        cube([25, 25, 2]);

    // Heatsink
    color([0.7, 0.7, 0.7]) {
        translate([2.5, 2.5, 2])
            cube([20, 20, 8]);

        // Fins
        for (i = [0:8]) {
            translate([2.5 + i * 2, 2.5, 10])
                cube([1, 20, 5]);
        }
    }

    // Label
    color([1, 1, 1])
        translate([12.5, 12.5, 10.5])
            linear_extrude(height = 0.1)
                text(label, size = 2, halign = "center", valign = "center");
}

// VRM (Voltage Regulator Module) section
module vrm_section() {
    // Power phases (6 phases)
    for (i = [0:5]) {
        color([0.15, 0.15, 0.15])
            translate([i * 8, 0, 0])
                cube([6, 6, 4]);

        // Chokes/inductors
        color([0.3, 0.3, 0.3])
            translate([i * 8 + 2, 8, 0])
                cylinder(h = 6, r = 2.5, $fn = 20);

        // MOSFETs
        color([0.1, 0.1, 0.1])
            translate([i * 8 + 1, -4, 0])
                cube([4, 3, 1.5]);
    }

    // Capacitors
    for (i = [0:10]) {
        color([0.8, 0.7, 0.1])
            translate([i * 4, 15, 0])
                cylinder(h = 8, r = 1.5, $fn = 16);
    }
}

// BIOS chip (EEPROM)
module bios_chip() {
    color([0.1, 0.1, 0.1])
        cube([8, 6, 2]);

    color([1, 1, 1])
        translate([4, 3, 2.01])
            linear_extrude(height = 0.05)
                text("BIOS", size = 1, halign = "center", valign = "center");
}

// CMOS battery (CR2032)
module cmos_battery() {
    color([0.7, 0.7, 0.7])
        cylinder(h = 3, r = 10, $fn = 30);

    color([0.2, 0.2, 0.2])
        translate([0, 0, 3])
            cylinder(h = 0.2, r = 10, $fn = 30);
}

// I/O Panel (rear connectors)
module io_panel() {
    // USB ports
    for (i = [0:5]) {
        color([0.1, 0.1, 0.1])
            translate([i * 15, 0, 0])
                cube([12, 14, 7]);
    }

    // Ethernet
    color([0.3, 0.3, 0.3])
        translate([100, 0, 0])
            cube([16, 21, 14]);

    // Audio jacks
    for (i = [0:2]) {
        color([0.5, 0.8, 0.3])
            translate([130 + i * 15, 5, 5])
                rotate([90, 0, 0])
                    cylinder(h = 15, r = 3, $fn = 20);
    }

    // HDMI/DisplayPort
    color([0.2, 0.2, 0.2])
        translate([180, 0, 0])
            cube([15, 12, 6]);
}

// Front panel headers
module front_panel_headers() {
    for (i = [0:2]) {
        color([0.1, 0.1, 0.1])
            translate([i * 15, 0, 0])
                cube([10, 5, 8]);

        color(gold_color) {
            for (p = [0:7]) {
                translate([i * 15 + 1 + p, 1, 0])
                    cube([0.5, 3, 6]);
            }
        }
    }
}

// SATA connector
module sata_connector() {
    color([0.1, 0.1, 0.1])
        cube([15, 10, 5]);

    color(gold_color)
        translate([2, 2, 1])
            cube([11, 6, 3]);
}

// M.2 slot (NVMe SSD)
module m2_slot() {
    slot_length = 80;

    color([0.15, 0.15, 0.15]) {
        cube([slot_length, 22, 3]);

        // Mounting standoff
        translate([slot_length - 5, 11, 3])
            cylinder(h = 3, r = 2, $fn = 20);
    }

    // Key notch
    color([0.1, 0.1, 0.1])
        translate([5, 8, 0.5])
            cube([slot_length - 10, 6, 2]);
}

// ATX 24-pin power header
module atx_24pin_header() {
    color([0.1, 0.1, 0.1])
        cube([30, 20, 15]);

    color(gold_color) {
        for (i = [0:23]) {
            translate([2 + (i % 12) * 2.5, 2 + floor(i / 12) * 5, 2])
                cube([0.6, 0.6, 12]);
        }
    }
}

// ATX 8-pin CPU power header
module atx_8pin_cpu_header() {
    color([0.1, 0.1, 0.1])
        cube([15, 10, 12]);

    color(gold_color) {
        for (i = [0:7]) {
            translate([2 + (i % 4) * 3, 2 + floor(i / 4) * 5, 2])
                cube([0.6, 0.6, 10]);
        }
    }
}

// PCB trace artwork (decorative)
module pcb_trace_art() {
    // Power planes and traces
    for (i = [0:20]) {
        translate([i * 15, 0, 0])
            cube([10, board_depth, 0.035]);
    }
}

// Motherboard silkscreen labels
module motherboard_labels() {
    // Main title
    translate([board_width/2, board_depth - 10, 0])
        linear_extrude(height = 0.05)
            text("NEILER-64 MOTHERBOARD", size = 8, halign = "center",
                 font = "Liberation Sans:style=Bold");

    // Model number
    translate([board_width/2, board_depth - 20, 0])
        linear_extrude(height = 0.05)
            text("Model: NLR-MB-ATX-01", size = 4, halign = "center");

    // Revision
    translate([10, 10, 0])
        linear_extrude(height = 0.05)
            text("REV 1.0", size = 3);
}

// Mounting holes (ATX standard)
module mounting_holes() {
    hole_positions = [
        [6.35, 6.35],
        [6.35, 237.49],
        [154.94, 6.35],
        [154.94, 237.49],
        [298.45, 6.35],
        [298.45, 237.49],
        [298.45, 83.82],
        [298.45, 170.18]
    ];

    for (pos = hole_positions) {
        translate([pos[0], pos[1], -0.1])
            cylinder(h = board_thickness + 0.2, r = 1.6, $fn = 20);
    }
}

// Render the motherboard
neiler_motherboard();
