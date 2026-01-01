#!/usr/bin/env python3
"""
Neilerdeck Keyboard Mount Generator
Creates a custom mechanical keyboard mounting plate
"""

import bpy
import bmesh
from math import radians

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Keyboard layout (60% layout)
KEY_UNIT = 19.05  # 1U key spacing in mm
PLATE_THICKNESS = 1.5
SWITCH_HOLE_SIZE = 14  # Cherry MX switch cutout

# Define key layout (60% keyboard)
LAYOUT = [
    # Row 1 (numbers)
    [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0), (11, 0), (12, 0), (13, 0)],
    # Row 2 (QWERTY)
    [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1), (11, 1), (12, 1), (13, 1)],
    # Row 3 (ASDF)
    [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (10, 2), (11, 2), (12.5, 2)],
    # Row 4 (ZXCV)
    [(0, 3), (1.5, 3), (2.5, 3), (3.5, 3), (4.5, 3), (5.5, 3), (6.5, 3), (7.5, 3), (8.5, 3), (9.5, 3), (10.5, 3), (11.5, 3), (13, 3)],
    # Row 5 (bottom)
    [(0, 4), (1.25, 4), (2.5, 4), (7, 4), (11.5, 4), (12.5, 4), (13.5, 4)]
]

def create_switch_hole(x, y):
    """Create a Cherry MX switch cutout"""
    bpy.ops.mesh.primitive_cube_add(size=SWITCH_HOLE_SIZE)
    hole = bpy.context.active_object
    hole.location = (x * KEY_UNIT, y * KEY_UNIT, 0)
    hole.scale = (1, 1, PLATE_THICKNESS * 2)
    return hole

def create_stabilizer_holes(x, y, key_size=2):
    """Create stabilizer cutouts for larger keys"""
    stab_offset = (key_size * KEY_UNIT - SWITCH_HOLE_SIZE) / 2 - 12

    holes = []
    for offset in [-stab_offset, stab_offset]:
        bpy.ops.mesh.primitive_cube_add(size=1)
        hole = bpy.context.active_object
        hole.scale = (3.5, 6.5, PLATE_THICKNESS * 2)
        hole.location = (x * KEY_UNIT + offset, y * KEY_UNIT, 0)
        holes.append(hole)

    return holes

def create_mounting_holes(plate_width, plate_height):
    """Create screw holes for mounting the plate"""
    margin = 10
    positions = [
        (margin, margin),
        (plate_width - margin, margin),
        (margin, plate_height - margin),
        (plate_width - margin, plate_height - margin),
        (plate_width/2, margin),
        (plate_width/2, plate_height - margin)
    ]

    holes = []
    for x, y in positions:
        bpy.ops.mesh.primitive_cylinder_add(radius=2, depth=PLATE_THICKNESS * 2)
        hole = bpy.context.active_object
        hole.location = (x - plate_width/2, y - plate_height/2, 0)
        holes.append(hole)

    return holes

def main():
    """Generate keyboard mounting plate"""
    print("Generating keyboard mounting plate...")

    # Calculate plate dimensions
    max_x = max([max([pos[0] for pos in row]) for row in LAYOUT])
    max_y = len(LAYOUT) - 1

    plate_width = (max_x + 1.5) * KEY_UNIT
    plate_height = (max_y + 1.5) * KEY_UNIT

    # Create base plate
    bpy.ops.mesh.primitive_cube_add(size=1)
    plate = bpy.context.active_object
    plate.name = "KeyboardPlate"
    plate.scale = (plate_width/2, plate_height/2, PLATE_THICKNESS/2)

    # Add rounded corners
    bevel = plate.modifiers.new(name="Bevel", type='BEVEL')
    bevel.width = 3
    bevel.segments = 4

    # Create switch holes
    all_holes = []
    for row in LAYOUT:
        for x, y in row:
            hole = create_switch_hole(x - max_x/2, y - max_y/2)
            all_holes.append(hole)

    # Add stabilizer holes for spacebar (assume 6.25U)
    stab_holes = create_stabilizer_holes(7 - max_x/2, 4 - max_y/2, 6.25)
    all_holes.extend(stab_holes)

    # Add mounting holes
    mount_holes = create_mounting_holes(plate_width, plate_height)
    all_holes.extend(mount_holes)

    # Boolean operations to cut holes
    for idx, hole in enumerate(all_holes):
        bool_mod = plate.modifiers.new(name=f"Cut_{idx}", type='BOOLEAN')
        bool_mod.operation = 'DIFFERENCE'
        bool_mod.object = hole

    # Apply modifiers
    bpy.context.view_layer.objects.active = plate
    for mod in plate.modifiers:
        try:
            bpy.ops.object.modifier_apply(modifier=mod.name)
        except:
            pass

    # Clean up boolean objects
    for hole in all_holes:
        bpy.data.objects.remove(hole, do_unlink=True)

    print(f"Keyboard plate generated: {plate_width:.1f}mm x {plate_height:.1f}mm")
    print("Ready for export!")

if __name__ == "__main__":
    main()
