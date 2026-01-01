// Neilerdeck Cyberdeck Case
// Open this file in OpenSCAD to view and render
// Install: sudo apt install openscad

// Main dimensions (mm)
case_width = 300;
case_depth = 200;
case_height = 80;
wall = 3;

// Display
display_w = 195;
display_h = 110;
display_x = 50;
display_y = 20;

// Keyboard
keyboard_w = 240;
keyboard_h = 50;
keyboard_y = 140;

// Components
pi_w = 85;
pi_h = 56;
fan_d = 40;

// Rendering quality
$fn = 50;

module rounded_box(size, r=5) {
    hull() {
        for(x=[r, size[0]-r])
            for(y=[r, size[1]-r])
                translate([x, y, 0])
                    cylinder(h=size[2], r=r);
    }
}

module mounting_hole(d=3.2) {
    cylinder(h=wall*3, d=d, center=true);
}

module usb_port() {
    cube([wall*2, 15, 7], center=true);
}

module ethernet_port() {
    cube([wall*2, 16, 14], center=true);
}

module fan_mount() {
    union() {
        cylinder(h=wall*2, d=fan_d, center=true);
        // Mounting holes
        for(a=[45:90:315])
            rotate([0, 0, a])
                translate([fan_d/2-4, 0, 0])
                    cylinder(h=wall*3, d=3.2, center=true);
    }
}

module top_panel() {
    difference() {
        // Main panel
        rounded_box([case_width, case_depth, wall]);

        // Display cutout
        translate([display_x, display_y, -1])
            rounded_box([display_w, display_h, wall+2], r=2);

        // Keyboard cutout
        translate([30, keyboard_y, -1])
            rounded_box([keyboard_w, keyboard_h, wall+2], r=2);

        // Trackball hole
        translate([260, 50, -1])
            cylinder(h=wall+2, d=30);

        // LED holes
        for(i=[0:2])
            translate([15, 100+i*10, -1])
                cylinder(h=wall+2, d=4);

        // Corner mounting holes
        for(x=[10, case_width-10])
            for(y=[10, case_depth-10])
                translate([x, y, -1])
                    mounting_hole();

        // Vent slots
        for(i=[0:5])
            translate([5, 30+i*5, -1])
                cube([30, 2, wall+2]);
    }
}

module bottom_panel() {
    difference() {
        // Main panel
        rounded_box([case_width, case_depth, wall]);

        // Battery access
        translate([40, 100, -1])
            rounded_box([80, 60, wall+2], r=2);

        // Ventilation grid
        for(x=[150:10:190])
            for(y=[30:10:60])
                translate([x, y, -1])
                    cylinder(h=wall+2, d=3);

        // Corner mounting holes
        for(x=[10, case_width-10])
            for(y=[10, case_depth-10])
                translate([x, y, -1])
                    mounting_hole();

        // Rubber feet holes
        for(x=[20, case_width-20])
            for(y=[20, case_depth-20])
                translate([x, y, -1])
                    cylinder(h=wall+2, d=4);
    }
}

module left_side() {
    difference() {
        // Main panel
        rounded_box([wall, case_depth, case_height], r=2);

        // USB ports
        for(i=[0:2])
            translate([0, 50, 20+i*17])
                rotate([0, 90, 0])
                    usb_port();

        // Antenna hole
        translate([0, 150, 40])
            rotate([0, 90, 0])
                cylinder(h=wall*2, d=6, center=true);
    }
}

module right_side() {
    difference() {
        // Main panel
        rounded_box([wall, case_depth, case_height], r=2);

        // Ethernet port
        translate([0, 50, 40])
            rotate([0, 90, 0])
                ethernet_port();

        // Power switch
        translate([0, 120, 50])
            rotate([0, 90, 0])
                cube([15, 10, wall*2], center=true);

        // HDMI
        translate([0, 160, 35])
            rotate([0, 90, 0])
                cube([15, 6, wall*2], center=true);
    }
}

module front_panel() {
    rounded_box([case_width, wall, case_height], r=2);
}

module back_panel() {
    difference() {
        // Main panel
        rounded_box([case_width, wall, case_height], r=2);

        // Fan mounts
        for(x=[80, 220])
            translate([x, 0, 40])
                rotate([90, 0, 0])
                    fan_mount();
    }
}

module pi_mount() {
    difference() {
        // Mount plate
        rounded_box([pi_w, pi_h, 2], r=2);

        // Pi mounting holes (standard Pi layout)
        holes = [[3.5, 3.5], [61.5, 3.5], [3.5, 52.5], [61.5, 52.5]];
        for(h=holes)
            translate([h[0], h[1], -1])
                cylinder(h=4, d=2.8);
    }
}

module battery_holder() {
    difference() {
        rounded_box([90, 70, 30], r=3);
        translate([wall, wall, wall])
            rounded_box([90-wall*2, 70-wall*2, 35], r=2);
    }
}

// Display assembly position
module display_assembly() {
    color("DarkSlateGray")
        translate([display_x+5, display_y+5, wall+1])
            cube([display_w-10, display_h-10, 3]);
}

// Complete assembly
module complete_case() {
    // Top panel
    color("SteelBlue", 0.8)
        translate([0, 0, case_height-wall])
            top_panel();

    // Bottom panel
    color("SteelBlue", 0.8)
        bottom_panel();

    // Sides
    color("SteelBlue", 0.9) {
        translate([0, 0, 0])
            left_side();

        translate([case_width-wall, 0, 0])
            right_side();

        translate([0, 0, 0])
            front_panel();

        translate([0, case_depth-wall, 0])
            back_panel();
    }

    // Internal components
    color("Green", 0.7)
        translate([20, 20, 5])
            pi_mount();

    color("Yellow", 0.5)
        translate([150, 100, 5])
            battery_holder();

    // Display representation
    display_assembly();
}

// Individual part rendering
// Uncomment the part you want to export as STL

complete_case(); // Full assembly view

// For exporting individual parts, comment above and uncomment one:
// top_panel();
// bottom_panel();
// left_side();
// right_side();
// front_panel();
// back_panel();
// pi_mount();
// battery_holder();
