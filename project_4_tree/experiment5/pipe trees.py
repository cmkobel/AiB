import subprocess

""" This file takes the increasing fasta files and creates corresponding trees with rapidnj. """

def bash(command):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode("utf-8")


# write into file
def write_file(file_name, content):
    with open(file_name, "w") as file:
        for i in content:
            file.write(i)

for i in range(2, 396):
	print(f'file: inc_fasta/seqs_{i}_of_{395}.fasta')
	output = bash(f'../data/macos10.12.6/rapidNJ/bin/rapidnj -i fa inc_fasta/seqs_{i}_of_{395}.fasta')
	write_file(f'inc_newick/out_{i}.new', output)
