from clinter.rules import BaseRule, BaseTest, RuleExecutionError
from etslint import CLinter

class RuleUnusedExpression(BaseRule):
    def __init__(self, reporter=None):
        BaseRule.__init__(self, "static", reporter)
        self.__parenter = None

    def visit_UnaryOp(self, node):
        if self.__parenter is None:
            raise RuleExecutionError("Unable to access node parents.")


    def visit_FileAST(self, node):
        self.__parenter = CLinter.NodeParenter.get_instance(node)
        self.generic_visit(node)


    """def visit_Compound(self, node):
        message = "Expression's result is not used."
        for stmt in node.stmt.block_items:
            if isinstance(stmt, UnaryOp) or isinstance(stmt, BinaryOp):
                self.reporter.do_report(self, node.coord, message)
            elif isinstance(stmt, Compound):
                self.visit_Compound(stmt)
            elif isinstance(stmt, For):
                self.visit_Compound(stmt)
    """


class TestUnusedExpression(BaseTest):
    def setUp(self):
        self._rule_instance = RuleUnusedExpression(self._reporter)

    def test1(self):
        self._tested_code = """
        
        int main();
        
        int main(){
            int a = 10 ;
            for( ; a < 10 ; ){


            }
        }
        """
        self._run_rule()
        #self.expect_no_error("For loop with empty body NOOK")
