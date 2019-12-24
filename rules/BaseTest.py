import unittest
from pycparser.c_parser import CParser
from reporters.NoopReporter import NoopReporter


class BaseTest(unittest.TestCase):
    _tested_code = ""
    _ast = None
    _parser = CParser()
    _reporter = NoopReporter()
    _rule_instance = None

    def _run_rule(self):
        self._ast = self._parser.parse(self._tested_code, "no_file.c")
        self._rule_instance.visit(self._ast)

    def expect_error(self, message=""):
        self.assertTrue(len(self._reporter.get_reports_by_rule(self._rule_instance)) > 0, message)
        self._reporter.clear()

    def expect_no_error(self, message=""):
        self.assertTrue(len(self._reporter.get_reports_by_rule(self._rule_instance)) == 0, message)
        self._reporter.clear()
