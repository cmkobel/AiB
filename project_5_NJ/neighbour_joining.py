
# Author: Carl Mathias Kobel 2018
from cnode import Node
import phylip_like_parser as plp
import numpy as np
from rfdist import Robinson_Foulds_distance



class NJ:
    def __init__(self, phylip_file):
        self.S = plp.parse(phylip_file)['taxa']
        self.D = plp.parse(phylip_file)['dissimilarity_matrix']


    def neighbour_joining(self):
        """ Saitou and Nei's neighbor-joining algorithm. """
        def d_(i, j):
            """ Get distance from taxon names (strings) from the mutable D and S """
            return D[S.index(i)][S.index(j)]
        def r_(i):
            """ r_i is a kind of normalized distance of i to all other taxa. """
            return 1 / (len(S)-2) * sum([d_(i, m) for m in S])
        def n_(i, j):
            return d_(i, j) - (r_(i) + r_(j))
        def right_top_coordinates(dim):
                j_start = 1
                for i in range(dim-1):
                    for j in range(dim)[j_start::]:
                        yield((i, j))
                    j_start += 1
  
        D = self.D # Input: n * n dissimilarity matrix D, where n >= 3
        
        S = self.S # 1. Let S be the set of taxa.

        # 2. Each taxon i is a leaf in the tree T.
        T = Node(0, '')
        for i in S: # add S to T:
            T.children.append(Node(0, i, [], T))

        while len(S) > 3:
            
            #calculate all r_i for reuse:
            rs = [r_(i) for i in S]            

            combinations = list(right_top_coordinates(len(S)))
            N = np.full((len(S), len(S)), float('inf'), dtype = np.float32)
            for i, j in combinations:
                N[i][j] = d_(S[i], S[j]) - (rs[i] + rs[j])

            # b) Select i, j in S so that n_i,j is a minimum entry in N
            min_pointer = (0, 0)
            min_val = float('inf')
            for i in range(len(N)):
                for j in range(len(N)):
                    if N[i][j] < min_val:
                        min_val = N[i][j]
                        min_pointer = (i, j)
            i, j = (S[i] for i in min_pointer)

            # 2. Add a new node k to the tree T     

            # find the nodes for i and j
            for node in T:
                if node.name == i: node_i = node
                elif node.name == j: node_j = node

            # remove children i,j from parent
            node_m = node_i.parent # assuming that node_i and node_j has the same parent.
            node_m.children = [node for node in filter(lambda x: x != node_i and x != node_j, node_m.children)] # Remove i and j as immediate children. Todo: his would look a lot prettier with a set instead of a list.

            # 2. Add a new node k to the tree T.
            node_k = Node(0, f'k[{i}_{j}]', [node_i, node_j], node_m) # Weight can always be added. For now I just want to add the nodes correctly.
            node_m.children.append(node_k)

            # 3. Add edges (k, i) and (k, j)
            node_i.parent = node_k
            node_j.parent = node_k

            # 4. Update the dissimilarity matrix D.
            # We know that S and D are sorted in the same order.
            new_indices = set(range(len(S))) - set([i for i in min_pointer]) # The indices that include the taxa.
            new_S = [S[i] for i in new_indices] # The taxa included
            
            k = [1/2 * (d_(i, m) + d_(j, m) - d_(i, j)) for m in new_S] # k is the column and row that is inserted after the merging of the two neighbours. At this point, new_S doesn't contain the merged node (k).

            new_D = [[D[i][j] for i in new_indices] + [k[_num]] for _num, j in enumerate(new_indices)] + [k + [0]] # new D that includes k in both directions.

            new_S += [f'k[{node_i.name}_{node_j.name}]'] # update S to include the name of the newly inserted node k.

            D = new_D
            S = new_S
            

        return T.newick()


# --------------------------------------------------------------



if __name__ == '__main__':

    # Instantiate neighbour joining object.
    newick_tree = NJ('89_Adeno_E3_CR1.phy').neighbour_joining()
    print('The newick tree of the current run.')
    print(newick_tree)

    # Save newick tree string to disk (my rfdistance program only works with files.)
    out_file_name = 'njoutput.newick'
    with open(out_file_name, 'w') as file:
        for i in newick_tree:
            file.write(i)

    
    compare_to = 'out_qt_89_Adeno_E3_CR1.phy.newick'
    print('The distance between Our Saitou Nei and the Quicktree file is:')
    dist = Robinson_Foulds_distance(out_file_name, compare_to)
    print(dist.distance)
