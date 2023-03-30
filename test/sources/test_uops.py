from python_x86_information.sources.uops import CCTX, get_intr_uop_information, get_intr_uop_matches, get_intr_uop_extended_information
import pprint

# TODO
def test_get_intr_uop_information():

    tmp = get_intr_uop_matches(CCTX, "adc", ["r64", "r64"], False)
    #pprint.pprint(tmp)
    tmp = get_intr_uop_matches(CCTX, "adc", ["r64", "rax"])
    #pprint.pprint(tmp)
    tmp = get_intr_uop_matches(CCTX, "vperm2i", ["ymm1", "ymm2", "2"])
    #instruction, throughput, latency = get_intr_uop_information("adc", ["r64", "rax"])
    #instruction, throughput, latency = get_intr_uop_information("vperm2i128", ["ymm", "ymm", "ymm", "i8"])
    #instruction, throughput, latency = get_intr_uop_information("vperm2i128", "ymm, ymm, ymm, imm8")
    #pprint.pprint(instruction)
    #pprint.pprint(throughput)
    #pprint.pprint(latency)

    instruction, throughput, latency = get_intr_uop_information("adc", ["r64", "rax"])
    pprint.pprint(instruction)
    pprint.pprint(throughput)
    pprint.pprint(latency)


    instruction, throughput, latency_min, latency_max = get_intr_uop_extended_information("adc", ["r64", "rax"])
    pprint.pprint(instruction)
    pprint.pprint(throughput)
    pprint.pprint(latency_min)
    pprint.pprint(latency_max)


if __name__ == "__main__":
    test_get_intr_uop_information()
