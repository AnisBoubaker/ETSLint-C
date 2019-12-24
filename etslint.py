import sys
from Linter import Linter
from reporters import PrintReporter

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'examples/memmgr.c'

    reporter = PrintReporter()
    lint = Linter(reporter)
    lint.run_all_rules(filename)
    reporter.generate_report()
