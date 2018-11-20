import subprocess, time

""" This program runs the distance matrices through rapid nj and quicktree. """


def timeit(method):
    """ Unused decorator """
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print( '%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result
    return timed



def bash(command):
    t1 = time.time()
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    t2 = time.time()
    return t2-t1, output.decode("utf-8")


print(bash("sleep 2"))

# other
def to_csv(input):
    print(f'time, file, taxa')
    for line in input:
        print(f'{line[0]}, {line[1]}, {line[2]}')





file_path = '../unique_distance_matrices/'
files = ['89_Adeno_E3_CR1.phy' ,'214_Arena_glycoprot.phy' ,'304_A1_Propeptide.phy' ,'401_DDE.phy' ,'494_Astro_capsid.phy' ,'608_Gemini_AL2.phy' ,'777_Gemini_V1.phy' ,'877_Glu_synthase.phy' ,'1347_FAINT.phy' ,'1493_Fe-ADH.phy' ,'1560_Ferritin.phy' ,'1689_FGGY_N.phy' ,'1756_FAD_binding_3.phy' ,'1849_FG-GAP.phy']
rapidnj = '../../../project_4_tree/data/macos10.12.6/rapidNJ/bin/./rapidnj'
quicktree = '../../../project_4_tree/data/macos10.12.6/quicktree_1.1/bin/./quicktree'



# rapidnj
if not True:
    rapid_nj_results = list()
    for file in files:
        print('file', file)

        n_replicates = 5
        replicate_sum = 0
        for replicate in range(n_replicates):
            print('replicate', replicate)
            test = bash(str(f'{rapidnj} -i pd {file_path}{file}'))
            replicate_sum += test[0]
            #print(test[1]) # debug
        rapid_nj_results.append((replicate_sum/n_replicates, file, file.split('_')[0]))
    
    print()
    print(to_csv(rapid_nj_results))

# quicktree
if not True:
    quicktree_results = list()
    for file in files:
        print('file', file)

        n_replicates = 5
        replicate_sum = 0
        for replicate in range(n_replicates):
            print('replicate', replicate)
            test = bash(str(f'{quicktree} -in m {file_path}{file}'))
            replicate_sum += test[0]
            #print(test[1]) # debug
        quicktree_results.append((replicate_sum/n_replicates, file, file.split('_')[0]))

    print()
    print(to_csv(quicktree_results))





