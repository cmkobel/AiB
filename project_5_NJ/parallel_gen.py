import neighbour_joining, logging, multiprocessing, time

logger = multiprocessing.log_to_stderr()
logger.setLevel(logging.INFO)


def write_file(f_name, f_content):
        with open(f_name, 'w') as file:
            for i in f_content:
                file.write(i)
#write_file('testout.txt', 'This is not just a test, this is for real. Surrender to the render\nsite.')



filenames = ['89_Adeno_E3_CR1.phy' ,'214_Arena_glycoprot.phy' ,'304_A1_Propeptide.phy' ,'401_DDE.phy' ,'494_Astro_capsid.phy' ,'608_Gemini_AL2.phy' ,'777_Gemini_V1.phy' ,'877_Glu_synthase.phy' ,'1347_FAINT.phy' ,'1493_Fe-ADH.phy' ,'1560_Ferritin.phy' ,'1689_FGGY_N.phy' ,'1756_FAD_binding_3.phy' ,'1849_FG-GAP.phy']
directory = 'data/unique_distance_matrices/'
files = [directory + filename for filename in filenames]


time_collector = []

def generate_unique_trees(file):
    t1 = time.time()
    rv = neighbour_joining.NJ(file).neighbour_joining()
    t2 = time.time()

    write_file(f'kobel_{file.split("/")[-1]}.newick', rv)
    time_collector.append(t2-t1)
    write_file(f'kobel_{file.split("/")[-1]}.time.txt', str(time_collector))




if __name__ == '__main__':
    with multiprocessing.Pool(4) as p:
        p.map(generate_unique_trees, files)
    