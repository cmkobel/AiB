from itertools import chain
from graphviz import Digraph
# Author: Carl M. Kobel

class tnode:
    """ A trie node. """
    def __init__(self, in_edge_label = None, string_label = None, siblings = [], children = []):
        self.in_edge_label = in_edge_label # The edge into this node. Contains some character(s).
        self.string_label = string_label # The sum of upstream in_edge_labels.
        self.siblings = [i for i in siblings] # unused
        self.children = [i for i in children] 

    def __str__(self):
        """ The .string_label is used more often, I guess? """
        return self.string_label

    def __iter__(self):
        yield self
        for node in chain(*map(iter, self.children)): # asterisken putter alle elementerne i en liste, og giver listen som argument til map.
            yield node

    def __repr__(self):
        return str(self)

    def visualize(self):


        dot = Digraph(comment='Suffix tree')

        #dot.node('A', 'King Arthur')
        #dot.node('B', 'Sir Bedevere the Wise')
        #dot.node('L', 'Sir Lancelot the Brave')

        #dot.edges(['AB', 'AL'])
        #dot.edge('B', 'L', label = 'john', constraint='false')

        for i in self:
            print(i)
            dot.node(i.in_edge_label + '|' + i.string_label, i.string_label)


        dot.render('test-output/suffix tree', view=True)





S = 'Mississippi'
n = len(S)
null_char = '$' # null character

def iter_string(S):
    for i in range(n):
        yield S[i:] + null_char
    yield null_char # Detablable whether the null_char should be returned for now.

def unfold_string(S):
    """ Unfolds the string in a way that makes it easy to populate edge_in_label and string_label in the nodes serially down the tree. """
    S += null_char # Append null char.
    for _i, i in enumerate(S):
        yield i, S[0:_i+1]


# Step 1) Add the full string to the trie, to build the initial tree.
root = tnode('', '')

node = root

for edge_in, string in unfold_string(S):
    
    new_node = tnode(edge_in, string)
    node.children.append(new_node)
    node = new_node







root.visualize()