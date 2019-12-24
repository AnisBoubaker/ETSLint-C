from rules import BaseRule


class RuleVarOnOwnLine(BaseRule):
    __declared = []
    __last_file = None

    def __init__(self, reporter=None):
        BaseRule.__init__(self, "style", reporter)

    def visit_Decl(self, node):
        if self.__last_file is None or self.__last_file != node.coord.file:
            self.__last_file = node.coord.file
            self.__declared.clear()

        sameline_variable = [var for var in self.__declared if var['line'] == node.coord.line]

        if len(sameline_variable):
            message = "Variable {} should be declared on its own line.".format(node.name)
            self.reporter.do_report(self, node.coord, message)

        # It's probably overkill to keep all declarations in a list. However, we can't be sure the AST traversal will be
        # sequential.
        self.__declared += [{'name': node.name, 'line': node.coord.line}]
