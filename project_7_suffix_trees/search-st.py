# Title: Search Suffix Tree
# Description: Builds a suffix tree from a string. Most functions ended up as recursive. 

from trienode import trienode
# Author: Carl M. Kobel


class suffixtree:
    def __init__(self, S, null_char = '$', show = False):
        self.S = S + null_char
        self.null_char = null_char
        
        ## Workflow: ##

        # 1) Initialize the root node.
        self.tree = trienode('', '') 

        # 2) Add all suffixes to the tree.
        for _i, suffix in enumerate(self.suffixes(self.S)):
            self.recursively_append(self.tree, suffix, _i)

        # 3)
        self.compact(self.tree)

        # 4)
        if show:
            self.tree.visualize(True)


    def __iter__(self):
        return self.tree.__iter__()


    def add_string(self, node, string, start_index):
        """ Helper function that inserts a string, letter for letter - at a specific node. """

        def unfold_string(S): # Skal denne funktion ud, den bliver jo defineret gang på gang?
            """ Unfolds the string in a way that makes it easy to populate edge_in_label and string_label in the nodes serially down the tree. """
            for _i, i in enumerate(S):
                yield i, S[0:_i+1]

        previous_string_label = node.string_label
        for edge_in, string in unfold_string(string):
            new_node = trienode(edge_in, previous_string_label + edge_in, start_index = start_index)
            previous_string_label += edge_in
            node.children.append(new_node)
            node = new_node


    def recursively_append(self, node, suffix, start_index):

        # Overview of the following three possible cases:
        # 0: String is empty, close
        # 1: Diversion. add string.
        # 2: String matches tree. continue recursively
        
        # 0 Base case.
        if len(suffix) == 0: # base case
            return
        
        # 1 No child suffices, add string.
        elif suffix[0:1] not in [child.in_edge_label for child in node.children]:
            self.add_string(node, suffix, start_index)
            return

        # 2 The part that calls itself with a successively shorter string.
        else: 
            for child in node.children:
                if suffix[0:1] == child.in_edge_label:
                    self.recursively_append(child, suffix[1:], start_index) # recursively call yourself.


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


    def find_node(self, p):
        """ Returns the node where a match has been completed.
        If no match; returns False"""
        
        def rec_search(node, p):
            """ Returns the index in S where the match is found. """
            len_p = len(p)
            #print('recursive call; p:', p, ', node:', node, ', len_p:', len(p))
            if len_p == 0: # base case: when an empty string has been asked for, we are done.
                #print('DONE!')
                return node


            for child in node.children: # for hvert barn
                #print(' child:', child.in_edge_label) ##print barnet, så vi ved hvor vi er kommet til. 

                #len_in_edge = len(child.in_edge_label)
                lower_bound = min(len_p, len(child.in_edge_label))
                #print('   lower_bound', lower_bound)

                if p[0:lower_bound] == child.in_edge_label[0:lower_bound]:
        
                    #print('  match:', p[0:lower_bound], 'in child:', child.in_edge_label)
                    #print()
                    return rec_search(child, p[lower_bound:])
            return False

        return rec_search(self.tree, p)


    def find_position(self, p):
        """ Returns the first match position. """
        rv = self.find_node(p)
        if rv == False:
            return -1 # evt. ellers kunne man lave en særlig exception. Sikkert langsommere, men mere logisk.
        else: 
            return rv.start_index
        

    def find_positions(self, p):
        """ Returns all matches in a list.
        First, it finds a match nodes. Then it iterates through all children in order to 
        obtain all positions. """
        match_node = self.find_node(p)
        if match_node == False:
            return []
        else: # solutions exist:
            return list(set([subnode.start_index for subnode in match_node])) # try .children??? !!!Jeg kan ikke gennemskue om det er vigtigt at alle children kommer med.



if __name__ == "__main__":

    ## Light Tests:
    
    st = suffixtree('Mississippi', show = False)
    #                    ^^^^^

    print('testing single')
    match = st.find_position('Mississippie')
    print(match)
    print()

    test_list = ['Mississippi',
             'ississippi',
             'ssissippi',
             'sissippi',
             'issippi',
             'ssippi',
             'sippi',
             'ippi',
             'ppi',
             'pi',
             'i',
             'is', 
             'Mississippie',
             'Mississippe',
             'havemad',
             'thoadeunthaoieuhdaoe',
             '$', # 11
             '$$',
             'Mis$'] # ?

    print('testing single test_list...')
    for i in test_list:
        print(st.find_position(i))
    print('...done testing')
    print()

    print('testing multiple')
    print(st.find_positions('issi'))



