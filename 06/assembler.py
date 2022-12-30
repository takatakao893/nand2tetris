from parser import *
from symbol_table import SymbolTable
import code_writer
import re
import argparse
import os.path

symbol_pattern = re.compile(r'([0-9]+)|([0-9a-zA-Z_\.\$:]+)')

def int2bin(value, bitnum):
    bin_value = bin(value)[2:]
    if len(bin_value) > bitnum:
        raise Exception('Over binary size')
    return "0" * (bitnum - len(bin_value)) + bin_value

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('asm_file', type=str, help='asm file')

    args = parser.parse_args()
    asm_file = args.asm_file

    save_file = os.path.splitext(asm_file)[0] + ".hack"

    st = SymbolTable()

    with Parser(asm_file) as parser:

        op_address = 0

        while parser.advance() != None:
            cmd_type = parser.command_type()
            if cmd_type == A_COMMAND or cmd_type == C_COMMAND:
                op_address += 1
            elif cmd_type == L_COMMAND:
                st.add_entry(parser.symbol(), op_address)

    with Parser(asm_file) as parser:

        with open(save_file, 'w') as wf:

            while parser.advance() != None:

                cmd_type = parser.command_type()

                if cmd_type == A_COMMAND:
                    symbol = parser.symbol()
                    matched = symbol_pattern.match(symbol)

                    if matched.group(1):  
                        bincode = "0" + int2bin(int(matched.group(1)), 15)
                    elif matched.group(2):  
                        symbol = matched.group(2)
                        if st.contains(symbol):
                            address = st.get_address(symbol)
                            bincode = "0" + int2bin(address, 15)
                        else:
                            st.add_address(symbol)
                            address = st.get_address(symbol)
                            bincode = "0" + int2bin(address, 15)

                elif cmd_type == C_COMMAND:
                    bincode = '111' + code_writer.comp(parser.comp()) + code_writer.dest(parser.dest()) + code_writer.jump(parser.jump())

                if cmd_type != L_COMMAND:
                    wf.write(bincode + '\n')


if __name__ == '__main__':
    main()
