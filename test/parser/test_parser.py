import os
import sys
from antlr4 import *
from antlr4.tree import Trees
from antlr4.error.ErrorListener import ErrorListener

from python_x86_information.parser.intel_operation_languageLexer import intel_operation_languageLexer as Lexer
from python_x86_information.parser.intel_operation_languageParser import intel_operation_languageParser as Parser
from python_x86_information.parser.intel_operation_languageVisitor import intel_operation_languageVisitor as Visitor


# SRC: https://stackoverflow.com/questions/62301218/antlr4-python-in-unittest-how-to-abort-on-any-error
class MyErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise Exception("ERROR: when parsing line %d column %d: %s\n" % \
                        (line, column, msg))


def run(input: str):
    """
    runs the parser on the fiven input.
    Returns:
        True: on error
        False: on success
    """
    error_listener = MyErrorListener()
    if os.path.isfile(input):
        input_stream = FileStream(input)
    else:
        input_stream = InputStream(input)
    lexer = Lexer(input_stream)
    lexer.removeErrorListeners()
    lexer.addErrorListener(error_listener)

    stream = CommonTokenStream(lexer)

    parser = Parser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(error_listener)

    try:
        tree = parser.prog()
        return False
    except Exception as e:
        print(input)
        print(e)
        return True


def test_main():
    """
    Tests some arbitrary clauses.

    Returns: Nothing

    """
    if run("tmp := tmp"):
        return

    if run("tmp[out+31:out] := tmp[31:0]"):
        return

    if run("tmp[out+31:out] := 0"):
        return

    if run("tmp[0] := tmp[32]"):
        return

    if run("tmp := tmp + 1"):
        return

    if run("tmp[32:0] := a[31:0] + b[31:0] + ( cin > 0 ? 1 : 0 )"):
        return

    if run("dst[255:0] := (a[255:0] XOR b[255:0])"):
        return

    if run("(a[1] == b) ? 1: 0"):
        return

    if run("SignExtend32(word[a + 16:b + 0])"):
        return

    if run("SignExtend32(Cast_Int16(t.word[0]))"):
        return

    if run("0x3F"):
        return

    if run("""IF HW_NRND_GEN.ready == 1
	val[63:0] := HW_NRND_GEN.data
	dst := 1
ELSE
	val[63:0] := 0
	dst := 0
FI"""):

        if run("test/t01.in"):
            return

        if run("test/t02.in"):
            return

        if run("test/t03.in"):
            return

        if run("test/t04.in"):
            return

        if run("test/t05.in"):
            return

        return
