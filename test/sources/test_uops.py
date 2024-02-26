#!/usr/bin/env python3
"""tests for the uops package"""
from python_x86_information.sources.uops import CCTX, get_intr_uop_information, get_intr_uop_matches, \
    get_intr_uop_extended_information


def test_get_intr_uop_matches_adc():
    """test the `get_intr_uop_matches` function on the `adc` instruction"""
    tmp = get_intr_uop_matches(CCTX, "adc", ["r64", "m64"], True)
    assert isinstance(tmp, list)
    tmp = tmp[0]
    assert isinstance(tmp, dict)
    assert tmp["extension"] == "BASE"

    tmp = get_intr_uop_matches(CCTX, "adc", ["r64", "r64"], False)
    assert isinstance(tmp, list)
    tmp = get_intr_uop_matches(CCTX, "adc", ["r64", "r64"], True)
    assert isinstance(tmp, list)
    tmp = tmp[0]
    assert isinstance(tmp, dict)
    assert tmp["extension"] == "BASE"

    tmp = get_intr_uop_matches(CCTX, "adc", ["r64", "rax"])
    assert isinstance(tmp, list)
    tmp = tmp[0]
    assert isinstance(tmp, dict)
    assert tmp["extension"] == "BASE"

    tmp = get_intr_uop_matches(CCTX, "adc", target_form="r64, rax")
    assert isinstance(tmp, list)
    tmp = tmp[0]
    assert isinstance(tmp, dict)
    assert tmp["extension"] == "BASE"
    return


def test_get_intr_uop_matches_vpermps():
    """test the `get_intr_uop_matches` function on the `adc` instruction"""
    tmp = get_intr_uop_matches(CCTX, "vpermps", ["ymm", "ymm", "ymm"])
    assert isinstance(tmp, list)
    tmp = tmp[0]
    assert isinstance(tmp, dict)
    assert tmp["extension"] == "AVX2"
    return


def test_get_intr_uop_information_adc():
    """ test """
    instruction, throughput, latency = get_intr_uop_information("adc", ["r64", "rax"])
    assert throughput == [0.5, 0.5]
    assert latency == [1.0, 1.0]

    instruction, throughput, latency = get_intr_uop_information("adc", ["r64", "m64"])
    assert throughput == [0.5]
    assert latency == [1.0]


def test_get_intr_uop_information_vperm2i128():
    """ test """
    instruction, throughput, latency = get_intr_uop_information("vperm2i128",
                                                                ["ymm", "ymm", "m256", "i8"])
    assert throughput == [1.0]
    assert latency == [3.0]

    instruction, throughput, latency = get_intr_uop_information("vperm2i128", ["ymm", "ymm", "ymm", 0])
    assert throughput == [1.0]
    assert latency == [3.0]

    instruction, throughput, latency = get_intr_uop_information("vperm2i128",
                                                                ["ymm", "ymm", "ymm", "imm8"], exact=False)
    assert throughput == [1.0, 1.0]
    assert latency == [3.0, 3.0]
    instruction, throughput, latency = get_intr_uop_information("vperm2i128", "ymm, ymm, ymm, i8")
    assert throughput == [1.0]
    assert latency == [3.0]


def test_get_intr_uop_information_extended_adx():
    """ test """
    instruction, throughput, latency_min, latency_max = (
        get_intr_uop_extended_information("adc", ["r64", "rax"]))
    assert throughput == [0.5, 0.5]
    assert latency_min == [1.0, 1.0]
    assert latency_max == [1.0, 1.0]
