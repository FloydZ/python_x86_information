#!/usr/bin/python
from opcodes import __version__, __author__, __email__
from setuptools import setup


def read_text_file(path):
    import os
    with open(os.path.join(os.path.dirname(__file__), path)) as f:
        return f.read()


setup(
    name="python_x86_information",
    version=__version__,
    description="Database of Processor Instructions/Opcodes with a smooth interface",
    long_description=read_text_file("README.md"),
    author=__author__,
    author_email=__email__,
    url="https://github.com/FloydZ/python_x86_information",
    packages=["python_x86_information"],
    package_data={"python_x86_instruction": ["data-latest.xml", "instructions.xml"]},
    keywords=["assembly", "assembler", "asm", "opcodes", "x86", "x86-64", "isa", "cpu"],
    install_requires=["setuptools"],
    requires=[],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Assembly",
	    "Programming Language :: Python",
	    "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Topic :: Software Development :: Assemblers",
        "Topic :: Software Development :: Documentation"
    ])
