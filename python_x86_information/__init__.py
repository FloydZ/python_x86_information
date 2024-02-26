__author__ = "Floyd Zweydinger"
__copyright__ = "Copyright 2023"
__credits__ = ["Floyd Zweydinger"]
__license__ = "GPL2"
__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)
__maintainer__ = "Floyd Zweydinger"
__email__ = "floyd.zweydinger+github@rub.de"
__status__ = "Development"


from .sources.uops import ALL_ARCHES as ARCHES, get_uops_info, get_intr_uop_information
from .sources.intel import *
from .sources.opcode import get_instruction_set
from .information import *
from .instruction import *
