from pycca.asm import mkfunction

def exec_instructions(instr: Union[str, list[str]],
                      in_registers: dict[str, Any] = {},
                      out_registers: dict[str, Any] = {}):
    """
    SRC: https://github.com/pycca/pycca
    actually executes instructions


    instr:  list or string of assembly instrucitons
    in_registers
    NOTE: the input assembly code should and with a `ret` instruction, if not
        one is automatically appended.

    INPUT:
        - ``tech`` -- either None or an architecture

    EXAMPLES::

        >>> exec_instructions(["add rax, rbx"])

    """
    if type(instr) == list:
        instr = "\n".join(instr)

    # instr = """
    #         mov  eax, 0x1
    #         jmp  start
    #     end:
    #         ret
    #         mov  eax, 0x1
    #         mov  eax, 0x1
    #     start:
    #         mov  eax, 0xdeadbeef
    #         jmp  end
    #         mov  eax, 0x1
    # """

    # To set the registers with some input values we simpy mov the value into
    # via a `mov` instruction
    # TODO ok this is extremly X86 centered. Maybe this can be rewritten with
    # https://github.com/Maratyszcza/PeachPy
    registers_prepend = ""
    for key, item in in_registers.items():
        line = "mov " + key + ", " + str(item) + "\n"
        registers_prepend += line

    registers_prepend += "\n"

    # To get the values from the out register we again simply mov them
    # TODO thats going to be complicated.
    registers_postpone = ""

    # always append the ret, this is erally important
    registers_postpone += "\nret\n"

    # put evertyhing together
    cmd = registers_prepend + str(instr) + registers_postpone
    # print(cmd)

    # now generate the code
    fn = mkfunction(cmd)

    # Tell ctypes how to interpret the return value
    fn.restype = ctypes.c_uint64
    val = fn()
    return val
