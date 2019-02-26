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
        """ Should be called on the root. """

        dot = Digraph(comment='Suffix tree')


        def expand_content(node):
            node_content = node.in_edge_label + '|' + node.string_label
            edge_content =  node.string_label
            return node_content, edge_content

        #dot.node('A', 'King Arthur')
        #dot.node('B', 'Sir Bedevere the Wise')
        #dot.node('L', 'Sir Lancelot the Brave')

        #dot.edges(['AB', 'AL'])
        #dot.edge('B', 'L', label = 'john', constraint='false')


        def accept_node(node):
            """ adds children recursively """
            dot.node(*expand_content(node))
            for child in node.children: # Jeg ved ikke helt hvorfor jeg er nødt til at skrive .children.
                accept_node(child) # tilføj child
                dot.edge(expand_content(node)[0], expand_content(child)[0], child.in_edge_label) # peg fra parent til child.


        accept_node(self)








        dot.render('test-output/suffix tree', view=True)





S = 'mississippi'
n = len(S)
null_char = '$' # null character

def suffixes(S):
    """ Generates all suffixes from S """
    for i in range(n):
        yield S[i:] + null_char
    yield null_char # Detablable whether the null_char should be returned for now.

def unfold_string(S):
    """ Unfolds the string in a way that makes it easy to populate edge_in_label and string_label in the nodes serially down the tree. """
    S += null_char # Append null char.
    for _i, i in enumerate(S):
        yield i, S[0:_i+1]




# Step 1) Add the full string to the trie, to build the initial tree.
tree = tnode('', '(ROOT)')
node = tree
for edge_in, string in unfold_string(S):
    node.children.append(tnode(edge_in, string))
    node = node.children[0]


# Add all suffixes, one at a time.
for i in suffixes(S[1:]):
    #print(i)
    pass

# Add a selected suffix
suffix = 'sippi$'
for node in tree:
    print(node)

# Compact the tree.


#tree.children[0].children.append(tnode('in edge content', 'node content'))


tree.visualize_old()
