'''

Project 2 (due Sep 21): Global alignment with different gap costs
This project is about implementing and experimenting with pairwise sequence comparison methods to compute optimal global alignments of two sequences where the object is to minimize a cost.

Formalities
You should describe your work in a short report (2-3 pages plus figures) containing the following:

Introduction (< 10 lines):
A short status of your work. Does everything work as expected, or are there any problems or unsolved issues.
Methods (< 1 page):
An overview of the implemented programs. Comment on design/implementation choices that differ significantly from what we have talked about in class. Be precise in describing how to access and use your programs (e.g. how to specify the score matrix, gap cost, and input sequences).
Test (< 1 page):
Explain how you have verified the correctness of your programs, i.e. what tests were performed and why. Comment on if your programs perform as expected on the test cases presented in project2_examples.txt .
The answers to the questions in  project2_eval.txt .
Experiments (< 1 pages):
A plot showing the running time of global_linear, and a short discussion on whether or not the plot verifies the thereotical running times.
A plot showing the running time of global_affine, and a short discussion on wheter or not the plot verifies the theoretical running and how it compares to the running time of global_linear.
Your report (in pdf-format) and code (in a zip-archive) must be uploaded via Blackboard cf. assignment below before Thursday, September 21, 14:00.

This project will not be graded but you should be able to present your work and the underlying theory and algorithms at the oral exam. The project should be done in groups of 2-3 students.

Problem I: Implementing alignment methods
You should implement the following programs for pairwise global alignment of DNA sequences (i.e. alphabeth a, c, g, t) based on minimizing cost, i.e. the optimal score is the minimum score. You can use any programming language you like.

Mandatory: Make a program global_linear that implements global alignment using linear gap cost. The program should be implemented such that it takes at most quadratic time and space to compute the cost of an optimal global alignment. If requested, the program should output an optimal global alignment.
Mandatory: Make a program global_affine that implements global alignment using affine gap cost. The program should be implemented such that it takes at most quadratic time and space to compute the cost of an optimal global alignment. If requested, the program should output an optimal global alignment.
Optional: Make a program global_linear_linspace that is similar to global_linear but consumes only linear space, i.e. use Hirscberg's idea for finding an optimal global alignment in linear space.
Optional: Make a program global_affine_linspace that is similar to global_affine but consumes only linear space. You need to extend Hirscberg's idea to handle affine gap cost. (Explain in the report how you extend the idea, and verify carefully that your program computes an optimal alignment.)
In your report, you must explain how to use and access your programs. I must be able to verify that they work. In particular you should pay attention to the following:

(1) You must decide (and explain in your report) how to specify the two input sequences. The sequence can e.g. be specified on the command-line, or they can be listed in an input file. The first choice is ok for short input sequences, while the second choice is more useful for longer input sequences. Feel free to implement both options. If you decide that the input sequences should be listed in an input file, then it might be convenient to use FASTA format, which is a widely used text based format for specifying sequences. There are many libraries for reading sequences in FASTA format depending on your programming language. Feel free to use any library you can find.

(2) You must decide (and explain in your report) how to specify the character score matrix, and the parameters of the gap cost function, but aim for something simple. E.g. the parameters of the gap cost functions are specified as command line parameters, while the alphabet and character score matrix are specified in a control file read by the program. The file could e.g. be in the following "Phylip-like" format which is convenient for specifying both the score matrix and the alphabet. Here is an example of a score matrix for DNA in this format:

  4 
  A  0  5  2  5
  C  5  0  5  2
  G  2  5  0  5
  T  5  2  5  0

The first line in the file contains the number n of characters covered by the matrix. The next n lines describes the symbol for each character and its distance to the other characters. The above matrix says that matches (AA, CC, GG, TT) have distance 0, transitions (AG, GA, TC, CT) have distance 5, and transversions (AT, TA, AC, CA, GT, TG, GC, CG) have distance 2. If your input sequences contain characters which are not part of the specified alphabeth, your program should choose an appropriate action, e.g. terminate with an error message.

(3) The computed optimal alignment should be output in FASTA alignment format (also called Pearson format after the creator of the FASTA alignment program). In FASTA alignment format, the two aligned sequences are printed above each other with gaps inserted as described by the computed alignment. For example,

  >seq1 
  ctacgaaaggtcgtgtcacg-atgtcc------gc
  aagggatggcat---tgcatagaggaattgat--t
  gcaac

  >seq2
  ctt-----------------aatgtcccgcgta-c
  aagggatagcatgtg-gcatagaggaatagaata-
  gcagc

The FASTA alignment format is just one of many used alignment formats. The Jalview program makes it easy to read and display alignments in many different formats. Jalview can be used as an applet or downloaded and installed locally (see their www page for documentation and details).

Problem II: Experimenting with alignment methods
In the second part of this project you should design and implement experiments to examine the compuational qualities of your alignment methods. You should:

Construct test data and perform test runs to ensure that each of the programs perform as expected. In the report, you must explain how you have constructed test data to ensure that each program is tested properly. You should also verify that your global alignment performs as expected on the 4 test cases presented in  project2_examples.txt .
Perform experiments that illustrate that the time consumption of the programs are as expected according to the theoretical bounds. E.g. by measuring the running time of your programs using the Unix time-command for sequences of increasing lengths.
Perform experiments that compare the running time for computing an optimal alignment using linear gap cost in quadratic space and the running time for computing an optimal alignment using affine gap cost. What do you expect, and do your experiments confirm this?
If you have implemented the optional parts above, you should also perform experiments that examine their running times.

'''


class General_GC:
  pass