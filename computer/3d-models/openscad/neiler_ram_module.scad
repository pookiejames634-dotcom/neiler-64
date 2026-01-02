// Neiler RAM Module - 3D Model
// Custom 8MB RAM module for Neiler-64
// DIMM-style connector with 8 TSOP chips

// Parameters
pcb_width = 133.35;   // Standard DIMM width
pcb_height = 30.0;
pcb_thickness = 1.6;
chip_count = 8;       // 8x 1MB chips
tsop_width = 18.4;
tsop_length = 8.0;
tsop_height = 1.2;

module neiler_ram_module() {
    // PCB
    color("DarkGreen") {
        difference() {
            cube([pcb_width, pcb_height, pcb_thickness], center=true);

            // Mounting holes
            for(x = [-pcb_width/2 + 5, pcb_width/2 - 5]) {
                translate([x, 0, 0])
                    cylinder(r=1.5, h=pcb_thickness + 1, center=true, $fn=20);
            }

            // Notch for keying
            translate([0, -pcb_height/2, 0])
                cube([5, 2, pcb_thickness + 1], center=true);
        }
    }

    // Gold edge connector
    color("Gold")
    translate([0, -pcb_height/2 + 0.5, -pcb_thickness/2 - 1.5])
        cube([pcb_width - 10, 1, 3], center=true);

    // RAM chips on top
    for(i = [0 : chip_count - 1]) {
        translate([- pcb_width/2 + 15 + i*15, 5, pcb_thickness/2 + tsop_height/2])
            tsop_chip(i);
    }

    // RAM chips on bottom (back side)
    for(i = [0 : chip_count - 1]) {
        translate([- pcb_width/2 + 15 + i*15, -5, -pcb_thickness/2 - tsop_height/2])
            rotate([180, 0, 0])
            tsop_chip(i);
    }

    // Label
    color("White")
    translate([0, 10, pcb_thickness/2 + 0.01])
        linear_extrude(height=0.05)
        text("NEILER-64 RAM 8MB", size=2.5, halign="center", valign="center", font="Liberation Sans:style=Bold");
}

module tsop_chip(index) {
    color("Black") {
        // Chip body
        cube([tsop_width, tsop_length, tsop_height], center=true);

        // Chip label
        color("White")
        translate([0, 0, tsop_height/2 + 0.01])
            linear_extrude(height=0.02)
            text(str("1MB-", index), size=1.5, halign="center", valign="center");
    }

    // Pins
    color("Silver") {
        pin_count = 44;
        pin_pitch = (tsop_width - 2) / (pin_count/2);
        for(i = [0 : pin_count/2 - 1]) {
            offset = -tsop_width/2 + 1 + i*pin_pitch;
            // Top pins
            translate([offset, tsop_length/2, 0])
                cube([0.3, 0.8, 0.15], center=true);
            // Bottom pins
            translate([offset, -tsop_length/2, 0])
                cube([0.3, 0.8, 0.15], center=true);
        }
    }
}

// Render RAM module
neiler_ram_module();
