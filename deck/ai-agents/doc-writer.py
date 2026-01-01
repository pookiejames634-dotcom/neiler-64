#!/usr/bin/env python3
"""
Neilerdeck Documentation Writer Agent
Automatically generates and updates documentation
"""

import os
from datetime import datetime

class DocWriter:
    def __init__(self, project_root="/home/neil/neilerdeck"):
        self.root = project_root
        self.docs_dir = os.path.join(project_root, "docs")

    def generate_readme(self):
        """Generate main README.md"""
        readme = """# Neilerdeck

A custom cyberdeck built for security research, development, and portable computing.

![Neilerdeck](docs/images/neilerdeck-hero.jpg)

## Features

- **Portable**: Lightweight and rugged design
- **Powerful**: Raspberry Pi 5 with 8GB RAM
- **Versatile**: Built-in SDR, WiFi pentesting, 4G connectivity
- **Expandable**: Multiple USB ports, GPIO access, expansion slots
- **Long Battery Life**: 8+ hours of runtime

## Specifications

See [hardware/SPECS.md](hardware/SPECS.md) for full specifications.

## Build Guide

1. [Order Components](hardware/COMPONENTS.md)
2. [3D Print Enclosure](3d-models/README.md)
3. [Assemble Hardware](docs/ASSEMBLY.md)
4. [Install Software](software/OS-SETUP.md)
5. [Configure System](docs/CONFIGURATION.md)

## Quick Start

```bash
# Clone this repo
git clone https://github.com/yourusername/neilerdeck.git
cd neilerdeck

# Run setup script
chmod +x software/install.sh
sudo ./software/install.sh
```

## Project Structure

```
neilerdeck/
├── hardware/          # Hardware specs and component lists
├── software/          # OS configs and software setup
├── 3d-models/         # Case designs and STL files
├── ai-agents/         # Helper scripts and automation
├── docs/              # Documentation and guides
└── build-log/         # Build progress and notes
```

## AI Agents

This project includes helper AI agents:

- **component-researcher.py**: Find and compare components
- **config-generator.py**: Auto-generate system configs
- **doc-writer.py**: Maintain documentation

## Contributing

This is a personal project, but feel free to fork and adapt for your own cyberdeck!

## License

MIT License - See LICENSE file

## Credits

Built by Neil - {date}
""".format(date=datetime.now().year)

        return readme

    def generate_assembly_guide(self):
        """Generate assembly instructions"""
        guide = """# Neilerdeck Assembly Guide

## Tools Required

- Phillips screwdriver
- Hex key set
- Soldering iron (for some connections)
- Multimeter
- Wire strippers
- Heat gun (for heat-shrink tubing)

## Step 1: Prepare the Enclosure

1. Print all 3D parts (see 3d-models/)
2. Install heat-set inserts in mounting holes
3. Test fit all panels

## Step 2: Install the Raspberry Pi

1. Mount Pi 5 to mounting plate
2. Attach heatsink and active cooler
3. Connect NVMe SSD to bottom of Pi
4. Secure with M2.5 screws

## Step 3: Power System

1. Install PiSugar 3 or BMS
2. Connect LiPo battery (observe polarity!)
3. Wire power switch
4. Test voltage with multimeter (should be ~5V output)

## Step 4: Display

1. Mount display in top panel cutout
2. Connect HDMI cable to Pi
3. Connect display power
4. Secure with mounting screws

## Step 5: Input Devices

1. Install keyboard in mounting holes
2. Mount trackball module
3. Connect via USB to Pi

## Step 6: Connectivity

1. Install WiFi adapter in USB port
2. Mount 4G HAT on GPIO (if using)
3. Connect antennas
4. Secure cables with zip ties

## Step 7: Expansion

1. Install SDR dongle
2. Mount GPS module (if using)
3. Route cables cleanly

## Step 8: Final Assembly

1. Install cooling fans
2. Close all panels
3. Secure with screws
4. Apply rubber feet

## Step 9: First Boot

1. Insert microSD or boot from NVMe
2. Power on and check LEDs
3. Connect to display
4. Boot into OS

## Troubleshooting

- **No boot**: Check power connections
- **No display**: Verify HDMI connection
- **Overheating**: Check fan operation
- **WiFi issues**: Check adapter compatibility

## Safety Notes

- Always disconnect battery before working on electronics
- Use proper ESD protection
- Never short LiPo battery terminals
- Ensure proper ventilation
"""
        return guide

    def write_all_docs(self):
        """Generate all documentation"""
        os.makedirs(self.docs_dir, exist_ok=True)

        docs = {
            'README.md': self.generate_readme(),
            'docs/ASSEMBLY.md': self.generate_assembly_guide()
        }

        for filename, content in docs.items():
            filepath = os.path.join(self.root, filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as f:
                f.write(content)
            print(f"Generated: {filepath}")

if __name__ == "__main__":
    writer = DocWriter()
    writer.write_all_docs()
    print("\nDocumentation generation complete!")
