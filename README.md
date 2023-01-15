Intel x86/64 instruction information python package. Let you easily pull all
sorts of information for a instruction via python.

Features:
=========
 - in memory compiler/assembler via [pycca](https://github.com/campagnola/pycca)

Installation:
=============

Run:
```
git clone https://github.com/FloydZ/python_x86_information
cd python_x86_information
./setup.sh
```

Note the `setup.sh` script at the end. its needed to download all necessary data.

Usage:
======

To recieve general information about an instruction you can call:
```python
i = information("adc")
print(i)
```

All function return a list of return values if it was not possible to detect precisly which instruction was meant.

To get the exact instruction infromation returned call one the following
```python
information("adc", ["rax", "rbx"])
information("adc", "r64, rbx")
```
Note that you can either pass the arguments as a list of strings or as a single string. Also you can either pass the original register/memory 'names' or their types like `r16,r32,r64,m64` and so on.

Furthermore each function has an additional parameter called `arch`, which let
one to specify the architecture for which the information should be returned.
Allowed values are `'CON', 'WOL', 'NHM', 'WSM', 'SNB', 'IVB', 'HSW', 'BDW', 'SKL', 'SKX', 'KBL', 'CFL', 'CNL', 'ICL', 'ZEN+', 'ZEN2'`



Information Source:
===================

Many thanks to the great work of [zwegners x86-info-term](https://github.com/zwegner/x86-info-term) and
[uops](https://uica.uops.info/)

- [Intel](https://www.intel.com/content/dam/develop/public/us/en/include/intrinsics-guide/data-latest.xml)
- [uops](https://www.uops.info/instructions.xml)

TODO:
======
 - [ ] parser for the C type language in intel description

