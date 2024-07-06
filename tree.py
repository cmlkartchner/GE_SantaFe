
# test mutation stuff

class Node:

    def __init__(self, symbol, children):
        self.symbol = symbol
        self.children = children
        self.coordinate = None # (1,1) = 'first child of the first child of the root'
    
    def add_child(self, child):
        self.children.append(child)

    # def __repr__(self, level=0):
    #     ret = "\t" * level + self.symbol + "\n"
    #     for child in self.children:
    #         ret += child.__repr__(level + 1)
    #     return ret

    def __str__(self):
        return self.pretty_print()
    
    def pretty_print(self, prefix="", is_tail=True):
        ret = prefix + ("└── " if is_tail else "├── ") + str(self.symbol) + "\n"
        for i, child in enumerate(self.children):
            is_last = i == (len(self.children) - 1)
            new_prefix = prefix + ("    " if is_tail else "│   ")
            ret += child.pretty_print(new_prefix, is_last)
        return ret

    # def pretty_print(self, level=0):
    #     ret = "  " * level + str(self.symbol) + "\n"
    #     for child in self.children:
    #         ret += child.pretty_print(level + 1)
    #     return ret

    def __repr__(self):
        return f"TreeNode({repr(self.symbol)}, {repr(self.children)})"
