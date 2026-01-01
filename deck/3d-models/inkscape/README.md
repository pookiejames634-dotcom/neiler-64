# Neilerdeck Inkscape Graphics & Markup

## Overview
This directory contains SVG files for graphics, labels, decals, and laser cutting templates.

## Files

### case_graphics.svg
Main case graphics and decorations:
- Neilerdeck logo and branding
- Status indicator labels
- Port labels
- Decorative elements (circuit traces, grid patterns)
- QR code placeholder
- Battery indicator graphic
- Kill switch labels
- Corner brackets

**Usage**: Print or laser engrave onto case

### labels_and_decals.svg
Printable labels sheet (A4 size):
- Port labels (USB, Ethernet, HDMI, Audio)
- Status LED indicators
- Warning labels
- Icon set for engraving
- Large logo decal

**Usage**: Print on vinyl or label paper, cut and apply

### laser_cutting_template.svg
Complete laser cutting template (600x400mm):
- Top panel with display and keyboard cutouts
- Bottom panel with battery access
- Left/right side panels with ports
- Internal mounting plates
- Fan grilles
- All cutting and engraving paths

**Usage**: Import into laser cutter software (Lightburn, RDWorks)

## Working with Inkscape

### Installation
```bash
# Linux
sudo apt install inkscape

# macOS
brew install --cask inkscape

# Or download from inkscape.org
```

### Opening Files
```bash
inkscape case_graphics.svg
```

## Customization

### Changing Text
1. Select text with text tool (T)
2. Edit content
3. Change font in text menu (Text → Font)

### Colors
Colors have specific meanings:
- **Red (#ff0000)**: Cut lines for laser
- **Blue (#0000ff)**: Engrave lines
- **Black (#000000)**: Raster engraving
- **Green (#00ff00)**: Decorative (print/paint)

### Logo Customization
Edit the logo in `case_graphics.svg`:
```xml
<text class="cyberdeck-text" x="0" y="0">YOUR_NAME</text>
```

### Adding QR Code
1. Generate QR code online (qr-code-generator.com)
2. Download as SVG
3. Import into Inkscape
4. Replace placeholder in graphics file

## Laser Cutting Guide

### Material Settings
For 3mm acrylic:
```
Cut (Red lines):
- Power: 80-100%
- Speed: 8-10 mm/s
- Passes: 1

Engrave (Blue lines):
- Power: 20-30%
- Speed: 300 mm/s
- Passes: 1

Raster (Black areas):
- Power: 15-25%
- Speed: 400 mm/s
- DPI: 300
```

### Preparing for Laser
1. Open `laser_cutting_template.svg` in Inkscape
2. Check document size (File → Document Properties)
3. Export → Save As → DXF or keep as SVG
4. Import into laser software
5. Assign colors to operations:
   - Red → Cut
   - Blue → Engrave
   - Black → Raster

### Test Cuts
Always run a small test:
1. Cut a small corner section first
2. Verify dimensions with calipers
3. Test fit with actual components
4. Adjust power/speed if needed

## Vinyl Decals

### Printing Labels
1. Open `labels_and_decals.svg`
2. Print on vinyl label paper
3. Settings:
   - Paper: Vinyl or waterproof label stock
   - Quality: High (1200+ DPI)
   - Color: Full color or black/white

### Cutting
1. Use scissors or craft knife
2. Or use vinyl cutter (Cricut, Silhouette)
3. Weed excess material
4. Apply transfer tape

### Application
1. Clean surface with isopropyl alcohol
2. Position decal
3. Apply with squeegee
4. Remove transfer tape slowly

## Screen Printing

For professional look:
1. Export logo as high-res PNG (300+ DPI)
2. Print transparency
3. Create screen printing screen
4. Print with plastisol ink on case

## Paint/Powder Coating

Use SVG files as stencils:
1. Cut stencil from vinyl or mylar
2. Apply to case
3. Spray paint or powder coat
4. Remove stencil

## Advanced Techniques

### Multi-layer Graphics
Layer multiple materials:
1. Base layer: Laser engrave
2. Fill: Acrylic paint
3. Top layer: Clear coat

### LED Backlit Labels
1. Engrave text into translucent acrylic
2. Mount LED behind
3. Creates glowing effect

### Holographic Decals
Print on holographic vinyl for cyberpunk aesthetic

## Export Formats

### For Printing
```bash
# High-res PNG
inkscape --export-type=png --export-dpi=300 labels_and_decals.svg

# PDF (for print shop)
inkscape --export-type=pdf case_graphics.svg
```

### For Laser Cutting
```bash
# DXF (most laser cutters)
inkscape --export-type=dxf laser_cutting_template.svg

# Or keep as SVG (Lightburn supports SVG)
```

### For Vinyl Cutter
```bash
# Export as DXF or EPS
inkscape --export-type=eps labels_and_decals.svg
```

## Layer Management

SVG files are organized in layers:
- **Annotations**: Measurements and notes (hide before export)
- **Cut Lines**: Red lines for cutting
- **Engrave Lines**: Blue lines for engraving
- **Graphics**: Decorative elements
- **Text**: Labels and typography

Toggle layers: Object → Layers (Ctrl+Shift+L)

## Design Guidelines

### Typography
- Logo: Courier New Bold, 24pt
- Labels: Arial, 6-8pt
- Status: Monospace fonts for tech aesthetic

### Colors
Cyberpunk/hacker aesthetic:
- Primary: Matrix green (#00ff00)
- Accent: Electric blue (#00aaff)
- Warning: Yellow/red (#ffff00, #ff0000)
- Background: Black (#000000)

### Icon Style
- Simple outlines
- High contrast
- 1mm stroke width minimum
- No fine details (hard to engrave)

## Troubleshooting

### Lines Not Cutting Through
- Increase laser power 5-10%
- Decrease speed
- Add second pass
- Check material thickness

### Engraving Too Deep
- Reduce power
- Increase speed
- Check focus distance

### Raster Quality Poor
- Increase DPI
- Convert images to 1-bit (black/white)
- Check image resolution

### Inkscape Crashes
- Simplify complex paths (Path → Simplify)
- Reduce node count
- Split into multiple files

## File Sizes

- case_graphics.svg: ~50KB
- labels_and_decals.svg: ~80KB
- laser_cutting_template.svg: ~120KB

If files are large:
```bash
# Optimize SVG
scour -i input.svg -o output.svg --enable-viewboxing
```

## Resources

- [Inkscape Documentation](https://inkscape.org/doc/)
- [SVG Specification](https://www.w3.org/TR/SVG2/)
- [Laser Cutting Guide](https://www.festi.info/boxes.py/)
- [Free Cyberpunk Fonts](https://www.dafont.com/theme.php?cat=106)

## Inspiration

Design inspired by:
- Cyberdeck subreddit builds
- Ghost in the Shell aesthetics
- Retro-futuristic hardware
- Military equipment labels
- DIY electronics culture

## Tips

1. **Test Everything**: Print/cut small samples first
2. **Backup Files**: Keep copies of working versions
3. **Document Changes**: Note successful laser settings
4. **Material Matters**: Different acrylics respond differently
5. **Ventilation**: Always use proper ventilation when laser cutting

## Gallery

(Add photos of finished labels and laser-cut parts here)
