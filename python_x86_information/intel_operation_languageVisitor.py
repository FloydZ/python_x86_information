# Generated from intel_operation_language.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .intel_operation_languageParser import intel_operation_languageParser
else:
    from intel_operation_languageParser import intel_operation_languageParser

# This class defines a complete generic visitor for a parse tree produced by intel_operation_languageParser.

class intel_operation_languageVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by intel_operation_languageParser#prog.
    def visitProg(self, ctx:intel_operation_languageParser.ProgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by intel_operation_languageParser#base_block.
    def visitBase_block(self, ctx:intel_operation_languageParser.Base_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by intel_operation_languageParser#base_line.
    def visitBase_line(self, ctx:intel_operation_languageParser.Base_lineContext):
        return self.visitChildren(ctx)



del intel_operation_languageParser