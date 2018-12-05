# Author: Carl Mathias Kobel 2018

from cnode import Node
import phylip_like_parser as plp
import numpy as np


class RNJ:
    def __init__(self, phylip_file):
        self.taxa = plp.parse(phylip_file)['taxa']
        self.D = plp.parse(phylip_file)['dissimilarity_matrix']

    def neighbour_joining(self):
        def u(i, n_taxa):
            """ A kind of normalized sum of distances from i to others. """
            return 1 / (n_taxa-2) * sum([D[i][m] for m in range(n_taxa)])

        D = np.array(self.D)

        # Indices in free_nodes correspond to indeces in D.
        free_nodes = [Node(name) for name in self.taxa]
        
        round = 0
        while len(free_nodes) > 3:
            print(f'\nwhile {len(free_nodes)} > 3 ---(round {round})------------------------------------------')
            round += 1

            print('free_nodes:', free_nodes)

            q_min = float('inf') # The best q-value at a given point in an iteration. Update later in the loop than here in the beginning. I guess it has to be reset at every iteration?
            u_max = np.sum(D, 1).max() # The maximum row sum in D. # Jeg behøver først u_max når jeg skal implementere sætningen der gør at man kan droppe resten af rækken.


            print('D:')
            print(D)


            # Jeg har fundet fejlen. Problemet er, at jeg sorterer D igen fra den D der var i sidste runde, og ikke fra den D der var i starten. Derved passer navnene ikke sammen længere.
            # Nej, det passer ikke, for jeg har ikke ændret noget i D ud over at slette de passende rækker og kolonner.

            # map V
            V = np.argsort(D, 1) # The map from S to D. Indicates what old index is used at what new position
            #print('V:\n', V)

            S = np.sort(D) # Would probably be faster to reuse the map V. PORAE
            #print('S:\n', S)


            # (Partially) compute Q of S
            #for _row, row in enumerate(S):
            #    for _col, col in enumerate(row): 
            n_taxa = len(free_nodes)
            print('N:')
            for _row in range(len(free_nodes)):
                for _col in range(len(free_nodes)):
                # This is where there ought to be an optimization step, surpassing the rest of a row, depending on u_max. Let's make it work in the first plac.

                    q = S[_row][_col] - u(_row, n_taxa) - u(V[_row][_col], n_taxa) # PORAE: u(_row) kan genbruges.

                    print(q, end = '\t')
                    if q < q_min:
                        # Record the lowest value.
                        if _row != V[_row][_col]: # PORAE: It would be faster to fill the diagonal with ones, instead of inserting if-statements.
                            q_min = q

                            # Record which taxa to join.
                            _i = _row
                            _j = V[_row][_col]
                print()
            print()




            dist_ij = D[_i][_j] # Optimization
            dist_k = [0.5 * (D[_i][_m] + D[_j][_m] - dist_ij) for _m in range(len(free_nodes))] # PORAE:  D[_i][_j] can be precomputed, as it doesn't change 
            print('dist_k: ', dist_k)
            
            node_i = free_nodes[_i] # Overwritten with node k later.
            node_j = free_nodes.pop(_j) # delete item.
            print(f'joining ({_i}, {_j}): {node_i}, {node_j}')
            # D: update rows and cols _i with k, then delete rows and cols _j
            D[:, _i] = dist_k
            D[_i] = dist_k


            # Delete _j'th column from each axis
            D = np.delete(D, _j, 1)
            D = np.delete(D, _j, 0)

            

            node_k = Node(f'k[{node_i.name}_{node_j.name}]', [node_i, node_j])
            free_nodes[_i] = node_k

        
            # break

        # Collect the free_nodes and print.
        return Node('', free_nodes).newick()
# ------------------------------------------------------------






if __name__ == '__main__':

    
    if True:
        newick_tree = RNJ('data/example_slide4.phy').neighbour_joining() #
        #newick_tree = RNJ('data/10.phy').neighbour_joining() # (((8_Q9DK06_, 9_Q9DK03_), ((4_VGLY_PI, 5_O11998_), (6_O11999_, 7_O11997_))), (2_Q9YTW9_, 3_Q9YTW8_), (0_Q9YTX1_, 1_O90423_)); # prøv at køre SRNJ på datasættet og se hvad det bør give.
        #newick_tree = RNJ('data/89_Adeno_E3_CR1.phy').neighbour_joining() #

        print('\n\n', newick_tree)

"""
DEBUGGING 
---------

* Først troede jeg at jeg sorterede D til V forkert. Men det fungerer fint.
* Nu vil jeg prøve at se hvis q-værdierne her bliver præcist de samme som i 5













"""




            








