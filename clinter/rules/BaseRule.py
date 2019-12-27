"""
Base rule class, subclassed by every rule.

Provides a set of utility methods used or expose by concrete rule classes:
- __str__: converts a rule instance into string, including the rule name along with it's package name
"""
from pycparser import c_ast


class BaseRule(c_ast.NodeVisitor):
    def __init__(self, category=None, reporter=None):
        self.__category = category
        self.__reporter = reporter

    @property
    def category(self):
        return self.__category

    @property
    def reporter(self):
        return self.__reporter

    def __str__(self):
        """Gives rule's name, including its container module."""
        return self.__module__
