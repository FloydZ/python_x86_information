#!/usr/bin/env python3
"""test the information source `opcodes`"""

from python_x86_information.sources.opcode import get_instruction_set


def test1():
    """ tests the given instructions from the python packages `opcodes`
    """
    bla = get_instruction_set()
    assert bla
