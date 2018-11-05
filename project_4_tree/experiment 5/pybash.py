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

write_file("ny_fil.txt", """Der var engang en ko paa en mark,
den hed superko""")