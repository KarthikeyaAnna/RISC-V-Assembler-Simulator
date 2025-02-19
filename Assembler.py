import sys

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
def convert(x):

    y=12
    a=""
    x=int(x)
    if x<0:
      x=x+4096
    while y>0:
        if x%2==0:
            a="0"+a
        else:
            a="1"+a
        x=x//2
        y=y-1
    return a


s=""
inputfile=sys.argv[-2]
outputfile=sys.argv[-1]

with open(inputfile,'r') as file:
    program_counter=-4

    for line in file:
        program_counter+=4
        line=line.strip()
        print(line)
        list_line_sep=line.split(" ")
        for i in range(len(list_line_sep)):
            list_line_sep[i]=list_line_sep[i].strip(',')
        if(',' in list_line_sep[-1]):
            new=list_line_sep[i].split(',')
            
            list_line_sep.pop(-1)
            for i in new:
                list_line_sep.append(i)
        #print(list_line_sep)
        if(list_line_sep[0 in data["OPCODES"]]):
            instruction=list_line_sep[0]
        else:
            continue
            

        if(list_line_sep[1] in data["INSTRUCTION_FORMATS"]["R"] or list_line_sep[1] in data["INSTRUCTION_FORMATS"]["S"] or list_line_sep[1] in data["INSTRUCTION_FORMATS"]["I"] or list_line_sep[1] in data["INSTRUCTION_FORMATS"]["B"] or list_line_sep[1] in data["INSTRUCTION_FORMATS"]["J"]):
            list_line_sep.pop(0)
            instruction=list_line_sep[0]
        
        binary_output=""
        #classify the instruction as R type
        if(instruction  in data["INSTRUCTION_FORMATS"]["R"] or list_line_sep[1] in data["INSTRUCTION_FORMATS"]["R"]):
            if( list_line_sep[1] in data["INSTRUCTION_FORMATS"]["R"]):
                list_line_sep.pop(0)
                instruction=list_line_sep[0]
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


        #classify the instruction as I type
        if(instruction in data["INSTRUCTION_FORMATS"]["I"]):
            if '(' in list_line_sep[2]:
                split_value=list_line_sep[2].strip('()').split('(')
                list_line_sep.pop(2)
                list_line_sep.insert(2,split_value[1]) 
                list_line_sep.insert(2,split_value[0])
                if(len(list_line_sep)!=4):  
                    binary_output="ERROR"
                else:  
                    rd=list_line_sep[1]
                    imm=list_line_sep[2]
                    r1=list_line_sep[3]
                    binary_output+=convert(imm)+data["REGISTER_MAP"][r1]+data["FUNCT3"][instruction]+data["REGISTER_MAP"][rd]+data["OPCODES"][instruction]

            else:
                if len(list_line_sep)!=4:
                    binary_output="ERROR"
                else:
                    rd=list_line_sep[1]
                    r1=list_line_sep[2]
                    imm=list_line_sep[3]
                    binary_output+=convert(imm)+data["REGISTER_MAP"][r1]+data["FUNCT3"][instruction]+data["REGISTER_MAP"][rd]+data["OPCODES"][instruction]
          
        
        if(instruction in data["INSTRUCTION_FORMATS"]["S"]):
            if (len(list_line_sep)>4 or len(list_line_sep)<3):
                binary_output="ERROR: Invalid Format"
            else:
                if len(list_line_sep)==3:
                    split_value=list_line_sep[2].strip('()').split('(')
                    
                    if len(split_value)!=2:
                        binary_output="ERROR: Invalid Format"
                    
                    else:
                        list_line_sep.pop(2)
                        list_line_sep.insert(2,split_value[1]) 
                        list_line_sep.insert(2,split_value[0])
                        
                        
                        if(list_line_sep[3].isdigit()):
                            
                            binary_output="ERROR"
                        else:
                            r2=list_line_sep[1]
                            r1=list_line_sep[3]
                            
                            netimm=convert(list_line_sep[2])
                            
                            imm_11_5=netimm[:7]
                            imm_4_0=netimm[7:]
                            
                            binary_output+=imm_11_5+data["REGISTER_MAP"][r2]+data["REGISTER_MAP"][r1]+data["FUNCT3"][instruction]+imm_4_0+data["OPCODES"][instruction]
                            if int(list_line_sep[2])>2**12:
                                
                                binary_output="Error"
                   
                elif len(list_line_sep)==4: 
                    split_value=list_line_sep[2].strip('()').split('(')
                    list_line_sep.pop(2)
                    list_line_sep.insert(2,split_value[1]) 
                    list_line_sep.insert(2,split_value[0])
                    r2=list_line_sep[1]
                    r1=list_line_sep[3]
                    netimm=convert(list_line_sep[2])
                    imm_11_5=netimm[:7]
                    imm_4_0=netimm[7:]
                    binary_output+=imm_11_5+data["REGISTER_MAP"][r2]+data["REGISTER_MAP"][r1]+data["FUNCT3"][instruction]+imm_4_0+data["OPCODES"][instruction]
                    if int(netimm)>2**12:
                        
                        binary_output="Error"



        def convert20bit(x):
            x = int(x) & 0xFFFFF  # Ensure 20-bit two's complement format
            return format(x, '020b')

        #classify the instruction as B type
                # classify the instruction as B type
        if ':' in list_line_sep[0]:
            parts = list_line_sep[0].split(':')
            # Replace the first token with the instruction part (e.g. "beq")
            list_line_sep[0] = parts[1].strip()
            instruction=list_line_sep[0]
       

        if instruction in data["INSTRUCTION_FORMATS"]["B"]:
            if len(list_line_sep) != 4:
                binary_output = "ERROR"
            else:
                r1 = list_line_sep[1]   # rs1
                r2 = list_line_sep[2]   # rs2
                target = list_line_sep[3]  # branch target (label or immediate)

                # Process if target is not purely numeric (i.e. a label)
                if not target.lstrip('-').isdigit():
                    label = target
                    search_pc = -4
                    found_pc = None

                    with open(inputfile, "r") as temp_file:
                        for line in temp_file:
                            search_pc += 4
                            line = line.strip()
                            if not line:
                                continue

                            if ':' in line:
                                current_label = line.split(':')[0].strip()
                                if current_label == label:
                                    found_pc = search_pc
                                    break

                    if found_pc is None:
                        binary_output = "ERROR"
                    else:
                        # Calculate branch offset (branch offsets are in 2-byte increments)
                        offset = (found_pc - program_counter) // 2

                        # For negative offsets, perform sign extension (using 13 bits then taking lower 12 bits)
                        if offset < 0:
                            offset = (1 << 13) + offset
                        newimm = format(offset & 0xFFF, '012b')  # 12-bit binary string

                        # Reorder the bits for B-type: 
                        # newimm[0] -> imm[12], newimm[1] -> imm[11], newimm[2:8] -> imm[10:5], newimm[8:12] -> imm[4:1]
                        bit_12    = newimm[0]
                        bit_11    = newimm[1]
                        bits_10_5 = newimm[2:8]
                        bits_4_1  = newimm[8:12]

                        binary_output = (
                            bit_12 +
                            bits_10_5 +
                            data["REGISTER_MAP"][r2] +
                            data["REGISTER_MAP"][r1] +
                            data["FUNCT3"][instruction] +
                            bits_4_1 +
                            bit_11 +
                            data["OPCODES"][instruction]
                        )
                else:
                    # If the target is a numeric immediate:
                    imm = int(target) // 2
                    if imm < 0:
                        imm = (1 << 12) + imm
                    newimm = format(imm & 0xFFF, '012b')

                    bit_12    = newimm[0]
                    bit_11    = newimm[1]
                    bits_10_5 = newimm[2:8]
                    bits_4_1  = newimm[8:12]

                    binary_output = (
                        bit_12 +
                        bits_10_5 +
                        data["REGISTER_MAP"][r2] +
                        data["REGISTER_MAP"][r1] +
                        data["FUNCT3"][instruction] +
                        bits_4_1 +
                        bit_11 +
                        data["OPCODES"][instruction]
                    )

        
        if instruction in data["INSTRUCTION_FORMATS"]["J"]:
            if len(list_line_sep) != 3:
                binary_output = "ERROR"
            else:
                if list_line_sep[2].lstrip('-').isdigit():


                    rd = list_line_sep[1]
                    imm = list_line_sep[2]
                    # For JAL, the immediate must be divided by 2 before conversion.
                    newimm = convert20bit(int(imm) // 2)
                    bit_20    = newimm[0]          # imm[20]
                    bits_10_1 = newimm[10:20]       # imm[10:1]
                    bit_11    = newimm[9]           # imm[11]
                    bits_19_12= newimm[1:9]         # imm[19:12]
                    binary_output += (bit_20 + bits_10_1 + bit_11 + bits_19_12 +
                                    data["REGISTER_MAP"][rd] +
                                    data["OPCODES"][instruction])
                else:
                    label = list_line_sep[2]
                    newprogramcounter = -4
                    with open(inputfile, "r") as temp_file:
                        for line in temp_file:
                            newprogramcounter += 4
                            line = line.strip()
                            listlinesep = line.split(" ")
                            for i in range(len(listlinesep)):
                                listlinesep[i] = listlinesep[i].strip(',')
                                if ',' in listlinesep[-1]:
                                    neww = listlinesep[i].split(',')
                                    listlinesep.pop(-1)
                                    for i in neww:
                                        listlinesep.append(i)
                            if listlinesep[0][:-1] == label:
                                break
                    offset_encoding = (newprogramcounter - program_counter) // 2
                    newimm = convert20bit(offset_encoding)
                    rd = list_line_sep[1]
                    bit_20    = newimm[0]
                    bits_10_1 = newimm[10:20]
                    bit_11    = newimm[9]
                    bits_19_12= newimm[1:9]
                    binary_output += (bit_20 + bits_10_1 + bit_11 + bits_19_12 +
                                    data["REGISTER_MAP"][rd] +
                                    data["OPCODES"][instruction])
      

        s+=binary_output+"\n"
    with open(outputfile,"w") as shit:
        shit.write(s)

        
        

          
