from typing import Union
import xml.etree.ElementTree as ET
import re
import logging


# Helper dictionary to translate from registers names to generic names.
# NOTE:
#   The dictionary can also handle uppercase inputs
#   NOTE this only translates registers
# EXAMPLE:
#   "r64" = TRANSLATION["rax"]
#   "r16" = TRANSLATION["sp"]
TRANSLATION_REGISTERS = {
    "r8": "r8",
    "al": "r8",
    "ah": "r8",
    "bl": "r8",
    "bh": "r8",
    "cl": "r8",
    "ch": "r8",
    "dl": "r8",
    "dh": "r8",
    "bpl": "r8",
    "sil": "r8",
    "dil": "r8",
    "spl": "r8",
    "r8b": "r8",
    "r9b": "r8",
    "r10b": "r8",
    "r11b": "r8",
    "r12b": "r8",
    "r13b": "r8",
    "r14b": "r8",
    "r15b": "r8",

    "r16": "r16",
    "ax": "r16",
    "bx": "r16",
    "cx": "r16",
    "dx": "r16",
    "bp": "r16",
    "si": "r16",
    "di": "r16",
    "sp": "r16",
    "ip": "r16",
    "r8w": "r16",
    "r9w": "r16",
    "r10w": "r16",
    "r11w": "r16",
    "r12w": "r16",
    "r13w": "r16",
    "r14w": "r16",
    "r15w": "r16",

    "eax": "r32",
    "ebx": "r32",
    "ecx": "r32",
    "edx": "r32",
    "ebp": "r32",
    "esi": "r32",
    "edi": "r32",
    "esp": "r32",
    "eip": "r32",
    "r8d": "r32",
    "r9d": "r32",
    "r10d": "r32",
    "r11d": "r32",
    "r12d": "r32",
    "r13d": "r32",
    "r14d": "r32",
    "r15d": "r32",

    "r64": "r64",
    "rax": "r64",
    "rbx": "r64",
    "rcx": "r64",
    "rdx": "r64",
    "rbp": "r64",
    "rsi": "r64",
    "rdi": "r64",
    "rip": "r64",
    "r8d": "r64",
    "r9d": "r64",
    "r10d": "r64",
    "r11d": "r64",
    "r12d": "r64",
    "r13d": "r64",
    "r14d": "r64",
    "r15d": "r64",

    "mm0": "r64",
    "mm1": "r64",
    "mm2": "r64",
    "mm3": "r64",
    "mm4": "r64",
    "mm5": "r64",
    "mm6": "r64",
    "mm7": "r64",

    "xmm": "xmm",
    "xmm0": "xmm",
    "xmm1": "xmm",
    "xmm2": "xmm",
    "xmm4": "xmm",
    "xmm5": "xmm",
    "xmm6": "xmm",
    "xmm7": "xmm",
    "xmm8": "xmm",
    "xmm9": "xmm",
    "xmm10": "xmm",
    "xmm11": "xmm",
    "xmm12": "xmm",
    "xmm13": "xmm",
    "xmm14": "xmm",
    "xmm15": "xmm",

    "ymm": "ymm",
    "ymm0": "ymm",
    "ymm1": "ymm",
    "ymm2": "ymm",
    "ymm4": "ymm",
    "ymm5": "ymm",
    "ymm6": "ymm",
    "ymm7": "ymm",
    "ymm8": "ymm",
    "ymm9": "ymm",
    "ymm10": "ymm",
    "ymm11": "ymm",
    "ymm12": "ymm",
    "ymm13": "ymm",
    "ymm14": "ymm",
    "ymm15": "ymm",

    "zmm": "zmm",
    "zmm0": "zmm",
    "zmm1": "zmm",
    "zmm2": "zmm",
    "zmm4": "zmm",
    "zmm5": "zmm",
    "zmm6": "zmm",
    "zmm7": "zmm",
    "zmm8": "zmm",
    "zmm9": "zmm",
    "zmm10": "zmm",
    "zmm11": "zmm",
    "zmm12": "zmm",
    "zmm13": "zmm",
    "zmm14": "zmm",
    "zmm15": "zmm",
    "zmm16": "zmm",
    "zmm17": "zmm",
    "zmm18": "zmm",
    "zmm19": "zmm",
    "zmm20": "zmm",
    "zmm21": "zmm",
    "zmm22": "zmm",
    "zmm23": "zmm",
    "zmm24": "zmm",
    "zmm25": "zmm",
    "zmm26": "zmm",
    "zmm27": "zmm",
    "zmm28": "zmm",
    "zmm29": "zmm",
    "zmm30": "zmm",
    "zmm31": "zmm",

    # Uppercase
    "R8": "r8",
    "AL": "r8",
    "AH": "r8",
    "BL": "r8",
    "BH": "r8",
    "CL": "r8",
    "CH": "r8",
    "DL": "r8",
    "DH": "r8",
    "BPL": "r8",
    "SIL": "r8",
    "DIL": "r8",
    "SPL": "r8",
    "R8B": "r8",
    "R9B": "r8",
    "R10B": "r8",
    "R11B": "r8",
    "R12B": "r8",
    "R13B": "r8",
    "R14B": "r8",
    "R15B": "r8",

    "R16": "r16",
    "AX": "r16",
    "BX": "r16",
    "CX": "r16",
    "DX": "r16",
    "BP": "r16",
    "SI": "r16",
    "DI": "r16",
    "SP": "r16",
    "IP": "r16",
    "R8W": "r16",
    "R9W": "r16",
    "R10W": "r16",
    "R11W": "r16",
    "R12W": "r16",
    "R13W": "r16",
    "R14W": "r16",
    "R15W": "r16",

    "EAX": "r32",
    "EBX": "r32",
    "ECX": "r32",
    "EDX": "r32",
    "EBP": "r32",
    "ESI": "r32",
    "EDI": "r32",
    "ESP": "r32",
    "EIP": "r32",
    "R8D": "r32",
    "R9D": "r32",
    "R10D": "r32",
    "R11D": "r32",
    "R12D": "r32",
    "R13D": "r32",
    "R14D": "r32",
    "R15D": "r32",

    "R64": "r64",
    "RAX": "r64",
    "RBX": "r64",
    "RCX": "r64",
    "RDX": "r64",
    "RBP": "r64",
    "RSI": "r64",
    "RDI": "r64",
    "RIP": "r64",
    "R8D": "r64",
    "R9D": "r64",
    "R10D": "r64",
    "R11D": "r64",
    "R12D": "r64",
    "R13D": "r64",
    "R14D": "r64",
    "R15D": "r64",

    "MM0": "r64",
    "MM1": "r64",
    "MM2": "r64",
    "MM3": "r64",
    "MM4": "r64",
    "MM5": "r64",
    "MM6": "r64",
    "MM7": "r64",

    "XMM0": "xmm",
    "XMM1": "xmm",
    "XMM2": "xmm",
    "XMM4": "xmm",
    "XMM5": "xmm",
    "XMM6": "xmm",
    "XMM7": "xmm",
    "XMM8": "xmm",
    "XMM9": "xmm",
    "XMM10": "xmm",
    "XMM11": "xmm",
    "XMM12": "xmm",
    "XMM13": "xmm",
    "XMM14": "xmm",
    "XMM15": "xmm",

    "YMM0": "ymm",
    "YMM1": "ymm",
    "YMM2": "ymm",
    "YMM4": "ymm",
    "YMM5": "ymm",
    "YMM6": "ymm",
    "YMM7": "ymm",
    "YMM8": "ymm",
    "YMM9": "ymm",
    "YMM10": "ymm",
    "YMM11": "ymm",
    "YMM12": "ymm",
    "YMM13": "ymm",
    "YMM14": "ymm",
    "YMM15": "ymm",

    "ZMM0": "zmm",
    "ZMM1": "zmm",
    "ZMM2": "zmm",
    "ZMM4": "zmm",
    "ZMM5": "zmm",
    "ZMM6": "zmm",
    "ZMM7": "zmm",
    "ZMM8": "zmm",
    "ZMM9": "zmm",
    "ZMM10": "zmm",
    "ZMM11": "zmm",
    "ZMM12": "zmm",
    "ZMM13": "zmm",
    "ZMM14": "zmm",
    "ZMM15": "zmm",
    "ZMM16": "zmm",
    "ZMM17": "zmm",
    "ZMM18": "zmm",
    "ZMM19": "zmm",
    "ZMM20": "zmm",
    "ZMM21": "zmm",
    "ZMM22": "zmm",
    "ZMM23": "zmm",
    "ZMM24": "zmm",
    "ZMM25": "zmm",
    "ZMM26": "zmm",
    "ZMM27": "zmm",
    "ZMM28": "zmm",
    "ZMM29": "zmm",
    "ZMM30": "zmm",
    "ZMM31": "zmm",
}


TRANSLATION_IMMEDIATE = {
    "i8": "imm8",
    "i16": "imm16",
    "i32": "imm32",
    "i64": "imm64",
    "imm8": "imm8",
    "imm16": "imm16",
    "imm32": "imm32",
    "imm64": "imm64",
}

TRANSLATION = {}
TRANSLATION.update(TRANSLATION_IMMEDIATE)
TRANSLATION.update(TRANSLATION_REGISTERS)

# special translation dict for the intel dataset
INTEL_TRANSLATION = {
    "i8": "imm8",
    "i16": "imm16",
    "i32": "imm32",
    "i64": "imm64",
    "imm8": "imm8",
    "imm16": "imm16",
    "imm32": "imm32",
    "imm64": "imm64",
}

###############################################################################
## Info from uops.info ########################################################
###############################################################################


# All architectures measured by uops.info. This is just here for consistent
# ordering
ALL_ARCHES = ['CON', 'WOL', 'NHM', 'WSM', 'SNB', 'IVB', 'HSW', 'BDW', 'SKL',
              'SKX', 'KBL', 'CFL', 'CNL', 'ICL', 'ZEN+', 'ZEN2']

# Sentinel value for unknown latency
MAX_LATENCY = 1e100

class Context:
    """
    Helper class for parsing uops intrinsic guide.
    """
    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)


# Dummy obj
Table = Context

################################################################################
## Intrinsic/uops.info unification #############################################
################################################################################
INTR_ARG_REMAP = {
    'vm32x': 'vsib_xmm',
    'vm32y': 'vsib_ymm',
    'vm32z': 'vsib_zmm',
    'vm64x': 'vsib_xmm',
    'vm64y': 'vsib_ymm',
    'vm64z': 'vsib_zmm',
    'mib':   'm192',
    'imm8':  'i8',
}


# Extra argument options: intrinsic register args can match memory args of the
# same size, but not vice versa--if an intrinsic has a memory arg, it's generally
# a load/store etc. and requires memory
INTR_ARG_EXTRA = {
    'r16': {'m16', 'i16'},
    'r32': {'m32', 'i32'},
    'r64': {'m64', 'i64'},
    'r8':  {'m8', 'i8'},
    'i8':  {'r8'},  # Special case for ror/rol reg, cl
    'xmm': {'m128'},
    'ymm': {'m256'},
    'zmm': {'m512'},
}


UOP_ARG_REMAP = {
    'al':        'r8',
    'ax':        'r16',
    'cl':        'r8',
    'dx':        'r16',
    'eax':       'r32',
    'rax':       'r64',
    'm32_1to2':  'm64',
    'm32_1to4':  'm128',
    'm32_1to8':  'm256',
    'm32_1to16': 'm512',
    'm64_1to2':  'm128',
    'm64_1to4':  'm256',
    'm64_1to8':  'm512',
}


def parse_uops_info(path: str):
    """
    Parses `instructions.xml` from uops.info

    INPUT:
    - ``path`` -- path to the `instructions.xml` from `uops.info`. This file should
                  be automatically donwloaded by `setup.sh`. Alternativly you
                  can download it with:
                    wget https://www.uops.info/instructions.xml

    EXAMPLES::

        >>> from python_x86_information.sources.uops import parse_uops_info
        >>> _, table = parse_uops_info("deps/instructions.xml")
        >>> print(table)

    """
    root = ET.parse(path)

    version = root.getroot().attrib['date']

    uops_info = {}
    for ext in root.findall('extension'):
        extension = ext.attrib['name']
        for inst in ext.findall('instruction'):
            mnem = inst.attrib['asm'].lower()
            form = inst.attrib['string'].lower()
            arch_info = {}
            for arch in inst.findall('architecture'):
                arch_name = arch.attrib['name']
                for meas in arch.findall('measurement'):
                    ports = meas.attrib.get('ports', '')
                    ports = re.sub(r'\b1\*', '', ports)
                    if 'TP' in meas.attrib:
                        tp = meas.attrib['TP']
                    else:
                        tp = meas.attrib['TP_unrolled']

                    # Look through every operand->result latency measurement,
                    # and get the min/max. Each of min/max can be an upper
                    # bound, meaning the measurement method can't guarantee the
                    # "true" minimum latency, and it might actually be lower.
                    # We store these as (latency, is_exact) tuples, which sort
                    # in the right way to get the overall min/max.
                    lat_min = (MAX_LATENCY, True)
                    lat_max = (0, False)
                    for lat in meas.findall('latency'):
                        for attr, value in lat.attrib.items():
                            if 'upper_bound' in attr:
                                assert value == '1'
                            elif 'cycles' in attr:
                                is_exact = (
                                                   attr + '_is_upper_bound') not in lat.attrib
                                latency = (int(value), is_exact)
                                lat_min = min(lat_min, latency)
                                lat_max = max(lat_max, latency)
                            else:
                                assert attr in ('start_op', 'target_op')
                    arch_info[arch_name] = (ports, tp, (lat_min, lat_max))
            if not arch_info:
                continue

            # Strip out extra uops specifiers, like "lock", "{store}", etc.
            if ' ' in mnem:
                [prefix, mnem] = mnem.rsplit(None, 1)
                form = prefix + ' ' + form

            # Add a dict to hold all forms of this mnemonic
            # XXX We store the first extension here to use for sorting, though
            # not all forms have the same extension
            if mnem not in uops_info:
                uops_info[mnem] = {
                    'id': len(uops_info),
                    'mnem': mnem,
                    'extension': extension,
                    'forms': []
                }

            uops_info[mnem]['forms'].append({
                'form': form,
                'extension': extension,
                'search-key': (form + ' ' + extension).lower(),
                'arch': arch_info
            })

    # Update the search key for each instruction with all the forms
    for [mnem, uop] in uops_info.items():
        uop['search-key'] = ' '.join(f['search-key'] for f in uop['forms'])

    return [version, uops_info]


def get_intr_uop_matches(ctx: Context, mnem: str, target_form: Union[str, list[str]], exact=True):
    """
    Get a list of matching uop instruction forms for the given mnemonic
    Returns a list of matching instructions. If no instruction is found, an
    empty list is returned


    INPUT:
    - ``ctx`` -- context
    - ``mnem`` -- mnemonic to analyse
    - ``target_form`` -- arguments of the mnemonic
    - ``exact`` --

    EXAMPLES::

        >>> get_intr_uop_matches(CCTX, "adc", ["rax", "r64"])
        [ {'form': '{load} adc_11 (r64, r64)',
           'extension': 'BASE',
           'search-key': '{load} adc_11 (r64, r64) base',
           'arch': {'CON': ('2*p015', '1.00', ((1, True), (2, True))),
                    'WOL': ('2*p015', '1.00', ((1, True), (2, True))),
                    'NHM': ('2*p015', '1.00', ((1, True), (2, True))),
                    'WSM': ('2*p015', '1.00', ((1, True), (2, True))),
                    ....}}]

        >>> get_intr_uop_matches(CCTX, "adc", ["rax", "r64"], exact=False)
        []

        >>> get_intr_uop_matches(CCTX, "adc", ["r64", "r64"], exact=False)
        [{'form': 'adc (m64, r64)',
          'extension': 'BASE',
          'search-key': 'adc (m64, r64) base',
          'arch': {'CON': ('3*p015+p2+p3+p4', '2.00', ((1, True), (10, False))),
                   'WOL': ('3*p015+p2+p3+p4', '2.00', ((1, True), (10, False))),
                   'NHM': ('3*p015+p2+p3+p4', '2.00', ((1, True), (8, False))),
                   'WSM': ('3*p015+p2+p3+p4', '2.00', ((1, True), (8, False))),
                   ...}},
         {'form': '{load} adc_11 (r64, r64)',
          'extension': 'BASE',
          'search-key': '{load} adc_11 (r64, r64) base',
          'arch': {...
                   'ZEN+': ('', '0.50', ((1, True), (1, True))),
                   'ZEN2': ('', '0.50', ((1, True), (1, True))),
                   'ZEN3': ('', '0.50', ((1, True), (1, True))),
                   'ZEN4': ('', '0.50', ((1, True), (1, True)))}},
         {'form': 'adc (r64, m64)',
          'extension': 'BASE',
          'search-key': 'adc (r64, m64) base',
          'arch': {'CON': ('2*p015+p2', '1.00', ((2, True), (5, True))),
                   'WOL': ('2*p015+p2', '1.00', ((2, True), (5, True))),
                   'NHM': ('2*p015+p2', '1.00', ((3, True), (5, True))),
                   ...}},
        {'form': '{store} adc_13 (r64, r64)',
         'extension': 'BASE',
         'search-key': '{store} adc_13 (r64, r64) base',
         'arch': {'CON': ('2*p015', '1.00', ((1, True), (2, True))),
                  'WOL': ('2*p015', '1.00', ((1, True), (2, True))),
                  'NHM': ('2*p015', '1.00', ((1, True), (2, True))),
                  'WSM': ('2*p015', '1.00', ((1, True), (2, True))),
                  ...}}]
        {'form': 'lock adc_lock (m64, r64)',
         'extension': 'BASE',
         'search-key': 'lock adc_lock (m64, r64) base',
         'arch': {'CON': ('2*p015+p05+p2+2*p3+p4+p5', '21.00', ((13, True), (31, False))),
                  'WOL': ('2*p015+p2+2*p3+p4+2*p5', '21.00', ((13, True), (31, False))),
                  'NHM': ('3*p015+p2+p3+p4', '20.00', ((11, True), (28, False))),
                  'WSM': ('3*p015+p2+p3+p4', '19.00', ((11, True), (28, False))),
                  'SNB': ('5*p015+p05+p1+2*p23+p4+2*p5', '23.00', ((13, True), (34, False)))
                  ...}}]

    """
    # return value
    matching_forms = []

    # Create a set of matching arguments for each instruction argument
    intr_args = []

    if mnem not in ctx.uops_info:
        return []

    # translate to list
    if type(target_form) == str:
        target_form = target_form.split(',')

    for arg in target_form:

        # if the argumetn is a number replace it with i8
        if type(arg) == int:
            arg = "i8"
        else:
            try:
                arg = int(arg)
                arg = "i8"
            except:
                # Filter out some stuff and normalize
                arg = (arg.replace(' {z}', ', z')
                       .replace(' {k}', ', k')
                       .replace(' {er}', '')
                       .replace(' {sae}', '')
                       .replace(' ', ''))
                arg = TRANSLATION[arg]

        arg = INTR_ARG_REMAP.get(arg, arg)

        if not exact:
            # Add an extra option for register/memory matching
            arg_opts = {arg} | INTR_ARG_EXTRA.get(arg, set())
        else:
            arg_opts = {TRANSLATION[arg]}
        intr_args.append(arg_opts)

    # Loop through all uop forms with the same mnemonic
    for form in ctx.uops_info[mnem]['forms']:
        inst, _, inst_form = form['form'].rstrip(')').partition(' (')
        # Mask zeroing variants in AVX-512 are indicated by a _z suffix. In
        # that case, replace any mask arguments 'k' with 'z', which we used
        # in the intrinsic replacements above to indicate the zeroing variant.
        if '_z' in inst:
            assert inst.endswith('_z')
            inst_form = inst_form.replace('k,', 'z,')

        uops_args = [UOP_ARG_REMAP.get(arg, arg)
                     for arg in inst_form.split(', ')]

        if target_form != "":
            # See if any form of the intrinsic matches this form. Note that zip()
            # only iterates as far as the shortest of the arguments, so it will
            # allow mismatched lengths as long as the prefix matches. This actually
            # works in our favor, for intrinsics like _mm256_cmpge_epi8_mask that
            # don't show an immediate in the instruction, since the immediate is
            # implied by the intrinsic (i.e. _MM_CMPINT_NLT). OK maybe this isn't
            # always beneficial but it will only lead to false positives...
            # if all(arg in opts for [arg, opts] in zip(uops_args, intr_args)):
            #    matching_forms.append(form)
            same = True
            for i in range(len(uops_args)):
                # print(uops_args[i], intr_args[i], uops_args[i] not in intr_args[i])
                if uops_args[i] not in intr_args[i]:
                    same = False
                    break
            if same:
                matching_forms.append(form)
        else:
            matching_forms.append(form)

    return matching_forms





_, data_uops = parse_uops_info("deps/instructions.xml")
CCTX = Context(data_source="", uops_info=data_uops)

def get_intr_uop_information(mnem: str, target_form: Union[str, list[str]],
                             ARCH="ZEN2", exact=True):
    """
    Returns the instruction and expected cycles to execute the instruction on the
    given arch. If valid instructions are found, which maches the mnemonic ALL will be returned.

    Returns     instruction, throughput, latency
     on error:  None, None, None
    NOTE:
        the class `Instruction` is not supported.

    INPUT:
    - ``mnem`` -- mnemonic to analyse
    - ``target_form`` -- arguments of the mnemonic, e.g:
                ["rax", "rbx"]
                ["r64", "r64"]
                "rax, r64"
                "rbx, rcx"
    - ``ARCH`` -- architecture to base the analysis on
    - ``exact`` -- if true only exact matches of mnemoric argument are returned.

    EXAMPLES:

        >>> instruction, throughput, latency = get_intr_uop_cycles(CCTX, "adc", ["r64", "rax"])
        >>> print(instruction, cycles, latency)
        [{'arch': {'ADL-E': ('', '0.75', ((1, True), (2, True))),
                   'ADL-P': ('p06', '0.50', ((1, True), (1, True))),
                    ...
                   'ZEN4': ('', '0.50', ((1, True), (1, True)))},
          'extension': 'BASE',
          'form': '{load} adc_11 (r64, r64)',
          'search-key': '{load} adc_11 (r64, r64) base'},
         {'arch': {'ADL-E': ('', '0.75', ((1, True), (2, True))),
                   'ADL-P': ('p06', '0.50', ((1, True), (1, True))),
                    ...
                   'ZEN3': ('', '0.50', ((1, True), (1, True))),
                   'ZEN4': ('', '0.50', ((1, True), (1, True)))},
          'extension': 'BASE',
          'form': '{store} adc_13 (r64, r64)',
          'search-key': '{store} adc_13 (r64, r64) base'}]
        [0.5, 0.5]
        [1.0, 1.0]

    """
    if ARCH not in ALL_ARCHES:
        logging.warning("invalid arch")
        return None, None, None

    instr = get_intr_uop_matches(CCTX, mnem, target_form, exact)
    if len(instr) == 0:
        logging.info("no instruction found")
        return None, None, None

    throughput = [float(a['arch'][ARCH][1]) for a in instr]
    latency = [float(a['arch'][ARCH][2][0][0]) for a in instr]
    return instr, throughput, latency



def get_intr_uop_extended_information(mnem: str, target_form: Union[str, list[str]],
                             ARCH="ZEN2", exact=True):
    """
    Returns the instruction and expected cycles to execute the instruction on the
    given arch. If valid instructions are found, which maches the mnemonic, ALL will be returned.

    Returns     instruction, throughput, latency_min, latency_max
     on error:  None, None, None, None
    NOTE:
        the class `Instruction` is not supported.

    INPUT:
    - ``mnem`` -- mnemonic to analyse
    - ``target_form`` -- arguments of the mnemonic, e.g:
                ["rax", "rbx"]
                ["r64", "r64"]
                "rax, r64"
                "rbx, rcx"
    - ``ARCH`` -- architecture to base the analysis on
    - ``exact`` -- if true only exact matches of mnemoric argument are returned.

    EXAMPLES:

        >>> instruction, throughput, latency_min, latency_max = get_intr_uop_cycles(CCTX, "adc", ["r64", "rax"])
        >>> print(instruction, cycles, latency_min, latency_max)
        [{'arch': {'ADL-E': ('', '0.75', ((1, True), (2, True))),
                   'ADL-P': ('p06', '0.50', ((1, True), (1, True))),
                    ...
                   'ZEN4': ('', '0.50', ((1, True), (1, True)))},
          'extension': 'BASE',
          'form': '{load} adc_11 (r64, r64)',
          'search-key': '{load} adc_11 (r64, r64) base'},
         {'arch': {'ADL-E': ('', '0.75', ((1, True), (2, True))),
                   'ADL-P': ('p06', '0.50', ((1, True), (1, True))),
                    ...
                   'ZEN3': ('', '0.50', ((1, True), (1, True))),
                   'ZEN4': ('', '0.50', ((1, True), (1, True)))},
          'extension': 'BASE',
          'form': '{store} adc_13 (r64, r64)',
          'search-key': '{store} adc_13 (r64, r64) base'}]
        [0.5, 0.5]
        [1.0, 1.0]
        [1.0, 1.0]

    """
    if ARCH not in ALL_ARCHES:
        logging.warning("invalid arch")
        return None, None, None, None

    instr = get_intr_uop_matches(CCTX, mnem, target_form, exact)
    if len(instr) == 0:
        logging.info("no instruction found")
        return None, None, None, None

    throughput = [float(a['arch'][ARCH][1]) for a in instr]
    latency_min = [float(a['arch'][ARCH][2][0][0]) for a in instr]
    latency_max = [float(a['arch'][ARCH][2][1][0]) for a in instr]

    assert len(throughput) == len(latency_max) == len(latency_min)
    if len(throughput) == 1:
        return instr[0], throughput[0], latency_min[0], latency_max[0]
    return instr, throughput, latency_min, latency_max


def get_uops_info(ARCH=""):
    """
    TODO implement ARCH selector

    INPUT:
    - ``test.in`` -- test.in
    EXAMPLES:
    """
    global CCTX
    return CCTX
