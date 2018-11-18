# Author: Carl Mathias Kobel 2018

from itertools import chain

class Node: # A tree node
    def __init__(self, value = (0, "no_name"), children = [], parent = None):
        self.value = value # tuple: (weight, name)
        self.children = [Node(i) for i in children]
        self.parent = parent

    def __str__(self):
        return str(self.value)
    def __repr__(self):
        return str(self)

    def __repr__(self):
        return f'Node with value: {self.value}{", parent: " + self.parent.value[1] if self.parent != None else ""}{", children: " + str(self.children) if len(self.children) > 0 else ""}\n'


    def __iter__(self):
        """ Implement the iterator protocol. """
        for node in chain(*map(iter, self.children)):
            yield node
        yield self


class NJ:
    def __init__(self, phylip_file):

        def phylip_like_parser(input_file):
            with open(input_file, 'r') as file:
                raw = [line.strip().split() for line in file]
                rv = {'N': raw[0],
                      'taxa': [i[0] for i in raw[1:]],
                      'dissimilarity_matrix': [[float(elem) for elem in list[1:]] for list in raw[1:]]}
            return rv
        
        self.S = phylip_like_parser(phylip_file)['taxa']
        self.D = phylip_like_parser(phylip_file)['dissimilarity_matrix']

        


        self.neighbour_joining()


    def neighbour_joining(self):
        """ Algorithm 10.7, Saitou and Nei's neighbor-joining algorithm. """
        def flatten(input_list):
            return [i for sub in input_list for i in sub]
        def d_(i, j):
            """ Get distance from taxon names (strings) """
            return self.D[self.S.index(i)][self.S.index(j)]
        def r_(i):
            return 1/(len(S)-2) * sum([d_(i, m) for m in S])
        def n_(i, j):
            return round(d_(i, j) - (r_(i) + r_(j)), 2) # don't round in the hand in code.
        
        D = self.D # Input: n * n dissimilarity matrix D, where n >= 3

        # Initialization
        
        S = self.S # 1. Let S be the set of taxa.

        # 2. Each taxon i is a leaf in the tree T.
        T = Node((0, 'init. center'))
        for i in S: # add S to T:
            T.children.append(Node((0, i), [], T))

        # print(repr(T)) # debug
    

        while len(S) > 3:
            # 1. a) Compute the matrix N
            N = [[n_(i, j) if _i > _j else float('inf') for _j, j in enumerate(S)] for _i, i in enumerate(S)] 

            


            #    b) Select i, j in S so that n_i,j is a minimum entry in N
            min_pointer = (0, 0)
            min_val = float('inf')
            for i in range(len(N)):
                for j in range(len(N)):
                    if N[i][j] < min_val:
                        min_val = N[i][j]
                        min_pointer = (i, j)
            print(min_val, '@', min_pointer) # debug
            i, j = (self.S[i] for i in min_pointer)
            #print(i, j)

            # 2. Add a new node k to the tree T            
            
            # II: identify edges

            # find the nodes for i and j
            for node in T:
                if node.value[1] == i: node_i = node
                elif node.value[1] == j:node_j = node

            print(node_i, node_j) # debug

            # remove children from k
            node_i.parent.children = [node for node in filter(lambda x: x != node_i and x != node_j, node_i.parent.children)]

            # add k and and set the parent of node_i and j to the newly added node_k
            node_k = Node((0, f'k({i}, {j})'))
            node_i.parent.children.append(node_k) # fix weight later. For now i just want to add the nodes correctly.
            node_i.parent = node_k
            node_j.parent = node_k

            node_k.children.append(node_i)
            node_k.children.append(node_j)

            # 2. Is done.



            # Now I just need to set the weights correctly. 

            # Then update D and S accordingly



            



            # gamma =  


            break


    

        






o = NJ('data/example_slide4.phy')

