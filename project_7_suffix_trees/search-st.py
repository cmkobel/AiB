# Title: Search Suffix Tree
# Description: Builds a suffix tree from a string
from trienode import trienode
# Author: Carl M. Kobel

# class-ify
class suffixtree:
    def __init__(self, S, null_char = '$', debug = False):
        self.S = S + null_char
        self.null_char = null_char
        self.DEBUG = debug
        
        self.tree = trienode('', '') # Initialize the trie.

        for suffix in self.suffixes(self.S):
            self.recursive_appender(self.tree, suffix)

        # compact 
        self.compact(self.tree)


        self.tree.visualize(True)


    def dprint(self, *args, **kwargs): #
        """ To easily toggle debugprints. """
        if self.DEBUG:
            print(*args, **kwargs)


    def recursive_appender(self, node, suffix):
            
        def add_string(node, string):
            """ Helper function that inserts a string, letter for letter - at a specific node. """

            def unfold_string(S):
                """ Unfolds the string in a way that makes it easy to populate edge_in_label and string_label in the nodes serially down the tree. 
                This function was made to put in the full string in the beginning, but because I want the same function that appends suffixes to
                automatically put in the full string. """
                #S += null_char # Append null char.
                for _i, i in enumerate(S):
                    yield i, S[0:_i+1]

            previous_string_label = node.string_label
            for edge_in, string in unfold_string(string):
                new_node = trienode(edge_in, previous_string_label + edge_in)
                previous_string_label = previous_string_label + edge_in # or previous_string_label += edge_in
                node.children.append(new_node)
                node = new_node
        

        # Overview of the following three possible cases:
        # 0: String is empty, close
        # 1: Diversion. add string.
        # 2: String matches tree. continue recursively
        
        # 0 Base case.
        self.dprint('suffix:', suffix)
        if len(suffix) == 0: # base case
            self.dprint('0) reached the end')
            return 
        
        # 1 No child suffices, add string.
        elif suffix[0:1] not in [child.in_edge_label for child in node.children]:
            self.dprint('1)', suffix[0:1], 'from', suffix, 'not in node, adding...')
            add_string(node, suffix)
            return

        # 2 The part that calls itself.
        else: 
            self.dprint('2) else; suffix[0:1]', suffix[0:1], 'exists in children,',[i.in_edge_label for i in node.children], ' calling next suffix')
            for child in node.children:
                if suffix[0:1] == child.in_edge_label:
                    self.dprint('calling for suffix[1:]:', suffix[1:])
                    self.recursive_appender(child, suffix[1:])


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



