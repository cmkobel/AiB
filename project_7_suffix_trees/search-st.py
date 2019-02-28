# Title: Search Suffix Tree
# Description: Builds a suffix tree from a string
from trienode import trienode
# Author: Carl M. Kobel


null_char = '$' # null character
S = 'mississippi' # tatat, mississippi
S += null_char
n = len(S)
DEBUG = not True


def dprint(*args, **kwargs): #
    """ To easily toggle debugprints. """
    if DEBUG:
        print(*args, **kwargs)



tree = trienode('', '') # Initialize the trie.


def recursive_appender(node, suffix):
        
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
    dprint('suffix:', suffix)
    if len(suffix) == 0: # base case
        dprint('0) reached the end')
        return 
    
    # 1 No child suffices, add string.
    elif suffix[0:1] not in [child.in_edge_label for child in node.children]:
        dprint('1)', suffix[0:1], 'from', suffix, 'not in node, adding...')
        add_string(node, suffix)
        return

    # 2 The part that calls itself.
    else: 
        dprint('2) else; suffix[0:1]', suffix[0:1], 'exists in children,',[i.in_edge_label for i in node.children], ' calling next suffix')
        for child in node.children:
            if suffix[0:1] == child.in_edge_label:
                dprint('calling for suffix[1:]:', suffix[1:])
                recursive_appender(child, suffix[1:])


def suffixes(S):
        """ Generates all suffixes from S """
        for i in range(n):
            yield S[i:]

for suffix in suffixes(S):
    recursive_appender(tree, suffix)



def compact(node):
    for node in tree:
        while(len(node.children) == 1): # Når node har éen child; spis den næste.
            node.in_edge_label += node.children[0].in_edge_label
            node.string_label += node.children[0].in_edge_label
            node.children = node.children[0].children




compact(tree)


tree.visualize(True)










