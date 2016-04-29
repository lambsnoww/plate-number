#-*-coding:utf-8-*-
'''
Created on 2016年4月29日

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

plateImbi = Image.open("car7.bmp")
arr = np.array(plateImbi)
print arr
plateEdge =  rf.findPlateEdge(plateImbi)

r = list(plateImbi.size)[1]
c = list(plateImbi.size)[0]
flag = False
for i in range(r):
    if plateEdge[i] >= 7 and flag == False:
        s = i
        e = i
        flag = True
    elif plateEdge[i] < 7 and flag == True:
        e = i - 1
        break
print "the scope of the characters is: "
print (s, e)
plateImbiCroped = plateImbi.crop((0, s, list(plateImbi.size)[0], e))
plateImbiCroped.show()

