// Neiler PSU 3D Model
// Custom 200W ATX-style power supply
// Modular design with efficient switching regulation

// PSU dimensions (ATX SFX form factor)
psu_width = 125;      // mm
psu_depth = 100;      // mm
psu_height = 63.5;    // mm (SFX standard)
wall_thickness = 1.5; // mm

// Fan specifications
fan_size = 80;        // mm (80mm fan)
fan_thickness = 25;   // mm

// Connector specifications
atx_connector_width = 20;
atx_connector_depth = 12;
atx_connector_height = 8;

// Colors
case_color = [0.2, 0.2, 0.2];          // Black steel
fan_color = [0.15, 0.15, 0.15];        // Black plastic
pcb_color = [0.1, 0.35, 0.1];          // Green PCB
component_color = [0.3, 0.3, 0.35];    // Components
connector_color = [1.0, 0.85, 0.1];    // Yellow/black
label_color = [1.0, 1.0, 1.0];         // White

module neiler_psu() {
    union() {
        // Main enclosure
        color(case_color) {
            difference() {
                // Outer shell
                cube([psu_width, psu_depth, psu_height]);

                // Hollow interior
                translate([wall_thickness, wall_thickness, wall_thickness])
                    cube([psu_width - 2*wall_thickness,
                          psu_depth - 2*wall_thickness,
                          psu_height - wall_thickness]);

                // Fan cutout (80mm fan mount)
                translate([psu_width/2, psu_depth - wall_thickness - 0.1, psu_height/2])
                    rotate([90, 0, 0])
                        cylinder(h = wall_thickness + 0.2, r = fan_size/2 - 2, $fn = 60);

                // Fan mounting holes
                for (x = [-1, 1]) {
                    for (y = [-1, 1]) {
                        translate([psu_width/2 + x * (fan_size/2 - 4),
                                  psu_depth - wall_thickness - 0.1,
                                  psu_height/2 + y * (fan_size/2 - 4)])
                            rotate([90, 0, 0])
                                cylinder(h = wall_thickness + 0.2, r = 2, $fn = 20);
                    }
                }

                // Ventilation holes (honeycomb pattern)
                for (x = [0:8]) {
                    for (z = [0:4]) {
                        translate([12 + x * 12,
                                  -0.1,
                                  10 + z * 10 + (x % 2) * 5])
                            rotate([90, 0, 0])
                                cylinder(h = wall_thickness + 0.2, r = 4, $fn = 6);
                    }
                }

                // Rear connector cutouts
                translate([psu_width - 60, -0.1, psu_height - 20])
                    cube([50, wall_thickness + 0.2, 15]);

                // Power switch cutout
                translate([10, -0.1, psu_height - 15])
                    cube([15, wall_thickness + 0.2, 10]);

                // AC inlet cutout
                translate([30, -0.1, psu_height - 20])
                    cube([25, wall_thickness + 0.2, 18]);
            }

            // Mounting brackets
            for (corner = [[5, 5], [psu_width - 10, 5], [5, psu_depth - 10], [psu_width - 10, psu_depth - 10]]) {
                translate([corner[0], corner[1], 0])
                    difference() {
                        cylinder(h = 3, r = 4, $fn = 20);
                        translate([0, 0, -0.1])
                            cylinder(h = 3.2, r = 1.5, $fn = 20);
                    }
            }
        }

        // Cooling fan
        color(fan_color) {
            translate([psu_width/2, psu_depth - wall_thickness - fan_thickness, psu_height/2])
                rotate([90, 0, 0])
                    cooling_fan(fan_size);
        }

        // Internal PCB
        color(pcb_color) {
            translate([wall_thickness + 2, wall_thickness + 2, wall_thickness + 2])
                cube([psu_width - 2*wall_thickness - 4, psu_depth - 2*wall_thickness - fan_thickness - 4, 1.6]);
        }

        // Power components (transformers, capacitors)
        color(component_color) {
            // Main transformer
            translate([20, 20, wall_thickness + 3.6])
                cube([25, 20, 15]);

            // Electrolytic capacitors
            for (i = [0:3]) {
                translate([55 + i * 12, 15, wall_thickness + 3.6])
                    cylinder(h = 20, r = 4, $fn = 20);
            }

            // Heatsinks
            translate([15, 50, wall_thickness + 3.6])
                cube([40, 30, 12]);
        }

        // Modular cable connectors (rear panel)
        color(connector_color) {
            // 24-pin ATX main power
            translate([psu_width - 55, wall_thickness, psu_height - 18])
                rotate([90, 0, 0])
                    atx_24pin_connector();

            // 8-pin CPU power
            translate([psu_width - 35, wall_thickness, psu_height - 18])
                rotate([90, 0, 0])
                    atx_8pin_connector();

            // 6-pin PCIe power
            translate([psu_width - 20, wall_thickness, psu_height - 18])
                rotate([90, 0, 0])
                    atx_6pin_connector();
        }

        // PSU labeling
        color(label_color) {
            // Model name
            translate([psu_width/2, psu_depth - 2, psu_height - 5])
                rotate([90, 0, 0])
                    linear_extrude(height = 0.2) {
                        text("NEILER PSU", size = 5, halign = "center",
                             font = "Liberation Sans:style=Bold");
                    }

            // Specifications
            translate([psu_width/2, psu_depth - 2, psu_height - 12])
                rotate([90, 0, 0])
                    linear_extrude(height = 0.2) {
                        text("200W 80+ GOLD", size = 3, halign = "center");
                    }

            // Voltage ratings (side panel)
            translate([2, psu_depth/2, psu_height/2])
                rotate([90, 0, 90])
                    linear_extrude(height = 0.2) {
                        text("+3.3V @ 20A", size = 2, halign = "center");
                    }

            translate([2, psu_depth/2 - 5, psu_height/2])
                rotate([90, 0, 90])
                    linear_extrude(height = 0.2) {
                        text("+5V @ 30A", size = 2, halign = "center");
                    }

            translate([2, psu_depth/2 - 10, psu_height/2])
                rotate([90, 0, 90])
                    linear_extrude(height = 0.2) {
                        text("+12V @ 16A", size = 2, halign = "center");
                    }

            // Safety certification logos
            translate([10, psu_depth - 2, 10])
                rotate([90, 0, 0])
                    linear_extrude(height = 0.2) {
                        text("UL", size = 3);
                    }

            translate([25, psu_depth - 2, 10])
                rotate([90, 0, 0])
                    linear_extrude(height = 0.2) {
                        text("CE", size = 3);
                    }
        }
    }
}

// 80mm cooling fan module
module cooling_fan(size) {
    union() {
        // Fan frame
        difference() {
            cylinder(h = 3, r = size/2, $fn = 60);
            translate([0, 0, -0.1])
                cylinder(h = 3.2, r = size/2 - 2, $fn = 60);

            // Corner supports
            for (a = [0:90:270]) {
                rotate([0, 0, a + 45])
                    translate([size/2 - 10, -1, -0.1])
                        cube([10, 2, 3.2]);
            }
        }

        // Fan hub
        cylinder(h = fan_thickness, r = 8, $fn = 30);

        // Fan blades (7 blades)
        for (a = [0:51.4:308.6]) {
            rotate([0, 0, a])
                translate([8, 0, fan_thickness/2])
                    rotate([0, 15, 0])
                        cube([size/2 - 10, 1.5, 0.5], center = true);
        }

        // Label sticker
        color([0.8, 0.8, 0]) {
            translate([0, 0, fan_thickness - 0.1])
                cylinder(h = 0.1, r = 12, $fn = 30);
        }

        color([0, 0, 0]) {
            translate([0, 0, fan_thickness - 0.05])
                linear_extrude(height = 0.06)
                    text("12V", size = 3, halign = "center", valign = "center");
        }
    }
}

// ATX 24-pin connector
module atx_24pin_connector() {
    color([0, 0, 0]) {
        cube([24, atx_connector_depth, atx_connector_height]);
    }
    color(connector_color) {
        for (i = [0:23]) {
            translate([i + 0.25, atx_connector_depth, atx_connector_height/2 - 0.5])
                cube([0.5, 3, 1]);
        }
    }
}

// ATX 8-pin CPU connector
module atx_8pin_connector() {
    color([0, 0, 0]) {
        cube([9, atx_connector_depth, atx_connector_height]);
    }
    color(connector_color) {
        for (i = [0:7]) {
            translate([i + 0.25, atx_connector_depth, atx_connector_height/2 - 0.5])
                cube([0.5, 3, 1]);
        }
    }
}

// ATX 6-pin PCIe connector
module atx_6pin_connector() {
    color([0, 0, 0]) {
        cube([7, atx_connector_depth, atx_connector_height]);
    }
    color(connector_color) {
        for (i = [0:5]) {
            translate([i + 0.25, atx_connector_depth, atx_connector_height/2 - 0.5])
                cube([0.5, 3, 1]);
        }
    }
}

// Render the PSU
neiler_psu();
