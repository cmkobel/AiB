

import rfdist
import time



files = ['89_Adeno_E3_CR1.phy' ,'214_Arena_glycoprot.phy' ,'304_A1_Propeptide.phy' ,'401_DDE.phy' ,'494_Astro_capsid.phy' ,'608_Gemini_AL2.phy' ,'777_Gemini_V1.phy' ,'877_Glu_synthase.phy' ,'1347_FAINT.phy' ,'1493_Fe-ADH.phy' ,'1560_Ferritin.phy' ,'1689_FGGY_N.phy' ,'1756_FAD_binding_3.phy' ,'1849_FG-GAP.phy']
print(files[0:5:])
files = files[0:5:]
path = '../../running time/newick/'





# our:rnj
if True:
    print(f'file, rfdist(GenericNJ:RapidNJ)')
    for file in files:

        o = rfdist.Robinson_Foulds_distance(f'{file}.newick',
                                            f'{path}out_rnj_{file}.newick')
        print(f'{file}, {o.distance}')

# our:qt
if True:
    print(f'file, rfdist(GenericNJ:QuickTree)')
    for file in files:

        o = rfdist.Robinson_Foulds_distance(f'{file}.newick',
                                            f'{path}out_qt_{file}.newick')
        print(f'{file}, {o.distance}')

