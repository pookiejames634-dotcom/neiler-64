# Neilerdeck 3D Models & Designs

## Case Design

### Main Enclosure
- Dimensions: 300mm x 200mm x 80mm
- Material: PETG (recommended) or ABS
- Print Settings:
  - Layer height: 0.2mm
  - Infill: 20%
  - Supports: Yes
  - Print time: ~24 hours

### Components to Design

#### Top Panel
- Keyboard mounting holes
- Display cutout (adjust for your screen size)
- Trackball mount
- Ventilation grilles

#### Bottom Panel
- Battery compartment
- Rubber feet mounting points
- Access panel for components
- Cable routing channels

#### Side Panels
- USB port cutouts
- Ethernet port
- Power switch
- Antenna holes for WiFi adapter

#### Internal Mounts
- Pi 5 mounting plate
- SSD mount
- Battery holder with straps
- Fan mounts (40mm x2)
- Cable management clips

## OpenSCAD Design (Parametric)

```openscad
// Neilerdeck Case Parameters
case_width = 300;
case_depth = 200;
case_height = 80;
wall_thickness = 3;

// Display cutout
display_width = 195;
display_height = 110;

// Generate case
difference() {
    cube([case_width, case_depth, case_height]);
    translate([wall_thickness, wall_thickness, wall_thickness])
        cube([case_width-2*wall_thickness,
              case_depth-2*wall_thickness,
              case_height]);
}
```

## FreeCAD Files
Store .FCStd files in this directory

## STL Files
Export STL files here for printing:
- top_panel.stl
- bottom_panel.stl
- side_left.stl
- side_right.stl
- pi_mount.stl
- battery_holder.stl

## Laser Cutting Files
DXF files for acrylic case alternative

## Assembly Notes
1. Print all parts in PETG for durability
2. Use M3 heat-set inserts for assembly
3. Sand mating surfaces for better fit
4. Test fit before final assembly
