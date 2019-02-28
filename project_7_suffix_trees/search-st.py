# Title: Search Suffix Tree

from trienode import trienode
# Author: Carl M. Kobel




null_char = '$' # null character
S = 'mississippi' # tatat
S += null_char
n = len(S)


def suffixes(S):
    """ Generates all suffixes from S """
    for i in range(n):
        yield S[i:]# + null_char
    #yield null_char # Debatable whether the null_char should be returned for now.

def unfold_string(S):
    """ Unfolds the string in a way that makes it easy to populate edge_in_label and string_label in the nodes serially down the tree. 
    This function was made to put in the full string in the beginning, but because I want the same function that appends suffixes to
    automatically put in the full string. """
    #S += null_char # Append null char.
    for _i, i in enumerate(S):
        yield i, S[0:_i+1]


tree = trienode('', '') # Initialize the trie.


def add_string_to_tree_at_node(node, string):
    """ Helper function that inserts a string, letter for letter - at a specific node. """
    previous_string_label = node.string_label
    for edge_in, string in unfold_string(string):
        new_node = trienode(edge_in, previous_string_label + edge_in)
        previous_string_label = previous_string_label + edge_in # or previous_string_label += edge_in
        node.children.append(new_node)
        node = new_node


   
# for suffix in suffixes(S):
#     print('suffix:', suffix)
    
#     char_iter = iter(suffix) # Så jeg kan kalde next

#     #char = next(char_iter)
#     for node in tree:
#         if next(char_iter) not in [child.in_edge_label for child in node.children]:
#             # No child exists with an in_edge_label that matches the char we're at.
#             add_string_to_tree_at_node(node, suffix)
#             break
#     break




def recursive_appender(node, suffix):
    # if diversion: add string and break.
    # else: call recursively with next suffix
    
    # 0 base case
    print('suffix:', suffix)
    if len(suffix) == 0: # base case
        print('0) reached the end')
        return
    
    # 1 no child suffices, add string.
    elif suffix[0:1] not in [child.in_edge_label for child in node.children]:
        print('1)', suffix[0:1], 'from', suffix, 'not in node, adding...')
        add_string_to_tree_at_node(node, suffix)
        return

    # 2 the part that calls itself.
    # if a child exists, that overlaps with the first index of the suffix, we can call ourselves rec. and continue.
    else: 
        print('2) else; suffix[0:1]', suffix[0:1], 'exists in children,',[i.in_edge_label for i in node.children], ' calling next suffix')
        for child in node.children:
            print('hat')
            if suffix[0:1] == child.in_edge_label:
                print('calling for suffix[1:]:', suffix[1:])
                recursive_appender(child, suffix[1:])


for suffix in suffixes(S):
    recursive_appender(tree, suffix)
#recursive_appender(tree, S[1:])

    #break # only first suffix, just to get started.
















tree.visualize(True)

