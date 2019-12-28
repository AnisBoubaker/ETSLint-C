from pycparser import c_ast
from pycparser.c_ast import FileAST


class NodeParenter(c_ast.NodeVisitor):
    """
    AST Visitor that collects node parents of each AST node, implemented as a Singleton
    """
    __instances = {}

    def __init__(self, ast):
        self.__parents = {}
        self.__ast = ast
        self.visit(ast)

    @staticmethod
    def get_instance(ast: FileAST):
        if ast not in NodeParenter.__instances:
            NodeParenter.__instances[ast] = NodeParenter(ast)

        return NodeParenter.__instances[ast]

    def visit(self, node):
        children = node.children()
        for child in children:
            self.__parents[child[1]] = node
            self.visit(child[1])

    @property
    def parents(self):
        return self.__parents

    def get_parent(self, node: c_ast.Node, level=1):
        """Retrieves the ancestor node of `node` going up `level` levels in the hierarchy"""
        curr_node = node
        while level > 0:
            if curr_node not in self.__parents:
                return None
            curr_node = self.__parents[node]
            level -= 1
        return curr_node

    def get_farthest_parent_of_type(self, node: c_ast.Node, type_list: list):
        current_parent = node
        while self.get_parent(current_parent).__class__.__name__ in type_list:
            current_parent = self.get_parent(current_parent)
        if current_parent == node:
            return None
        return current_parent

    def __str__(self):
        result = ""
        for child in self.__parents.keys():
            result += "Child: " + type(child).__name__ + " Parent: " + type(self.__parents[child]).__name__ + "\n"
        return result

    def __repr__(self):
        return self.__str__()

