from pycparser import c_ast


class ConditionAnalyzer(object):

    def __init__(self, cond):
        self.__cond = cond
        self.__groups = []

    def __get_all_leafs(self, node):
        leafs = []
        child: c_ast.Node
        if not isinstance(node, c_ast.BinaryOp) or node.op not in ['&&', '||']:
            return leafs
        if isinstance(node.left, c_ast.BinaryOp) and node.left.op in ['&&', '||']:
            leafs += self.__get_all_leafs(node.left)
        else:
            leafs += [node.left]

        if isinstance(node.right, c_ast.BinaryOp) and node.right.op in ['&&', '||']:
            leafs += self.__get_all_leafs(node.right)
        else:
            leafs += [node.right]

        return leafs

    def __analyze_conjunction(self, node):
        # print(self.__get_all_leafs(node))
        return [self.__get_all_leafs(node)]

    def __analyze_disjunction(self, disj: c_ast.Node):
        subgroups = []
        if isinstance(disj, c_ast.BinaryOp) and disj.op in ['||']:
            subgroups += self.__analyze_disjunction(disj.left)
            subgroups += self.__analyze_disjunction(disj.right)
        elif isinstance(disj, c_ast.BinaryOp) and disj.op in ['&&']:
            subgroups = self.__analyze_conjunction(disj)
        else:
            subgroups = [[disj]]

        return subgroups

    def analyze(self):
        if isinstance(self.__cond, c_ast.BinaryOp) and self.__cond.op == "&&":
            self.__groups += self.__analyze_conjunction(self.__cond)
        elif isinstance(self.__cond, c_ast.BinaryOp) and self.__cond.op == "||":
            self.__groups += self.__analyze_disjunction(self.__cond.left)
            self.__groups += self.__analyze_disjunction(self.__cond.right)
        else:
            self.__groups += [[self.__cond]]

    def __str__(self):
        text = ""
        for subgroup in self.__groups:
            text += "("
            for item in subgroup:
                text += ConditionAnalyzer.__to_str(item) + " "
            text += ") "
        return text

    @staticmethod
    def __to_str(node):
        if isinstance(node, c_ast.ID):
            return node.name
        if isinstance(node, c_ast.StructRef):
            text = ""
            text += ConditionAnalyzer.__to_str(node.name)
            text += node.type
            text += ConditionAnalyzer.__to_str(node.field)
            return text
        if isinstance(node, c_ast.Constant):
            return node.value
        if isinstance(node, c_ast.BinaryOp):
            return ConditionAnalyzer.__to_str(node.left)+node.op+ConditionAnalyzer.__to_str(node.right)
        if isinstance(node, c_ast.FuncCall):
            text = ""
            text += ConditionAnalyzer.__to_str(node.name)
            text += "(" + ConditionAnalyzer.__to_str(node.args) + ")"
            return text
        if isinstance(node, c_ast.ExprList):
            text = ""
            for exp in node.exprs:
                text += ConditionAnalyzer.__to_str(exp)
                text += ","
            return text[:-1]
        if isinstance(node, c_ast.ArrayRef):
            return ConditionAnalyzer.__to_str(node.name)+"["+ConditionAnalyzer.__to_str(node.subscript)+"]"
        return node.__class__.__name__
