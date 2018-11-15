# Author: Carl Mathias Kobel 2018

#from * import *

class Node: # A tree node
    def __init__(self, value = (0, "no_name"), children = [], parent = None):
        self.value = value # tuple: (weight, name)
        self.children = [Node(i) for i in children]
        self.parent = parent

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f'Node with value {self.value}{", Parent " + self.parent.value[1] if self.parent != None else ""} and children: {self.children}\n'


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

        print(repr(T))
    

        while len(S) > 3:
            # 1. a) Compute the matrix N
            N = [[n_(i, j) if _i > _j else float('inf') for _j, j in enumerate(S)] for _i, i in enumerate(S)] 

            
            for i in N: print(i) #debug

            #    b) Select i, j in S so that n_i,j is a minimum entry in N
            minimum_pointer = (0, 0)
            minimum_value = float('inf')
            for _i, i in enumerate(N):
                for _j, j in enumerate(i):
                    if N[_i][_j] < minimum_value:
                        minimum_value = N[_i][_j]
                        minimum_pointer = (_i, _j)
            print(minimum_value, '@', minimum_pointer) # debug

            # 2. Add a new node k to the tree T






            



            # gamma =  


            break


    

        






o = NJ('data/example_slide4.phy')

