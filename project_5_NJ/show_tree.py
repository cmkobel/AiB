from Bio import Phylo
from io import StringIO

from neighbour_joining import NJ


o = NJ('data/unique_distance_matrices/89_Adeno_E3_CR1.phy')
#o = NJ('data/6_Adeno_E3_CR1.phy')

treedata = o.neighbour_joining()

handle = StringIO(treedata)
tree = Phylo.read(handle, "newick")



Phylo.draw(tree)
Phylo.draw_ascii(tree)
