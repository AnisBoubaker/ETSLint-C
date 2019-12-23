from pycparser import c_ast
from rules import BaseRule


class RuleVarOnOwnLine(BaseRule):
    __declared = []

    def __init__(self):
        self.__reporter = None

    @property
    def reporter(self):
        return self.__reporter

    def visit_Decl(self, node):
        sameline_variable = [var for var in self.__declared if var['line'] == node.coord.line]

        if len(sameline_variable):
            print("Variable {} should be declared on its own line.".format(node.name))

        self.__declared += [{'name': node.name, 'line': node.coord.line}]
