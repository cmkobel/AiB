# Author: Carl Mathias Kobel 2018

#from * import *

class Node: # A tree node
    def __init__(self, value, children = []):
        self.value = value # tuple with weight and name
        self.children = [Node(i) for i in children]

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f'Node with value {(self.value)} and children {self.children}'


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
        def d_(i, j):
            return self.D[self.S.index(i)][self.S.index(j)]
        def r_(i):
            return 1/(len(S)-2) * sum([d_(i, m) for m in S])
        def n_(i, j):
            return d_(i, j) - (r_(i) + r_(j))
        
        S = self.S
        D = self.D
        T = Node(0)
    

        while len(S) > 3:
            break

    

        






o = NJ('data/example_slide4.phy')

