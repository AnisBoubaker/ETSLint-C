import rules
from pycparser import c_ast, parse_file
import pycparser_fake_libc


class Linter(object):

    def __init__(self):
        self.__rules_available = []
        self.__get_all_rules()

    def run_all_rules(self, filename):
        # Note that cpp is used. Provide a path to your own cpp or
        # make sure one exists in PATH.
        fake_libc_arg = "-I" + pycparser_fake_libc.directory

        ast = parse_file(filename, use_cpp=True, cpp_args=r"-I" + fake_libc_arg)

        for rule in self.__rules_available:
            rule.visit(ast)

    def __get_all_rules(self):
        classes = []
        for attr in dir(rules):
            var = getattr(rules, attr)
            if type(var) == type and var is not rules.BaseRule and issubclass(var, c_ast.NodeVisitor):
                classes.append(var)
        self.__rules_available = [c() for c in classes]
