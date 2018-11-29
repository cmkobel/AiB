
# Author: Carl Mathias Kobel 2018
from cnode import Node
import phylip_like_parser as plp



class NJ:
    def __init__(self, phylip_file):
        self.S = plp.parse(phylip_file)['taxa']
        self.D = plp.parse(phylip_file)['dissimilarity_matrix']

        #self.neighbour_joining()


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

        
        D = self.D # Input: n * n dissimilarity matrix D, where n >= 3
        
        S = self.S # 1. Let S be the set of taxa.

        # 2. Each taxon i is a leaf in the tree T.
        T = Node(0, '')
        for i in S: # add S to T:
            T.children.append(Node(0, i, [], T))

        while len(S) > 3:
            print(f'\nwhile {len(S)} > 3: -----------------------------------------------')
            
            print('S =', S)

            print('D =')
            for i in D:
                print(i)


            # a) Compute the matrix N
            N = [[n_(i, j) if _i > _j else float('inf') for _j, j in enumerate(S)] for _i, i in enumerate(S)] 


            print('N = ')
            for i in N:
                for j in i:
                    print(round(j, 3), end = '\t')
                print()
            # Hvordan beregner man N, og skal de være negative?


            # b) Select i, j in S so that n_i,j is a minimum entry in N
            min_pointer = (0, 0)
            min_val = float('inf')
            for i in range(len(N)):
                for j in range(len(N)):
                    if N[i][j] < min_val:
                        min_val = N[i][j]
                        min_pointer = (i, j)
            i, j = (S[i] for i in min_pointer)
            print('i, j:', (S.index(i), S.index(j)),
                  (i, j),
                  N[S.index(i)][S.index(j)])


            # 2. Add a new node k to the tree T     

            # find the nodes for i and j
            for node in T:
                if node.name == i: node_i = node
                elif node.name == j: node_j = node
                # i and j represent the names of the taxa selected.
            print(repr(node_i), '|', repr(node_j))

            # remove children i,j from parent
            node_m = node_i.parent # assuming that node_i and node_j has the same parent.
            node_m.children = [node for node in filter(lambda x: x != node_i and x != node_j, node_m.children)] # Remove i and j as immediate children. Todo: his would look a lot prettier with a set instead of a list.

            # 2. Add a new node k to the tree T.
            node_k = Node(0, f'k[{i}_{j}]', [node_i, node_j], node_m) # fix weight later. For now I just want to add the nodes correctly.
            node_m.children.append(node_k)

            # 3. Add edges (k, i) and (k, j)
            node_i.parent = node_k
            node_j.parent = node_k


            # 4. Update the dissimilarity matrix D.

            # We know that S and D are sorted in the same order.
            new_indices = set(range(len(S))) - set([i for i in min_pointer]) # The indices that include the taxa.

            print('bef')
            print(S)
            new_S = [S[i] for i in new_indices] # The taxa included
            print(new_S)

            k = [1/2 * d_(i, m) + d_(j, m) - d_(i, j) for m in new_S] # k is the column and row that is inserted after the merging of the two neighbours. At this point, new_S doesn't contain the merged node (k).
            print('k before insertion', k)

            new_D = [[D[i][j] for i in new_indices] + [k[_num]] for _num, j in enumerate(new_indices)] + [k + [0]] # new D that includes k in both directions.
            for i in new_D:
                print(i)

            new_S += [f'k[{node_i.name}_{node_j.name}]'] # update S to include the name of the newly inserted node k.
            #print('hvad', f'k[{node_i.name}_{node_j.name}]')
            print(new_S)
 


            D = new_D
            S = new_S
            

        #print(T.display())
        return T.newick()


# --------------------------------------------------------------



if __name__ == '__main__':
    rv = o = NJ('data/example_slide4.phy').neighbour_joining()
    #rv = NJ('data/unique_distance_matrices/89/89_Adeno_E3_CR1.phy').neighbour_joining()
    #rv = NJ('data/custom_distance_matrices/214/50.phy').neighbour_joining()
    #rv = NJ('data/unique_distance_matrices/89_Adeno_E3_CR1.phy').neighbour_joining()


    print('\nThe newick tree of the current run.')
    print(rv)


    #print(tree)

    #Phylo.draw_ascii(tree)

    #print(3)

    #o = NJ('data/6_Adeno_E3_CR1.phy')
    #o = NJ('data/unique_distance_matrices/89_Adeno_E3_CR1.phy')


