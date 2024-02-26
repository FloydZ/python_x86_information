from opcodes.x86_64 import read_instruction_set


def get_instruction_set():
    """
    one of the main entry points of this module from the package `opcodes`
    each entry looks like: {
        'name': 'ADCX',
        'summary': 'Unsigned Integer Addition of Two Operands with Carry Flag',
        'forms': [ADCX r32, r32, ADCX r32, m32, ADCX r64, r64, ADCX r64, m64]
    }

    INPUT:

    EXAMPLES::

        >>> from python_x86_information.sources.opcode import get_instruction_set
        >>> get_instruction_set()

    """
    # taken from: opcodes
    instruction_set = read_instruction_set()
    instruction_set = transform_instruction_set(instruction_set)
    return instruction_set


def transform_instruction_set(instruction_set):
    """
    SRC: https://github.com/Maratyszcza/Opcodes
    transform the list of instruction return by `instruction_set = read_instruction_set()`
    into a dictionary index by the instruction name.

    INPUT:

    - ``instruction_set`` -- output of `read_instruction_set()`

    EXAMPLES:

    """
    ret = {}
    for entry in instruction_set:
        name = entry.name.lower()
        if name not in ret.keys():
            ret[name] = {}

        # sometimes needed for debugging
        # print(entry.__dict__)
        ret[name] = entry
    return ret
