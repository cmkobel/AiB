from Bio import Phylo
from io import StringIO

import neighbour_joining


def show():
    handle = StringIO(newick_tree)
    tree = Phylo.read(StringIO(newick_tree), "newick")
    #Phylo.draw(tree)
    Phylo.draw_ascii(tree)




#newick_tree = neighbour_joining.NJ('data/custom_distance_matrices/14_Adeno_E3_CR1.phy').neighbour_joining()
newick_tree = neighbour_joining.NJ('data/unique_distance_matrices/89_Adeno_E3_CR1.phy').neighbour_joining()

print(newick_tree)




show()
