#!/usr/bin/env python3
from python_x86_information.instructions import *



def test1():
    """
    test.in Intel intrinsic guide, by simply requesting only a instruction
    """
    intel = get_intrinsics_guide()
    assert len(intel["adc"]) == 2


def test_information():
    """
    test.in some specific versions of `adc``
    """
    r = information("adc")
    assert len(r) == 2

    r = information("adc", ["r64", "r64"])
    assert r == ""

    r = information("adc", ["r64", "rax"])
    assert r == ""

    r = information("adc", "rax, r64")
    assert r == ""

    r = information("adc", "rax,r64")
    assert r == ""

    r = information("adc", "rax, rbx")
    assert r == ""


if __name__ == "__main__":
    """
    """
    test1()
