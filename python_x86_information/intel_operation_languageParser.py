# Generated from intel_operation_language.g4 by ANTLR 4.8
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\7")
        buf.write("\33\4\2\t\2\4\3\t\3\4\4\t\4\3\2\7\2\n\n\2\f\2\16\2\r\13")
        buf.write("\2\3\2\3\2\3\3\3\3\3\4\3\4\3\4\3\4\3\4\3\4\5\4\31\n\4")
        buf.write("\3\4\2\2\5\2\4\6\2\2\2\33\2\13\3\2\2\2\4\20\3\2\2\2\6")
        buf.write("\22\3\2\2\2\b\n\5\4\3\2\t\b\3\2\2\2\n\r\3\2\2\2\13\t\3")
        buf.write("\2\2\2\13\f\3\2\2\2\f\16\3\2\2\2\r\13\3\2\2\2\16\17\7")
        buf.write("\2\2\3\17\3\3\2\2\2\20\21\5\6\4\2\21\5\3\2\2\2\22\23\7")
        buf.write("\6\2\2\23\30\7\5\2\2\24\31\5\6\4\2\25\31\7\7\2\2\26\31")
        buf.write("\7\4\2\2\27\31\7\6\2\2\30\24\3\2\2\2\30\25\3\2\2\2\30")
        buf.write("\26\3\2\2\2\30\27\3\2\2\2\31\7\3\2\2\2\4\13\30")
        return buf.getvalue()


class intel_operation_languageParser ( Parser ):

    grammarFileName = "intel_operation_language.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "':='" ]

    symbolicNames = [ "<INVALID>", "WS", "OPERATION", "DEFINITION", "NAME", 
                      "INT" ]

    RULE_prog = 0
    RULE_base_block = 1
    RULE_base_line = 2

    ruleNames =  [ "prog", "base_block", "base_line" ]

    EOF = Token.EOF
    WS=1
    OPERATION=2
    DEFINITION=3
    NAME=4
    INT=5

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.8")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(intel_operation_languageParser.EOF, 0)

        def base_block(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(intel_operation_languageParser.Base_blockContext)
            else:
                return self.getTypedRuleContext(intel_operation_languageParser.Base_blockContext,i)


        def getRuleIndex(self):
            return intel_operation_languageParser.RULE_prog

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProg" ):
                listener.enterProg(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProg" ):
                listener.exitProg(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProg" ):
                return visitor.visitProg(self)
            else:
                return visitor.visitChildren(self)




    def prog(self):

        localctx = intel_operation_languageParser.ProgContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_prog)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 9
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==intel_operation_languageParser.NAME:
                self.state = 6
                self.base_block()
                self.state = 11
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 12
            self.match(intel_operation_languageParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Base_blockContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def base_line(self):
            return self.getTypedRuleContext(intel_operation_languageParser.Base_lineContext,0)


        def getRuleIndex(self):
            return intel_operation_languageParser.RULE_base_block

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBase_block" ):
                listener.enterBase_block(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBase_block" ):
                listener.exitBase_block(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBase_block" ):
                return visitor.visitBase_block(self)
            else:
                return visitor.visitChildren(self)




    def base_block(self):

        localctx = intel_operation_languageParser.Base_blockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_base_block)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 14
            self.base_line()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Base_lineContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self, i:int=None):
            if i is None:
                return self.getTokens(intel_operation_languageParser.NAME)
            else:
                return self.getToken(intel_operation_languageParser.NAME, i)

        def DEFINITION(self):
            return self.getToken(intel_operation_languageParser.DEFINITION, 0)

        def base_line(self):
            return self.getTypedRuleContext(intel_operation_languageParser.Base_lineContext,0)


        def INT(self):
            return self.getToken(intel_operation_languageParser.INT, 0)

        def OPERATION(self):
            return self.getToken(intel_operation_languageParser.OPERATION, 0)

        def getRuleIndex(self):
            return intel_operation_languageParser.RULE_base_line

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBase_line" ):
                listener.enterBase_line(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBase_line" ):
                listener.exitBase_line(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBase_line" ):
                return visitor.visitBase_line(self)
            else:
                return visitor.visitChildren(self)




    def base_line(self):

        localctx = intel_operation_languageParser.Base_lineContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_base_line)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 16
            self.match(intel_operation_languageParser.NAME)
            self.state = 17
            self.match(intel_operation_languageParser.DEFINITION)
            self.state = 22
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                self.state = 18
                self.base_line()
                pass

            elif la_ == 2:
                self.state = 19
                self.match(intel_operation_languageParser.INT)
                pass

            elif la_ == 3:
                self.state = 20
                self.match(intel_operation_languageParser.OPERATION)
                pass

            elif la_ == 4:
                self.state = 21
                self.match(intel_operation_languageParser.NAME)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





