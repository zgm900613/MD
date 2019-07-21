# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 10:47:06 2019

@author: GM Zhu
"""

import pandas as pd
import numpy as np
from tqdm import tqdm

def inlmp(file_path, skip, col):   #define a function to import log file
    x = pd.read_table(file_path, skiprows = skip, sep = '\s+|,', header = None)
    xM = x.ix[:, 0 : col]
    xMatrix = np.matrix(xM)
    return(xMatrix)

plane_list = ('basal_edge', 'basal_screw',
              'prism_edge', 'prism_screw',
              'pyrIa_edge', 'pyrIa_screw',
              'pyrIca_edge', 'pyrIca_screw',
              'pyrII_edge', 'pyrII_screw')

plane = 'pyrIca_screw'

data0_raw = inlmp(r'm10000_'+str(plane)+'.lmp', 9, 4)
atom0_raw = inlmp(str(plane)+'_raw.txt', 1, 4)

pos = np.zeros((len(atom0_raw), 7))

for i in tqdm(range(len(atom0_raw))):
    for j in range(len(data0_raw)):
        if atom0_raw[i, 1] == data0_raw[j, 0]:
            pos[i, 0] = atom0_raw[i, 0]
            pos[i, 1] = atom0_raw[i, 1]
            pos[i, 2] = atom0_raw[i, 2]
            pos[i, 3] = atom0_raw[i, 3]
            pos[i, 4] = data0_raw[j, 2]
            pos[i, 5] = data0_raw[j, 3]
            pos[i, 6] = data0_raw[j, 4]

doc = open('atom_pos_'+str(plane)+'.txt', 'w+')
doc.write('pos_No\tatom_No\tenergy\tabs_energy\tpos_x\tpos_y\tpos_z\n')

line_No, column_No = np.shape(pos)

for i in range(line_No):
    for j in range(column_No):
        doc.write(str(pos[i, j]))
        doc.write('\t')
    doc.write('\n')
doc.close()



