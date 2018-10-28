from Bio import Phylo as ph

# author: Carl Mathias Kobel


tree0 = ph.read("data/Testdata/tree0.new", "newick")
tree1 = ph.read("data/Testdata/tree1.new", "newick")
tree2 = ph.read("data/Testdata/tree2.new", "newick")


ph.draw_ascii(tree0)




def terminals(root):
    """ Takes a root element, and returns the terminal clades (leaves). """
    leaves = []
    
    def rec(clade):
        """ Recursively traverses the tree, looking for terminals. """
        if clade.is_terminal():
            #leaves.append(clade)
            leaves.append(clade.name) # easier, but less flexible
            return
        else:
            for clade in clade.clades:
                rec(clade)

    rec(root)
    leaves.sort() # sort to get comparable lists
    return leaves

#test:
#print(terminals(tree0.root))


def internals(root):
    """ Traverses the internal elements. 
    Could have been a generator. """
    rv = []
    
    def rec(clade):
        """ Recursively traverses the tree, looking for internals. """
        if not clade.is_terminal():
            rv.append(clade)

        for clade in clade.clades:
            rec(clade)

    rec(root)
    return rv

#test:
#print(internals(tree0.root))


shared = 0
non_shared = 0
for i_1 in internals(tree1.root):
    for i_2 in internals(tree2.root):
        if terminals(i_1) == terminals(i_2):
            shared += 1

#print(shared)

# assuming num of internal is the same as splits, probably not true for polytomous trees
print(len(internals(tree1.root)) + len(internals(tree2.root)) - 2*shared)

print(tree0.root.clades[1])