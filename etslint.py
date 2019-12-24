import sys
from Linter import Linter
from reporters import JsonReporter

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'examples/memmgr.c'

    reporter = JsonReporter('report.json')
    lint = Linter(reporter)
    lint.run_all_rules(filename)
    print(reporter.generate_report())
