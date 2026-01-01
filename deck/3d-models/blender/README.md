# Neilerdeck Blender 3D Models

## Overview
This directory contains Blender Python scripts for generating the Neilerdeck case components procedurally.

## Scripts

### case_generator.py
Complete case generator with all panels and features:
- Top panel with display and keyboard cutouts
- Bottom panel with battery compartment
- Side panels with port cutouts
- Internal mounting structures
- Cable management
- Ventilation grilles
- Assembly features

**Usage:**
```bash
blender --background --python case_generator.py
# Or open Blender and run in scripting console
```

### keyboard_mount.py
Generates a custom mechanical keyboard mounting plate:
- 60% keyboard layout
- Cherry MX switch cutouts
- Stabilizer holes for large keys
- Mounting screw holes

**Usage:**
```bash
blender --background --python keyboard_mount.py
```

## Blender Requirements
- Blender 3.0 or newer
- Python 3.10+ (included with Blender)

## Customization

### Case Dimensions
Edit these variables in `case_generator.py`:
```python
CASE_WIDTH = 300        # Total width in mm
CASE_DEPTH = 200        # Total depth in mm
CASE_HEIGHT = 80        # Total height in mm
WALL_THICKNESS = 3      # Wall thickness
CORNER_RADIUS = 5       # Corner rounding
```

### Display Size
Adjust display cutout:
```python
DISPLAY_WIDTH = 195     # Your display width
DISPLAY_HEIGHT = 110    # Your display height
DISPLAY_OFFSET_X = 50   # Position from left
DISPLAY_OFFSET_Y = 15   # Position from top
```

### Keyboard Layout
Modify the `LAYOUT` array in `keyboard_mount.py` for different keyboard layouts.

## Export Settings

### For 3D Printing (STL)
1. Run the script in Blender
2. Select the object to export
3. File → Export → STL
4. Settings:
   - Scale: 1.0
   - ASCII: No
   - Apply Modifiers: Yes

### For CNC (STEP)
1. File → Export → STEP
2. Use for CAM programming

## Workflow

### 1. Generate Models
```bash
# Generate all case parts
blender --background --python case_generator.py --render-output /tmp/case
```

### 2. Inspect in Blender
Open Blender GUI and run script to inspect:
- Check dimensions
- Verify hole placements
- Test fit with components

### 3. Export Individual Parts
Select each part and export separately:
- top_panel.stl
- bottom_panel.stl
- left_panel.stl
- right_panel.stl
- internal_mounts.stl

### 4. Slice for Printing
Import STL files into your slicer:
- Cura
- PrusaSlicer
- Simplify3D

## Recommended Print Settings

```
Material: PETG or ABS
Layer Height: 0.2mm
Infill: 20%
Wall Count: 3 (for strength)
Supports: Yes (for overhangs)
Adhesion: Brim recommended
Print Temperature: 230-250°C (PETG)
Bed Temperature: 70-80°C
```

## Modifications

### Adding New Ports
In `case_generator.py`, add new cutouts in `create_side_panels()`:
```python
bpy.ops.mesh.primitive_cube_add(size=1)
new_port = bpy.context.active_object
new_port.scale = (thickness, width/2, height/2)
new_port.location = (x, y, z)

bool_mod = panel.modifiers.new(name="NewPort", type='BOOLEAN')
bool_mod.operation = 'DIFFERENCE'
bool_mod.object = new_port
```

### Adjusting Mounting Points
Modify `create_internal_mounts()` to match your component dimensions.

## Tips

1. **Test Print Small Parts First**: Print a corner section to verify dimensions
2. **Use Heat-Set Inserts**: Better than tapping plastic threads
3. **Print Orientation**: Top/bottom panels flat on bed for best quality
4. **Ventilation**: Don't block fan grilles
5. **Tolerances**: Add 0.2-0.5mm clearance for tight-fitting parts

## Troubleshooting

### Boolean Operations Fail
- Ensure manifold geometry (no holes in mesh)
- Check for overlapping faces
- Try "Recalculate Normals" (Alt+N)

### Parts Don't Fit
- Verify printer calibration
- Check scaling (should be 1:1)
- Add tolerances in script

### Warping During Print
- Use heated bed
- Add brim or raft
- Reduce print speed
- Use enclosure

## Advanced Features

### Parametric Design
All dimensions are variables - easy to resize entire case:
```python
SCALE_FACTOR = 1.1  # Make 10% larger
CASE_WIDTH *= SCALE_FACTOR
CASE_DEPTH *= SCALE_FACTOR
```

### Adding Text/Logos
Use Blender's text object and convert to mesh:
```python
bpy.ops.object.text_add()
text_obj = bpy.context.active_object
text_obj.data.body = "NEILERDECK"
bpy.ops.object.convert(target='MESH')
```

### Custom Textures
For rendering previews:
```python
mat = bpy.data.materials.new(name="CaseMaterial")
mat.use_nodes = True
bsdf = mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs['Base Color'].default_value = (0, 1, 0, 1)  # Green
```

## Resources

- [Blender Python API](https://docs.blender.org/api/current/)
- [BMesh Module](https://docs.blender.org/api/current/bmesh.html)
- [Boolean Modifiers](https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/booleans.html)

## Files Generated

After running scripts, you'll have:
- Blender project file (.blend)
- STL files for 3D printing
- Optional: Renders for documentation

Total print time: ~24-36 hours
Total material: ~800g filament
