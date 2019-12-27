from clinter.rules import BaseRule, BaseTest, RuleExecutionError
from clinter.NodeParenter import NodeParenter
from pycparser.c_ast import Compound, FileAST, Decl, ArrayDecl


class RuleMisplacedDeclaration(BaseRule):

    def __init__(self, reporter=None):
        BaseRule.__init__(self, "static", reporter)
        self.__parenter = None
        self.__compounds_ended_decl = {}

    def visit(self, node):
        if isinstance(node, FileAST):
            return self.visit_FileAST(node)
        elif isinstance(node, Decl):
            return self.visit_Decl(node)
        elif isinstance(node, ArrayDecl):
            return self.visit_ArrayDecl(node)
        else:
            return self.visit_Others(node)

    def visit_Decl(self, node):
        if self.__parenter is None:
            raise RuleExecutionError("Unable to access node parents.")
        the_parent = self.__parenter.get_parent(node)
        # we ignore all declarations which are not part of a compound (eg. id declarations happens in for( ... ;  ; ) )
        if not isinstance(the_parent, Compound):
            return
        message = "Misplaced declaration. All declarations must be located at the beginning of a block."
        if the_parent not in self.__compounds_ended_decl:
            self.__compounds_ended_decl[the_parent] = False
        if self.__compounds_ended_decl[the_parent]:
            self.reporter.do_report(self, node.coord, message)

    def visit_ArrayDecl(self, node):
        self.visit_TypeDecl()

    def visit_FileAST(self, node):
        # print(node)
        self.__parenter = NodeParenter.get_instance(node)
        self.generic_visit(node)

    def visit_Others(self, node):
        if self.__parenter is None:
            raise RuleExecutionError("Unable to access node parents.")
        the_parent = self.__parenter.get_parent(node)
        if not isinstance(the_parent, Compound):
            self.generic_visit(node)
            return

        self.__compounds_ended_decl[the_parent] = True
        self.generic_visit(node)



class TestMisplacedDeclaration(BaseTest):
    def setUp(self):
        self._rule_instance = RuleMisplacedDeclaration(self._reporter)

    def test1(self):
        self._tested_code = """

        int main();

        int z;
        
        void test()
        {
            int x = 10;
        }

        int main(){
            int a = 10 ;

            for( ; a -20 ; ){
                printf("");

            }
            int b;
        }
        """
        self._run_rule()
        self.expect_error("b declaration is misplaced NOOK")

    def test2(self):
        self._tested_code = """
        int z;

        void test()
        {
            int x = 10;
        }

        int main(){
            int a = 10 ;

            for( ; a -20 ; ){
                printf("");
                
                int b;
                
                printf("");
            }
        }
        """
        self._run_rule()
        self.expect_error("b declaration in subblock is misplaced NOOK")

    def test3(self):
        self._tested_code = """

        int main();

        int z;

        void test()
        {
            int x = 10;
        }

        int main(){
            int a = 10 ;
            int b;
            
            for( ; a -20 ; ){
                printf("");

            }
        }
        """
        self._run_rule()
        self.expect_no_error("b declaration is correctly placed OK")

    def test4(self):
        self._tested_code = """
        int z;

        void test()
        {
            int x = 10;
        }

        int main(){
            int a = 10 ;

            for( ; a -20 ; ){
                int b;
                
                printf("");

                printf("");
            }
        }
        """
        self._run_rule()
        self.expect_no_error("b declaration in subblock is correctly placed OK")

    def test5(self):
        self._tested_code = """
        int z;

        typedef struct{
            int f1;
            int f2;
        } my_type;

        int main(){
            int a = 10 ;
            my_type *var;

            var->f1 = 10;
            for( ; a -20 ; ){
                printf("");

                int tab[10] = {10, 5};
                printf("");
            }
        }
        """
        self._run_rule()
        self.expect_error("tab declaration is misplaced NOOK")

    def test6(self):
        self._tested_code = """
        int z;

        typedef struct{
            int f1;
            int f2;
        } my_type;

        int main(){
            int a = 10 ;
            
            for( ; a -20 ; ){
                printf("");
                printf("");
            }
            
            my_type *var;

            var->f1 = 10;
        }
        """
        self._run_rule()
        self.expect_error("var pointer declaration is misplaced NOOK")

    def test7(self):
        self._tested_code = """
        int z;

        typedef struct{
            int f1;
            int f2;
        } my_type;

        int main(){
            int a = 10 ;
            my_type *var;
            
            for( ; a -20 ; ){
                printf("");
                printf("");
            }

            var->f1 = 10;
        }
        """
        self._run_rule()
        self.expect_no_error("var pointer declaration is correctly placed NOOK")