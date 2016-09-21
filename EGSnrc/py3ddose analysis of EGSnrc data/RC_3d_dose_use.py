# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 12:41:29 2016

@author: robincole
"""

data1 = DoseFile('RC_air_bone_interface_example.3ddose')  # prints shape of loaded data, here (20, 21, 21), i.e. identical to data1.shape
data1.dose.max()   # print the max dose

import matplotlib.pyplot as plt

# data1.dump('data1_np') # not working since  data1.uncertainty is empty