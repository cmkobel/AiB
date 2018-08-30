
Test cases for global alignment usign linear gap cost
-----------------------------------------------------

Consider the below score matrix M for dna sequences:

   A  C  G  T    
A 10  2  5  2    
C  2 10  2  5    
G  5  2 10  2    
T  2  5  2 10  


Case 1
------

>seq1
TCCAGAGA

>seq2
TCGAT

Using score matrix M and linear gap cost g(k) = -5*k, the score of an
optimal is:

27

and there are 4 optimal alignments:

TCCAGAGA
TC--GAT-

TCCAGAGA
T-C-GAT-

TCCAGAGA
TC--GA-T

TCCAGAGA
T-C-GA-T


Case 2
------

>seq1
CGTGTCAAGTCT

>seq2
ACGTCGTAGCTAGG

Using score matrix M and linear gap cost g(k) = -5*k, the score of an
optimal is:

61

and there are 3 optimal alignments:

-CGT-GTCAAGTCT-
ACGTCGT-AGCTAGG

-CGT-GTCAAGTC-T
ACGTCGT-AGCTAGG

-CGT-GTCAAGT-CT
ACGTCGT-AGCTAGG
