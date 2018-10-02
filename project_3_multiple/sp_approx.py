# Author: Carl M. Kobel 2018

# Implements the 2-approximation algorithm for any number of sequences (described in Section 8.2.2 in BA, or in Section 14.6.2 in Gusfield's book).

"""
Procedure
    · Compute pairwise edit distances to find ind the center string
        · Det er vel bare alle mulige kombinationer af strenge, og så tage den bedste.
        · Genbrug kode fra tidligere.
    · Align alle par: S1 - Si over alle i+1 ... n




"""


class SP_approx:
    def __init__(self, sequences):
        self.sequences = sequences


    def calculate_all_pairwise_distances(self):
        """ To find center string"""
        pass


    def align_pairs_S1_Si(self):
        pass

    def calculate_sum_of_pairs_score_of_alignments(self):
        pass