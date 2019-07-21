ho# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 11:46:32 2019

@author: GM Zhu
"""
import pandas as pd
import numpy as np
from tqdm import tqdm
import matplotlib.pylab as plt
import matplotlib.tri as tri

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

plane = 'pyrIca_screw'   #plane_list[0]
atom0 = inlmp(r'atom_pos_'+str(plane)+'.txt', 1, 7)

'''
------------------------------------------
'''
if plane == 'basal_screw':
    x = np.zeros((len(atom0)-5)*2)
    y = np.zeros((len(atom0)-5)*2)
    energy = np.zeros((len(atom0)-5)*2)
    
    for i in range(5):
        x[i] = atom0[i, 4]
        y[i] = atom0[i, 5]
        energy[i] = atom0[i, 3]
    
    for i in range(len(atom0)-10):
        x[i+5] = atom0[i+10, 4]
        y[i+5] = atom0[i+10, 5]
        energy[i+5] = atom0[i+10, 3]
        
        
    mid_x = (atom0[4, 4] + atom0[5, 4]) / 2
    mid_y = (atom0[4, 5] + atom0[5, 5]) / 2
    
    for i in range(len(atom0)-5):
        x[i + len(atom0)-5] = -(x[i] - mid_x) + mid_x
        y[i + len(atom0)-5] = -(y[i] - mid_y) + mid_y
        energy[i + len(atom0)-5] = energy[i]
elif plane == 'pyrII_screw':
    x = np.array(atom0[:, 4])[:,0]
    y = np.array(atom0[:, 5])[:,0]
    energy = np.array(atom0[:, 3])[:,0]
    
    y[52] = 7.7267
    x[52] = -13.8909
    y[144] = 6.38466
    x[144] = 5.44908
    y[137] = -0.801681
    x[137] = 2.66784

elif plane == 'pyrIa_edge':
    x = np.zeros(len(atom0)*2)
    y = np.zeros(len(atom0)*2)
    energy = np.zeros(len(atom0)*2)
    for i in range(len(atom0)):
        x[i] = atom0[i, 4]
        y[i] = atom0[i, 5]
        energy[i] = atom0[i, 3]
    mid_x = 0.001729
    for i in range(len(atom0)):
        x[i + len(atom0)] = -(x[i] - mid_x) + mid_x
        y[i + len(atom0)] = y[i]
        energy[i + len(atom0)] = energy[i]
else:
    x = np.array(atom0[:, 4])[:,0]
    y = np.array(atom0[:, 5])[:,0]
    energy = np.array(atom0[:, 3])[:,0]


for i in range(len(atom0)):
    if energy[i] > 10:
        energy[i] = 'nan'


plt.figure(figsize = (25,10))

xi = np.linspace(min(x), max(x), 200)
yi = np.linspace(min(y), max(y), 200)


triang = tri.Triangulation(x, y)
interpolator = tri.LinearTriInterpolator(triang, energy)
Xi, Yi = np.meshgrid(xi, yi)
zi = interpolator(Xi, Yi)

plt.contour(xi, yi, zi, linewidths=0.5, colors='k')
cntr1 = plt.contourf(xi, yi, zi, cmap="RdBu_r")

plt.colorbar(cntr1)
plt.scatter(x, y, s=50, c='k')

plt.title(str(plane), fontsize=30)
plt.axis('scaled')
#plt.axis('equal')
#plt.axis((min(x), max(x), min(y), max(y)))
plt.xticks([])
plt.yticks([])
plt.axis('off')
plt.savefig(str(plane)+'.jpg', dpi=300)
plt.show()















