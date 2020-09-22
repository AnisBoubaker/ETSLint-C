from clinter.rules import BaseRule, BaseTest, RuleExecutionError
from clinter.NodeParenter import NodeParenter
from pycparser.c_ast import Node, BinaryOp, UnaryOp, ID, StructRef
from ConditionAnalzer import ConditionAnalyzer


class RuleBrokenNullCheck(BaseRule):

    def __init__(self, reporter=None):
        BaseRule.__init__(self, "static", reporter)
        self.__parenter : NodeParenter = None

    @staticmethod
    def __is_null_check(node : Node):
        """Verify if the given node is a NULL check

        If the node is actually a NULL check, return a tuple containing:
        - The node encompassing the reference checked against NULL (an ID or a StructRef)
        - The operator used to check ('==' or '!=')
        :param node: The node to check
        :return: A tuple (Node, str)
        """
        if isinstance(node, BinaryOp) and node.op not in ['==', '!=']:
            return None, None
        if isinstance(node, UnaryOp) and node.op != "!":
            return None, None

        # Detect broken NULL check of type `if(x)` or `if(x->y)`
        if isinstance(node, (ID, StructRef)):
            return node, "!="

        # Detect broken NULL check of type `x == NULL` or `x->y == NULL` or `NULL == x` (or != equivalents)
        if isinstance(node, BinaryOp) and node.op in ['==', '!=']:
            if isinstance(node.left, (ID, StructRef)) and isinstance(node.right, ID) and node.right.name == "NULL":
                return node.left, node.op
            if isinstance(node.right, (ID, StructRef)) and isinstance(node.left, ID) and node.left.name == "NULL":
                return node.right, node.op

        # Detect broken NULL check of type `!x` or `!x->y`
        if isinstance(node, UnaryOp):
            if isinstance(node.expr, (ID, StructRef)):
                return node.expr, "!="

        return None, None

    """def visit_BinaryOp(self, node):
        null_checks = []
        if node.op not in ('&&', '||', '!=', '=='):
            return
        if node.op in ('==', '!='):
            null_check1 = self.__is_null_check(node)
            if null_check1[0] is not None:
                null_checks += [null_check1]
        for c in node:
            if isinstance(c, (ID, StructRef)):
                null_check1 = self.__is_null_check(c)
                if null_check1[0] is not None:
                    null_checks += [null_check1]
            else:
                self.generic_visit(node)
        if len(null_checks) == 0:
            return
        parent_node = self.__parenter.get_first_parent_of_type(node, ['If', 'For', 'While', 'DoWhile'])
        print()
        print(parent_node.cond)
        for (null_check, _) in null_checks:
            print("THE NEXT ARE:")
            print(self.__parenter.get_all_next_siblings(parent_node.cond, null_check, deep_search=True))

    def visit_UnaryOp(self, node):
        null_checks = []
        if node.op == "!":
            null_check1 = self.__is_null_check(node)
            if null_check1[0] is not None:
                null_checks += [null_check1]
            else:
                self.generic_visit(node)
        if len(null_checks) == 0:
            return
        parent_node = self.__parenter.get_first_parent_of_type(node, ['If', 'For', 'While', 'DoWhile'])
        print()
        print(node)
        for (null_check, _) in null_checks:
            print("THE NEXT ARE:")
            print(self.__parenter.get_all_next_siblings(parent_node.cond, null_check, deep_search=True))
    """

    def visit_If(self, node):
        analyzer = ConditionAnalyzer(node.cond)
        analyzer.analyze()
        print(analyzer)


    def visit_FileAST(self, node):
        self.__parenter = NodeParenter.get_instance(node)
        self.generic_visit(node)


class TestBrokenNullCheck(BaseTest):
    def setUp(self):
        self._rule_instance = RuleBrokenNullCheck(self._reporter)

    def test1(self):
        self._tested_code = """
        typedef struct{
            int x;
        } my_type;
        int main(){
            my_type *a;
            if( b || a->x->y && a && (a->y==1 || toto) || func(a,b)==1 || tab[1][2] == 10) ;
        }
        """
        self._run_rule()
        self.expect_no_error("Expression used as condition OK")


# if !a && a->x
# if a==NULL