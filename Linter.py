import rules
from pycparser import c_ast, parse_file, c_parser
import pycparser_fake_libc
from os import walk
import os.path

class Linter(object):

    __extensions = ["c", "cpp"]

    def __init__(self, reporter, file_path):
        self.__reporter = reporter
        self.__rules_available = []
        self.__file_path = file_path
        self.__files_to_parse = []
        self.__get_all_rules()
        self.__get_all_parsable_files()

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
            ast = parse_file(file, use_cpp=True, cpp_args=r"-I" + fake_libc_arg)
            print

            for rule in self.__rules_available:
                rule.visit(ast)

    def __get_all_rules(self):
        classes = []
        for attr in dir(rules):
            var = getattr(rules, attr)
            if type(var) == type and var is not rules.BaseRule and issubclass(var, c_ast.NodeVisitor):
                classes.append(var)
        self.__rules_available = [c(self.__reporter) for c in classes]
