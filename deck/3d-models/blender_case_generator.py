#!/usr/bin/env python3
"""
Neilerdeck Blender Case Generator
Parametric 3D case design using Blender Python API

Usage:
    blender --background --python blender_case_generator.py
    or run from within Blender's scripting environment
"""

import bpy
import bmesh
from math import radians

# Case parameters (all dimensions in mm, converted to Blender units)
SCALE = 0.001  # mm to meters for Blender

class NeilerdeckCase:
    def __init__(self):
        # Main dimensions
        self.case_width = 300 * SCALE
        self.case_depth = 200 * SCALE
        self.case_height = 80 * SCALE
        self.wall_thickness = 3 * SCALE

        # Display specs
        self.display_width = 195 * SCALE
        self.display_height = 110 * SCALE
        self.display_offset_x = 50 * SCALE
        self.display_offset_y = 20 * SCALE

        # Keyboard area
        self.keyboard_width = 240 * SCALE
        self.keyboard_depth = 80 * SCALE
        self.keyboard_offset_y = 140 * SCALE

        # Component mounts
        self.pi_mount_size = [85 * SCALE, 56 * SCALE, 2 * SCALE]
        self.pi_mount_pos = [20 * SCALE, 20 * SCALE, 5 * SCALE]

        # Ports and cutouts
        self.usb_port_size = [15 * SCALE, 7 * SCALE]
        self.ethernet_port_size = [16 * SCALE, 14 * SCALE]
        self.hdmi_port_size = [15 * SCALE, 6 * SCALE]

        # Ventilation
        self.fan_diameter = 40 * SCALE
        self.vent_hole_size = 3 * SCALE

    def clear_scene(self):
        """Remove all objects from scene"""
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

    def create_rounded_box(self, name, size, location, radius=0.005):
        """Create a rounded box primitive"""
        bpy.ops.mesh.primitive_cube_add(size=1, location=location)
        obj = bpy.context.active_object
        obj.name = name
        obj.scale = size

        # Add bevel modifier for rounded edges
        bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
        bevel.width = radius
        bevel.segments = 4

        return obj

    def create_top_panel(self):
        """Generate top panel with display and keyboard cutouts"""
        panel = self.create_rounded_box(
            "TopPanel",
            [self.case_width/2, self.case_depth/2, self.wall_thickness/2],
            [0, 0, self.case_height/2]
        )

        # Create display cutout
        display_cut = self.create_rounded_box(
            "DisplayCutout",
            [self.display_width/2, self.display_height/2, self.wall_thickness],
            [self.display_offset_x, self.display_offset_y, self.case_height/2],
            radius=0.002
        )

        # Boolean difference for display
        mod = panel.modifiers.new(name="DisplayCut", type='BOOLEAN')
        mod.operation = 'DIFFERENCE'
        mod.object = display_cut
        display_cut.hide_viewport = True

        # Keyboard area cutout
        keyboard_cut = self.create_rounded_box(
            "KeyboardCutout",
            [self.keyboard_width/2, self.keyboard_depth/2, self.wall_thickness],
            [0, self.keyboard_offset_y, self.case_height/2],
            radius=0.002
        )

        mod = panel.modifiers.new(name="KeyboardCut", type='BOOLEAN')
        mod.operation = 'DIFFERENCE'
        mod.object = keyboard_cut
        keyboard_cut.hide_viewport = True

        # Add mounting holes (M3 screws)
        self.add_mounting_holes(panel, 4)

        return panel

    def create_bottom_panel(self):
        """Generate bottom panel with ventilation and battery access"""
        panel = self.create_rounded_box(
            "BottomPanel",
            [self.case_width/2, self.case_depth/2, self.wall_thickness/2],
            [0, 0, -self.case_height/2]
        )

        # Ventilation grid
        vent_array = self.create_ventilation_grid(
            20, 15,
            [0, 0, -self.case_height/2]
        )

        # Boolean for ventilation
        mod = panel.modifiers.new(name="Ventilation", type='BOOLEAN')
        mod.operation = 'DIFFERENCE'
        mod.object = vent_array
        vent_array.hide_viewport = True

        # Battery access panel cutout
        battery_access = self.create_rounded_box(
            "BatteryAccess",
            [80 * SCALE, 60 * SCALE, self.wall_thickness],
            [-80 * SCALE, -50 * SCALE, -self.case_height/2]
        )

        mod = panel.modifiers.new(name="BatteryAccess", type='BOOLEAN')
        mod.operation = 'DIFFERENCE'
        mod.object = battery_access
        battery_access.hide_viewport = True

        return panel

    def create_side_panels(self):
        """Generate side panels with port cutouts"""
        # Left side
        left_panel = self.create_rounded_box(
            "LeftSidePanel",
            [self.wall_thickness/2, self.case_depth/2, self.case_height/2],
            [-self.case_width/2, 0, 0]
        )

        # Add USB port cutouts
        usb_positions = [
            [-self.case_width/2, 50 * SCALE, 20 * SCALE],
            [-self.case_width/2, 50 * SCALE, 0],
            [-self.case_width/2, 50 * SCALE, -20 * SCALE],
        ]

        for i, pos in enumerate(usb_positions):
            usb_cut = self.create_rounded_box(
                f"USB_Port_{i}",
                [self.wall_thickness, self.usb_port_size[0]/2, self.usb_port_size[1]/2],
                pos,
                radius=0.001
            )
            mod = left_panel.modifiers.new(name=f"USB_{i}", type='BOOLEAN')
            mod.operation = 'DIFFERENCE'
            mod.object = usb_cut
            usb_cut.hide_viewport = True

        # Right side
        right_panel = self.create_rounded_box(
            "RightSidePanel",
            [self.wall_thickness/2, self.case_depth/2, self.case_height/2],
            [self.case_width/2, 0, 0]
        )

        # Ethernet port
        eth_cut = self.create_rounded_box(
            "EthernetPort",
            [self.wall_thickness, self.ethernet_port_size[0]/2, self.ethernet_port_size[1]/2],
            [self.case_width/2, 50 * SCALE, 0],
            radius=0.001
        )
        mod = right_panel.modifiers.new(name="Ethernet", type='BOOLEAN')
        mod.operation = 'DIFFERENCE'
        mod.object = eth_cut
        eth_cut.hide_viewport = True

        # Power switch cutout
        power_cut = self.create_rounded_box(
            "PowerSwitch",
            [self.wall_thickness, 15 * SCALE, 10 * SCALE],
            [self.case_width/2, -70 * SCALE, 10 * SCALE]
        )
        mod = right_panel.modifiers.new(name="PowerSwitch", type='BOOLEAN')
        mod.operation = 'DIFFERENCE'
        mod.object = power_cut
        power_cut.hide_viewport = True

        return left_panel, right_panel

    def create_front_back_panels(self):
        """Generate front and back panels"""
        # Front panel (keyboard side)
        front_panel = self.create_rounded_box(
            "FrontPanel",
            [self.case_width/2, self.wall_thickness/2, self.case_height/2],
            [0, self.case_depth/2, 0]
        )

        # Back panel with fan mounts
        back_panel = self.create_rounded_box(
            "BackPanel",
            [self.case_width/2, self.wall_thickness/2, self.case_height/2],
            [0, -self.case_depth/2, 0]
        )

        # Add fan cutouts
        fan_positions = [
            [-50 * SCALE, -self.case_depth/2, 0],
            [50 * SCALE, -self.case_depth/2, 0]
        ]

        for i, pos in enumerate(fan_positions):
            fan_cut = self.create_fan_cutout(f"Fan_{i}", pos)
            mod = back_panel.modifiers.new(name=f"Fan_{i}", type='BOOLEAN')
            mod.operation = 'DIFFERENCE'
            mod.object = fan_cut
            fan_cut.hide_viewport = True

        # HDMI port
        hdmi_cut = self.create_rounded_box(
            "HDMI_Port",
            [20 * SCALE, self.wall_thickness, self.hdmi_port_size[1]/2],
            [0, -self.case_depth/2, -15 * SCALE],
            radius=0.001
        )
        mod = back_panel.modifiers.new(name="HDMI", type='BOOLEAN')
        mod.operation = 'DIFFERENCE'
        mod.object = hdmi_cut
        hdmi_cut.hide_viewport = True

        return front_panel, back_panel

    def create_fan_cutout(self, name, position):
        """Create circular fan cutout with mounting holes"""
        bpy.ops.mesh.primitive_cylinder_add(
            radius=self.fan_diameter/2,
            depth=self.wall_thickness * 2,
            location=position
        )
        fan = bpy.context.active_object
        fan.name = name
        fan.rotation_euler = (0, radians(90), 0)

        return fan

    def create_ventilation_grid(self, rows, cols, position):
        """Create grid of ventilation holes"""
        spacing_x = 10 * SCALE
        spacing_y = 10 * SCALE

        bpy.ops.mesh.primitive_plane_add(location=position)
        grid = bpy.context.active_object
        grid.name = "VentilationGrid"

        # Use array modifiers for grid
        array_x = grid.modifiers.new(name="ArrayX", type='ARRAY')
        array_x.count = cols
        array_x.relative_offset_displace = (1.5, 0, 0)

        array_y = grid.modifiers.new(name="ArrayY", type='ARRAY')
        array_y.count = rows
        array_y.relative_offset_displace = (0, 1.5, 0)

        grid.scale = (self.vent_hole_size, self.vent_hole_size, 1)

        return grid

    def add_mounting_holes(self, obj, count=4):
        """Add mounting holes to corners"""
        hole_positions = [
            [130 * SCALE, 90 * SCALE],
            [-130 * SCALE, 90 * SCALE],
            [130 * SCALE, -90 * SCALE],
            [-130 * SCALE, -90 * SCALE]
        ]

        for i, (x, y) in enumerate(hole_positions[:count]):
            bpy.ops.mesh.primitive_cylinder_add(
                radius=1.5 * SCALE,  # M3 hole
                depth=self.wall_thickness * 2,
                location=[x, y, obj.location.z]
            )
            hole = bpy.context.active_object
            hole.name = f"MountingHole_{i}"

            mod = obj.modifiers.new(name=f"Hole_{i}", type='BOOLEAN')
            mod.operation = 'DIFFERENCE'
            mod.object = hole
            hole.hide_viewport = True

    def create_internal_mounts(self):
        """Create internal mounting plates for components"""
        # Pi mounting plate
        pi_mount = self.create_rounded_box(
            "PiMount",
            [self.pi_mount_size[0]/2, self.pi_mount_size[1]/2, self.pi_mount_size[2]/2],
            self.pi_mount_pos,
            radius=0.002
        )

        # Add Pi mounting holes (58mm x 49mm)
        pi_hole_positions = [
            [3.5 * SCALE, 3.5 * SCALE],
            [61.5 * SCALE, 3.5 * SCALE],
            [3.5 * SCALE, 52.5 * SCALE],
            [61.5 * SCALE, 52.5 * SCALE]
        ]

        for i, (x, y) in enumerate(pi_hole_positions):
            bpy.ops.mesh.primitive_cylinder_add(
                radius=1.5 * SCALE,
                depth=self.pi_mount_size[2] * 2,
                location=[
                    self.pi_mount_pos[0] + x - 32 * SCALE,
                    self.pi_mount_pos[1] + y - 28 * SCALE,
                    self.pi_mount_pos[2]
                ]
            )
            hole = bpy.context.active_object
            hole.name = f"PiHole_{i}"

            mod = pi_mount.modifiers.new(name=f"PiHole_{i}", type='BOOLEAN')
            mod.operation = 'DIFFERENCE'
            mod.object = hole
            hole.hide_viewport = True

        # Battery holder
        battery_holder = self.create_rounded_box(
            "BatteryHolder",
            [90 * SCALE, 70 * SCALE, 30 * SCALE],
            [-80 * SCALE, -50 * SCALE, -20 * SCALE]
        )

        return pi_mount, battery_holder

    def generate_complete_case(self):
        """Generate all case components"""
        print("Generating Neilerdeck case...")

        self.clear_scene()

        # Create all panels
        top = self.create_top_panel()
        bottom = self.create_bottom_panel()
        left, right = self.create_side_panels()
        front, back = self.create_front_back_panels()

        # Create internal mounts
        pi_mount, battery = self.create_internal_mounts()

        # Add collection for organization
        collection = bpy.data.collections.new("Neilerdeck_Case")
        bpy.context.scene.collection.children.link(collection)

        # Move objects to collection
        for obj in [top, bottom, left, right, front, back, pi_mount, battery]:
            if obj.name in bpy.context.scene.collection.objects:
                bpy.context.scene.collection.objects.unlink(obj)
            collection.objects.link(obj)

        print("Case generation complete!")
        print("Top panel: Export as top_panel.stl")
        print("Bottom panel: Export as bottom_panel.stl")
        print("Apply all modifiers before exporting")

    def export_stl_files(self, output_dir="/home/neil/neilerdeck/3d-models/stl/"):
        """Export all parts as STL files"""
        import os
        os.makedirs(output_dir, exist_ok=True)

        parts = {
            "TopPanel": "top_panel.stl",
            "BottomPanel": "bottom_panel.stl",
            "LeftSidePanel": "left_side.stl",
            "RightSidePanel": "right_side.stl",
            "FrontPanel": "front_panel.stl",
            "BackPanel": "back_panel.stl",
            "PiMount": "pi_mount.stl",
            "BatteryHolder": "battery_holder.stl"
        }

        for obj_name, filename in parts.items():
            if obj_name in bpy.data.objects:
                obj = bpy.data.objects[obj_name]
                bpy.ops.object.select_all(action='DESELECT')
                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj

                # Apply modifiers
                for mod in obj.modifiers:
                    bpy.ops.object.modifier_apply(modifier=mod.name)

                filepath = os.path.join(output_dir, filename)
                bpy.ops.export_mesh.stl(
                    filepath=filepath,
                    use_selection=True
                )
                print(f"Exported: {filepath}")

# Main execution
if __name__ == "__main__":
    generator = NeilerdeckCase()
    generator.generate_complete_case()

    # Uncomment to auto-export STL files
    # generator.export_stl_files()
