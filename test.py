#-*-coding:utf-8-*-

import sys, os
import Image, ImageDraw
import numpy as np
from scipy.stats.mstats_basic import tmax
from _imaging import draw
import mytools, mytools2, mytools3

im = Image.open("car4.jpg")
im.show()
print im.mode
R, G, B = 0, 1, 2

sz = im.size
r, c = sz
#print r, c

#im = mytools.userFilter(im, "filter")#降噪
#im.show()
#im = mytools.userFilter(im, "sharpen")#锐化
#im.show()
#im = mytools.hist(im)#直方均衡
#im.show()
im = im.convert('L')#转化成黑白图片
im = mytools2.findEdge(im)#找到竖直方向边缘
im.show()
im = mytools2.binaryzation(im, 180)#二值化
im.show()
im = mytools2.horPro(im)#向垂直方向投影
im.show()
im.save('result.png')

print "DONE!"


