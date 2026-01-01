"""
Neiler-8 Assembler
Converts assembly language to machine code

Usage: python asm.py input.asm -o output.bin
"""

import sys
import re

class Neiler8Assembler:
    def __init__(self):
        # Opcode mapping (mnemonic -> opcode)
        self.opcodes = {
            'NOP': 0x00,
            'MOV A,': 0x01,
            'MOV B,': 0x02,
            'MOV C,': 0x03,
            'MOV D,': 0x04,
            'MOV X,': 0x05,
            'MOV Y,': 0x06,
            'MOV A, B': 0x10,
            'MOV A, C': 0x11,
            'MOV B, A': 0x12,
            'MOV C, A': 0x13,
            'LOAD A,': 0x20,
            'LOAD B,': 0x21,
            'STORE A,': 0x22,
            'STORE B,': 0x23,
            'PUSH A': 0x30,
            'PUSH B': 0x31,
            'POP A': 0x32,
            'POP B': 0x33,
            'ADD A, B': 0x40,
            'ADD A,': 0x41,
            'SUB A, B': 0x42,
            'SUB A,': 0x43,
            'INC A': 0x44,
            'INC B': 0x45,
            'INC X': 0x46,
            'INC Y': 0x47,
            'DEC A': 0x48,
            'DEC B': 0x49,
            'DEC X': 0x4A,
            'DEC Y': 0x4B,
            'AND A, B': 0x50,
            'OR A, B': 0x51,
            'XOR A, B': 0x52,
            'NOT A': 0x53,
            'SHL A': 0x54,
            'SHR A': 0x55,
            'CMP A, B': 0x60,
            'CMP A,': 0x61,
            'JMP': 0x70,
            'JZ': 0x71,
            'JNZ': 0x72,
            'JC': 0x73,
            'JNC': 0x74,
            'JN': 0x75,
            'CALL': 0x80,
            'RET': 0x81,
            'IN A,': 0x90,
            'OUT': 0x91,
            'HLT': 0xFF,
        }

        self.labels = {}
        self.current_address = 0x0200

    def parse_value(self, value_str):
        """Parse numeric value (hex, decimal, or label)"""
        value_str = value_str.strip()

        # Hex value
        if value_str.startswith('0x') or value_str.startswith('$'):
            return int(value_str.replace('$', '0x'), 16)

        # Binary value
        if value_str.startswith('0b') or value_str.startswith('%'):
            return int(value_str.replace('%', '0b'), 2)

        # Label reference
        if value_str in self.labels:
            return self.labels[value_str]

        # Decimal value
        try:
            return int(value_str)
        except:
            raise ValueError(f"Cannot parse value: {value_str}")

    def assemble_line(self, line):
        """Assemble single line of code"""
        # Remove comments
        if ';' in line:
            line = line[:line.index(';')]

        line = line.strip().upper()

        if not line:
            return []

        # Check for label definition
        if line.endswith(':'):
            label = line[:-1]
            self.labels[label] = self.current_address
            return []

        # Find matching opcode
        machine_code = []

        for mnemonic, opcode in self.opcodes.items():
            if line.startswith(mnemonic):
                machine_code.append(opcode)

                # Extract operand if present
                operand_part = line[len(mnemonic):].strip()

                if operand_part:
                    # Handle different operand types
                    if ',' in operand_part:
                        parts = operand_part.split(',')
                        operand = parts[-1].strip()
                    else:
                        operand = operand_part

                    # Parse operand value
                    try:
                        value = self.parse_value(operand)

                        # Check if it's a word (2 bytes) or byte
                        if opcode in [0x70, 0x71, 0x72, 0x73, 0x74, 0x75, 0x80]:  # Jump/Call
                            # 16-bit address
                            machine_code.append(value & 0xFF)  # Low byte
                            machine_code.append((value >> 8) & 0xFF)  # High byte
                        else:
                            # 8-bit immediate
                            machine_code.append(value & 0xFF)
                    except:
                        pass

                break

        return machine_code

    def assemble(self, source_code):
        """Assemble complete program"""
        lines = source_code.split('\n')

        # First pass: collect labels
        self.current_address = 0x0200
        for line in lines:
            stripped = line.strip()
            if stripped.endswith(':'):
                label = stripped[:-1].upper()
                self.labels[label] = self.current_address
            else:
                # Estimate instruction size
                temp_code = self.assemble_line(line)
                self.current_address += len(temp_code)

        # Second pass: generate machine code
        self.current_address = 0x0200
        machine_code = []

        for line in lines:
            code = self.assemble_line(line)
            machine_code.extend(code)
            self.current_address += len(code)

        return bytearray(machine_code)


def main():
    if len(sys.argv) < 2:
        print("Usage: python asm.py input.asm [-o output.bin]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = "output.bin"

    if "-o" in sys.argv:
        idx = sys.argv.index("-o")
        if idx + 1 < len(sys.argv):
            output_file = sys.argv[idx + 1]

    # Read source file
    try:
        with open(input_file, 'r') as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)

    # Assemble
    assembler = Neiler8Assembler()
    try:
        machine_code = assembler.assemble(source)
        print(f"✓ Assembly successful!")
        print(f"  Code size: {len(machine_code)} bytes")
        print(f"  Labels: {len(assembler.labels)}")

        # Write output
        with open(output_file, 'wb') as f:
            f.write(machine_code)

        print(f"✓ Written to: {output_file}")

    except Exception as e:
        print(f"✗ Assembly error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
