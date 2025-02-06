data = {
    "INSTRUCTION_FORMATS": {
        "R": ["add", "sub", "slt", "srl", "or", "and"],
        "I": ["lw", "addi", "jalr"],
        "S": ["sw"],
        "B": ["beq", "bne", "blt"],
        "J": ["jal"]
    },
    "OPCODES": {
        "add": "0110011",
        "sub": "0110011",
        "slt": "0110011",
        "srl": "0110011",
        "or": "0110011",
        "and": "0110011",
        "lw": "0000011",
        "addi": "0010011",
        "jalr": "1100111",
        "sw": "0100011",
        "beq": "1100011",
        "bne": "1100011",
        "blt": "1100011",
        "jal": "1101111"
    },
    "FUNCT3": {
        "add": "000",
        "sub": "000",
        "slt": "010",
        "srl": "101",
        "or": "110",
        "and": "111",
        "lw": "010",
        "addi": "000",
        "jalr": "000",
        "sw": "010",
        "beq": "000",
        "bne": "001",
        "blt": "100"
    },
    "FUNCT7": {
        "add": "0000000",
        "sub": "0100000",
        "slt": "0000000",
        "srl": "0000000",
        "or": "0000000",
        "and": "0000000"
    },
    "REGISTER_MAP": {
        "zero": "00000",
        "ra": "00001",
        "sp": "00010",
        "gp": "00011",
        "tp": "00100",
        "t0": "00101",
        "t1": "00110",
        "t2": "00111",
        "s0": "01000",
        "s1": "01001",
        "a0": "01010",
        "a1": "01011",
        "a2": "01100",
        "a3": "01101",
        "a4": "01110",
        "a5": "01111",
        "a6": "10000",
        "a7": "10001",
        "s2": "10010",
        "s3": "10011",
        "s4": "10100",
        "s5": "10101",
        "s6": "10110",
        "s7": "10111",
        "s8": "11000",
        "s9": "11001",
        "s10": "11010",
        "s11": "11011",
        "t3": "11100",
        "t4": "11101",
        "t5": "11110",
        "t6": "11111"
    }
}

with open("input.txt",'r') as file:
    
    for line in file:
        line=line.strip()
        list_line_sep=line.split(" ")
        for i in range(len(list_line_sep)):
            list_line_sep[i]=list_line_sep[i].strip(',')
        if(',' in list_line_sep[-1]):
            new=list_line_sep[i].split(',')
            list_line_sep.pop(-1)
            for i in new:
                list_line_sep.append(i)
        print(list_line_sep)
        
        
        instruction=list_line_sep[0]
        binary_output=""
        #classify the instruction as R type
        if(instruction in data["INSTRUCTION_FORMATS"]["R"]):

            if(len(list_line_sep)!=4):
                binary_output="ERROR"
            else:
                rd=list_line_sep[1]
                r1=list_line_sep[2]
                r2=list_line_sep[3]
                #1)fun7
                binary_output+=data["FUNCT7"][instruction]
                #2)rs2,rs1,func3,rd,opcode
                binary_output+=data["REGISTER_MAP"][r2]+data["REGISTER_MAP"][r1]+data["FUNCT3"][instruction]+data["REGISTER_MAP"][rd]+data["OPCODES"][instruction]
        print(binary_output)

        #shreyas is a gay
        #shreyas is binary
        

        #guys list_line_sep is the list containing ["add","sr","s1","s2"]
        #if any line is not getting tokenized just let me know.
        #to create your instruction ; just create a if condintion weather the instruction is present in instructions and write your code under it
        #to store your answer use binary_output
        
    

