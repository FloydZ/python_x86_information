from .sources.intel import get_intrinsics_guide


def information(mnemonic: str, arg=None, arch=None):
    """
    Receive useful information about an instruction.
    TODO correctly model whats in instructions

    INPUT:
    - ``mnemonic`` -- instruction mnemonic to fetch information from
    - ``arg`` --
    - ``arch`` --

    EXAMPLES::

        >>> from python_x86_information import information
        >>> information("adx")
    """
    intel = get_intrinsics_guide(arch)
    try:
        tmp = intel[mnemonic]

        # TODO here filtering of args
        return tmp
    except Exception as e:
        return e
