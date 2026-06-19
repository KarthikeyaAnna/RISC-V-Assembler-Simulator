
---

# RISC-V Assembler and Simulator in Python

## 📌 Overview

This project implements a complete **RISC-V RV32I Assembler and Simulator** in Python.

The system consists of two major modules:

* **Assembler**
  Converts human-readable RISC-V assembly instructions into 32-bit binary machine code.

* **Simulator**
  Executes the generated machine code while maintaining:

  * 32 General Purpose Registers
  * Program Counter (PC)
  * Data Memory
  * Instruction Execution Flow

---

# 📂 Project Structure

| File                  | Purpose                                       |
| --------------------- | --------------------------------------------- |
| `assembler.py`        | Converts assembly code to binary machine code |
| `simulator.py`        | Executes binary instructions                  |
| `input.asm`           | RISC-V assembly program                       |
| `output.bin`          | Generated 32-bit machine instructions         |
| `register_output.txt` | Register state after each instruction         |
| `memory_output.txt`   | Memory contents after execution               |

---

# 🏗 System Architecture

```
                Assembly Program
                       |
                       v
                +--------------+
                |  Assembler   |
                +--------------+
                       |
                       v
              32-bit Binary Code
                       |
                       v
                +--------------+
                |  Simulator   |
                +--------------+
                       |
       +---------------+---------------+
       |                               |
       v                               v
 Register File                     Memory
 32 Registers                  Data Storage
```

---

# Supported Instruction Formats

| Format | Description                     | Supported Instructions      |
| ------ | ------------------------------- | --------------------------- |
| R-Type | Register to register operations | ADD, SUB, SLT, SRL, OR, AND |
| I-Type | Immediate and load operations   | ADDI, LW, JALR              |
| S-Type | Store instructions              | SW                          |
| B-Type | Conditional branches            | BEQ, BNE, BLT               |
| J-Type | Jump instructions               | JAL                         |
| Custom | Additional instructions         | MUL, RST, HALT, RVRS        |

---

# RISC-V Register Map

| Register | Binary Address | Decimal Address | Purpose                          |
| -------- | -------------- | --------------- | -------------------------------- |
| zero     | 00000          | x0              | Hardwired constant zero          |
| ra       | 00001          | x1              | Return address                   |
| sp       | 00010          | x2              | Stack pointer                    |
| gp       | 00011          | x3              | Global pointer                   |
| tp       | 00100          | x4              | Thread pointer                   |
| t0       | 00101          | x5              | Temporary register               |
| t1       | 00110          | x6              | Temporary register               |
| t2       | 00111          | x7              | Temporary register               |
| s0/fp    | 01000          | x8              | Saved register / Frame pointer   |
| s1       | 01001          | x9              | Saved register                   |
| a0       | 01010          | x10             | Function argument / Return value |
| a1       | 01011          | x11             | Function argument                |
| a2       | 01100          | x12             | Function argument                |
| a3       | 01101          | x13             | Function argument                |
| a4       | 01110          | x14             | Function argument                |
| a5       | 01111          | x15             | Function argument                |
| a6       | 10000          | x16             | Function argument                |
| a7       | 10001          | x17             | Function argument                |
| s2       | 10010          | x18             | Saved register                   |
| s3       | 10011          | x19             | Saved register                   |
| s4       | 10100          | x20             | Saved register                   |
| s5       | 10101          | x21             | Saved register                   |
| s6       | 10110          | x22             | Saved register                   |
| s7       | 10111          | x23             | Saved register                   |
| s8       | 11000          | x24             | Saved register                   |
| s9       | 11001          | x25             | Saved register                   |
| s10      | 11010          | x26             | Saved register                   |
| s11      | 11011          | x27             | Saved register                   |
| t3       | 11100          | x28             | Temporary register               |
| t4       | 11101          | x29             | Temporary register               |
| t5       | 11110          | x30             | Temporary register               |
| t6       | 11111          | x31             | Temporary register               |

---

# R-Type Instruction Encoding

```
31        25 24 20 19 15 14 12 11 7 6      0
+----------+-----+-----+------+----+--------+
| funct7   | rs2 | rs1 |funct3| rd | opcode |
+----------+-----+-----+------+----+--------+
```

| Instruction | funct7  | funct3 | Opcode  | Operation                         |
| ----------- | ------- | ------ | ------- | --------------------------------- |
| ADD         | 0000000 | 000    | 0110011 | rd = rs1 + rs2                    |
| SUB         | 0100000 | 000    | 0110011 | rd = rs1 - rs2                    |
| SLT         | 0000000 | 010    | 0110011 | rd = (rs1 < rs2)                  |
| SRL         | 0000000 | 101    | 0110011 | Logical right shift               |
| OR          | 0000000 | 110    | 0110011 | Bitwise OR                        |
| AND         | 0000000 | 111    | 0110011 | Bitwise AND                       |
| MUL*        | 0000001 | 000    | 0110011 | Multiplication (custom extension) |

---

# I-Type Instruction Encoding

```
31                 20 19 15 14 12 11 7 6 0
+--------------------+-----+------+----+------+
|      immediate      | rs1 |funct3| rd |opcode|
+--------------------+-----+------+----+------+
```

| Instruction | funct3 | Opcode  | Operation              |
| ----------- | ------ | ------- | ---------------------- |
| ADDI        | 000    | 0010011 | rd = rs1 + immediate   |
| LW          | 010    | 0000011 | Load word from memory  |
| JALR        | 000    | 1100111 | Jump and link register |

---

# S-Type Instruction Encoding

```
31      25 24 20 19 15 14 12 11 7 6 0
+---------+-----+-----+------+----+
| imm[11:5]|rs2 | rs1 |funct3|imm |
+---------+-----+-----+------+----+
```

| Instruction | funct3 | Opcode  | Operation                        |
| ----------- | ------ | ------- | -------------------------------- |
| SW          | 010    | 0100011 | Store register value into memory |

---

# B-Type Instruction Encoding

| Instruction | funct3 | Opcode  | Condition            |
| ----------- | ------ | ------- | -------------------- |
| BEQ         | 000    | 1100011 | Branch if rs1 == rs2 |
| BNE         | 001    | 1100011 | Branch if rs1 != rs2 |
| BLT         | 100    | 1100011 | Branch if rs1 < rs2  |

---

# J-Type Instruction Encoding

| Instruction | Opcode  | Operation                     |
| ----------- | ------- | ----------------------------- |
| JAL         | 1101111 | Jump and store return address |

---

# Custom Bonus Instructions

| Instruction | Description               | Operation                         |
| ----------- | ------------------------- | --------------------------------- |
| MUL         | Integer multiplication    | rd = rs1 × rs2                    |
| RST         | Reset processor registers | All registers reset to zero       |
| HALT        | Stop execution            | Terminates simulator              |
| RVRS        | Reverse bits              | Reverses 32-bit value of register |

---

# Memory Model

The simulator implements a word-addressable memory.

| Property                           | Value      |
| ---------------------------------- | ---------- |
| Starting Address                   | 0x00010000 |
| Address Increment                  | 4 bytes    |
| Number of Initial Memory Locations | 32         |
| Data Width                         | 32 bits    |

---

# Program Counter (PC)

| Event              | PC Update            |
| ------------------ | -------------------- |
| Normal instruction | PC = PC + 4          |
| Branch taken       | PC = PC + immediate  |
| JAL                | PC = PC + offset     |
| JALR               | PC = rs1 + immediate |
| HALT               | Execution stops      |

---

# Running the Assembler

```bash
python assembler.py input.asm output.bin
```

Example:

```assembly
addi a0, zero, 10
addi a1, zero, 20
add a2, a0, a1
```

Generated machine code:

```
00000000101000000000010100010011
00000001010000000000010110010011
00000000101101010000011000110011
```

---

# Running the Simulator

```bash
python simulator.py input.bin register_output.txt memory_output.txt
```

---

# Execution Trace

After every instruction the simulator records:

* Current Program Counter
* Values of all 32 registers
* Final state of memory

---

# Error Handling

The assembler detects:

* Invalid instruction names
* Incorrect operand count
* Invalid register names
* Incorrect immediate values
* Undefined labels

---

# Future Improvements

* Support complete RV32I instruction set
* Add floating-point instructions
* Implement pipelined processor simulation
* Add cache memory simulation
* Add graphical debugging interface

---

# Author

**RISC-V Assembler and Simulator implemented using Python**

---


