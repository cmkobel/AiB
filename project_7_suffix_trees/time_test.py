from st import suffixtree
from parsers import parse_fasta, parse_fastq
import string
from time import time



#full_string = string.printable[:94] * 5





# Build alphabet:
alphabet = ''
for i in range(9968, 9968+6): #9400-11000 in tests
    #print('alphabet size:', i)
    letter = chr(i)#.encode('utf-8')
    #print(letter)
    alphabet += letter

#print(alphabet.encode('utf-8'))

print(alphabet[0:10].encode('utf-8'))



if True: # Test tree construction 
    # Iterate through alphabet:
    for i in range(0, len(alphabet.encode('utf-8')), 10):
        genome = alphabet[:i].encode('utf-8')
        #print(genome)
        print(len(genome), end = ', ')

        t1 = time()
        st = suffixtree(genome.decode('utf-8'), show = True)
        t2 = time()
        print(t2-t1, end = ', ')


        #print('matches:', end ='')
        t3 = time()
        for match in st.find_positions(''):
            #print('', match, end = '')
            pass
        t4 = time()
        print(t4-t3)
