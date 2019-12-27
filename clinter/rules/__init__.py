"""
Provides the set of rules that are used by the linter.

This module exposes all the rules that could be used by the linter. Each rule is a visitor subclass of
c_ast.NodeVisitor.

Note: by design, each rule must be exposed explicitly through an import in this file. This prevents from including
rule classes that are not production ready.
"""



from .BaseRule import BaseRule
from .BaseTest import BaseTest
from .variables import *
from .bugprone import *
from .readability import *
from .RuleExecutionError import *
