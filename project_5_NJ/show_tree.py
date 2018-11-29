from Bio import Phylo
from io import StringIO

import neighbour_joining


def show():
    handle = StringIO(newick_tree)
    tree = Phylo.read(StringIO(newick_tree), "newick")
    #Phylo.draw(tree)
    Phylo.draw_ascii(tree)






#newick_tree = neighbour_joining.NJ('data/custom_distance_matrices/7_alt_Adeno_E3_CR1.phy').neighbour_joining()
#newick_tree = neighbour_joining.NJ('data/custom_distance_matrices/10_Adeno_E3_CR1.phy').neighbour_joining()
newick_tree = neighbour_joining.NJ('data/custom_distance_matrices/12_Adeno_E3_CR1.phy').neighbour_joining()
#newick_tree = neighbour_joining.NJ('data/custom_distance_matrices/14_Adeno_E3_CR1.phy').neighbour_joining()


# det ser ud til at newick writeren virker fint.

print(newick_tree)




show()
