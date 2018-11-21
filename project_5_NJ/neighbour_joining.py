# Author: Carl Mathias Kobel 2018

from cnode import Node
import phylip_like_parser as plp


class NJ:
    def __init__(self, phylip_file):
        self.S = plp.parse(phylip_file)['taxa']
        self.D = plp.parse(phylip_file)['dissimilarity_matrix']

        self.neighbour_joining()


    def neighbour_joining(self):
        """ Algorithm 10.7, Saitou and Nei's neighbor-joining algorithm. """
        def flatten(input_list):
            return [i for sub in input_list for i in sub]
        def od_(i, j):
            """ Get distance from taxon names (strings) """
            return self.D[self.S.index(i)][self.S.index(j)]
        def d_(i, j):
            """ Get distance from taxon names (strings) from the mutable D and S """
            return D[S.index(i)][S.index(j)]
        def r_(i):
            return 1/(len(S)-2) * sum([d_(i, m) for m in S])
        def n_(i, j):
            return d_(i, j) - (r_(i) + r_(j)) # don't round in the hand in code.

        
        D = self.D # Input: n * n dissimilarity matrix D, where n >= 3

        print('\ninitial D')
        for a in D:
            print(a)
        print()

        # Initialization
        
        S = self.S # 1. Let S be the set of taxa.

        # 2. Each taxon i is a leaf in the tree T.
        T = Node(0, 'center')
        for i in S: # add S to T:
            T.children.append(Node(0, i, [], T))


        print('initial tree T:\n', T.display())


        while len(S) > 3:
            print(f'\n\nwhile len(S) = {len(S)} > 3: ---------------------------------------------------------')
            
            print('S =', S)


            # 1. a) Compute the matrix N
            print('\n1:\n')
            N = [[n_(i, j) if _i > _j else float('inf') for _j, j in enumerate(S)] for _i, i in enumerate(S)] 

            print('N:')
            for n in N:
                print(n)


            #    b) Select i, j in S so that n_i,j is a minimum entry in N
            min_pointer = (0, 0)
            min_val = float('inf')
            for i in range(len(N)):
                for j in range(len(N)):
                    if N[i][j] < min_val:
                        min_val = N[i][j]
                        min_pointer = (i, j)
            i, j = (S[i] for i in min_pointer)
            print(i, j)


            # 2. Add a new node k to the tree T     
            print('\n2:\n')      
            
            # II: identify edges

            # find the nodes for i and j
            for node in T:
                if node.name == i: node_i = node
                elif node.name == j:node_j = node
                # i and j represent the names of the taxa selected.

            # remove children i,j from parent
            node_m = node_i.parent # assuming that node_i and node_j has the same parent.
            node_m.children = [node for node in filter(lambda x: x != node_i and x != node_j, node_m.children)] # Remove i and j as immediate children. Todo: his would look a lot prettier with a set instead of a list.

            # add k to the tree
            node_k = Node(0, f'k({i}, {j})', [node_i, node_j], node_m) # fix weight later. For now I just want to add the nodes correctly.
            

            # 3. Add edges (k, i) and (k, j)
            print('\n3:\n')

            node_m.children.append(node_k)

            node_i.parent = node_k
            node_j.parent = node_k

            # So Andy tells me that weights in the tree are not really necessary. #node_i.weight = 1/2 * (d_(i, j) + r_(i) - r_(j)) #node_j.weight = 1/2 * (d_(i, j) + r_(j) - r_(i))

            print(T.display())


            # 4. Update the dissimilarity matrix D
            print('\n4:\n')

            # We know that S and D are sorted in the same order.
            new_indices = set(range(len(S))) - set([i for i in min_pointer]) # The indices that include the taxa.

            new_S = [S[i] for i in new_indices] # The taxa included

            k = [1/2 * d_(i, m) + d_(j, m) - d_(i, j) for m in new_S] # k is the column and row that is inserted after the merging of the two neighbours. At this point, new_S doesn't contain the merged node (k).

            new_D = [[D[i][j] for i in new_indices] + [k[_num]] for _num, j in enumerate(new_indices)] + [k + [0]] # new D that includes k in both directions.
            new_S += [f'k({i}, {j})'] # update S to include the name of the newly inserted node k.
 


            D = new_D
            S = new_S
            


    

# --------------------------------------------------------------






o = NJ('data/example_slide4.phy')

