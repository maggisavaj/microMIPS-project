import sys


op_codes = {
    "000000": "add",
    "000000": "sub",
    "000000": "and",
    "000000": "or",
    "000000": "slt",
    "100011": "lw",
    "101011": "sw",
    "000100": "beq",
    "000101": "bne",
    "000000": "emptyregs",
    "000000": "flip",
    "000000": "sleep",
    "000000": "rand",
    "000000": "push",
    "000000": "pop",
    "000000": "mod",
    "000000": "stimer",
    "010100": "ranmult",
    "010101": "popcount",
    "010110": "rotr",
    "001000" : "addi",
    "010111" : "printint",
}
func_codes = {
    "100000": "add",
    "100010": "sub",
    "100100": "and",
    "100101": "or",
    "101010": "slt",
    "000000": "ranmult",
    "000000": "popcount",
    "000000": "rotr",
    "010100": "emptyregs",
    "010101": "flip",
    "010110": "sleep",
    "010111": "rand",
    "011100": "push",
    "011101": "pop",
    "011110": "mod",
    "011111": "stimer",
    "000000" : "addi",
    "000000" : "printint",


}
registers = {
    "00000": "$r0",
    "01001": "$r1",
    "01010": "$r2",
    "01011": "$r3",
    "01100": "$r4",
    "01101": "$r5",
    "01110": "$r6",
    "01111": "$r7",
    "10000": "$r8",
    "10001": "$r9",
    "10010": "$r10",
    "10011": "$r11",
    "10100": "$r12",
    "10101": "$r13",
    "10110": "$r14",
    "10111": "$r15",
    "00010" : "$v0",
    "11001": "$rem",
    "11010": "$rnd",
    "11011": "$status",
    "11100": "$gp",
    "11101": "$sp",
    "11110": "$fp",
    "11111": "$ra",
    "11000": "$time",
}

labels = dict()

def handle_lines(bin_file: str):
    input_file = open(bin_file, "r")
    line = input_file.readlines()[0].strip()
    mips_instructions = bin_to_mips(line)
    output_file = open("BACK_TO_MIPS.txt", "w")
    for instruction in mips_instructions:
        output_file.write(instruction)
        output_file.write("\n")


def bin_to_mips(line):
    global labels
    mips = []
    bit_string = ""
    for i in range(0, len(line)):
        bit_string += line[i]
        if len(bit_string) == 32:
            op_code = bit_string[0:6]
            print(op_code)

            if op_code == "000000":
                rs, rt, rd, shift, func_code = (
                    bit_string[6:11],
                    bit_string[11:16],
                    bit_string[16:21],
                    bit_string[21:26],
                    bit_string[26:32],
                )
                if func_codes[func_code] == "pop":
                    mips.append(
                        f"{func_codes[func_code]} {registers[rd]}"
                    )
                elif func_codes[func_code] == "push":
                    mips.append(
                        f"{func_codes[func_code]} {registers[rs]}"
                    )
                elif func_codes[func_code] == "mod":
                    mips.append(
                        f"{func_codes[func_code]} {registers[rs]}, {registers[rt]}"
                    )
                elif func_codes[func_code] == "stimer":
                    mips.append(
                        f"{func_codes[func_code]}"
                    )
                elif func_codes[func_code] == "emptyregs":
                    mips.append(
                        f"{func_codes[func_code]}"
                    )
                elif func_codes[func_code] == "flip":
                    mips.append(
                        f"{func_codes[func_code]} {registers[rd]}, {registers[rs]}"
                    )
                elif func_codes[func_code] == "rand":
                    mips.append(
                        f"{func_codes[func_code]} {registers[rd]}, {registers[rs]}"
                    )
                elif func_codes[func_code] == "sleep":
                    mips.append(
                        f"{func_codes[func_code]} {registers[rs]}"
                    )
                else:
                    mips.append(
                        f"{func_codes[func_code]} {registers[rd]}, {registers[rs]}, {registers[rt]}"
                    )
            elif op_codes[op_code] == "addi":
                rs, rd, immediate = (
                    bit_string[6:11],
                    bit_string[11:16],
                    bit_string[17:32]
                )
                mips.append(
                    f"{op_codes[op_code]} {registers[rd]}, {registers[rs]}, {int(immediate, 2)}"
                )
            elif op_codes[op_code] == "beq":
                print("test")
                rs, rt, offset = bit_string[6:11], bit_string[11:16], bit_string[16:32]
                mips.append(
                    f"{op_codes[op_code]} {registers[rs]}, {registers[rt]}, {int(offset, 2)}"
                )
            
            elif op_codes[op_code] == "printint":
                rs, rt, rd, shift, func_code = (
                    bit_string[6:11],
                    bit_string[11:16],
                    bit_string[16:21],
                    bit_string[21:26],
                    bit_string[26:32],
                )
                mips.append(
                    f"{func_codes[func_code]} {registers[rs]}"
                )

            elif op_code not in ["100011", "101011"]:
                rs, rt, rd, shift, func_code = (
                    bit_string[6:11],
                    bit_string[11:16],
                    bit_string[16:21],
                    bit_string[21:26],
                    bit_string[26:32],
                )
                if op_codes[op_code] == "ranmult":
                    mips.append(
                        f"{op_codes[op_code]} {registers[rd]}"
                    )
                elif op_codes[op_code] == "popcount":
                    mips.append(
                        f"{op_codes[op_code]} {registers[rd]}, {registers[rs]}"
                    )
                elif op_codes[op_code] == "rotr":
                    mips.append(
                        f"{op_codes[op_code]} {registers[rd]}, {registers[rs]}, {registers[rt]}"
                    )

            elif op_code in ["100011", "101011"]:
                rs, rt, offset = bit_string[6:11], bit_string[11:16], bit_string[16:32]
                mips.append(
                    f"{op_codes[op_code]} {registers[rt]}, {int(offset, 2)}({registers[rs]})"
                )



            bit_string = ""
    return mips


if __name__ == "__main__":
    # handle_lines(sys.argv[1])
    handle_lines("program7.bin")
