

import rfdist
import time



files = ['89_Adeno_E3_CR1.phy' ,'214_Arena_glycoprot.phy' ,'304_A1_Propeptide.phy' ,'401_DDE.phy' ,'494_Astro_capsid.phy' ,'608_Gemini_AL2.phy' ,'777_Gemini_V1.phy' ,'877_Glu_synthase.phy' ,'1347_FAINT.phy' ,'1493_Fe-ADH.phy' ,'1560_Ferritin.phy' ,'1689_FGGY_N.phy' ,'1756_FAD_binding_3.phy' ,'1849_FG-GAP.phy']


files = files[:11]
print(files)
#raise ValueError()

path_others = '../rnjqttrees/'
path_ours = '../../../parallel_output/'





# our:rnj
if not True:
    cumulated = f'file, rfdist(OurNJ:RapidNJ)\n'
    for file in files:

        o = rfdist.Robinson_Foulds_distance(f'{path_ours}kobel_{file}.newick',
                                            f'{path_others}out_rnj_{file}.newick')
        new_line = f'{file}, {o.distance}'
        print(new_line)
        cumulated += new_line + '\n'
    
    with open('ourVSrnj.csv', 'w') as file:
        for i in cumulated:
            file.write(i)

# our:qt
if True:
    cumulated = f'file, rfdist(OurNJ:QuickTree)\n'
    for file in files:

        o = rfdist.Robinson_Foulds_distance(f'{path_ours}kobel_{file}.newick',
                                            f'{path_others}out_qt_{file}.newick')

        new_line = f'{file}, {o.distance}'
        print(new_line)
        cumulated += new_line + '\n'

    with open('ourVSqt.csv', 'w') as file:
        for i in cumulated:
            file.write(i)