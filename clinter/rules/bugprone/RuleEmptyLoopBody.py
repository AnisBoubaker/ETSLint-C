from clinter.rules import BaseRule, BaseTest
from pycparser.c_ast import EmptyStatement, Compound


class RuleEmptyLoopBody(BaseRule):
    def __init__(self, reporter=None):
        BaseRule.__init__(self, "static", reporter)

    def visit_For(self, node, message=None):
        if message is None:
            message = "For loop has an empty block."
        # in case we have an EmptyStatement, we discard it as it'll be piked up by LoopOrConditionnalWithoutStatement
        if isinstance(node.stmt, EmptyStatement):
            return
        if isinstance(node.stmt, Compound) and node.stmt.block_items is None:
            self.reporter.do_report(self, node.coord, message)
            return
        for stmt in node.stmt.block_items:
            if not isinstance(stmt, EmptyStatement):
                return
        self.reporter.do_report(self, node.coord, message)

    def visit_While(self, node):
        message = "While loop has an empty block."
        self.visit_For(node, message)


class TestEmptyLoopBody(BaseTest):
    def setUp(self):
        self._rule_instance = RuleEmptyLoopBody(self._reporter)

    def test1(self):
        self._tested_code = """
        int main(){
            int a = 10 ;
            for( ; a < 10 ; ){
               
               
            }
        }
        """
        self._run_rule()
        self.expect_error("For loop with empty body NOOK")

    def test2(self):
        self._tested_code = """
        int main(){
            int a = 10 ;
            while( a < 10 ){


            }
        }
        """
        self._run_rule()
        self.expect_error("While loop with empty body NOOK")

    def test3(self):
        self._tested_code = """
        int main(){
            int a = 10 ;
            while( a < 10 ){
                ;
                ;
                ;
            }
        }
        """
        self._run_rule()
        self.expect_error("While loop with body containing only empty statements NOOK")

    def test3(self):
        self._tested_code = """
        int main(){
            int a = 10 ;
            while( a < 10 ){
                printf("Not empty!");
            }
        }
        """
        self._run_rule()
        self.expect_no_error("While loop with non-empty body OK")

    def test4(self):
        self._tested_code = """
        int main(){
            int a = 10 ;
            while( a < 10 ){
                ;
                ;
                printf("Not empty!");
                ;
            }
        }
        """
        self._run_rule()
        self.expect_no_error("While loop with mix of empty statements and non-empty statements OK")

