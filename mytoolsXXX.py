#-*-coding:utf-8-*-
'''
Created on 2016年5月23日
膨胀与腐蚀，目的是定位车牌、消除噪声，并对三个候选车牌进行筛选

@author: linxue
'''
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
import Image, ImageDraw, ImageOps
import mytools as t1
import mytools2 as t2
import mytools3 as t3
import collections

if __name__ == '__main__':
    im = Image.open('plateBi.bmp')
    print im.size
    print list(im.size)[0]
    print list(im.size)[1]
    