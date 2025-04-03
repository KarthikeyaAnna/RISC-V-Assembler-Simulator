import sys
#simulator
class Simulator:
    def __init__(self, input_file_name, output_file_name, output_file_name_R):

        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.output_file_name_R = output_file_name_R

        # Initialize registers, memory, and program counter
        self.Register_value = {
            "00000": 0,
            "00001": 0,
            "00010": 380,
            "00011": 0,
            "00100": 0,
            "00101": 0,
            "00110": 0,
            "00111": 0,
            "01000": 0,
            "01001": 0,
            "01010": 0,
            "01011": 0,
            "01100": 0,
            "01101": 0,
            "01110": 0,
            "01111": 0,
            "10000": 0,
            "10001": 0,
            "10010": 0,
            "10011": 0,
            "10100": 0,
            "10101": 0,
            "10110": 0,
            "10111": 0,
            "11000": 0,
            "11001": 0,
            "11010": 0,
            "11011": 0,
            "11100": 0,
            "11101": 0,
            "11110": 0,
            "11111": 0
        }

        self.Memory = {
            65536: 0,
            65540: 0,
            65544: 0,
            65548: 0,
            65552: 0,
            65556: 0,
            65560: 0,
            65564: 0,
            65568: 0,
            65572: 0,
            65576: 0,
            65580: 0,
            65584: 0,
            65588: 0,
            65592: 0,
            65596: 0,
            65600: 0,
            65604: 0,
            65608: 0,
            65612: 0,
            65616: 0,
            65620: 0,
            65624: 0,
            65628: 0,
            65632: 0,
            65636: 0,
            65640: 0,
            65644: 0,
            65648: 0,
            65652: 0,
            65656: 0,
            65660: 0
        }

        self.PC = 0

        # Open output files
        self.g = open(self.output_file_name_R, "w")
        self.g_b = open(self.output_file_name, "w")

        # Instruction type dictionaries
        self.R_type = { "00000000000110011": "ADD",
                        "00000001010110011": "SRL",
                        "00000000100110011": "SLT",
                        "01000000000110011": "SUB",
                        "00000001100110011": "OR",
                        "00000001110110011": "AND"
                        }
        
        self.I_type = { "0100000011": "LW",
                        "0000010011": "ADDI", 
                        "0001100111": "JALR"
                        }
        
        self.S_type = {"0000100011": "SW"}

        self.B_type = {"0001100011": "BEQ",
                        "0011100011": "BNE",
                        "1001100011": "BLT"}
        
        self.J_type = {"1101111": "JAL"}
        self.opcode_define = {"0110011": "R",
                              "0000011": "I",
                              "0010011": "I",
                              "1100111": "I",
                              "1100011": "B",
                              "1101111": "J",
                              "0100011": "S"
                              }

        # Read instructions from file
        self.data_in_list = []
        with open(self.input_file_name, "r") as f:
            for line in f.readlines():
                if len(line.strip()) > 0:
                    self.data_in_list.append(line.strip())

    # Functions used by instructions
    def twos_complement(self, bin_str):
        k = 0
        for j in range(len(bin_str)):
            k = j
            if bin_str[len(bin_str) - 1 - j] == '1':
                break
        bin_break = list(bin_str[:len(bin_str) - k - 1])
        for i in range(len(bin_break)):
            if bin_break[i] == "1":
                bin_break[i] = "0"
            else:
                bin_break[i] = "1"
        bin_break = "".join(bin_break)
        binary = bin_break + bin_str[len(bin_str) - 1 - k:]
        return binary

    def decimal_to_hexadecimal(self, decimal_num):
        return "0x" + format(decimal_num, "08X")

    def decimal_to_binary(self, number, bits):
        if number > 0:
            binary = 0
            i = 0
            while number != 0:
                remainder = number % 2
                binary = remainder * (10 ** i) + binary
                number = number // 2
                i += 1
            binary = str(binary)
            if len(binary) < bits:
                binary = '0' * (bits - len(binary)) + binary
            return binary
        elif number < 0:
            number = number * (-1)
            b = bits
            bin_str = self.decimal_to_binary(number, b)
            bin_str = self.twos_complement(bin_str)
            return bin_str
        else:
            return "0" * bits

    def binary_to_decimal(self, binary):
        if binary[0] == '1':
            positive_binary = self.twos_complement(binary)
            decimal = 0
            for i in range(len(positive_binary)):
                decimal += int(positive_binary[len(positive_binary) - 1 - i]) * (2 ** i)
            decimal = decimal * (-1)
            return decimal 
        else:
            decimal = 0
            for i in range(len(binary)):
                decimal += int(binary[len(binary) - 1 - i]) * (2 ** i)
            return decimal

    # Instruction functions
    def R_instruction(self, instruction):
        x = instruction[0:7] + instruction[17:20] + instruction[25:32]
        operation_type = self.R_type.get(x)
        rs1 = instruction[12:17]
        rs2 = instruction[7:12]
        rd = instruction[20:25]
        if rd == "00000":
            return
        else:
            if operation_type == "ADD":
                x = self.Register_value[rs1] + self.Register_value[rs2]
                self.Register_value[rd] = x
                return
            elif operation_type == "SUB":
                x = self.Register_value[rs1] - self.Register_value[rs2]
                self.Register_value[rd] = x
                return
            elif operation_type == "SRL":
                y = self.decimal_to_binary(self.Register_value[rs2], 32)
                y = self.binary_to_decimal(y[27:32])  # Extracting last 5 bits for shift amount
                x = self.Register_value[rs1] >> y  # Logical right shift
                self.Register_value[rd] = x
                return
            elif operation_type == "SLT":
                x = self.Register_value[rs1]
                y = self.Register_value[rs2]
                if x < y:
                    self.Register_value[rd] = 1
                return
            elif operation_type == "MUL":
                x = self.Register_value[rs1] * self.Register_value[rs2]
                self.Register_value[rd] = x
                return
            elif operation_type == "AND":
                x = ["0"] * 32
                rs1_bin = self.decimal_to_binary(self.Register_value[rs1], 32)
                rs2_bin = self.decimal_to_binary(self.Register_value[rs2], 32)
                for i in range(32):
                    if rs1_bin[i] == "1" and rs2_bin[i] == "1":
                        x[i] = "1"
                x = "".join(x)  
                self.Register_value[rd] = self.binary_to_decimal(x)
                return
            elif operation_type == "OR":
                x = ["0"] * 32
                rs1_binary = self.decimal_to_binary(self.Register_value[rs1], 32)
                rs2_binary = self.decimal_to_binary(self.Register_value[rs2], 32)
                for i in range(32):
                    if rs1_binary[i] == "1" or rs2_binary[i] == "1":
                        x[i] = "1"
                x = "".join(x)
                self.Register_value[rd] = self.binary_to_decimal(x)
                return
        return 

    def I_instruction(self, instruction, PC):
        operation_type = self.I_type.get(instruction[17:20] + instruction[25:32])
        rs1 = instruction[12:17]
        rd = instruction[20:25]
        imm = instruction[0:12]
        if operation_type == "ADDI":
            imm = self.binary_to_decimal(imm)
            temp = imm + self.Register_value.get(rs1)
            if rd == "00000":
                return
            else:
                self.Register_value[rd] = temp
        elif operation_type == "LW":
            if rd == "00000":
                return
            else:
                memory_add = int(self.Register_value.get(rs1) + self.binary_to_decimal(imm))
                if memory_add in self.Memory:
                    self.Register_value[rd] = self.Memory.get(memory_add)
                    return
                else:
                    self.Memory[memory_add] = 0
                    self.Register_value[rd] = self.Memory.get(memory_add)
                    return
        elif operation_type == "JALR":
            if rd == "00000":
                PC = self.Register_value.get(rs1) + self.binary_to_decimal(imm)
                return PC
            else:
                self.Register_value[rd] = PC + 4
                PC = self.Register_value.get(rs1) + self.binary_to_decimal(imm)
                return PC
        else:
            print("invalid instruction")
            return

    def B_instruction(self, instruction, PC):
        operation_type = self.B_type.get(instruction[17:20] + instruction[25:32])
        value_of_rs1 = self.Register_value.get(instruction[12:17])
        value_of_rs2 = self.Register_value.get(instruction[7:12])
        imm = instruction[0] + instruction[24] + instruction[1:7] + instruction[20:24]
        imm = self.binary_to_decimal(imm)
        imm = imm * 2  # left shift by 1

        if operation_type == "BEQ":
            if value_of_rs1 == value_of_rs2:
                PC = PC + imm
                return str(PC)
            else:
                p = str(PC + 4)
                return p
        elif operation_type == "BNE":
            if value_of_rs1 != value_of_rs2:
                PC = PC + imm
                p = str(PC)
                return p
            else:
                p = str(PC + 4)
                return p
        elif operation_type == "BLT":
            if value_of_rs1 < value_of_rs2:
                PC = PC + imm
                p = str(PC)
                return p
            else:
                p = str(PC + 4)
                return p

    def S_instruction(self, instruction):
        rs2 = instruction[7:12]
        rs1 = instruction[12:17]
        imm = instruction[0:7] + instruction[20:25]
        imm = self.binary_to_decimal(imm)
        rs1_value = self.Register_value.get(rs1)
        memory_address = rs1_value + imm
        self.Memory[memory_address] = self.Register_value.get(rs2)
        return  

    def J_instruction(self, instruction, PC):
        imm = instruction[0] + instruction[12:20] + instruction[11] + instruction[1:11] + "0"
        imm = self.binary_to_decimal(imm)
        rd = instruction[20:25]
        if rd == "00000":
            return PC + 4
        else:
            self.Register_value[rd] = PC + 4
            PC = PC + imm
            return PC

    def print_values(self):
        for i in self.Register_value.values():
            a = "0b" + self.decimal_to_binary(i, 32)
            a = " " + a
            i_str = " " + str(i)
            self.g_b.write(a)
            self.g.write(i_str)
        self.g.write(" " + '\n')
        self.g_b.write(" " + '\n')
        return

    def run(self):
        i = 0
        while i < len(self.data_in_list):
            # Check for bonus instructions.
            # We assume bonus instructions have opcode "1111111" (bits [25:32])
            if self.data_in_list[i][25:32] == "1111111":
                # Use bits [11:16] as bonus function code
                bonus_code = self.data_in_list[i][11:16]
                if bonus_code == "00000":  # rst: reset all registers except PC (and x0 remains unchanged)
                    for reg in self.Register_value:
                        if reg != "00000":
                            self.Register_value[reg] = 0
                    i += 1
                    self.PC = i * 4
                    P = "0b" + self.decimal_to_binary(self.PC, 32)
                    tem = str(self.PC)
                    self.g.write(tem)
                    self.g_b.write(P)
                    self.print_values()
                    continue
                elif bonus_code == "00001":  # halt: stop execution
                    self.PC = i * 4
                    P = "0b" + self.decimal_to_binary(self.PC, 32)
                    tem = str(self.PC)
                    self.g.write(tem)
                    self.g_b.write(P)
                    self.print_values()
                    break
                elif bonus_code == "00010":  # rvrs: reverse the bits of register rs1 and store in rd
                    rs1 = self.data_in_list[i][12:17]
                    rd = self.data_in_list[i][20:25]
                    bin_str = self.decimal_to_binary(self.Register_value[rs1], 32)
                    rev_bin = bin_str[::-1]
                    self.Register_value[rd] = self.binary_to_decimal(rev_bin)
                    i += 1
                    self.PC = i * 4
                    P = "0b" + self.decimal_to_binary(self.PC, 32)
                    tem = str(self.PC)
                    self.g.write(tem)
                    self.g_b.write(P)
                    self.print_values()
                    continue
                else:
                    self.g.write("Invalid bonus instruction")
                    self.g_b.write("Invalid bonus instruction")
                
                    self.PC = i * 4
                    break

            opcode = self.data_in_list[i][25:32]
            instruction_type = self.opcode_define[opcode]
            if instruction_type == "R":
                self.R_instruction(self.data_in_list[i])
                i = i + 1
                self.PC = (i) * 4
                P = "0b" + self.decimal_to_binary(self.PC, 32)
                tem = str(self.PC)
                self.g.write(tem)
                self.g_b.write(P)
                self.print_values()
            elif instruction_type == "B":
                if self.data_in_list[i] == "00000000000000000000000001100011":
                    self.PC = i * 4
                    P = "0b" + self.decimal_to_binary(self.PC, 32)
                    tem = str(self.PC)
                    self.g.write(tem)
                    self.g_b.write(P)
                    self.print_values()
                    i = i + 4
                    break
                b = int(self.B_instruction(self.data_in_list[i], self.PC))
                self.PC = b
                P = "0b" + self.decimal_to_binary(self.PC, 32)
                self.g.write(str(self.PC))
                self.g_b.write(P)
                i = int(self.PC / 4)
                self.print_values()
            elif instruction_type == "S":
                self.S_instruction(self.data_in_list[i])
                i = i + 1
                self.PC = i * 4
                P = "0b" + self.decimal_to_binary(self.PC, 32)
                tem = str(self.PC)
                self.g_b.write(P)
                self.g.write(tem)
                self.print_values()
            elif instruction_type == "I":
                if opcode == "1100111":
                    self.PC = self.I_instruction(self.data_in_list[i], self.PC)
                    i = int(self.PC // 4)
                    tem = str(self.PC)
                    P = "0b" + self.decimal_to_binary(self.PC, 32)
                    self.g_b.write(P)
                    self.g.write(tem)
                    self.print_values()
                else:
                    self.I_instruction(self.data_in_list[i], self.PC)
                    i = i + 1
                    self.PC = i * 4
                    P = "0b" + self.decimal_to_binary(self.PC, 32)
                    tem = str(self.PC)
                    self.g_b.write(P)
                    self.g.write(tem)
                    self.print_values()
            elif instruction_type == "J":
                self.PC = self.J_instruction(self.data_in_list[i], self.PC)
                i = self.PC // 4
                tem = str(self.PC)
                P = "0b" + self.decimal_to_binary(self.PC, 32)
                self.g_b.write(P)
                self.g.write(tem)
                self.print_values()
            else:
                self.g.write("INVALID TILL NOW")
                self.g.write("Invalid")
               
                self.PC = i * 4
                break

        for j in self.Memory.keys():
            a = str(self.decimal_to_hexadecimal(j)) + ":" + "0b" + self.decimal_to_binary(self.Memory[j], 32)
            if j == 65660:
                self.g.write(a)
                self.g_b.write(a)
                break
            else:
                a = a + "\n"
                self.g_b.write(a)
                self.g.write(a)

    def close(self):
        self.g.close()
        self.g_b.close()

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python simulator.py <input_file> <output_file> <output_file_R>")
        sys.exit(1)
    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]
    output_file_name_R = sys.argv[3]
    
    sim = Simulator(input_file_name, output_file_name, output_file_name_R)
    sim.run()
    sim.close()
