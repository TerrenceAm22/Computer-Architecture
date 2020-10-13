"""CPU functionality."""

import sys

# Flag
FL = [0] * 3
# Stack Pointer
SP = 7
# interrupt mask
IM = 5
# Interrupt status
IS = 6
INT = [0] * 8

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.pc = 0
        self.ir = None
        self.ram = [0] * 256
        self.sp = 256
        self.commands = {
            0b00000001: self.hlt,
            0b10000010: self.ldi,
            0b01000111: self.prn,
        }
        

    def load(self, program):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
           0b10000010, # LDI R0,8
           0b00000000,
           0b00001000,
           0b01000111, # PRN R0
           0b00000000,
           0b00000001, # HLT
        ]

        for instruction in program:
           self.ram[address] = instruction
           address += 1
        with open(program) as f:
            for line in f:
                comment_split = line.split('#')
                num = comment_split[0].strip()

                try:
                    self.ram_write(int(num, 2), address)
                    address += 1
                except ValueError:
                    print("Value Error")
                    pass


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    
    def ram_read(self, MAR):
        return self.ram[MAR]
    
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR
    
    def hlt(self):
        self.running = False
     
    def ldi(self, reg_num, value):
        self.reg[reg_num] = value
        self.pc += 3
    
    def prn(self, operand_a, operand_b):
        print(self.reg[operand_a])
        return(2, True)

    def run(self):
        """Run the CPU."""
        running = True
        
        while running:
            instruction_register = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            try:
                f = self.commands[instruction_register]
                # print(f)
                operation_op = f(operand_a, operand_b
                                 )
                running = operation_op[1]
                self.pc += operation_op[0]

            except:
                print(f"Error: Instruction {instruction_register} not found")
                sys.exit(1)