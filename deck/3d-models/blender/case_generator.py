#!/usr/bin/env python3
"""
Neilerdeck Case Generator - Blender Script
Run this in Blender's scripting console to generate the cyberdeck case
Usage: blender --python case_generator.py
"""

import bpy
import bmesh
from math import radians

# Clear existing mesh objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Case dimensions (mm)
CASE_WIDTH = 300
CASE_DEPTH = 200
CASE_HEIGHT = 80
WALL_THICKNESS = 3
CORNER_RADIUS = 5

# Display cutout dimensions
DISPLAY_WIDTH = 195
DISPLAY_HEIGHT = 110
DISPLAY_OFFSET_X = 50
DISPLAY_OFFSET_Y = 15

# Keyboard area
KEYBOARD_WIDTH = 240
KEYBOARD_HEIGHT = 100
KEYBOARD_OFFSET_X = 30
KEYBOARD_OFFSET_Y = 130

def create_rounded_box(name, width, depth, height, radius):
    """Create a box with rounded corners"""
    bpy.ops.mesh.primitive_cube_add(size=1)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (width/2, depth/2, height/2)
    bpy.ops.object.transform_apply(scale=True)

    # Add bevel modifier for rounded edges
    bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel.width = radius
    bevel.segments = 4
    bevel.limit_method = 'ANGLE'

    return obj

def create_top_panel():
    """Create the top panel with display and keyboard cutouts"""
    print("Creating top panel...")

    # Main panel
    top = create_rounded_box("TopPanel", CASE_WIDTH, CASE_DEPTH, WALL_THICKNESS, CORNER_RADIUS)
    top.location = (0, 0, CASE_HEIGHT/2)

    # Display cutout
    bpy.ops.mesh.primitive_cube_add(size=1)
    display_cutout = bpy.context.active_object
    display_cutout.name = "DisplayCutout"
    display_cutout.scale = (DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2, WALL_THICKNESS)
    display_cutout.location = (
        DISPLAY_OFFSET_X - CASE_WIDTH/2 + DISPLAY_WIDTH/2,
        CASE_DEPTH/2 - DISPLAY_OFFSET_Y - DISPLAY_HEIGHT/2,
        CASE_HEIGHT/2
    )

    # Boolean modifier to cut display hole
    bool_mod = top.modifiers.new(name="DisplayCut", type='BOOLEAN')
    bool_mod.operation = 'DIFFERENCE'
    bool_mod.object = display_cutout

    # Keyboard cutout
    bpy.ops.mesh.primitive_cube_add(size=1)
    kb_cutout = bpy.context.active_object
    kb_cutout.name = "KeyboardCutout"
    kb_cutout.scale = (KEYBOARD_WIDTH/2, KEYBOARD_HEIGHT/2, WALL_THICKNESS)
    kb_cutout.location = (
        KEYBOARD_OFFSET_X - CASE_WIDTH/2 + KEYBOARD_WIDTH/2,
        -CASE_DEPTH/2 + KEYBOARD_OFFSET_Y + KEYBOARD_HEIGHT/2,
        CASE_HEIGHT/2
    )

    bool_mod2 = top.modifiers.new(name="KeyboardCut", type='BOOLEAN')
    bool_mod2.operation = 'DIFFERENCE'
    bool_mod2.object = kb_cutout

    # Add ventilation grilles
    create_vent_grilles(top, CASE_WIDTH - 50, -CASE_DEPTH/2 + 20, CASE_HEIGHT/2)

    return top

def create_vent_grilles(parent, x, y, z):
    """Create ventilation grilles"""
    for i in range(10):
        bpy.ops.mesh.primitive_cube_add(size=1)
        vent = bpy.context.active_object
        vent.name = f"Vent_{i}"
        vent.scale = (2, 15, WALL_THICKNESS)
        vent.location = (x + i*5 - 25, y, z)

        # Boolean to cut vent
        bool_mod = parent.modifiers.new(name=f"VentCut_{i}", type='BOOLEAN')
        bool_mod.operation = 'DIFFERENCE'
        bool_mod.object = vent

def create_bottom_panel():
    """Create the bottom panel with battery compartment"""
    print("Creating bottom panel...")

    bottom = create_rounded_box("BottomPanel", CASE_WIDTH, CASE_DEPTH, WALL_THICKNESS, CORNER_RADIUS)
    bottom.location = (0, 0, -CASE_HEIGHT/2)

    # Battery compartment (raised area)
    bpy.ops.mesh.primitive_cube_add(size=1)
    battery_comp = bpy.context.active_object
    battery_comp.name = "BatteryCompartment"
    battery_comp.scale = (150/2, 80/2, 5/2)
    battery_comp.location = (0, -30, -CASE_HEIGHT/2 + 5/2)

    # Add rubber feet mounting holes
    for x_pos in [-130, 130]:
        for y_pos in [-80, 80]:
            bpy.ops.mesh.primitive_cylinder_add(radius=3, depth=WALL_THICKNESS*2)
            foot_hole = bpy.context.active_object
            foot_hole.name = f"FootHole_{x_pos}_{y_pos}"
            foot_hole.location = (x_pos, y_pos, -CASE_HEIGHT/2)

            bool_mod = bottom.modifiers.new(name=f"FootCut_{x_pos}_{y_pos}", type='BOOLEAN')
            bool_mod.operation = 'DIFFERENCE'
            bool_mod.object = foot_hole

    return bottom

def create_side_panels():
    """Create left and right side panels with port cutouts"""
    print("Creating side panels...")

    # Left panel
    left = create_rounded_box("LeftPanel", WALL_THICKNESS, CASE_DEPTH, CASE_HEIGHT, CORNER_RADIUS)
    left.location = (-CASE_WIDTH/2, 0, 0)

    # USB port cutouts on left
    usb_positions = [(0, 50, 10), (0, 50, 25), (0, 50, 40)]
    for idx, (x, y, z) in enumerate(usb_positions):
        bpy.ops.mesh.primitive_cube_add(size=1)
        usb = bpy.context.active_object
        usb.name = f"USB_{idx}"
        usb.scale = (WALL_THICKNESS*2, 15/2, 8/2)
        usb.location = (-CASE_WIDTH/2, y, z)

        bool_mod = left.modifiers.new(name=f"USBCut_{idx}", type='BOOLEAN')
        bool_mod.operation = 'DIFFERENCE'
        bool_mod.object = usb

    # Right panel
    right = create_rounded_box("RightPanel", WALL_THICKNESS, CASE_DEPTH, CASE_HEIGHT, CORNER_RADIUS)
    right.location = (CASE_WIDTH/2, 0, 0)

    # Ethernet port
    bpy.ops.mesh.primitive_cube_add(size=1)
    ethernet = bpy.context.active_object
    ethernet.name = "EthernetPort"
    ethernet.scale = (WALL_THICKNESS*2, 16/2, 14/2)
    ethernet.location = (CASE_WIDTH/2, 50, 15)

    bool_mod = right.modifiers.new(name="EthernetCut", type='BOOLEAN')
    bool_mod.operation = 'DIFFERENCE'
    bool_mod.object = ethernet

    # HDMI port
    bpy.ops.mesh.primitive_cube_add(size=1)
    hdmi = bpy.context.active_object
    hdmi.name = "HDMIPort"
    hdmi.scale = (WALL_THICKNESS*2, 15/2, 6/2)
    hdmi.location = (CASE_WIDTH/2, 30, 15)

    bool_mod = right.modifiers.new(name="HDMICut", type='BOOLEAN')
    bool_mod.operation = 'DIFFERENCE'
    bool_mod.object = hdmi

    # Power switch
    bpy.ops.mesh.primitive_cylinder_add(radius=8, depth=WALL_THICKNESS*2)
    power_switch = bpy.context.active_object
    power_switch.name = "PowerSwitch"
    power_switch.rotation_euler = (0, radians(90), 0)
    power_switch.location = (CASE_WIDTH/2, -70, 30)

    bool_mod = right.modifiers.new(name="PowerSwitchCut", type='BOOLEAN')
    bool_mod.operation = 'DIFFERENCE'
    bool_mod.object = power_switch

    return left, right

def create_internal_mounts():
    """Create mounting points for internal components"""
    print("Creating internal mounts...")

    # Pi mounting plate
    bpy.ops.mesh.primitive_cube_add(size=1)
    pi_mount = bpy.context.active_object
    pi_mount.name = "PiMount"
    pi_mount.scale = (85/2, 56/2, 2/2)
    pi_mount.location = (-50, 40, -20)

    # Add mounting holes to Pi plate
    for x in [-58/2, 58/2]:
        for y in [-49/2, 49/2]:
            bpy.ops.mesh.primitive_cylinder_add(radius=1.5, depth=4)
            hole = bpy.context.active_object
            hole.name = f"PiHole_{x}_{y}"
            hole.location = (-50 + x, 40 + y, -20)

            bool_mod = pi_mount.modifiers.new(name=f"PiHoleCut_{x}_{y}", type='BOOLEAN')
            bool_mod.operation = 'DIFFERENCE'
            bool_mod.object = hole

    # Standoffs for display
    for x in [-DISPLAY_WIDTH/2 + 10, DISPLAY_WIDTH/2 - 10]:
        for y in [-DISPLAY_HEIGHT/2 + 10, DISPLAY_HEIGHT/2 - 10]:
            bpy.ops.mesh.primitive_cylinder_add(radius=3, depth=8)
            standoff = bpy.context.active_object
            standoff.name = f"DisplayStandoff_{x}_{y}"
            standoff.location = (
                DISPLAY_OFFSET_X - CASE_WIDTH/2 + DISPLAY_WIDTH/2 + x,
                CASE_DEPTH/2 - DISPLAY_OFFSET_Y - DISPLAY_HEIGHT/2 + y,
                CASE_HEIGHT/2 - 8/2
            )

            # Add screw hole
            bpy.ops.mesh.primitive_cylinder_add(radius=1.5, depth=10)
            screw_hole = bpy.context.active_object
            screw_hole.location = standoff.location

            bool_mod = standoff.modifiers.new(name=f"ScrewHole_{x}_{y}", type='BOOLEAN')
            bool_mod.operation = 'DIFFERENCE'
            bool_mod.object = screw_hole

    # Fan mounts (40mm fans)
    for x_pos in [-60, 60]:
        bpy.ops.mesh.primitive_cube_add(size=1)
        fan_mount = bpy.context.active_object
        fan_mount.name = f"FanMount_{x_pos}"
        fan_mount.scale = (45/2, 45/2, 2/2)
        fan_mount.location = (x_pos, -CASE_DEPTH/2 + 30, -CASE_HEIGHT/2 + 10)

        # Fan screw holes
        for fx in [-16, 16]:
            for fy in [-16, 16]:
                bpy.ops.mesh.primitive_cylinder_add(radius=2, depth=4)
                fan_hole = bpy.context.active_object
                fan_hole.location = (x_pos + fx, -CASE_DEPTH/2 + 30 + fy, -CASE_HEIGHT/2 + 10)

                bool_mod = fan_mount.modifiers.new(name=f"FanHole_{x_pos}_{fx}_{fy}", type='BOOLEAN')
                bool_mod.operation = 'DIFFERENCE'
                bool_mod.object = fan_hole

def add_assembly_features():
    """Add features for assembly like screw posts and clips"""
    print("Adding assembly features...")

    # Corner posts for screws
    positions = [
        (-CASE_WIDTH/2 + 10, -CASE_DEPTH/2 + 10),
        (CASE_WIDTH/2 - 10, -CASE_DEPTH/2 + 10),
        (-CASE_WIDTH/2 + 10, CASE_DEPTH/2 - 10),
        (CASE_WIDTH/2 - 10, CASE_DEPTH/2 - 10)
    ]

    for idx, (x, y) in enumerate(positions):
        bpy.ops.mesh.primitive_cylinder_add(radius=4, depth=CASE_HEIGHT - WALL_THICKNESS*2)
        post = bpy.context.active_object
        post.name = f"CornerPost_{idx}"
        post.location = (x, y, 0)

        # Screw hole through post
        bpy.ops.mesh.primitive_cylinder_add(radius=1.5, depth=CASE_HEIGHT)
        hole = bpy.context.active_object
        hole.location = (x, y, 0)

        bool_mod = post.modifiers.new(name=f"PostHole_{idx}", type='BOOLEAN')
        bool_mod.operation = 'DIFFERENCE'
        bool_mod.object = hole

def create_cable_management():
    """Create cable routing channels and clips"""
    print("Creating cable management...")

    # Cable channel along bottom
    bpy.ops.mesh.primitive_cube_add(size=1)
    channel = bpy.context.active_object
    channel.name = "CableChannel"
    channel.scale = (250/2, 10/2, 8/2)
    channel.location = (0, -CASE_DEPTH/2 + 15, -CASE_HEIGHT/2 + 8)

    # Cable clips (small hooks)
    for i in range(5):
        bpy.ops.mesh.primitive_torus_add(
            major_radius=3,
            minor_radius=1,
            major_segments=16,
            minor_segments=8
        )
        clip = bpy.context.active_object
        clip.name = f"CableClip_{i}"
        clip.rotation_euler = (radians(90), 0, 0)
        clip.location = (-100 + i*50, -CASE_DEPTH/2 + 15, -CASE_HEIGHT/2 + 15)
        clip.scale = (1, 1, 0.5)

def main():
    """Main function to generate the complete case"""
    print("=" * 50)
    print("Neilerdeck Case Generator")
    print("=" * 50)

    # Create all components
    top_panel = create_top_panel()
    bottom_panel = create_bottom_panel()
    left_panel, right_panel = create_side_panels()
    create_internal_mounts()
    add_assembly_features()
    create_cable_management()

    # Apply all boolean modifiers
    print("Applying modifiers...")
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            bpy.context.view_layer.objects.active = obj
            for mod in obj.modifiers:
                if mod.type == 'BOOLEAN':
                    try:
                        bpy.ops.object.modifier_apply(modifier=mod.name)
                    except:
                        print(f"Could not apply modifier {mod.name} on {obj.name}")

    # Clean up boolean objects
    for obj in bpy.data.objects:
        if 'Cutout' in obj.name or 'Hole' in obj.name or 'Port' in obj.name or 'Switch' in obj.name:
            bpy.data.objects.remove(obj, do_unlink=True)

    # Set viewport shading
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'SOLID'

    # Frame all objects
    bpy.ops.view3d.view_all()

    print("=" * 50)
    print("Case generation complete!")
    print("Export as STL: File > Export > STL")
    print("=" * 50)

if __name__ == "__main__":
    main()
