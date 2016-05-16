#-*-coding:utf-8-*-
'''
Created on 2016年5月16日

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

def thin(eng, name):
    print "Start thin process"
    eng.eval("imbi = imread('%d.bmp');"%name, nargout = 0)
    eng.eval("imthin = bwmorph(imbi, 'thin', Inf);", nargout = 0)
    imbipy = Image.open('1.bmp')
    c = list(imbipy.size)[0]
    r = list(imbipy.size)[1]
    print "c, r = " + str(c) + ',' + str(r)
    eval_str = "imshow(imthin,'border','tight','initialmagnification','fit');\
        set (gcf,'Position',[0,0,%d,%d]);axis normal;"%(c, r)
    eng.eval(eval_str, nargout = 0)
    eng.eval("imwrite(imthin,'%d.jpg', 'jpg');"%name, nargout = 0)#这个才好用
#    eng.eval("saveas(gcf, '2thin', 'bmp');", nargout = 0)
    print "Thinned pic saved!"

def getNumberOfVerticalLines(im):
#    im = Image.open(name + '.bmp')
    arr = np.array(im)
    r = len(arr)
    c = len(arr[0])
#    for i in range(r):
#        for j in range(c):
#            print arr[i][j],
#        print
    verThreshold = c * 4 / 7#竖直方向假定有超过4/7长度便定义为有一条直线
    numOfLines = 0
    for i in range(c):
        count = 0
        for j in range(r):
            if arr[j][i] >= 200:
                count = count + 1
                
        if count >= verThreshold:
            numOfLines = numOfLines + 1
    return numOfLines


                    
    
    

if __name__ == "__main__":
    print "Initializing Matlab Engine"
    eng = matlab.engine.start_matlab()
    print "Initializing Complete!"
    name = 3
    thin(eng, name)
    im = Image.open(str(name) + ".jpg")
    verLines = getNumberOfVerticalLines(im)
    print verLines
    
    