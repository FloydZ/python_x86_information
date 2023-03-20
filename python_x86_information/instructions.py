#! /usr/bin/python3
from pycca.asm import mkfunction
from opcodes.x86_64 import read_instruction_set
import xml.etree.ElementTree as ET
import re
import ctypes
from typing import Union, Any


class Context:
    """
    Helper class for parsing intrinsic guide
    """
    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

# Dummy obj
Table = Context

TRANSLATION = {
        "r64": "r64",
        "rax": "r64",
        "rbx": "r64",
        "rsp": "r64",
        "rbp": "r64",
}


class AStr:
    """
    AStr is a wrapper for strings keeping attributes on ranges of characters
    This is probably overengineering but its fun+pretty, so whatever
    """

    def __init__(self, value, attrs=None):
        self.value = value
        if attrs is None:
            attrs = [(0, 'default')]
        elif isinstance(attrs, str):
            attrs = [(0, attrs)]
        self.attrs = attrs
    def offset_attrs(self, delta):
        attrs = [(offset + delta, attr) for offset, attr in self.attrs]
        # Chop off negative entries, unless they cover the start
        start = 0
        for i, [offset, attr] in enumerate(self.attrs):
            if offset > 0:
                break
            start = i
        return attrs[start:]

    def __add__(self, other):
        if not isinstance(other, AStr):
            other = AStr(other)
        attrs = self.attrs + other.offset_attrs(len(self.value))
        return AStr(self.value + other.value, attrs)
    def __radd__(self, other):
        return AStr(other) + self
    def __getitem__(self, s):
        assert isinstance(s, slice)
        assert s.step == 1 or s.step is None
        attrs = self.attrs
        if s.start:
            # Convert negative indices to positive so offset_attrs() works
            if s.start < 0:
                s = slice(max(0, len(self.value)+s.start), s.stop, s.step)
            attrs = self.offset_attrs(-s.start)
        if s.stop:
            attrs = [(offset, attr) for offset, attr in attrs if offset < s.stop]
        return AStr(self.value[s], attrs=attrs)
    def __len__(self):
        return len(self.value)

    # Hacky reimplementations of str methods
    def splitlines(self):
        while '\n' in self.value:
            index = self.value.find('\n')
            line, self = self[:index], self[index+1:]
            yield line
        yield self
    def rfind(self, *args):
        return self.value.rfind(*args)
    def strip(self):
        # This is dumb+inefficient
        sub = self.value.lstrip()
        start = len(self) - len(sub)
        return self[start:start + len(sub.rstrip())]
    def lstrip(self):
        sub = self.value.lstrip()
        attrs = self.offset_attrs(len(sub) - len(self))
        return AStr(sub, attrs=attrs)
    def replace(self, pat, sub):
        result = AStr('')
        while pat in self.value:
            index = self.value.find(pat)
            result = self.value[:index] + sub
            self = self[index + 1:]
        return result


def parse_intrinsics_guide(path):
    """
    SRC:    
        https://github.com/zwegner/x86-info-term/blob/master/x86_info_term.py
    parses the intel instruction file `data-latest.xml`
    """
    root = ET.parse(path)

    version = root.getroot().attrib['version']
    version = tuple(int(x) for x in version.split('.'))

    table = []
    for i, intrinsic in enumerate(root.findall('intrinsic')):
        name = ""
        try:
            tech = intrinsic.attrib['tech']
            name = intrinsic.attrib['name']
            desc = [d.text for d in intrinsic.findall('description')][0]
            insts = [(inst.attrib['name'].lower(), inst.attrib.get('form', ''))
                     for inst in intrinsic.findall('instruction')]
            # Return type spec changed in XML as of 3.5.0
            return_type = (intrinsic.attrib['rettype'] if version < (3, 5, 0) else
                           [r.attrib['type'] for r in intrinsic.findall('return')][0])
            key = '%s %s %s %s' % (tech, name, desc, insts)
            table.append({
                'id': i,
                'tech': tech,
                'name': name,
                'params': [(p.attrib.get('varname', ''), p.attrib['type'])
                           for p in intrinsic.findall('parameter')],
                'return_type': return_type,
                'desc': desc,
                'operations': [op.text for op in intrinsic.findall('operation')],
                'insts': insts,
                'search-key': key.lower(),
            })
        except:
            print('Error while parsing %s:' % name)
            print(ET.tostring(intrinsic, encoding='unicode'))
            raise

    return [version, table]


def transform_intrinsics_guide(table, tech=None):
    """
    trasforms the intel intrinsics guide into a dictonary.
    """
    ret = {}
    for entry in table:
        if tech is not None and entry["tech"] != tech:
            continue

        if len(entry["insts"]) == 0:
            # in this case the function is not coresponding to a asm instruction
            # but a library wrapper function
            #print(entry)
            continue

        assert len(entry["insts"]) > 0
        insts = entry["insts"][0][0].split(" ")[0]
        if insts not in ret.keys():
            ret[insts] = []

        ret[insts].append(entry)

    return ret

###############################################################################
## Info from uops.info ########################################################
###############################################################################


# All architectures measured by uops.info. This is just here for consistent
# ordering
ALL_ARCHES = ['CON', 'WOL', 'NHM', 'WSM', 'SNB', 'IVB', 'HSW', 'BDW', 'SKL',
              'SKX', 'KBL', 'CFL', 'CNL', 'ICL', 'ZEN+', 'ZEN2']

# Sentinel value for unknown latency
MAX_LATENCY = 1e100


def parse_uops_info(path: str):
    """

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


def get_uop_table(ctx, start, stop, folds={}):
    """
    """
    rows = []
    prev_ext = ''
    for [i, uop] in enumerate(ctx.filtered_data[start:stop]):
        expand = (uop['id'] in folds)
        subtables = [get_uop_subtable(ctx, uop)] if expand else []

        ext = uop['extension']
        # Hacky: get a color for this instruction by matching the longest
        # prefix of the extension that's also an intrinsic extension
        color = 'Other'
        for prefix in range(len(ext), 0, -1):
            if ext[:prefix] in INTR_COLORS:
                color = ext[:prefix]
                break

        # Make a clean-ish description line with all the instruction forms
        forms = ';  '.join(re.sub(r'.*\((.*)\)', r'\1', form['form'])
                           for form in uop['forms'])

        row = {
            'id': i + start,
            'cells': [
                ['',  {'attr': color}],
                [ext if expand or prev_ext != ext else '', {}],
                # Pad mnemonic on left
                [' ' + uop['mnem'], {'attr': 'bold'}],
                forms,
            ],
            'subtables': subtables,
        }
        prev_ext = ext
        rows.append(row)

    widths = [2, 12, -1, 0]
    return Table(rows=rows, widths=widths, alignment=[0, 0, 0, 0])


def get_uop_subtable(ctx, uop, uop_forms=None):
    """
    Get the union of all arches in each form for consistent columns. We sort
    by the entries in ALL_ARCHES, but add any extra arches at the end for
    future proofing
    """
    seen_arches = {arch for form in uop['forms'] for arch in form['arch']}
    arches = [a for a in ALL_ARCHES if a in seen_arches] + \
        list(seen_arches - set(ALL_ARCHES))
    if ctx.arches:
        arches = [a for a in arches if a.lower() in ctx.arches]

    if not arches:
        return None

    columns = len(arches) + 1
    blank_row = [''] * columns
    pad = ' ' * 4
    header = [AStr(arch, 'bold') for arch in arches]

    if uop_forms is None:
        uop_forms = uop['forms']

    rows = []
    for form in uop_forms:
        latencies = []
        throughputs = []
        port_usages = []
        # Create separate rows for latency/throughput/port usage
        for arch in arches:
            if arch in form['arch']:
                [ports, tp, lat_bounds] = form['arch'][arch]

                if lat_bounds[0][0] != MAX_LATENCY:
                    lat_bounds = ['%s%s' % (('≤' if not is_exact else ''), value)
                                  for [value, is_exact] in lat_bounds]
                    [lat_min, lat_max] = lat_bounds
                    lat = lat_min if lat_min == lat_max else '%s;%s' % (
                        lat_min, lat_max)
                    latencies.append(lat)
                else:
                    latencies.append('-')
                throughputs.append(str(tp))
                port_usages.append(str(ports))
            else:
                latencies.append('-')
                throughputs.append('-')
                port_usages.append('-')

        rows.extend([
            {'cells': [AStr(pad + form['form'], 'inst')], 'span': True},
            ['', *header],
            [AStr(pad + 'Ports:', 'bold'), *port_usages],
            [AStr(pad + 'Latency:', 'bold'), *latencies],
            [AStr(pad + 'Throughput:', 'bold'), *throughputs],
            blank_row,
        ])

    widths = [-1] * columns
    alignment = [False] * columns
    scroll = [True] * columns
    scroll[0] = False
    return Table(rows=rows, widths=widths, alignment=alignment, scroll=scroll)


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


# Get a list of matching uop instruction forms for this instruction
def get_intr_uop_matches(ctx, mnem, target_form, exact=True):
    matching_forms = []

    # Filter out some stuff and normalize
    target_form = (target_form.replace(' {z}', ', z').replace(' {k}', ', k')
                   .replace(' {er}', '').replace(' {sae}', '').replace(' ', ''))

    # Create a set of matching arguments for each instruction argument
    intr_args = []
    for arg in target_form.split(','):
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
            #if all(arg in opts for [arg, opts] in zip(uops_args, intr_args)):
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


def get_intr_uop_cycles(ctx, mnem, target_form):
    """
    """
    ARCH = "ZEN2"
    if type(target_form) == list:
        target_form = ",".join(target_form)
    
    instr = get_intr_uop_matches(ctx, mnem, target_form)
    # pprint.pprint(instr)
    cycles = [float(a['arch'][ARCH][1]) for a in instr]
    return instr[0], cycles[0]


def transform_instruction_set(instruction_set):
    """
    SRC: https://github.com/Maratyszcza/Opcodes
    transform the list of instruction return by
        `instruction_set = read_instruction_set()`
    into a dictonary index by the instruction name.
    """
    ret = {}
    for entry in instruction_set:
        name = entry.name.lower()
        if name not in ret.keys():
            ret[name] = {}

        ret[name] = entry
    return ret


def find_in_instruction_set(instruction_set, instr, form=[]):
    """
        finds an exact instruction for a given mnemoric
        e.g.:
            `find_in_instruction_set(instruction_set. "mov", ["rax", "rbx"])`
        NOTE:
            one can pass either the register names or:
                "r64", "r32", "r16", "m64", ..., "imm8"
            the implementation will automatically choose the correct representation.
    """
    if instr not in instruction_set.keys():
        return None
    
    nr_args = len(form)
    trans_form = [TRANSLATION[f] for f in form]
    pos_inf = instruction_set[instr]

    for inf in pos_inf.forms:
        if len(inf.operands) == nr_args:
            same = True
            for i in range(nr_args):
                if inf.operands[i].type != trans_form[i]:
                    same = False
                    break

            if same:
                return inf

    return None


# TODO pass full path
# Core datasets from intel
_, data_intr_ = parse_intrinsics_guide("deps/data-latest.xml")
data_intr = transform_intrinsics_guide(data_intr)

# and uops
_, data_uops = parse_uops_info("deps/instructions.xml")
cctx = Context(data_source="", uops_info=data_uops)


def get_intrinsics_guide(tech=None):
    """
    One of the main entry points of this module
    Returning the Intel intrinsic guide.

    EXAMPLES::

    """
    global data_intr_

    # TODO simplify, so not for every request the whole thing needs to be computed
    data_intr = transform_intrinsics_guide(data_intr_, tech=tech)
    return data_intr


def get_uops_info(ARCH=""):
    """
    one of the main entry points of thos modul;

    TODO implement ARCH selector

    """
    global cctx
    return cctx


def get_instruction_set():
    """
    one of the main entry points of this modul

    from the package `opcodes`
    """
    # taken from: opcodes
    instruction_set = read_instruction_set()
    instruction_set = transform_instruction_set(instruction_set)
    return instruction_set


def exec_instructions(instr: Union[str, list[str]], 
                      in_registers: dict[str, Any]={},
                      out_registers: dict[str, Any]={}):
    """
    SRC: https://github.com/pycca/pycca
    actually executes instructions
    
    instr:  list or string of assembly instrucitons
    in_registers
    NOTE: the input assembly code should and with a `ret` instruction, if not
        one is automatically appended.
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

# class Instruction:
#     def __init__(self):
#         pprint.pprint(instruction_set[0].forms[17].__dict__)
#         # pprint.pprint(instruction_set[0].forms)
# 
# ins = Instruction()
# exit(1)



def information(mnemonic: str, arg=None, arch=None):
    """
        recieve usefull infroamtion about an instruction. 
    """
    
    return None
