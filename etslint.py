import sys
from Linter import Linter

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'examples/memmgr.c'

    lint = Linter()
    lint.run_all_rules(filename)
