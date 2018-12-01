
# Author: Carl Mathias Kobel 2018
from cnode import Node
import phylip_like_parser as plp
import numpy as np
import time 


class NJ:
    def __init__(self, phylip_file):
        self.S = plp.parse(phylip_file)['taxa']
        self.D = plp.parse(phylip_file)['dissimilarity_matrix']
        self.phyfile = phylip_file

        #self.neighbour_joining()
        print(f'NJ starting ({len(self.S)}) {self.phyfile}')


    def neighbour_joining(self):
        """ Algorithm 10.7, Saitou and Nei's neighbor-joining algorithm. """
        def flatten(input_list):
            """ Takes a 2d-list and flattens it to 1d. 
            Probably not in use.. """
            return [i for sub in input_list for i in sub]
        
        def d_(i, j):
            """ Get distance from taxon names (strings) from the mutable D and S """
            return D[S.index(i)][S.index(j)]
        def r_(i):
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
            #print(f'while {len(S)} > 3:')

            #calculate all r_i, and reuse:
            rs = [r_(i) for i in S]
            #print('rs', rs)

            

            combinations = list(right_top_coordinates(len(S)))
            N = np.full((len(S), len(S)), float('inf'), dtype = np.float32)
            t = time.time()
            for i, j in combinations:
                N[i][j] = d_(S[i], S[j]) - (rs[i] + rs[j])
            
            
            #print(N)

            # b) Select i, j in S so that n_i,j is a minimum entry in N
            min_pointer = np.unravel_index(np.argmin(N, axis=None), N.shape)
            min_val = N[min_pointer[0]][min_pointer[1]]
            i, j = (S[i] for i in min_pointer)
            #print('i, j:', (S.index(i), S.index(j)), (i, j), N[S.index(i)][S.index(j)])

           

            # 2. Add a new node k to the tree T     

            # find the nodes for i and j
            for node in T:
                if node.name == i: node_i = node
                elif node.name == j: node_j = node
                # i and j represent the names of the taxa selected.

            # remove children i,j from parent
            node_m = node_i.parent # assuming that node_i and node_j has the same parent.
            node_m.children = [node for node in filter(lambda x: x != node_i and x != node_j, node_m.children)] # Remove i and j as immediate children. Todo: his would look a lot prettier with a set instead of a list.

            # 2. Add a new node k to the tree T.
            node_k = Node(0, f'k[{i}_{j}]', [node_i, node_j], node_m) # fix weight later. For now I just want to add the nodes correctly.
            node_m.children.append(node_k)

            # 3. Add edges (k, i) and (k, j)
            node_i.parent = node_k
            node_j.parent = node_k

            tttt = time.time()

            # 4. Update the dissimilarity matrix D.

            # We know that S and D are sorted in the same order.
            new_indices = set(range(len(S))) - set([i for i in min_pointer]) # The indices that include the taxa.
        

            new_S = [S[i] for i in new_indices] # The taxa included
            #print('new_S', new_S)

            # Update rs firsthand.
            k = [1/2 * (d_(i, m) + d_(j, m) - d_(i, j)) for m in new_S] # k is the column and row that is inserted after the merging of the two neighbours. At this point, new_S doesn't contain the merged node (k).
            #print('k before insertion', k)

            new_D = [[D[i][j] for i in new_indices] + [k[_num]] for _num, j in enumerate(new_indices)] + [k + [0]] # new D that includes k in both directions.

            new_S += [f'k[{node_i.name}_{node_j.name}]'] # update S to include the name of the newly inserted node k.

 
            D = new_D
            S = new_S

        print(f'..done with ({len(self.S)}) {self.phyfile}' )
        return T.newick()


# --------------------------------------------------------------



if __name__ == '__main__':
    #rv = o = NJ('data/example_slide4.phy').neighbour_joining()
    rv = NJ('data/unique_distance_matrices/89_Adeno_E3_CR1.phy').neighbour_joining()
    #rv = NJ('data/unique_distance_matrices/214_Arena_glycoprot.phy').neighbour_joining()
    #rv = NJ('data/unique_distance_matrices/304_A1_Propeptide.phy').neighbour_joining()

    
    #rv = NJ('data/custom_distance_matrices/214/10.phy').neighbour_joining() # Tror dette er rigtigt: (((8_Q9DK06_, 9_Q9DK03_), ((4_VGLY_PI, 5_O11998_), (6_O11999_, 7_O11997_))), (2_Q9YTW9_, 3_Q9YTW8_), (0_Q9YTX1_, 1_O90423_));
    #rv = NJ('data/unique_distance_matrices/89_Adeno_E3_CR1.phy').neighbour_joining()


    print('\nThe newick tree of the current run.')
    print(rv)


    #print(tree)

    #Phylo.draw_ascii(tree)

    #print(3)

    #o = NJ('data/6_Adeno_E3_CR1.phy')
    #o = NJ('data/unique_distance_matrices/89_Adeno_E3_CR1.phy')











