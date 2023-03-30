#! /usr/bin/python3
import ctypes
import logging
from typing import Union, Any
from .sources.uops import ALL_ARCHES as ARCHES, TRANSLATION_REGISTERS, get_intr_uop_information



# original code from: https://github.com/Maratyszcza/Opcodes/blob/master/opcodes/x86_64.py
# adapted by floydZ
class Operand:
    """An explicit instruction operand.
    :ivar type: the type of the instruction operand. Possible values are:
        "1"
            The constant value `1`.
        "3"
            The constant value `3`.
        "al"
            The al register.
        "ax"
            The ax register.
        "eax"
            The eax register.
        "rax"
            The rax register.
        "cl"
            The cl register.
        "xmm0"
            The xmm0 register.
        "rel8"
            An 8-bit signed offset relative to the address of instruction end.
        "rel32"
            A 32-bit signed offset relative to the address of instruction end.
        "imm4"
            A 4-bit immediate value.
        "imm8"
            An 8-bit immediate value.
        "imm16"
            A 16-bit immediate value.
        "imm32"
            A 32-bit immediate value.
        "imm64"
            A 64-bit immediate value.
        "r8"
            An 8-bit general-purpose register (al, bl, cl, dl, sil, dil, bpl, spl, r8b-r15b).
        "r16"
            A 16-bit general-purpose register (ax, bx, cx, dx, si, di, bp, sp, r8w-r15w).
        "r32"
            A 32-bit general-purpose register (eax, ebx, ecx, edx, esi, edi, ebp, esp, r8d-r15d).
        "r64"
            A 64-bit general-purpose register (rax, rbx, rcx, rdx, rsi, rdi, rbp, rsp, r8-r15).
        "mm"
            A 64-bit MMX SIMD register (mm0-mm7).
        "xmm"
            A 128-bit XMM SIMD register (xmm0-xmm31).
        "xmm{k}"
            A 128-bit XMM SIMD register (xmm0-xmm31), optionally merge-masked by an AVX-512 mask register (k1-k7).
        "xmm{k}{z}"
            A 128-bit XMM SIMD register (xmm0-xmm31), optionally masked by an AVX-512 mask register (k1-k7).
        "ymm"
            A 256-bit YMM SIMD register (ymm0-ymm31).
        "ymm{k}"
            A 256-bit YMM SIMD register (ymm0-ymm31), optionally merge-masked by an AVX-512 mask register (k1-k7).
        "ymm{k}{z}"
            A 256-bit YMM SIMD register (ymm0-ymm31), optionally masked by an AVX-512 mask register (k1-k7).
        "zmm"
            A 512-bit ZMM SIMD register (zmm0-zmm31).
        "zmm{k}"
            A 512-bit ZMM SIMD register (zmm0-zmm31), optionally merge-masked by an AVX-512 mask register (k1-k7).
        "zmm{k}{z}"
            A 512-bit ZMM SIMD register (zmm0-zmm31), optionally masked by an AVX-512 mask register (k1-k7).
        "k"
            An AVX-512 mask register (k0-k7).
        "k{k}"
            An AVX-512 mask register (k0-k7), optionally merge-masked by an AVX-512 mask register (k1-k7).
        "m"
            A memory operand of any size.
        "m8"
            An 8-bit memory operand.
        "m16"
            A 16-bit memory operand.
        "m16{k}{z}"
            A 16-bit memory operand, optionally masked by an AVX-512 mask register (k1-k7).
        "m32"
            A 32-bit memory operand.
        "m32{k}"
            A 32-bit memory operand, optionally merge-masked by an AVX-512 mask register (k1-k7).
        "m32{k}{z}"
            A 32-bit memory operand, optionally masked by an AVX-512 mask register (k1-k7).
        "m64"
            A 64-bit memory operand.
        "m64{k}"
            A 64-bit memory operand, optionally merge-masked by an AVX-512 mask register (k1-k7).
        "m64{k}{z}"
            A 64-bit memory operand, optionally masked by an AVX-512 mask register (k1-k7).
        "m80"
            An 80-bit memory operand.
        "m128"
            A 128-bit memory operand.
        "m128{k}{z}"
            A 128-bit memory operand, optionally masked by an AVX-512 mask register (k1-k7).
        "m256"
            A 256-bit memory operand.
        "m256{k}{z}"
            A 256-bit memory operand, optionally masked by an AVX-512 mask register (k1-k7).
        "m512"
            A 512-bit memory operand.
        "m512{k}{z}"
            A 512-bit memory operand, optionally masked by an AVX-512 mask register (k1-k7).
        "m64/m32bcst"
            A 64-bit memory operand or a 32-bit memory operand broadcasted to 64 bits {1to2}.
        "m128/m32bcst"
            A 128-bit memory operand or a 32-bit memory operand broadcasted to 128 bits {1to4}.
        "m256/m32bcst"
            A 256-bit memory operand or a 32-bit memory operand broadcasted to 256 bits {1to8}.
        "m512/m32bcst"
            A 512-bit memory operand or a 32-bit memory operand broadcasted to 512 bits {1to16}.
        "m128/m64bcst"
            A 128-bit memory operand or a 64-bit memory operand broadcasted to 128 bits {1to2}.
        "m256/m64bcst"
            A 256-bit memory operand or a 64-bit memory operand broadcasted to 256 bits {1to4}.
        "m512/m64bcst"
            A 512-bit memory operand or a 64-bit memory operand broadcasted to 512 bits {1to8}.
        "vm32x"
            A vector of memory addresses using VSIB with 32-bit indices in XMM register.
        "vm32x{k}"
            A vector of memory addresses using VSIB with 32-bit indices in XMM register merge-masked by an AVX-512 mask
            register (k1-k7).
        "vm32y"
            A vector of memory addresses using VSIB with 32-bit indices in YMM register.
        "vm32y{k}"
            A vector of memory addresses using VSIB with 32-bit indices in YMM register merge-masked by an AVX-512 mask
            register (k1-k7).
        "vm32z"
            A vector of memory addresses using VSIB with 32-bit indices in ZMM register.
        "vm32z{k}"
            A vector of memory addresses using VSIB with 32-bit indices in ZMM register merge-masked by an AVX-512 mask
            register (k1-k7).
        "vm64x"
            A vector of memory addresses using VSIB with 64-bit indices in XMM register.
        "vm64x{k}"
            A vector of memory addresses using VSIB with 64-bit indices in XMM register merge-masked by an AVX-512 mask
            register (k1-k7).
        "vm64y"
            A vector of memory addresses using VSIB with 64-bit indices in YMM register.
        "vm64y{k}"
            A vector of memory addresses using VSIB with 64-bit indices in YMM register merge-masked by an AVX-512 mask
            register (k1-k7).
        "vm64z"
            A vector of memory addresses using VSIB with 64-bit indices in ZMM register.
        "vm64z{k}"
            A vector of memory addresses using VSIB with 64-bit indices in ZMM register merge-masked by an AVX-512 mask
            register (k1-k7).
        "{sae}"
            Suppress-all-exceptions modifier. This operand is optional and can be omitted.
        "{er}"
            Embedded rounding control. This operand is optional and can be omitted.
    :ivar is_input: indicates if the instruction reads the variable specified by this operand.
    :ivar is_output: indicates if the instruction writes the variable specified by this operand.
    :ivar extended_size: for immediate operands the size of the value in bytes after size-extension.
        The extended size affects which operand values can be encoded. E.g. a signed imm8 operand would normally \
        encode values in the [-128, 127] range. But if it is extended to 4 bytes, it can also encode values in \
        [2**32 - 128, 2**32 - 1] range.
    """

    immediates = ["imm4", "imm8", "imm16", "imm32", "imm64", "i4", "i8", "i16", "i32", "i64"]
    memory = ["m", "m8", "m16", "m32", "m64", "m80", "m128", "m256", "m512",
                   "m64/m32bcst", "m128/m32bcst", "m256/m32bcst", "m512/m32bcst",
                   "m128/m64bcst", "m256/m64bcst", "m512/m64bcst",
                   "vm32x", "vm32y", "vm32z", "vm64x", "vm64y", "vm64z"]
    registers1 = list(TRANSLATION_REGISTERS.keys())
    registers2 = ["al", "cl", "ax", "eax", "rax", "xmm0", "r8", "r16", "r32", "r64", "r8l", "r16l", "r32l", "mm",
                   "xmm", "ymm", "zmm", "k"]

    registers = registers2 + registers1

    def __init__(self, name: str):
        self.is_input = False
        self.is_output = False
        self.extended_size = None
        self.name = name

    def __str__(self):
        """Return string representation of the operand type and its read/write attributes"""
        return {
            (False, False): self.type,
            (True, False): "[in] " + self.type,
            (False, True): "[out] " + self.type,
            (True, True): "[in/out] " + self.type
        }[(self.is_input, self.is_output)]

    def __repr__(self):
        return str(self)

    @property
    def is_variable(self):
        """Indicates whether this operand refers to a variable (i.e. specifies either a register or a memory location)"""
        return self.is_input or self.is_output

    @property
    def is_register(self):
        """Indicates whether this operand specifies a register"""
        return self.name.replace("{k}{z}", "").replace("{k}", "") \
               in registers

    @property
    def is_memory(self):
        """Indicates whether this operand specifies a memory location"""
        return self.name.replace("{k}{z}", "").replace("{k}", "") \
               in Operand.memory

    @property
    def is_immediate(self):
        """Indicates whether this operand is an immediate constant"""
        return self.name in Operand.immediates

    @staticmethod
    def from_str():
        """
        creates an operand object from a string

        Returns:

        INPUT:


        EXAMPLES:

            >>> TODO

        """
        pass


# original code from: https://github.com/Maratyszcza/Opcodes/blob/master/opcodes/x86_64.py
# adapted by floydZ
class Instruction:
    """
    Instruction form is a combination of mnemonic name and operand types.
    An instruction form may have multiple possible encodings.
    :ivar name: instruction name in PeachPy, NASM and YASM assemblers.
    :ivar gas_name: instruction form name in GNU assembler (gas).
    :ivar go_name: instruction form name in Go/Plan 9 assembler (8a).
        None means instruction is not supported in Go/Plan 9 assembler.
    :ivar mmx_mode: MMX technology state required or forced by this instruction. Possible values are:
        "FPU"
            Instruction requires the MMX technology state to be clear.
        "MMX"
            Instruction causes transition to MMX technology state.
        None
            Instruction neither affects nor cares about the MMX technology state.
    :ivar xmm_mode: XMM registers state accessed by this instruction. Possible values are:
        "SSE"
            Instruction accesses XMM registers in legacy SSE mode.
        "AVX"
            Instruction accesses XMM registers in AVX mode.
        None
            Instruction does not affect XMM registers and does not change XMM registers access mode.
    :ivar cancelling_inputs: indicates that the instruction form has not dependency on the values of input operands
        when they refer to the same register. E.g. **VPXOR xmm1, xmm0, xmm0** does not depend on *xmm0*.
        Instruction forms with cancelling inputs have only two input operands, which have the same register type.
    :ivar operands: a list of :class:`Operand` objects representing the instruction operands.
    :ivar implicit_inputs: a set of register names that are implicitly read by this instruction.
    :ivar implicit_outputs: a set of register names that are implicitly written by this instruction.
    :ivar isa_extensions: a list of :class:`ISAExtension` objects that represent the ISA extensions required to execute
        the instruction.
    :ivar encodings: a list of :class:`Encoding` objects representing the possible encodings for this instruction.
    :ivar throughput
    :ivar latency
    """


    """
    Global architecture:
    Each `Instruction` object will query information based on this value. So make sure to set it to a correct value
    before you are starting. 
    """
    ARCH = "zen2"

    def __init__(self, name: str, operands: Union[str, list[str], Operand, list[Operand], None] = None):
        """

        INPUT:
        - ``name`` -- mnemonic of the instruction
        - ``operands`` -- operands, can be in the following form:
                ["rax", "rbx"]
                ["r64", "r64"]
                "rax, r64"
                "rbx, rcx"
                Operand
                [Operand, ...]

        EXAMPLES:

            >>> TODO

        """
        self.name = name
        self.gas_name = None
        self.go_name = None
        self.mmx_mode = None
        self.xmm_mode = None
        self.cancelling_inputs = None
        self.operands = []
        self.implicit_inputs = set()
        self.implicit_outputs = set()
        self.isa_extensions = []
        self.encodings = []


        self.throughput = -1
        self.latency = -1

        if type(operands) == str:
            # operands in the form "rax,rbx" must be split
            if "," in operands:
                self.operands = [Operand.from_str(op) for op in operands.split(",")]
            else:
                self.operands = [Operand.from_str(operands)]

        if type(operands) == list[str]:
            self.operands = [Operand.from_str(operand) for operand in operands]

        if type(operands) == Operand:
            self.operands = [operands]

        if type(operands) == list[Operand]:
            self.operands = operands

        _, throughput, latency = get_intr_uop_infomation(name, [op.name for op in self.operands])
        if type(throughput) == list:
            assert len(throughput) == len(latency)
            logging.warning("found multiple instructions for ", name)
            throughput = throughput[0]
            latency = latency[0]

        self.throughput = throughput
        self.latency = latency

    def __str__(self):
        """Returns string representation of the instruction form and its operands in Intel-style assembly"""
        if self.operands:
            return self.name + " " + ", ".join(operand.type for operand in self.operands)
        else:
            return self.name

    def __repr__(self):
        return str(self)

    def nr_operands(self) -> int:
        return len(self.operands)

    @classmethod
    def set_arch(cls, arch: str):
        if arch not in ARCHES:
            logging.warning("wrong arch", arch)
            return

        cls.ARCH = arch


class SequenceOfInstructions:
    """
    Collection information about a sequence of instructions.

    :ivar throughput
    :ivar latency
    """
    def __init__(self, instructions: Union[list[str], list[Instruction]]):
        """
        INPUT:
        - ``instructions`` -- sequence of instructions, can be of the form:
            ["mov rax, rbx",
             "mov rbx, rcx",
             ...]

            [Instruction1: Instructions,
             Instruction2]

        EXAMPLES:

            >>> TODO

        """
        self.instructions = []
        # TODO get this from llvm-mci or uiCA 
        self.throughput = -1
        self.latency = -1

        if type(instructions) == list[str]:
            self.instructions = [Instruction(instr) for instr in instructions]

        self.instructions =instructions

