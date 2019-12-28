# ETSLINT
## Yet another programming language style linter

## Description
This pure Python linter aims at detecting patterns in source code based on a set of rules through static analysis. Each rule is a Python class implementing pattern logic based on the abstract syntax tree of the source code. Rules detected will be reported by various reporters (for now, two reporters are available: console print and json file reports).

This project intends to offer a linter for various programming languages (as long as a Python parser of the so-called language is available). For the time being, it works only on C code (C99) and relies on [pycparser](https://github.com/eliben/pycparser). 

## Usage
Typical use of this tool would be to detect deviations from prescribed coding standards. However, any source code static analysis could be performed as long as the information could be found in the abstract syntax tree (AST).
