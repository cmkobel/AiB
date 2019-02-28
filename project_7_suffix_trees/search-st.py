# Title: Search Suffix Tree
# Description: Builds a suffix tree from a string
from trienode import trienode
# Author: Carl M. Kobel


class suffixtree:
    def __init__(self, S, null_char = '$', debug = False):
        self.S = S + null_char
        self.null_char = null_char
        self.DEBUG = debug
        

        ## Workflow: ##

        # 1) Initialize an root node.
        self.tree = trienode('', '') 

        # 2) Add all suffixes to the tree.
        for suffix in self.suffixes(self.S):
            self.recursively_append(self.tree, suffix)

        # 3)
        self.compact(self.tree)

        # 4)
        self.tree.visualize(True)


    def add_string(self, node, string):
        """ Helper function that inserts a string, letter for letter - at a specific node. """

        def unfold_string(S):
            """ Unfolds the string in a way that makes it easy to populate edge_in_label and string_label in the nodes serially down the tree. """
            for _i, i in enumerate(S):
                yield i, S[0:_i+1]

        previous_string_label = node.string_label
        for edge_in, string in unfold_string(string):
            new_node = trienode(edge_in, previous_string_label + edge_in)
            previous_string_label += edge_in
            node.children.append(new_node)
            node = new_node


    def recursively_append(self, node, suffix):

        # Overview of the following three possible cases:
        # 0: String is empty, close
        # 1: Diversion. add string.
        # 2: String matches tree. continue recursively
        
        # 0 Base case.

        if len(suffix) == 0: # base case
            return
        
        # 1 No child suffices, add string.
        elif suffix[0:1] not in [child.in_edge_label for child in node.children]:
            self.add_string(node, suffix)
            return

        # 2 The part that calls itself.
        else: 
            for child in node.children:
                if suffix[0:1] == child.in_edge_label:
                    self.recursively_append(child, suffix[1:])


    def suffixes(self, S):
            """ Generates all suffixes from S """
            for i in range(len(self.S)):
                yield S[i:]


    def compact(self, node):
        for node in self.tree:
            while(len(node.children) == 1): # Eat the child if it is lone.
                node.in_edge_label += node.children[0].in_edge_label
                node.string_label += node.children[0].in_edge_label
                node.children = node.children[0].children



if __name__ == "__main__":
    o = suffixtree('tatat')



