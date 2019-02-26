# Title: Search Suffix Tree
from itertools import chain
from graphviz import Digraph
# Author: Carl M. Kobel

class tnode:
    """ A trie node. """
    def __init__(self, in_edge_label = None, string_label = None, siblings = [], children = []):
        self.in_edge_label = in_edge_label # The edge into this node. Contains some character(s).
        self.string_label = string_label # The sum of upstream in_edge_labels.
        self.children = [i for i in children] 

    def __str__(self):
        """ The .string_label is used more often, I guess? """
        return self.string_label

    def __iter__(self):
        yield self
        for node in chain(*map(iter, self.children)):
            yield node

    def __repr__(self):
        return str(self)

    def visualize_old(self):
        """ Draws a graph with graphviz. """

        dot = Digraph(comment='Suffix tree')

        def node_format(node):
            node_content = node.in_edge_label + '|' + node.string_label
            edge_content =  node.string_label
            return node_content, edge_content


        def accept_node(node):
            """ Adds children recursively. """
            dot.node(*node_format(node))
            for child in node.children: # 
                accept_node(child) # tilføj child
                dot.edge(node_format(node)[0],
                         node_format(child)[0],
                         label = child.in_edge_label) # peg fra parent til child.


        accept_node(self)

        dot.render('test-output/suffix tree.gv', view=True)





null_char = '$' # null character
S = 'tatat' + null_char
n = len(S)

def suffixes(S):
    """ Generates all suffixes from S """
    for i in range(n):
        yield S[i:] + null_char
    yield null_char # Detablable whether the null_char should be returned for now.

def unfold_string(S):
    """ Unfolds the string in a way that makes it easy to populate edge_in_label and string_label in the nodes serially down the tree. """
    #S += null_char # Append null char.
    for _i, i in enumerate(S):
        yield i, S[0:_i+1]


tree = tnode('', '')

# Step 1) Add the full string to the trie, to start the building of the suffix tree.

def add_string_to_tree_at_node(node, string):
    #node = tree
    previous_string_label = node.string_label
    for edge_in, string in unfold_string(string):
        #new_node = tnode(edge_in, string) # string skal ikke være lig string, men være lig en udvidelse af foregående string_label
        new_node = tnode(edge_in, previous_string_label + edge_in)
        previous_string_label = string
        node.children.append(new_node)
        node = new_node

add_string_to_tree_at_node(tree, S)

# Add all suffixes, one at a time.
for i in suffixes(S[1:]):
    #print(i)
    pass # for later..


# Add a selected suffix
suffix = 'tata'

if True:
    for node in tree:
        print(node)
        if node.string_label == suffix:
            print('hooray')
            add_string_to_tree_at_node(node, '$')
            break # suffixet eksisterer ikke som en underdel af noget andet, og skal derfor tilføjes fra roden



# Compact the tree.


#tree.children[0].children.append(tnode('in edge content', 'node content'))


tree.visualize_old()
