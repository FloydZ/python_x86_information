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


    # Visit a parse tree produced by intel_operation_languageParser#expression.
    def visitExpression(self, ctx:intel_operation_languageParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by intel_operation_languageParser#definition.
    def visitDefinition(self, ctx:intel_operation_languageParser.DefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by intel_operation_languageParser#ternaryoperator.
    def visitTernaryoperator(self, ctx:intel_operation_languageParser.TernaryoperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by intel_operation_languageParser#ifExpression.
    def visitIfExpression(self, ctx:intel_operation_languageParser.IfExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by intel_operation_languageParser#structAccess.
    def visitStructAccess(self, ctx:intel_operation_languageParser.StructAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by intel_operation_languageParser#comparison.
    def visitComparison(self, ctx:intel_operation_languageParser.ComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by intel_operation_languageParser#variable.
    def visitVariable(self, ctx:intel_operation_languageParser.VariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by intel_operation_languageParser#accessoperator.
    def visitAccessoperator(self, ctx:intel_operation_languageParser.AccessoperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by intel_operation_languageParser#accessoperatorname.
    def visitAccessoperatorname(self, ctx:intel_operation_languageParser.AccessoperatornameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by intel_operation_languageParser#operator.
    def visitOperator(self, ctx:intel_operation_languageParser.OperatorContext):
        return self.visitChildren(ctx)



del intel_operation_languageParser