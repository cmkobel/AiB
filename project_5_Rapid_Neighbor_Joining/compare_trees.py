import rapid_nj
import rfdist

if __name__ == "__main__":
    newick_tree = rapid_nj.RNJ('data/89_Adeno_E3_CR1.phy').neighbour_joining()
    #newick_tree = rapid_nj.RNJ('data/10.phy').neighbour_joining() # (((8_Q9DK06_, 9_Q9DK03_), ((4_VGLY_PI, 5_O11998_), (6_O11999_, 7_O11997_))), (2_Q9YTW9_, 3_Q9YTW8_), (0_Q9YTX1_, 1_O90423_));
    #newick_tree = RNJ('data/example_slide4.phy').neighbour_joining() #
    print('\n\n', newick_tree)


    out_file_name = 'data/rnjoutput.newick'
    with open(out_file_name, 'w') as file:
        for i in newick_tree:
            file.write(i)

    compare_to = 'data/out_qt_89_Adeno_E3_CR1.phy.newick'
    print('The distance between Our Rapid-NJ and the Quicktree tree is:')
    dist = rfdist.Robinson_Foulds_distance(out_file_name, compare_to)
    print(dist.distance)