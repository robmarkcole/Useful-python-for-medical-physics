# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 10:14:30 2016
http://tkinter.unpythonic.net/wiki/tkFileDialog
@author: robincole
"""

import Tkinter
import tkFileDialog

root = Tkinter.Tk().withdraw()     # Close the root window
file_path = tkFileDialog.askopenfilename()
print(file_path)
