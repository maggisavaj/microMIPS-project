import sys
import os


op_codes = {
    "add": "000000",
    "sub": "000000",
    "and:": "000000",
    "or:": "000000",
    "slt": "000000",
    "lw": "100011",
    "sw": "101011",
    "beq": "000100",
    "bne": "000100",
    "emptyregs" : "000000",
    "flip" : "000000",
    "sleep" : "000000",
    "rand" : "000000",
    "push" : "000000",
    "pop" : "000000",
    "mod" : "000000",
    "stimer" : "000000",
    "addi" : "001000",
    "li" : "001000",
    "ranmult" : "010100",
    "popcount" : "010101",
    "rotr" : "010110",
    "printint" : "010111",
}
func_codes = {
    "add": "100000",
    "sub": "100010",
    "and:": "100100",
    "or:": "100101",
    "slt": "101010",
    "emptyregs" : "010100",
    "flip" : "010101",
    "sleep" : "010110",
    "rand" : "010111",
    "push" : "011100",
    "pop" : "011101",
    "mod" : "011110",
    "stimer" : "000000",
    "addi" : "000000",
    "li" : "001000",
    "ranmult" : "000000",
    "popcount" : "000000",
    "rotr" : "000000",
    "printint" : "000000",

}
registers = {
    "$r0": "00000",
    "$r1": "01001",
    "$r2": "01010",
    "$r3": "01011",
    "$r4": "01100",
    "$r5": "01101",
    "$r6": "01110",
    "$r7": "01111",
    "$r8": "10000",
    "$r9": "10001",
    "$r10": "10010",
    "$r11": "10011",
    "$r12": "10100",
    "$r13": "10101",
    "$r14": "10110",
    "$r15": "10111",
    "$time": "11000",
    "$rem": "11001",
    "$rnd": "11010",
    "$status": "11011",
    "$gp": "11100",
    "$sp": "11101",
    "$fp": "11110",
    "$ra": "11111",
    "$v0": "00010"

}

labels = dict()

shift_logic_amount = "00000"

line_address = 0


def interpret_line(mips_file: str):
    global line_address
    input_file = open(mips_file, "r")
    output_file = open("program2.bin", "w")
    for instruction in input_file:
        bin = assemble(instruction)
        line_address += 4
        output_file.write(bin)


def assemble(line):
    line = line.split("#")[0].strip()

    if not line:
        return

    parts = line.split(" ")
    op_code = parts[0]

    if op_code in ["emptyregs", "stimer"]:
        return (
            "00000000000000000000000000" + func_codes[op_code]
        )
    
    elif op_code in ["push", "sleep", "printint"]:

        rs = parts[1]

        return (
            op_codes[op_code]
            + registers[rs]
            + "00000"
            + "00000"
            + "00000"
            + func_codes[op_code]
        )
    
    elif op_code in ["flip", "rand", "popcount"]:
        rd, rs = (
            parts[1].replace(",", ""),
            parts[2].replace(",", ""),
        )

        return (
            op_codes[op_code]
            + registers[rs]
            + "00000"
            + registers[rd]
            + shift_logic_amount
            + func_codes[op_code]
        )
    
    elif op_code in ["ranmult", "pop"]:
        rd = parts[1]
        return (
            op_codes[op_code]
            + "00000"
            + "00000"
            + registers[rd]
            + "00000"
            + func_codes[op_code]
        )
    
    elif op_code in ["mod", "pop"]:
        rs, rt = (
            parts[1].replace(",", ""),
            parts[2].replace(",", ""),
        )
        return (
            op_codes[op_code]
            + registers[rs]
            + registers[rt]
            + "00000"
            + "00000"
            + func_codes[op_code]
        )
    
    elif op_code in ["addi"]:
        rs, rt, immediate = (
            parts[1].replace(",", ""),
            parts[2].replace(",", ""),
            parts[3].replace(",", ""),
        )

        return (
            op_codes[op_code]
            + registers[rs]
            + registers[rt]
            + bin(int(immediate)).replace("0b", "").zfill(16)
        )
    elif op_code in ["li"]:
        rs, immediate = (
            parts[1].replace(",", ""),
            parts[2].replace(",", ""),
        )

        return (
            op_codes[op_code]
            + "00000"
            + registers[rs]
            + bin(int(immediate)).replace("0b", "").zfill(16)
        )

    elif op_code in func_codes:
        rd, rs, rt = (
            parts[1].replace(",", ""),
            parts[2].replace(",", ""),
            parts[3].replace(",", ""),
        )
        return (
            op_codes[op_code]
            + registers[rs]
            + registers[rt]
            + registers[rd]
            + shift_logic_amount
            + func_codes[op_code]
        )
    
    if op_code in ["lw", "sw", "beq"]:
        if op_code == "lw" or op_code == "sw":
            rt = parts[1].replace(",", "")
            offset, rs = parts[2].replace(")", "").split("(")
            offset_bin = bin(int(offset)).replace("0b", "").zfill(16)
            return op_codes[op_code] + registers[rs] + registers[rt] + offset_bin
        else:
            rs, rt, offset = (
                parts[1].replace(",", ""),
                parts[2].replace(",", ""),
                parts[3].replace(",", ""),
            )
            offset_bin = bin(int(offset)).replace("0b", "").zfill(16)
            return op_codes[op_code] + registers[rs] + registers[rt] + offset_bin
    
    # handles labels
    op_code = op_code.replace(":", "") 



if __name__ == "__main__":
    # mips_file = sys.argv[1]
    mips_file = "test.mips"
    interpret_line(mips_file)
