import sys
from Linter import Linter
from reporters import *
import argparse


extensions = ["c", "cpp"]


def run_linter():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("path", help="Path to the C file or a folder containing the C code to analyse.")
    arg_parser.add_argument("-r", "--report", help="The type of report that will be generated. 'print' report type"
                                                   "prints the report to stdout.",
                            choices=["print", "json"], default="print")
    arg_parser.add_argument("-o", "--output", help="File path where the report will be written (requires -r)")
    args = arg_parser.parse_args()

    if args.report == "print" and args.output:
        arg_parser.error("A report type other than 'print' must be set (using -r) in order to use -o option.")

    if args.report != "print" and not args.output:
        arg_parser.error("Output file must be specified (with -o option) when using a non 'print' report.")

    # Creates the reporter to be used by the Linter
    if args.report == "json":
        lint_reporter = JsonReporter(args.output)
    else:
        lint_reporter = PrintReporter()

    lint = Linter(lint_reporter, args.path)
    lint.run_all_rules()

    lint_reporter.generate_report()


if __name__ == "__main__":
    run_linter()
