from Bio import Phylo as ph

# author: Carl Mathias Kobel

class Robinson_Foulds_distance:
    def __init__(self, file1, file2):
        self.tree1 = ph.read(file1, "newick")
        self.tree2 = ph.read(file2, "newick")

        self.distance = self.rfdist()

    
    def is_leaf(self, node):
        return len(node.clades) == 0


    def terminals(self, root):
        """ Takes a root node, and returns the terminal clades (leaves). """
        leaves = []
        
        def rec(clade):
            """ Recursively traverses the tree, looking for terminals. """
            #if clade.is_terminal():
            if self.is_leaf(clade):    
                #leaves.append(clade)
                leaves.append(clade.name) # easier, but less flexible
                return
            else:
                for clade in clade.clades:
                    rec(clade)

        rec(root)
        leaves.sort() # sort to get comparable lists
        return leaves


    def internals(self, root):
        """ Traverses the internal elements. 
        Could have been a generator. """
        rv = []
        
        def rec(clade):
            """ Recursively traverses the tree, looking for internals. """
            if not self.is_leaf(clade):
                rv.append(clade)

            for clade in clade.clades:
                rec(clade)

        rec(root)
        return rv


    def rfdist(self):
        shared = 0
        for i_1 in self.internals(self.tree1.root):
            for i_2 in self.internals(self.tree2.root):
                if self.terminals(i_1) == self.terminals(i_2):
                    shared += 1
        return len(self.internals(self.tree1.root)) + len(self.internals(self.tree2.root)) - 2*shared




if __name__ == "__main__":
    o = Robinson_Foulds_distance("data/Testdata/tree1.new",
                                 "data/Testdata/tree2.new")
    print(o.distance)


