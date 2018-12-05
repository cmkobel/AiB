# Author: Carl Mathias Kobel 2018

from cnode import Node
import phylip_like_parser as plp
import numpy as np



class RNJ:
    def __init__(self, phylip_file):
        self.taxa = plp.parse(phylip_file)['taxa']
        self.D = plp.parse(phylip_file)['dissimilarity_matrix']

        


    def neighbour_joining(self):
        def u(i):
            """ A kind of normalized sum of distances from i to others. """
            rv = sum([D[i][m] for m in range(len(unjoined_nodes))])
            return rv


        
        D = np.array(self.D)


        # Indices in unjoined_nodes correspond to indeces in taxa and D.
        unjoined_nodes = [Node(name) for name in self.taxa]
        print(type(D[0][0]))

        
        while len(unjoined_nodes) > 3:
            




            q_min = float('inf') # The best q-value at a given point in an iteration. Update later in the loop than here in the beginning. I guess it has to be reset at every iteration?
            u_max = np.sum(D, 1).max() # The maximum row sum in D. # Jeg behøver først u_max når jeg skal implementere sætningen der gør at man kan droppe resten af rækken.





            print('D:', D, sep = '\n')

            #triu_indices = np.triu_indeces

            # map V
            V = np.argsort(D, 1) # The map from S to D. Indicates what old index is used at what new position
            print('V:', V, sep = '\n')


            S = np.sort(D) # Would probably be faster to reuse the map V. PORAE
            print('S:', S, sep = '\n')


            # Search each row in S
            for _row, row in enumerate(S):
                for _col, col in enumerate(row): # list compr.?
                # This is where there ought to be an optimization step, surpassing the rest of a row, depending on u_max.

                    
                    val = S[_row][_col] - u(_row) - u(V[_row][_col])
                    if val < q_min:
                        # Record the lowest value.
                        if _row != V[_row][_col]: # PORAE: It would be faster to fill the diagonal with ones, instead of inserting if-statements.
                            q_min = val

                            # Record which taxa to join.
                            _i = _row
                            _j = V[_row][_col]

                
            
        
            dist_ij = D[_i][_j] # Optimization
            dist_k = [0.5 * (D[_i][_m] + D[_j][_m] - dist_ij) for _m, m in enumerate(unjoined_nodes)] # PORAE:  D[_i][_j] can be precomputed, as it doesn't change 
            print('dist_k\n', dist_k)
            
            node_i = unjoined_nodes[_i] # Overwritten with node k later.
            node_j = unjoined_nodes.pop(_j) # delete item.
            
            # D: update rows and cols _i with k, then delete rows and cols _j
            D[:, _i] = dist_k
            D[_i] = dist_k
            D = np.delete(D, _j, 1)
            D = np.delete(D, _j, 0)
            print(D)



            node_k = Node(f'k[{node_i.name}_{node_j.name}]', [node_i, node_j])
            unjoined_nodes[_i] = node_k
            print(_i, _j, node_i, node_j)

            

            # calculate distance to new node
            print('last')
            print(unjoined_nodes)
            print(D)

            # Insert k into D
            #1/2 * (D(i, m) + D(j, m) - D(i, j))
            #dist_k = [0.5 * ()]



            # Update D


#            break
        

        # Collect the unjoined_nodes and print.
        return Node('', unjoined_nodes).newick()
# ------------------------------------------------------------






if __name__ == '__main__':

    
    if True:
        newick_tree = RNJ('data/10.phy').neighbour_joining() # (((8_Q9DK06_, 9_Q9DK03_), ((4_VGLY_PI, 5_O11998_), (6_O11999_, 7_O11997_))), (2_Q9YTW9_, 3_Q9YTW8_), (0_Q9YTX1_, 1_O90423_));
        #newick_tree = RNJ('data/example_slide4.phy').neighbour_joining() #
        print('\n\n', newick_tree)





        
            








