#-*-coding:utf-8-*-
import sys, os
import Image, ImageDraw
import numpy as np
from scipy.stats.mstats_basic import tmax
from _imaging import draw
import mytools3
from _ast import Add
import colorsys


def getArr(im):#从一幅binary或灰度图像得到它的矩阵
    sour = im.split()
    r = list(im.size)[1]
    c = list(im.size)[0]
    arr = [[0 for i in range(c)] for j in range(r)]
    for i in range(c):
        for j in range(r):
            arr[j][i] = sour[0].getpixel((i, j))
    return arr
im = Image.open("car1.jpg")
im = im.convert('L')
arr = getArr(im)
print arr
