// Neiler PSU Board - 3D Model
// ATX-style power supply board
// Multi-rail output: +5V, +12V, -12V, +3.3V

// Parameters
pcb_width = 150.0;
pcb_depth = 86.0;
pcb_thickness = 1.6;

module neiler_psu_board() {
    // Main PCB
    color("Blue") {
        cube([pcb_width, pcb_depth, pcb_thickness], center=true);
    }

    // ATX power connector (24-pin)
    color("Black")
    translate([pcb_width/2 - 15, 0, pcb_thickness/2 + 5.5])
        atx_connector();

    // Voltage regulators
    translate([-30, 20, pcb_thickness/2 + 2])
        voltage_regulator("+5V", "Green");
    translate([-30, 0, pcb_thickness/2 + 2])
        voltage_regulator("+12V", "Yellow");
    translate([-30, -20, pcb_thickness/2 + 2])
        voltage_regulator("+3.3V", "Orange");

    // Large filter capacitors
    for(x = [-10, 10, 30]) {
        translate([x, 25, pcb_thickness/2])
            electrolytic_cap(10, 20);
    }

    // Transformer
    color("Gray")
    translate([40, -15, pcb_thickness/2 + 12])
        cube([35, 30, 24], center=true);

    // Heatsinks
    color("Silver")
    for(x = [-50, -70]) {
        translate([x, -25, pcb_thickness/2 + 8])
            heatsink_fins(20, 25, 16);
    }

    // Power LED indicators
    translate([60, 30, pcb_thickness/2 + 1]) {
        led("Green", "+5V");
        translate([8, 0, 0]) led("Yellow", "+12V");
        translate([16, 0, 0]) led("Orange", "+3.3V");
    }

    // Label
    color("White")
    translate([0, -35, pcb_thickness/2 + 0.01])
        linear_extrude(height=0.05)
        text("NEILER PSU-64", size=4, halign="center", valign="center", font="Liberation Sans:style=Bold");

    translate([0, -40, pcb_thickness/2 + 0.01])
        linear_extrude(height=0.05)
        text("250W Multi-Rail", size=2, halign="center", valign="center");
}

module atx_connector() {
    cube([40, 20, 11], center=true);

    color("Yellow")
    for(i = [0:23]) {
        x = -18 + (i % 12) * 3;
        y = (i < 12) ? -4 : 4;
        translate([x, y, -2])
            cube([0.6, 0.6, 6], center=true);
    }
}

module voltage_regulator(label, led_color) {
    // TO-220 package
    color("Black") {
        cube([10, 15, 4], center=true);
        translate([0, 0, 6])
            cube([10, 1, 12], center=true);
    }

    // Label
    color("White")
    translate([0, 0, 2.1])
        rotate([0, 0, 0])
        linear_extrude(height=0.05)
        text(label, size=1.5, halign="center", valign="center");
}

module electrolytic_cap(diameter, height) {
    color("Blue") {
        cylinder(r=diameter/2, h=height, center=false, $fn=30);

        color("Silver")
        translate([0, 0, height])
            cylinder(r=diameter/2 - 1, h=1, center=false, $fn=30);
    }
}

module heatsink_fins(width, depth, height) {
    fin_count = 6;
    fin_thickness = 1.5;
    spacing = (depth - fin_count*fin_thickness) / (fin_count - 1);

    // Base
    translate([0, 0, -2])
        cube([width, depth, 2], center=true);

    // Fins
    for(i = [0 : fin_count - 1]) {
        translate([0, -depth/2 + i*(fin_thickness + spacing), height/2 - 1])
            cube([width, fin_thickness, height], center=true);
    }
}

module led(col, label) {
    color(col, 0.8)
        cylinder(r=2.5, h=4, center=false, $fn=20);

    color("White")
    translate([0, -6, 0])
        linear_extrude(height=0.05)
        text(label, size=1.2, halign="center", valign="center");
}

// Render PSU
neiler_psu_board();
