#-*-coding:utf-8-*-
'''
Created on 2016年4月30日

@author: linxue
'''

import sys, os
import Image, ImageDraw, ImageOps
import numpy as np
import colorsys
import matplotlib.pyplot as plt
import mytools as t1
import mytools2 as t2
from itertools import count
from _Res import Count1Resources
import Queue
from __builtin__ import False
import refa as rf
import collections
import matlab
import matlab.engine

im = Image.open("1.bmp")
arr = np.array(im)
r = len(arr)
c = len(arr[0])
print r, c
for i in range(r):
    for j in range(c):
        print arr[i][j],
#        if arr[i][j] == True:
#            print '1',
#        else:
#            print '0',
    print



