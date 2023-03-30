from python_x86_information.instruction import *

def test_arch():
    Instruction.set_arch("ZEN")
    ins = Instruction("adc", ["r64", "r64"])