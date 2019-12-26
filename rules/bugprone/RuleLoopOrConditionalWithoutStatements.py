from rules import BaseRule, BaseTest
from pycparser.c_ast import EmptyStatement


class RuleLoopOrConditionalWithoutStatements(BaseRule):
    def __init__(self, reporter=None):
        BaseRule.__init__(self, "static", reporter)

    def visit_If(self, node):
        if isinstance(node.iftrue, EmptyStatement):
            message = "If statement has no instructions. You should remove the `;` after `if` condition."
            self.reporter.do_report(self, node.coord, message)

    def visit_For(self, node):
        if isinstance(node.stmt, EmptyStatement):
            message = "For loop has no instructions. You should remove the `;` after `for` declaration."
            self.reporter.do_report(self, node.coord, message)

    def visit_While(self, node):
        self.visit_For(node)


class TestLoopOrConditionalWithoutStatements(BaseTest):
    def setUp(self):
        self._rule_instance = RuleLoopOrConditionalWithoutStatements(self._reporter)

    def test1(self):
        self._tested_code = """
        int main(){
            int a = 10 ;
            while(a < 10);
        }
        """
        self._run_rule()
        self.expect_error("While loop with no statements NOOK")

    def test2(self):
        self._tested_code = """
        int main(){
            int a = 10 ;
            while(a < 10){
            }
        }
        """
        self._run_rule()
        self.expect_no_error("While loop with empty block OK")

    def test3(self):
        self._tested_code = """
        int main(){
            int a = 10 ;
            while(a < 10)
                a = 20;
        }
        """
        self._run_rule()
        self.expect_no_error("While loop with one statement OK")

    def test4(self):
        self._tested_code = """
        int main(){
            int a = 10 ;
            while(a < 10){
                a = 20;
            }
        }
        """
        self._run_rule()
        self.expect_no_error("While loop with none empty block OK")

    def test5(self):
        self._tested_code = """
        int main(){
            int a = 10 ;
            for( ; a < 10 ; );
        }
        """
        self._run_rule()
        self.expect_error("For loop with no statements NOOK")

    def test6(self):
        self._tested_code = """
        int main(){
            int a = 10 ;
            if( a < 10 );
        }
        """
        self._run_rule()
        self.expect_error("If with no statements NOOK")

    def test7(self):
        self._tested_code = """
        int main(){
            int a = 10 ;
            if( a < 10 )
                a = 20;
        }
        """
        self._run_rule()
        self.expect_no_error("If with single statements OK")

    def test8(self):
        self._tested_code = """
        int main(){
            int a = 10 ;
            if( a < 10 ){
            }
        }
        """
        self._run_rule()
        self.expect_no_error("If with empty block OK")

    def test9(self):
        self._tested_code = """
        int main(){
            int a = 10 ;
            if( a < 10 ){
                a = 20;
            }
        }
        """
        self._run_rule()
        self.expect_no_error("If with non-empty block OK")

