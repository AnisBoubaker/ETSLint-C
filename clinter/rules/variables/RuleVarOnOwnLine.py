from clinter.rules import BaseRule, BaseTest
import unittest


class RuleVarOnOwnLine(BaseRule):
    __declared = []
    __last_file = None

    def __init__(self, reporter=None):
        BaseRule.__init__(self, "style", reporter)

    def visit_Decl(self, node):
        if self.__last_file is None or self.__last_file != node.coord.file:
            self.__last_file = node.coord.file
            self.__declared.clear()

        sameline_variable = [var for var in self.__declared if var['line'] == node.coord.line]

        if len(sameline_variable) > 0:
            message = "Variable {} should be declared on its own line.".format(node.name)
            self.reporter.do_report(self, node.coord, message)

        # It's probably overkill to keep all declarations in a list. However, we can't be sure the AST traversal will be
        # sequential.
        self.__declared += [{'name': node.name, 'line': node.coord.line}]


class TestVarOnOwnLine(BaseTest):

    def setUp(self):
        self._rule_instance = RuleVarOnOwnLine(self._reporter)

    def test1(self):
        self._tested_code = """
        int main(){
            int a, 
                b;
        }
        """
        self._run_rule()
        self.expect_no_error("Variable on each line OK")

    def test2(self):
        self._tested_code = """
        int main(){
            int a, b;
        }
        """
        self._run_rule()
        self.expect_error("two variables on same line NOOK")

    def test3(self):
        self._tested_code = """
        typedef struct{
            int x;
            double y;
        } my_type;
        
        int main(){
            my_type a, 
                    b;
        }
        """
        self._run_rule()
        self.expect_no_error("User defined variables on separate lines OK")

    def test4(self):
        self._tested_code = """
        typedef struct{
            int x;
            double y;
        } my_type;

        int main(){
            my_type a, b;
            a =!(10+5);
        }
        """
        self._run_rule()
        self.expect_error("User defined variables on the same line NOOK")


if __name__ == '__main__':
    unittest.main()
