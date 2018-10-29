from Bio import Phylo as ph
import pylab # for plotting

# author: Carl Mathias Kobel

class Robinson_Foulds_distance:
    """ Calculates the Robinson-Foulds distance between two trees defined in Newick-format. """
    def __init__(self, file1, file2):
        self.tree1 = ph.read(file1, "newick")
        self.tree2 = ph.read(file2, "newick")


        self.distance = self.rfdist()


        # print(f'tree1 is bifurc.: {self.tree1.is_bifurcating()}')
        # print(f'tree2 is bifurc.: {self.tree2.is_bifurcating()}')


    
    def is_leaf(self, node):
        return len(node.clades) == 0


    def terminals(self, root):
        """ Takes a root node, and returns the terminal clades (leaves). """
        leaves = []
        
        def recurse(clade):
            """ Recursively traverses the tree, looking for terminals. """
            #if clade.is_terminal():
            if self.is_leaf(clade):    
                #leaves.append(clade)
                leaves.append(clade.name) # easier, but less flexible
                return
            else:
                for clade in clade.clades:
                    recurse(clade)

        recurse(root)
        leaves.sort() # sort to get comparable lists
        return leaves


    def internals(self, root):
        """ Traverses the internal elements. 
        Could have been a generator. """
        rv = []
        
        def recurse(clade):
            """ Recursively traverses the tree, looking for internals. """
            if not self.is_leaf(clade):
                rv.append(clade)

            for clade in clade.clades:
                recurse(clade)

        recurse(root)
        return rv


    def splits(self, root):
        """ Denne funktion viser sig ikke at være den rigtige måde at beregne antallet af splits på."""
        rv = []
        #s_sum = 0
        
        def recurse(clade):
            """ Recursively traverses the tree, looking for internals, counting the number of splits """
            if not self.is_leaf(clade):
                rv.append(len(clade.clades)-1) 
                #s_sum += len(clade.clades)

            for clade in clade.clades:
                recurse(clade)

        recurse(root)

        return rv


    



    def rfdist(self):
        """ time-complexity: O(n^2) """
        shared = 0
        for i_1 in self.internals(self.tree1.root):
            for i_2 in self.internals(self.tree2.root):
                if self.terminals(i_1) == self.terminals(i_2):
                    shared += 1
        # Der er stadig noget galt med kalign
        # printer to forskellige måder. 1. hvor antal splits i hvert træ er defineret fra antal internal splits, og 2. fra antal children minus 1 på hver internal node.
        return (len(self.internals(self.tree1.root)) + len(self.internals(self.tree2.root)) - 2*shared) #,
                #sum(self.splits(self.tree1.root)) + sum(self.splits(self.tree2.root)) - 2*shared)




if __name__ == "__main__":

    def quick_test():

        # o = Robinson_Foulds_distance("data/Testdata/tree1.new",
        #                              "data/Testdata/tree2.new")
        
        o = Robinson_Foulds_distance("experiment1/stockholm/qt/kalign.new",
                                     "experiment1/stockholm/qt/kalign.new")

        print(o.distance)
        

        # print(sum(o.splits1))
        # ph.draw(o.tree2)
        # pylab.show()
        # #print(len(o.internals(o.tree1.root)))

    quick_test()






    # BUILD TABLE
    def build_table():
        def pprint(input):
                for i in input:
                    print(*i, sep = '\t')

        names = ['qt/clustalo.new', 'qt/kalign.new', 'qt/mafft.new', 'qt/muscle.new', 'rnj/clustalo.new', 'rnj/kalign.new', 'rnj/mafft.new', 'rnj/muscle.new']

        names_table = [["" for i in range(len(names))] for j in range(len(names))]
        distance_table = [[None for i in range(len(names))] for j in range(len(names))]


        for _i, i in enumerate(names):
            for _j, j in enumerate(names):
                if _j <= _i:
                    string = i + " | " + j
                    names_table[_i][_j] = string
                    print(string)

                    o = Robinson_Foulds_distance("experiment1/stockholm/" + i,
                                                 "experiment1/stockholm/" + j)
                    distance_table[_i][_j] = o.distance
                    print(o.distance)

                    print()


        pprint(names_table)

        pprint(distance_table)

    #build_table()