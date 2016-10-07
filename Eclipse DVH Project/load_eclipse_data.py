# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 13:57:25 2016

@author: robincole
"""

import numpy as np
file = 'case1_AAA.txt'
 
 # data = np.genfromtxt(file, dtype=None) # for column data
 
header =  np.genfromtxt(file, dtype=None, max_rows=6, delimiter=':') 