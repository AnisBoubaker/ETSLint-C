from rules import BaseRule
from pycparser.c_ast import BinaryOp, UnaryOp

class RuleBitwiseOperationInCondition(BaseRule):
    def __init__(self, reporter=None):
        BaseRule.__init__(self, "static", reporter)

    def __get_all_bitwise_conditions(self, cond):
        result = []
        conditions_stack = []
        if not isinstance(cond, BinaryOp) and not isinstance(cond, UnaryOp):
            return result
        conditions_stack.append(cond)
        while len(conditions_stack) > 0:
            current_cond = conditions_stack.pop()
            if current_cond.op == '&' or current_cond.op == '|':
                result.append(current_cond)
            if isinstance(current_cond, BinaryOp):
                if isinstance(current_cond.left, BinaryOp) or isinstance(current_cond.left, UnaryOp):
                    conditions_stack.append(current_cond.left)
                if isinstance(current_cond.right, BinaryOp) or isinstance(current_cond.right, UnaryOp):
                    conditions_stack.append(current_cond.right)
            else:  # current_cond is a UnaryOp
                if isinstance(current_cond.expr, BinaryOp) or isinstance(current_cond.expr, UnaryOp):
                    conditions_stack.append(current_cond.expr)

        return result

    def __report_bitwise_error(self, node, statement):
        bitwise_conds = self.__get_all_bitwise_conditions(node.cond)
        if len(bitwise_conds) == 0:
            return
        for cond in bitwise_conds:
            message = "Condition in {} statement uses bitwise operator {} (probable confusion with comparison operator {})."\
                .format(statement, cond.op, 2 * cond.op)
            self.reporter.do_report(self, node.coord, message)

    def visit_If(self, node):
        self.__report_bitwise_error(node, "if")

    def visit_For(self, node):
        self.__report_bitwise_error(node, "for")

    def visit_While(self, node):
        self.__report_bitwise_error(node, "while")

    def visit_DoWhile(self, node):
        self.__report_bitwise_error(node, "do..while")
