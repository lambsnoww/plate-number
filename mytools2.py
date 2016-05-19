#-*-coding:utf-8-*-
'''
Created on 2016年4月19日

@author: linxue
'''
import sys, os
import Image, ImageDraw
import numpy as np
from scipy.stats.mstats_basic import tmax
from _imaging import draw

from _ast import Add
import colorsys
from __builtin__ import True
from Carbon.Aliases import true
from Tkconstants import LAST
import matplotlib.pyplot as plt

#找到边缘 + 二值化 + 竖起方向投影 + 光滑化

def findEdge(im):#返回x、y、xy边缘图像三个，组成一个组 + 一般输入一个黑白图像
    newIm = Image.new('L',im.size)
    newIm2 = Image.new('L',im.size)
    newIm3 = Image.new('L',im.size)
    newIm4 = Image.new('L',im.size)
    
    draw = ImageDraw.Draw(newIm)
    draw2 = ImageDraw.Draw(newIm2)
    draw3 = ImageDraw.Draw(newIm3)
    draw4 = ImageDraw.Draw(newIm4)

    ###########################
    cols = list(im.size)[1]
    rows = list(im.size)[0]
    arr = [[0 for col in range(cols)] for row in range(rows)]#一定要这样建matrix啊!!!!!!!!!!!
    im1=im.convert('L')
    source = im1.split()
    for i in range(0, list(im.size)[0]):
        for j in range(0, list(im.size)[1]):
            arr[i][j] = source[0].getpixel((i,j))
            draw4.point([i,j], arr[i][j])

    #########################

    
    gx = gy = 0
    for i in range(1, list(im.size)[0] - 1):
        for j in range(1, list(im.size)[1] - 1):
            z1 = arr[i - 1][j - 1]
            z2 = arr[i - 1][j]
            z3 = arr[i - 1][j + 1]
            z4 = arr[i][j - 1]
            z5 = arr[i][j]
            z6 = arr[i][j + 1]
            z7 = arr[i + 1][j - 1]
            z8 = arr[i + 1][j]
            z9 = arr[i + 1][j + 1]
#            print z1,z2,z3,z4,z5,z6,z7,z8,z9
            gx = z7 + z8 + z9 - z1 - z2 - z3
            gy = z3 + z6 + z9 - z1 - z4 - z7
            gx = abs(gx)
            gy = abs(gy)
            gmax = max(gx, gy)
#            print gx, gy, gmax
            draw.point([i,j], gx)
            draw2.point([i,j], gy)
            draw3.point([i,j], gmax)
            draw4.point([i,j], arr[i][j])
#    newIm.show()
#    newIm2.show()
#    newIm3.show()
#    newIm4.show()
    del draw, draw2, draw3, draw4
#    return (newIm, newIm2, newIm3)
    return (newIm, newIm2, newIm3)
    
def binaryzation(im, n):
    source = im.split()
    cols = list(im.size)[0]
    rows = list(im.size)[1]
    newIm = Image.new('L', (cols, rows))
    draw = ImageDraw.Draw(newIm)
#    arr = [[0 for col in range(cols)] for row in range(rows)]#一定要这样建matrix啊!!!!!!!!!!!
    a = 0
    for i in range(0, rows):
        for j in range(0, cols):
            a = source[0].getpixel((j, i))
            if a > n:
                a = 255
            else:
                a = 0
            draw.point([j, i], a)
    del draw
    return newIm

def horPro(im):#竖直方向的投影

    cols = list(im.size)[0]
    rows = list(im.size)[1]
    proArr = [0.0 for col in range(rows)]
    source = im.split()
    for i in range(0, rows):
        for j in range(0, cols):
            if source[0].getpixel((j,i)) > 0:
                proArr[i] = proArr[i] + 1
    ma = max(proArr)
    c2 = cols/2#可自定义
    for i in range(0, rows):
        proArr[i] = proArr[i] * c2/ ma
#        print proArr[i]


#    newIm = Image.new('L',(c2 + 50 + cols,rows))
    sh = Image.new('L', (c2, rows))
    draw = ImageDraw.Draw(sh)
    for i in range(0,rows):
        for j in range(0,c2):
            if j > proArr[i]:
                draw.point([j,i],0)
            else:
                draw.point([j,i],255)
#    for i in range(0,rows):
#        for j in range(c2 + 50, c2 + 50 + cols):
#            draw.point([j,i],source[0].getpixel((j - c2 - 50,i)))

#    del draw
#    newIm.show()
    newIm = paste(sh, im, 50)
    return (newIm, proArr)#这里试着返回拼好的图像+频率矩阵

def paste(im1, im2, inte):

    c1 = list(im1.size)[0]
    r1 = list(im1.size)[1]
   
    c2 = list(im2.size)[0]
    r2 = list(im2.size)[1]
    r = min(r1, r2)
    newIm = Image.new('L',(c1 + inte + c2, r))
    draw = ImageDraw.Draw(newIm)
    source1 = im1.split()
    source2 = im2.split()
    for i in range(0, r):
        for j in range(0, c1):
            draw.point([j,i],source1[0].getpixel((j,i)))
    for i in range(0,r):
        for j in range(c1 + inte, c1 + inte + c2):
            draw.point([j,i],source2[0].getpixel((j - c1 - inte,i)))

    del draw

    return newIm
def pastev(im1, im2, inte):
    im1r = im1.rotate(270)       
    im2r = im2.rotate(270)
    im = paste(im1r, im2r, inte)
    im = im.rotate(90)
#    im.show()
    return im
def smooth(proArr, alp):
    ln = len(proArr)
    retArr = [0 for i in range(ln)]
    for i in range(1, ln):
        retArr[i] = proArr[i] * alp + proArr[i - 1] * (1 - alp)
    return retArr      

def findMaxCouple(arr, rangePercent):
    l = len(arr)
    max1 = 0
    max2 = 0
    maxIndex1 = 0
    maxIndex2 = 0
    for i in range(l):
        if arr[i] > max1:
            max1 = arr[i]
            maxIndex1 = i
    for i in range(l):
        if arr[i] > max2 and arr[i] < arr[maxIndex1]:
            if (i >= maxIndex1 + rangePercent * l) or (i <= maxIndex1 - rangePercent * l):
                max2 = arr[i]
                maxIndex2 = i
            else:
                continue
    return (maxIndex1, maxIndex2, max1, max2)
               
def findVerRange(arr, maxIndex, scop):#找到车牌的竖直位置范围
#    per = (0.1, 0.125, 0.15, 0.175, 0.2, 0.215, 0.25, 0.275, 0.3, 0.35, 0.4, 0.45)
    per = (0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.175, 0.2, 0.215, 0.25, 0.275, 0.3, 0.35, 0.4, 0.45 )
    for i in range(0, len(per)):
        a = min(int(maxIndex * (1 + per[i])), len(arr) - 1)
        if (arr[a] > (arr[maxIndex] * scop)):
#            print arr[maxIndex]
#            print (arr[a], (arr[maxIndex] * scop))
            continue
        else:
            break
    hIndex = int(maxIndex * (1 + per[i]))
    
    for i in range(0, len(per)):
        b = max(int(maxIndex * (1 - per[i])), 0)
        if (arr[b] > (arr[maxIndex] * scop)):
            continue
        else:
            break
    lIndex = int(maxIndex * (1 - per[i]))
    
    return (lIndex, hIndex)
 
def decideFromTowAlternative(im, alt1, alt2):#二者择一，根据定长范围内点多点少
    r = list(im.size)[1]
    c = list(im.size)[0]
    
    frame = int(c / 3)#因为车牌通常都占图片横向的三分之一，所以以此长度为窗口计算出现数目，多者胜出
#    step = 10#定义10为窗口移动单位
    arr = np.array(im)
    verticalScope = 10#为了减小误差，令范围内上下各10像素之内的点参与到计算中
    alist= [[0 for i in range(c)] for j in range(0, 2)]
    alt = [alt1, alt2]
    for k in range(0, 2):
        for i in range(alt[k] - verticalScope, alt[k] + 1 + verticalScope):
            if alt[k] - verticalScope >= 0 and alt[k] + 1 + verticalScope <= r:
                for j in range(c):
                    if arr[i][j] > 0:
                        alist[k][j] = alist[k][j]+ 1
#    print alist[0]
#    print alist[1]
    sum1 = sum(alist[0])
    sum2 = sum(alist[1])
    
    l = c - frame + 1
    blist= [[0 for i in range(l)] for j in range(0, 2)]
    ind = 0
    for k in range(0, 2):
        ind = 0
        for i in range(0, c - frame):
            blist[k][ind] = sumForArr(alist[k], i, i + frame)
            ind = ind + 1
#    print blist
    print "max1, sum1, max2, sum2"
    print max(blist[0]), sum1, max(blist[1]), sum2

    if (float(max(blist[0]) / sum1)  >= float(max(blist[1])) / sum2):
        return alt1
    else:
        return alt2

def sumForArr(arr, start, end):
    sum1 = 0
    for i in range(start, end):
        sum1  = sum1 + arr[i]
    return sum1

def getBiIm(arr):
    r = len(arr)
    c = len(arr[0])
    im = Image.new('L', (c, r))
    draw = ImageDraw.Draw(im)
    for i in range(r):
        for j in range(c):
            draw.point([j, i], arr[i][j])
    del draw
    return im

def derivative(arr):
    l = len(arr)
    b = [0 for i in range(l)]
    b[0] = arr[0]
    for i in range(1, l):
        b[i] = arr[i - 1] + arr[i]
    return b

def getPlateImage(im):#这里的im是经过了初步处理的彩色全车照片
    arr = np.array(im)
    
    
