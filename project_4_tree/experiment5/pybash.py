import subprocess




def bash(command):
	process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
	output, error = process.communicate()
	return output.decode("utf-8")


# make test files

# open more and more fasta files#



#print(bash("../data/macos10.12.6/quicktree_1.1/bin/quicktree mafft.stockholm "))

# write into file
def write_file(file_name, content):
	with open(file_name, "w") as file:
		for i in content:
			file.write(i)


file_name = 'patbase_aibtas.fasta'
num_seqs = sum(1 for line in open(file_name)) //2
#num_seqs = 10 # for testing
#print(num_lines)


with open(file_name, 'r') as input_file:
    file = [i for i in input_file]

for i in range((num_seqs * 2) + 1)[2::2]: # for each lines 2, 2-4, 2-6..
    print(f'{i//2} through {num_seqs}')
    with open(f'inc_fasta/seqs_{i//2}_of_{num_seqs}.fasta', 'w') as output_file: # create file
        for j in range(i):
            output_file.write(file[j])
    