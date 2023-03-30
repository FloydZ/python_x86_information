from python_x86_information import get_intrinsics_guide

def test1():
    """
    test.in Intel intrinsic guide, by simply requesting only a instruction
    """
    intel = get_intrinsics_guide()
    assert len(intel["adc"]) == 2

def test2():
    tmp = find_in_instruction_set(CCTX_INTEL, "vpermq", ["ymm1", "ymm2", "1"])
