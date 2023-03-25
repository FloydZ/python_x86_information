# Generated from intel_operation_language.g4 by ANTLR 4.8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\7")
        buf.write("#\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\3\2\6\2")
        buf.write("\17\n\2\r\2\16\2\20\3\2\3\2\3\3\3\3\3\4\3\4\3\4\3\5\6")
        buf.write("\5\33\n\5\r\5\16\5\34\3\6\6\6 \n\6\r\6\16\6!\2\2\7\3\3")
        buf.write("\5\4\7\5\t\6\13\7\3\2\6\5\2\13\f\17\17\"\"\5\2--//??\4")
        buf.write("\2C\\c|\3\2\62;\2%\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2")
        buf.write("\2\t\3\2\2\2\2\13\3\2\2\2\3\16\3\2\2\2\5\24\3\2\2\2\7")
        buf.write("\26\3\2\2\2\t\32\3\2\2\2\13\37\3\2\2\2\r\17\t\2\2\2\16")
        buf.write("\r\3\2\2\2\17\20\3\2\2\2\20\16\3\2\2\2\20\21\3\2\2\2\21")
        buf.write("\22\3\2\2\2\22\23\b\2\2\2\23\4\3\2\2\2\24\25\t\3\2\2\25")
        buf.write("\6\3\2\2\2\26\27\7<\2\2\27\30\7?\2\2\30\b\3\2\2\2\31\33")
        buf.write("\t\4\2\2\32\31\3\2\2\2\33\34\3\2\2\2\34\32\3\2\2\2\34")
        buf.write("\35\3\2\2\2\35\n\3\2\2\2\36 \t\5\2\2\37\36\3\2\2\2 !\3")
        buf.write("\2\2\2!\37\3\2\2\2!\"\3\2\2\2\"\f\3\2\2\2\6\2\20\34!\3")
        buf.write("\2\3\2")
        return buf.getvalue()


class intel_operation_languageLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    WS = 1
    OPERATION = 2
    DEFINITION = 3
    NAME = 4
    INT = 5

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "':='" ]

    symbolicNames = [ "<INVALID>",
            "WS", "OPERATION", "DEFINITION", "NAME", "INT" ]

    ruleNames = [ "WS", "OPERATION", "DEFINITION", "NAME", "INT" ]

    grammarFileName = "intel_operation_language.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.8")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


