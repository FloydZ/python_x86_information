#!/usr/bin/env python3
from instructions import *

def test1():
    """
    test intel intrinsic guide
    """
    intel = get_intrinsics_guide()
    assert len(intel["adc"]) == 2


if __name__ == "__main__":
    test1()
