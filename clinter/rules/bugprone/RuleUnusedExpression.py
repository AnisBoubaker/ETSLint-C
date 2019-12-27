from clinter.rules import BaseRule, BaseTest, RuleExecutionError
from clinter.NodeParenter import NodeParenter
from pycparser.c_ast import Compound

class RuleUnusedExpression(BaseRule):

    __side_effect_ops = ['p++', 'p--', '+=', '-=', '*=', '%=', '<<=', '>>=', '&=', '^=', '|=']

    def __init__(self, reporter=None):
        BaseRule.__init__(self, "static", reporter)
        self.__parenter = None

    def visit_UnaryOp(self, node):
        if self.__parenter is None:
            raise RuleExecutionError("Unable to access node parents.")
        the_parent = self.__parenter.get_parent(node)
        message = "Expression's result is not used."
        if isinstance(the_parent, Compound) and node.op not in self.__side_effect_ops:
            self.reporter.do_report(self, node.coord, message)

    def visit_BinaryOp(self, node):
        self.visit_UnaryOp(node)


    def visit_FileAST(self, node):
        self.__parenter = NodeParenter.get_instance(node)
        self.generic_visit(node)


class TestUnusedExpression(BaseTest):
    def setUp(self):
        self._rule_instance = RuleUnusedExpression(self._reporter)

    def test1(self):
        self._tested_code = """

        int main();

        int a;

        int main(){
            int a = 10 ;

            for( ; a -20 ; ){
                printf("");

            }
        }
        """
        self._run_rule()
        self.expect_no_error("Expression used as condition OK")

    def test2(self):
        self._tested_code = """

        int main();

        int main(){
            int a = 10 ;
            
            a - 20;
            
            for( ; a < 10 ; ){
                a + 20;

            }
        }
        """
        self._run_rule()
        self.expect_error("Useless expression in block NOOK")

    def test3(self):
        self._tested_code = """
        
        int main();
        
        int main(){
            int a = 10 ;
            for( ; a < 10 ; ){
                a + 20;

            }
        }
        """
        self._run_rule()
        self.expect_error("Useless expression in internal block NOOK")

    def test4(self):
        self._tested_code = """

        int main();

        int main(){
            int a = 10 ;
            for( ; a < 10 ; ){
                a &= 5;

            }
        }
        """
        self._run_rule()
        self.expect_no_error("Expression using side effect operator OK")
