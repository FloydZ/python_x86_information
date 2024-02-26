from typing import Union
import xml.etree.ElementTree as ET
import logging


def parse_intrinsics_guide(path: str):
    """
    SRC: https://github.com/zwegner/x86-info-term/blob/master/x86_info_term.py

    Parses the intel instruction file `data-latest.xml`.

    INPUT:
    - ``path`` -- path to the `data-latest.xml`

    EXAMPLES::

        >>> from python_x86_information import parse_intrinsics_guide
        >>> _, table = parse_intrinsics_guide("deps/data-latest.xml")
        >>> print(table)

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
            logging.error('Error while parsing %s:' % name)
            logging.error(ET.tostring(intrinsic, encoding='unicode'))
            raise

    return [version, table]


def transform_intrinsics_guide(table, tech=None):
    """
    transforms the intel intrinsics guide into a dictionary.


    INPUT:
    - ``table`` --
    - ``tec`` --

    EXAMPLES::

    """
    ret = {}
    for entry in table:
        if tech is not None and entry["tech"] != tech:
            continue

        if len(entry["insts"]) == 0:
            # in this case the function is not coresponding to a asm instruction
            # but a library wrapper function
            # print(entry)
            continue

        assert len(entry["insts"]) > 0
        insts = entry["insts"][0][0].split(" ")[0]
        if insts not in ret.keys():
            ret[insts] = []

        ret[insts].append(entry)

    return ret


def find_in_instruction_set(instruction_set: dict, instr: str,
                            target_form: Union[str, list[str]]):
    """
    finds an exact instruction for a given mnemoric. Searches in the intel dataset.
    If no instruction is found, None is returned

    NOTE:
        one can pass either the register names or:
            "r64", "r32", "r16", "m64", ..., "imm8"
        the implementation will automatically choose the correct representation.

    INPUT:

    - ``test.in`` -- test.in
    - ``test.in`` -- test.in
    - ``test.in`` -- test.in
    - ``test.in`` -- test.in

    EXAMPLES:

        >>> find_in_instruction_set(instruction_set, "mov", ["rax", "rbx"])
    """
    if instr not in instruction_set.keys():
        logging.warning("instruction {0} not found".format(instr))
        return None

    nr_args = len(target_form)
    trans_form = []
    for arg in target_form:
        # if the argumetn is a number replace it with i8
        if type(arg) == int:
            arg = "imm8"
        else:
            try:
                arg = int(arg)
                arg = "imm8"
            except:
                # Filter out some stuff and normalize
                arg = TRANSLATION[arg]
        trans_form.append(arg)

    pos_inf = instruction_set[instr]
    args = ", ".join(trans_form)

    ret = []
    for inf in pos_inf:
        insts = inf["insts"]
        assert len(insts) == 1
        insts = insts[0]
        assert len(insts) == 2
        assert insts[0] == instr

        if (insts[1] == args):
            ret.append(inf)

    return ret


# TODO move somewhere
# Core datasets from intel
_, data_intr_ = parse_intrinsics_guide("deps/data-latest.xml")
CCTX_INTEL = transform_intrinsics_guide(data_intr_)


def get_intrinsics_guide(tech=None):
    """
    One of the main entry points of this module
    Returning the Intel intrinsic guide.

    INPUT:
        - ``tech`` -- either None or an architecture

    EXAMPLES::

        >>>

    """
    global CCTX_INTEL
    if tech is None:
        return CCTX_INTEL

    global data_intr_
    return transform_intrinsics_guide(data_intr_, tech=tech)
