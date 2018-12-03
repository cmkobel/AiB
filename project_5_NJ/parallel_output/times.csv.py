files = ['89_Adeno_E3_CR1.phy' ,'214_Arena_glycoprot.phy' ,'304_A1_Propeptide.phy' ,'401_DDE.phy' ,'494_Astro_capsid.phy' ,'608_Gemini_AL2.phy' ,'777_Gemini_V1.phy' ,'877_Glu_synthase.phy' ,'1347_FAINT.phy' ,'1493_Fe-ADH.phy' ,'1560_Ferritin.phy' ,'1689_FGGY_N.phy' ,'1756_FAD_binding_3.phy' ,'1849_FG-GAP.phy']
otimes = [1.154876470565796, 25.9326593875885, 97.08338284492493, 309.9372878074646, 3777.9176139831543, 5931.679894447327, 57940.25156068802]

times = [1.154876470565796,
         25.9326593875885, 
         97.08338284492493,
         309.9372878074646,
         673.1710770130157,
         1440.750722169876,
         3777.9176139831543,
         5931.679894447327,
         31877.47610616684,
         47907.77636170387,
         57940.25156068802]











with open('times.csv', 'w') as file:
    file.write(f'files, times\n')
    for i, j in zip(files, times):
        file.write(f'{i}, {j}\n')