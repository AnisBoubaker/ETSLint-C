from pycparser import c_ast
from pycparser.c_ast import FileAST, ID, BinaryOp


class NodeParenter(c_ast.NodeVisitor):
    """
    AST Visitor that collects node parents of each AST node, implemented as a Singleton
    """
    __instances = {}

    def __init__(self, node):
        self.__parents = {}
        self.__ast = node
        self.visit(node)

    @staticmethod
    def get_instance(node: c_ast.Node):
        if node not in NodeParenter.__instances:
            NodeParenter.__instances[node] = NodeParenter(node)

        return NodeParenter.__instances[node]

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

    def get_first_parent_of_type(self, node: c_ast.Node, type_list: list):
        current_parent = node
        while self.get_parent(current_parent) is not None and \
                self.get_parent(current_parent).__class__.__name__ not in type_list:
            current_parent = self.get_parent(current_parent)
        return self.get_parent(current_parent)

    def get_first_parent_not_of_type(self, node: c_ast.Node, type_list: list):
        current_parent = node
        while self.get_parent(current_parent).__class__.__name__ in type_list:
            current_parent = self.get_parent(current_parent)
        if current_parent == node:
            return None
        return current_parent

    def get_all_childs(self, parent: c_ast.Node, deep_search=False):
        childs = []
        for c in parent:
            childs += [c]
            if deep_search:
                childs += self.get_all_childs(c)
        return childs

    def is_child_of(self, parent, node):
        for c in parent:
            if c == node:
                return True
            if self.is_child_of(c, node):
                return True
        return False

    def get_all_siblings(self, parent: c_ast.Node, ref_child: c_ast.Node, deep_search=False):
        childs = self.get_all_childs(parent, deep_search)
        siblings = []
        for c in childs:
            if c != ref_child and not self.is_child_of(ref_child, c):
                siblings += [c]
        return siblings

    def get_all_next_siblings(self, parent: c_ast.Node, ref_child: c_ast.Node, deep_search=False):
        childs = self.get_all_childs(parent, deep_search)
        next_childs = []
        found = False
        for c in childs:
            if found and not self.is_child_of(ref_child, c):
                next_childs += [c]
            if c == ref_child:
                found = True
        return next_childs

    def get_all_previous_siblings(self, parent: c_ast.Node, ref_child: c_ast.Node, deep_search=False):
        childs = self.get_all_childs(parent, deep_search)
        previous_childs = []
        for c in childs:
            if c == ref_child:
                return previous_childs
            if not self.is_child_of(ref_child, c):
                previous_childs += [c]
        return previous_childs

    def __str__(self):
        result = ""
        for child in self.__parents.keys():
            result += "Child: " + type(child).__name__ + " Parent: " + type(self.__parents[child]).__name__ + "\n"
        return result

    def __repr__(self):
        return self.__str__()

