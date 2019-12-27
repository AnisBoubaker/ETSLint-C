from clinter.rules import BaseRule
from clinter import rules
from pycparser import c_ast, parse_file
from pycparser.c_ast import FileAST
import pycparser_fake_libc
from os import walk
import os.path


class NodeParenter(c_ast.NodeVisitor):
    """
    AST Visitor that collects node parents of each AST node, implemented as a Singleton
    """
    __instances = {}

    def __init__(self, ast):
        self.__parents = {}
        self.__ast = ast
        self.visit(ast)

    @staticmethod
    def get_instance(ast: FileAST):
        if ast not in NodeParenter.__instances:
            NodeParenter.__instances[ast] = NodeParenter(ast)

        return NodeParenter.__instances[ast]

    def visit(self, node):
        children = node.children()
        for child in children:
            self.__parents[child[1]] = node
            self.visit(child[1])

    @property
    def parents(self):
        return self.__parents

    def get_parent(self, node, level=1):
        """Retrieves the ancestor node of `node` going up `level` levels in the hierarchy"""
        curr_node = node
        while level > 0:
            if curr_node not in self.__parents:
                return None
            curr_node = self.__parents[node]
            level -= 1
        return curr_node

    def __str__(self):
        result = ""
        for child in self.__parents.keys():
            result += "Child: " + type(child).__name__ + " Parent: " + type(self.__parents[child]).__name__ + "\n"
        return result

    def __repr__(self):
        return self.__str__()


class CLinter(object):

    __extensions = ["c", "cpp"]

    def __init__(self, reporter, file_path):
        self.__reporter = reporter
        self.__rules_available = []
        self.__file_path = file_path
        self.__files_to_parse = []
        self.__get_all_rules()
        self.__get_all_parsable_files()
        self.__ast = None

    def __get_all_parsable_files(self):
        self.__files_to_parse.clear()

        for (dirpath, _, filenames) in walk(self.__file_path):
            self.__files_to_parse += [dirpath + "/" + file for file in filenames if
                                      os.path.splitext(file)[1][1:] in self.__extensions]

    def run_all_rules(self):
        # Note that cpp is used. Provide a path to your own cpp or
        # make sure one exists in PATH.
        fake_libc_arg = "-I" + pycparser_fake_libc.directory

        for file in self.__files_to_parse:
            self.__ast = parse_file(file, use_cpp=True, cpp_args=r"-I" + fake_libc_arg)

            for rule in self.__rules_available:
                rule.visit(self.__ast)

    def __get_all_rules(self):
        classes = []
        for attr in dir(rules):
            var = getattr(rules, attr)
            if type(var) == type and var is not BaseRule and issubclass(var, c_ast.NodeVisitor):
                classes.append(var)
        self.__rules_available = [c(self.__reporter) for c in classes]
