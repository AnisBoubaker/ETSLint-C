from clinter.rules import BaseRule, BaseTest
from pycparser.c_ast import EmptyStatement, Compound


class RuleIfElseWithEmptyIf(BaseRule):
    def __init__(self, reporter=None):
        BaseRule.__init__(self, "static", reporter)

    def __compound_empty(self, node):
        if node.block_items is None:
            return True
        for item in node.block_items:
            if not isinstance(item, EmptyStatement):
                return False
        return True

    def visit_If(self, node):
        message = "If block is empty having a non-empty else block."
        if node.iffalse is None:
            return
        if isinstance(node.iffalse, EmptyStatement):
            return
        if isinstance(node.iffalse, Compound) and self.__compound_empty(node.iffalse):
            return
        if isinstance(node.iftrue, EmptyStatement):
            self.reporter.do_report(self, node.coord, message)
        if isinstance(node.iftrue, Compound) and self.__compound_empty(node.iftrue):
            self.reporter.do_report(self, node.coord, message)


class TestIfElseWithEmptyIf(BaseTest):
    def setUp(self):
        self._rule_instance = RuleIfElseWithEmptyIf(self._reporter)

    def test1(self):
        self._tested_code = """
        int main(){
            int a = 10;
            if(a<10){
            }
            else {
                a++;
            }
        }
        """
        self._run_rule()
        self.expect_error("If block empty and else is not empty NOOK")

    def test2(self):
        self._tested_code = """
        int main(){
            int a = 10;
            if(a<10) 
                ;
            else {
                a++;
            }
        }
        """
        self._run_rule()
        self.expect_error("If block have an empty statement and else is not empty NOOK")

    def test3(self):
        self._tested_code = """
        int main(){
            int a = 10;
            if(a<10) 
                printf("");
            else {
                a++;
            }
        }
        """
        self._run_rule()
        self.expect_no_error("If block have one statement and else is not empty OK")

    def test4(self):
        self._tested_code = """
        int main(){
            int a = 10;
            if(a<10){ 
                printf("");
            }
            else {
                a++;
            }
        }
        """
        self._run_rule()
        self.expect_no_error("If block have non-empty block and else is not empty OK")

    def test5(self):
        self._tested_code = """
        int main(){
            int a = 10;
            if(a<10)
                ;
        }
        """
        self._run_rule()
        self.expect_no_error("if block empty without else OK")

    def test6(self):
        self._tested_code = """
        int main(){
            int a = 10;
            if(a<10){
                printf("");
            }
        }
        """
        self._run_rule()
        self.expect_no_error("non empty if without else OK")

