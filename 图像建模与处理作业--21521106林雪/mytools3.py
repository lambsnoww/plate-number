
#-*-coding:utf-8-*-
'''
Created on 2016年4月26日

@author: linxue
'''
import sys, os
import Image, ImageDraw, ImageOps
import numpy as np
import colorsys
import matplotlib.pyplot as plt
import mytools as t1
import mytools2 as t2
import mytoolshsv as myhsv
from itertools import count
from _Res import Count1Resources
import Queue
from __builtin__ import False


def getWhitepointSumArr(im, mode):
    imArr = np.array(im)
    r = len(imArr)
    c = len(imArr[0])
    if mode == 'r':
        retArr = [0 for i in range(r)]
        for i in range(r):
            for j in range(c):
                if imArr[i][j] > 0:
                    retArr[i] = retArr[i] + 1
    elif mode == 'c':
        retArr = [0 for i in range(c)]
        for i in range(c):
            for j in range(r):
                if imArr[j][i] > 0:
                    retArr[i] = retArr[i] + 1
    return retArr

#返回(startIndex, endIndex, count)三元组，其中count达到最大
def findHorRange(im, ind):#对二值化的图片横长条，找到车牌所在的水平位置

    imArr = np.array(im)
    r = len(imArr)
    c = len(imArr[0])

    interval = int(c / 3 / 7)
    findList = []
    flag = False
    count = 0
    startIndex = 0
    endIndex = 0
    for i in range(c):

        if imArr[ind][i] > 0: #这里只考虑二值化之后的
            if flag == False:
                count = 1
                flag = True
                startIndex = i
                endIndex = i
                continue
            elif flag == True:
        
                if (i - endIndex) <= interval:
                    endIndex = i
                    if i > 0:
                        if imArr[ind][i - 1] == 0:
                            count = count + 1
                    continue
                elif (i - endIndex) > interval:
                    item = [startIndex, endIndex, count]
                    findList.append(item)
                    flag = True
                    count = 1
                    startIndex = i
                    endIndex = i
                    
                    continue
        else:
            if i == c - 1:
                item = [startIndex, endIndex, count]
                findList.append(item)
                break#都无所谓了，反正已经结束了
    maxCount = 0    
    maxInd = 0
    for i in range(len(findList)):
        if findList[i][2] > maxCount:
            maxCount = findList[i][2]
            maxInd = i
    return findList[maxInd]
                
def expand(im, n, m):#膨胀算法
    #这里是bi二值图像，一次扩张n个像素(一般n = 3）；第一个参数是row，第二个是col
    arr = np.array(im)
    r = len(arr)
    c = len(arr[0])
    brr = [[0 for i in range(c)] for j in range(r)]
    for i in range(r):
        for j in range(c):
            if arr[i][j] > 0:
                for k in range(n * (-1), n + 1):
                    for t in range(m * (-1), m + 1):
                        if i + k >= 0 and i + k <= r - 1 and j + t >= 0 and j + t <= c - 1:
                            brr[i + k][j + t] = 255
    image = t2.getBiIm(brr)
    return image

def printArr(arr):
    r = len(arr)
    c = len(arr[0])
    for i in range(r):
        for j in range(c):
            print "%3d" % arr[i][j],
        print
        
def findPlateEdge(im):
    arr = np.array(im)
    r = len(arr)
    c = len(arr[0])
    setNumForRow = [0 for i in range(r)]
    for i in range(r):
        setNum = 0
        flag = False
        for j in range(c):
            if arr[i][j] > 0 and flag == False:
                flag = True
                setNum = setNum + 1
            elif arr[i][j] > 0 and flag == True:
                continue
            elif arr[i][j] == 0 and flag == True:
                flag = False
                
        setNumForRow[i] = setNum
    return setNumForRow

def drawWaveByRow(arr, num):
    l = len(arr)
    ma = max(arr)
    brr = [[0 for i in range(l)] for j in range(num)]
    crr = [0 for i in range(l)]
    for i in range(l):
        crr[i] = float(arr[i]) * num / ma            
    for i in range(l):
        for j in range(num):
            if num - j < crr[i]:
                brr[j][i] = 255
            else:
                brr[j][i] = 0
    
    im = t2.getBiIm(brr)
    return im

def runFindPlate(im):#run run run
    imOrigin = im 
    imbw = im.convert("L")#黑白图
    imbwArr = np.array(imbw)#黑白图的矩阵
    row = len(imbwArr)
    col = len(imbwArr[1])
    print "原始图像尺寸：" + str((row, col))
    imXbw = t2.findEdge(imbw)[0]#X方向的黑白图
    imXbwArr = np.array(imXbw)
    imXbi = t2.binaryzation(imXbw, 120)#二值化的X方向的黑白图
    
    x = [i + 1 for i in range(row)]
    WhitepointSumArr = getWhitepointSumArr(imXbi, 'r')
    SmoothedWhitepointSumArr = t2.smooth(WhitepointSumArr, 0.6)
    SmoothedWhitepointSumArr = t2.smooth(SmoothedWhitepointSumArr, 0.6)
    SmoothedWhitepointSumArr = t2.smooth(SmoothedWhitepointSumArr, 0.6)
    SmoothedWhitepointSumArr = t2.smooth(SmoothedWhitepointSumArr, 0.6)

    
    maxIndex1, maxIndex2, maxIndex3, max1, max2, max3 \
        = t2.findMaxTriple(SmoothedWhitepointSumArr, 0.2)
    print "find max triple! -- ",
    print maxIndex1, maxIndex2, maxIndex3
    
    maxIndex = [maxIndex1, maxIndex2, maxIndex3]

    outcome = [(0,0,0,0,0) for i in range(3)]
    plateIm = []
    for i in range(3):
        print "%d :"%i
        #垂直定位函数（已找到其中一点的情况下）
        l, h = t2.findVerRange(SmoothedWhitepointSumArr, maxIndex[i], 0.5)
#        l = int(l - (h - l * 0.1))
#        h = int(l - (h - l * 0.1))
        print "l, h = %d, %d"%(l, h)
        m = int((l + h) / 2)
        lt, rt, fre = findHorRange(imXbi, m)
        outcome[i] = (l, h, lt, rt, fre)
        #outcome的最后一个量fre代表频率次数，一般越大，可能性越高，但也不绝对，因此只能作为参考
        outcome[i] = expandPlateScope((l, h, lt, rt, fre), 0.1, 0, row, col)
        print "outcome",
        print outcome[i],
        imshow = im.crop((outcome[i][2], outcome[i][0], outcome[i][3], outcome[i][1]))
        plateIm.append(imshow)

    print
    hsv = [[0 for i in range(3)] for j in range(3)]
    ratio = [0.0 for i in range(3)]
    for i in range(3):
        hsv[i] = myhsv.RGBtoHSV(plateIm[i])
        ratio[i] = calculateBlueRatio(hsv[i][0], hsv[i][1], hsv[i][2])
    print "ratio : ",
    print ratio[0], ratio[1], ratio[2]
    mo = findMax(ratio[0], ratio[1], ratio[2])
    imOut = plateIm[mo]#找到最可能的车牌，下面对它作一次HSV的检验，找出蓝色车牌，切边

    return imOut
    
    
    print "DONE@t3.runFindPlate"    

def findMax(a, b, c):
    if a > b:
        if a > c:
            return 0
        else:
            return 2
    elif b < c:
        return 2
    else:
        return 1

def expandPlateScope(outcome, percent1, percent2, row, col):
    l, h, lt, rt, fre = outcome
    le = max(0, int(l - (h - l) * percent1))
    he = min(row - 1, int(h + (h - l) * percent1))
    lte = max(0, int(lt - (rt - lt) * percent2))
    rte = min(col - 1, int(rt + (rt - lt) * percent2))  
    outcomeE = (le, he, lte, rte, fre)#进行0.2的扩张边缘，以防车牌缺角
    return outcomeE

#蓝色车牌
#H值范围：190 ~ 245
#S值范围： 0.35 ~ 1
#V值范围： 0.3 ~ 1
def calculateBlueRatio(h, s, v):
    r = len(h)
    c = len(h[1])
    count = 0
    
    for i in range(r):
        for j in range(c):
            if h[i][j] >= 190 and h[i][j] <= 245:
                count = count + 1


    return count / (float(r) * c)
    
