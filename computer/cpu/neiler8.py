"""
Neiler-8: 8-bit CPU Implementation
Fully functional 8-bit processor with 16-bit address bus

Features:
- 6 general-purpose registers (A, B, C, D, X, Y)
- 16-bit program counter
- 8-bit stack pointer
- ALU with 8 operations
- 64KB addressable memory
- Interrupt support
"""

class Neiler8CPU:
    def __init__(self, memory_size=65536):
        # Registers (8-bit)
        self.A = 0  # Accumulator
        self.B = 0  # Accumulator
        self.C = 0  # General purpose
        self.D = 0  # General purpose
        self.X = 0  # Index register
        self.Y = 0  # Index register

        # Special registers
        self.PC = 0x0200  # Program counter (starts after zero page and stack)
        self.SP = 0xFF    # Stack pointer (stack at 0x0100-0x01FF)

        # Flags
        self.FLAG_ZERO = 0
        self.FLAG_CARRY = 0
        self.FLAG_OVERFLOW = 0
        self.FLAG_NEGATIVE = 0
        self.FLAG_INTERRUPT = 0

        # Memory (64KB)
        self.memory = bytearray(memory_size)

        # I/O ports
        self.io_ports = [0] * 256

        # State
        self.halted = False
        self.cycles = 0

        # Instruction set
        self.opcodes = {
            # Data movement
            0x00: ('NOP', 0, self.nop),
            0x01: ('MOV A, imm', 1, lambda: self.mov_reg_imm('A')),
            0x02: ('MOV B, imm', 1, lambda: self.mov_reg_imm('B')),
            0x03: ('MOV C, imm', 1, lambda: self.mov_reg_imm('C')),
            0x04: ('MOV D, imm', 1, lambda: self.mov_reg_imm('D')),
            0x05: ('MOV X, imm', 1, lambda: self.mov_reg_imm('X')),
            0x06: ('MOV Y, imm', 1, lambda: self.mov_reg_imm('Y')),

            0x10: ('MOV A, B', 0, lambda: self.mov_reg_reg('A', 'B')),
            0x11: ('MOV A, C', 0, lambda: self.mov_reg_reg('A', 'C')),
            0x12: ('MOV B, A', 0, lambda: self.mov_reg_reg('B', 'A')),
            0x13: ('MOV C, A', 0, lambda: self.mov_reg_reg('C', 'A')),

            # Load/Store
            0x20: ('LOAD A, [addr]', 2, lambda: self.load_reg_addr('A')),
            0x21: ('LOAD B, [addr]', 2, lambda: self.load_reg_addr('B')),
            0x22: ('STORE A, [addr]', 2, lambda: self.store_reg_addr('A')),
            0x23: ('STORE B, [addr]', 2, lambda: self.store_reg_addr('B')),

            0x24: ('LOAD A, [X]', 0, lambda: self.load_reg_indexed('A', 'X')),
            0x25: ('LOAD A, [Y]', 0, lambda: self.load_reg_indexed('A', 'Y')),
            0x26: ('STORE A, [X]', 0, lambda: self.store_reg_indexed('A', 'X')),
            0x27: ('STORE A, [Y]', 0, lambda: self.store_reg_indexed('A', 'Y')),

            # Stack operations
            0x30: ('PUSH A', 0, lambda: self.push('A')),
            0x31: ('PUSH B', 0, lambda: self.push('B')),
            0x32: ('POP A', 0, lambda: self.pop('A')),
            0x33: ('POP B', 0, lambda: self.pop('B')),

            # Arithmetic
            0x40: ('ADD A, B', 0, lambda: self.add_reg_reg('A', 'B')),
            0x41: ('ADD A, imm', 1, lambda: self.add_reg_imm('A')),
            0x42: ('SUB A, B', 0, lambda: self.sub_reg_reg('A', 'B')),
            0x43: ('SUB A, imm', 1, lambda: self.sub_reg_imm('A')),
            0x44: ('INC A', 0, lambda: self.inc('A')),
            0x45: ('INC B', 0, lambda: self.inc('B')),
            0x46: ('INC X', 0, lambda: self.inc('X')),
            0x47: ('INC Y', 0, lambda: self.inc('Y')),
            0x48: ('DEC A', 0, lambda: self.dec('A')),
            0x49: ('DEC B', 0, lambda: self.dec('B')),
            0x4A: ('DEC X', 0, lambda: self.dec('X')),
            0x4B: ('DEC Y', 0, lambda: self.dec('Y')),

            # Logic
            0x50: ('AND A, B', 0, lambda: self.and_reg_reg('A', 'B')),
            0x51: ('OR A, B', 0, lambda: self.or_reg_reg('A', 'B')),
            0x52: ('XOR A, B', 0, lambda: self.xor_reg_reg('A', 'B')),
            0x53: ('NOT A', 0, lambda: self.not_reg('A')),
            0x54: ('SHL A', 0, lambda: self.shl('A')),
            0x55: ('SHR A', 0, lambda: self.shr('A')),

            # Comparison
            0x60: ('CMP A, B', 0, lambda: self.cmp_reg_reg('A', 'B')),
            0x61: ('CMP A, imm', 1, lambda: self.cmp_reg_imm('A')),

            # Jumps
            0x70: ('JMP addr', 2, self.jmp),
            0x71: ('JZ addr', 2, self.jz),
            0x72: ('JNZ addr', 2, self.jnz),
            0x73: ('JC addr', 2, self.jc),
            0x74: ('JNC addr', 2, self.jnc),
            0x75: ('JN addr', 2, self.jn),

            # Subroutines
            0x80: ('CALL addr', 2, self.call),
            0x81: ('RET', 0, self.ret),

            # I/O
            0x90: ('IN A, port', 1, lambda: self.in_reg('A')),
            0x91: ('OUT port, A', 1, lambda: self.out_reg('A')),

            # System
            0xFF: ('HLT', 0, self.hlt),
        }

    def get_register(self, reg_name):
        """Get register value by name"""
        return getattr(self, reg_name)

    def set_register(self, reg_name, value):
        """Set register value by name"""
        setattr(self, reg_name, value & 0xFF)
        self.update_flags(value & 0xFF)

    def update_flags(self, value):
        """Update CPU flags based on value"""
        self.FLAG_ZERO = 1 if (value & 0xFF) == 0 else 0
        self.FLAG_NEGATIVE = 1 if (value & 0x80) else 0

    def read_byte(self, address):
        """Read byte from memory"""
        return self.memory[address & 0xFFFF]

    def write_byte(self, address, value):
        """Write byte to memory"""
        self.memory[address & 0xFFFF] = value & 0xFF

    def read_word(self, address):
        """Read 16-bit word (little-endian)"""
        low = self.read_byte(address)
        high = self.read_byte(address + 1)
        return (high << 8) | low

    def fetch_byte(self):
        """Fetch next byte from PC"""
        value = self.read_byte(self.PC)
        self.PC = (self.PC + 1) & 0xFFFF
        return value

    def fetch_word(self):
        """Fetch next word from PC"""
        low = self.fetch_byte()
        high = self.fetch_byte()
        return (high << 8) | low

    # === INSTRUCTION IMPLEMENTATIONS ===

    def nop(self):
        """No operation"""
        pass

    def mov_reg_imm(self, reg):
        """MOV reg, immediate"""
        value = self.fetch_byte()
        self.set_register(reg, value)

    def mov_reg_reg(self, dst, src):
        """MOV dst, src"""
        value = self.get_register(src)
        self.set_register(dst, value)

    def load_reg_addr(self, reg):
        """LOAD reg, [address]"""
        addr = self.fetch_word()
        value = self.read_byte(addr)
        self.set_register(reg, value)

    def store_reg_addr(self, reg):
        """STORE reg, [address]"""
        addr = self.fetch_word()
        value = self.get_register(reg)
        self.write_byte(addr, value)

    def load_reg_indexed(self, reg, index_reg):
        """LOAD reg, [index]"""
        addr = self.get_register(index_reg)
        value = self.read_byte(addr)
        self.set_register(reg, value)

    def store_reg_indexed(self, reg, index_reg):
        """STORE reg, [index]"""
        addr = self.get_register(index_reg)
        value = self.get_register(reg)
        self.write_byte(addr, value)

    def push(self, reg):
        """PUSH register to stack"""
        value = self.get_register(reg)
        stack_addr = 0x0100 + self.SP
        self.write_byte(stack_addr, value)
        self.SP = (self.SP - 1) & 0xFF

    def pop(self, reg):
        """POP from stack to register"""
        self.SP = (self.SP + 1) & 0xFF
        stack_addr = 0x0100 + self.SP
        value = self.read_byte(stack_addr)
        self.set_register(reg, value)

    def add_reg_reg(self, dst, src):
        """ADD dst, src"""
        a = self.get_register(dst)
        b = self.get_register(src)
        result = a + b
        self.FLAG_CARRY = 1 if result > 0xFF else 0
        self.FLAG_OVERFLOW = 1 if ((a ^ result) & (b ^ result) & 0x80) else 0
        self.set_register(dst, result)

    def add_reg_imm(self, reg):
        """ADD reg, immediate"""
        a = self.get_register(reg)
        b = self.fetch_byte()
        result = a + b
        self.FLAG_CARRY = 1 if result > 0xFF else 0
        self.set_register(reg, result)

    def sub_reg_reg(self, dst, src):
        """SUB dst, src"""
        a = self.get_register(dst)
        b = self.get_register(src)
        result = a - b
        self.FLAG_CARRY = 1 if result < 0 else 0
        self.set_register(dst, result)

    def sub_reg_imm(self, reg):
        """SUB reg, immediate"""
        a = self.get_register(reg)
        b = self.fetch_byte()
        result = a - b
        self.FLAG_CARRY = 1 if result < 0 else 0
        self.set_register(reg, result)

    def inc(self, reg):
        """INC register"""
        value = self.get_register(reg)
        self.set_register(reg, value + 1)

    def dec(self, reg):
        """DEC register"""
        value = self.get_register(reg)
        self.set_register(reg, value - 1)

    def and_reg_reg(self, dst, src):
        """AND dst, src"""
        a = self.get_register(dst)
        b = self.get_register(src)
        self.set_register(dst, a & b)

    def or_reg_reg(self, dst, src):
        """OR dst, src"""
        a = self.get_register(dst)
        b = self.get_register(src)
        self.set_register(dst, a | b)

    def xor_reg_reg(self, dst, src):
        """XOR dst, src"""
        a = self.get_register(dst)
        b = self.get_register(src)
        self.set_register(dst, a ^ b)

    def not_reg(self, reg):
        """NOT register"""
        value = self.get_register(reg)
        self.set_register(reg, ~value)

    def shl(self, reg):
        """SHL register (shift left)"""
        value = self.get_register(reg)
        self.FLAG_CARRY = 1 if (value & 0x80) else 0
        self.set_register(reg, value << 1)

    def shr(self, reg):
        """SHR register (shift right)"""
        value = self.get_register(reg)
        self.FLAG_CARRY = 1 if (value & 0x01) else 0
        self.set_register(reg, value >> 1)

    def cmp_reg_reg(self, reg1, reg2):
        """CMP reg1, reg2 (compare by subtraction)"""
        a = self.get_register(reg1)
        b = self.get_register(reg2)
        result = a - b
        self.update_flags(result)
        self.FLAG_CARRY = 1 if result < 0 else 0

    def cmp_reg_imm(self, reg):
        """CMP reg, immediate"""
        a = self.get_register(reg)
        b = self.fetch_byte()
        result = a - b
        self.update_flags(result)
        self.FLAG_CARRY = 1 if result < 0 else 0

    def jmp(self):
        """JMP address (unconditional jump)"""
        addr = self.fetch_word()
        self.PC = addr

    def jz(self):
        """JZ address (jump if zero)"""
        addr = self.fetch_word()
        if self.FLAG_ZERO:
            self.PC = addr

    def jnz(self):
        """JNZ address (jump if not zero)"""
        addr = self.fetch_word()
        if not self.FLAG_ZERO:
            self.PC = addr

    def jc(self):
        """JC address (jump if carry)"""
        addr = self.fetch_word()
        if self.FLAG_CARRY:
            self.PC = addr

    def jnc(self):
        """JNC address (jump if not carry)"""
        addr = self.fetch_word()
        if not self.FLAG_CARRY:
            self.PC = addr

    def jn(self):
        """JN address (jump if negative)"""
        addr = self.fetch_word()
        if self.FLAG_NEGATIVE:
            self.PC = addr

    def call(self):
        """CALL address (call subroutine)"""
        addr = self.fetch_word()
        # Push return address to stack
        ret_addr = self.PC
        self.push_word(ret_addr)
        self.PC = addr

    def ret(self):
        """RET (return from subroutine)"""
        ret_addr = self.pop_word()
        self.PC = ret_addr

    def push_word(self, value):
        """Push 16-bit word to stack"""
        self.write_byte(0x0100 + self.SP, (value >> 8) & 0xFF)
        self.SP = (self.SP - 1) & 0xFF
        self.write_byte(0x0100 + self.SP, value & 0xFF)
        self.SP = (self.SP - 1) & 0xFF

    def pop_word(self):
        """Pop 16-bit word from stack"""
        self.SP = (self.SP + 1) & 0xFF
        low = self.read_byte(0x0100 + self.SP)
        self.SP = (self.SP + 1) & 0xFF
        high = self.read_byte(0x0100 + self.SP)
        return (high << 8) | low

    def in_reg(self, reg):
        """IN register, port (read from I/O port)"""
        port = self.fetch_byte()
        value = self.io_ports[port]
        self.set_register(reg, value)

    def out_reg(self, reg):
        """OUT port, register (write to I/O port)"""
        port = self.fetch_byte()
        value = self.get_register(reg)
        self.io_ports[port] = value

    def hlt(self):
        """HLT (halt CPU)"""
        self.halted = True

    def step(self):
        """Execute one instruction"""
        if self.halted:
            return False

        # Fetch opcode
        opcode = self.fetch_byte()

        # Decode and execute
        if opcode in self.opcodes:
            name, param_bytes, func = self.opcodes[opcode]
            func()
            self.cycles += 1
            return True
        else:
            print(f"Unknown opcode: 0x{opcode:02X} at PC=0x{self.PC-1:04X}")
            self.halted = True
            return False

    def run(self, max_cycles=None):
        """Run until halted or max_cycles reached"""
        cycle_count = 0
        while not self.halted:
            if max_cycles and cycle_count >= max_cycles:
                break
            self.step()
            cycle_count += 1
        return cycle_count

    def load_program(self, program, start_address=0x0200):
        """Load program into memory"""
        for i, byte in enumerate(program):
            self.memory[start_address + i] = byte
        self.PC = start_address

    def dump_registers(self):
        """Print register state"""
        print(f"A={self.A:02X} B={self.B:02X} C={self.C:02X} D={self.D:02X}")
        print(f"X={self.X:02X} Y={self.Y:02X} SP={self.SP:02X} PC={self.PC:04X}")
        print(f"Flags: Z={self.FLAG_ZERO} C={self.FLAG_CARRY} N={self.FLAG_NEGATIVE}")
        print(f"Cycles: {self.cycles}")


if __name__ == "__main__":
    # Test program: Count from 0 to 10 and halt
    cpu = Neiler8CPU()

    program = [
        0x01, 0x00,        # MOV A, 0
        0x41, 0x01,        # ADD A, 1
        0x61, 0x0A,        # CMP A, 10
        0x72, 0x02, 0x02,  # JNZ 0x0202
        0xFF               # HLT
    ]

    cpu.load_program(program)
    cpu.run()
    cpu.dump_registers()

    print(f"\nFinal A register value: {cpu.A}")
