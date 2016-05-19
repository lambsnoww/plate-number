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

def findHorRange(im, ind):#对二值化的图片横长条，找到车牌所在的水平位置
#    arr = getWhitepointSumArr(im, 'c')

    imArr = np.array(im)
#    print imArr[ind]
    r = len(imArr)
    c = len(imArr[0])

    interval = int(c / 3 / 7)
    findList = []
    flag = False
    count = 0
    startIndex = 0
    endIndex = 0
    for i in range(c):
#        print "index: " + str(i)
        if imArr[ind][i] > 0: #这里只考虑二值化之后的
#            print "i = %d, "%i
            if flag == False:
                #print "first enter" + str(i)
                count = 1
                flag = True
                startIndex = i
                endIndex = i
                continue
            elif flag == True:
        
                if (i - endIndex) <= interval:
                    #print "<= interval, i = " + str(i)
                    endIndex = i
                    if i > 0:
                        if imArr[ind][i - 1] == 0:
                            count = count + 1
                    continue
                elif (i - endIndex) > interval:
                    #print ">= interval, i = " + str(i)
                    #print "first come out" + str(i)
                    item = [startIndex, endIndex, count]
                    findList.append(item)
                    flag = True
                    count = 1
                    startIndex = i
                    endIndex = i
                    
                    continue
        else:
            if i == c - 1:# and  (i - endIndex) > interval:
                item = [startIndex, endIndex, count]
                findList.append(item)
                break#都无所谓了，反正已经结束了
    maxCount = 0    
    maxInd = 0
    for i in range(len(findList)):
        print findList[i]
        if findList[i][2] > maxCount:
            maxCount = findList[i][2]
            maxInd = i
#            print "maxIndex : %d"%maxInd
#    print findList
    return findList[maxInd]
                
def expand(im, n, m):#这里是bi二值图像，一次扩张n个像素(一般n = 3）；第一个参数是row，第二个是col
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
#    print brr
#    image.show()
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
#        print setNumForRow
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
    im.show()
    return im

def runFindPlate(im):#run run run
#    im = Image.open(name + ".jpg")#原图
#    im = t1.preprocess(im)
    imOrigin = im 
    imbw = im.convert("L")#黑白图
    imbwArr = np.array(imbw)#黑白图的矩阵
    r = len(imbwArr)
    c = len(imbwArr[1])
    print "原始图像尺寸：" + str((r, c))
    imXbw = t2.findEdge(imbw)[0]#X方向的黑白图
    #imXbw.show()
    imXbwArr = np.array(imXbw)
    imXbi = t2.binaryzation(imXbw, 120)#二值化的X方向的黑白图
    
    x = [i + 1 for i in range(r)]
    WhitepointSumArr = getWhitepointSumArr(imXbi, 'r')
    #plt.plot(x, y)
    #plt.show()
    SmoothedWhitepointSumArr = t2.smooth(WhitepointSumArr, 0.6)
    SmoothedWhitepointSumArr = t2.smooth(SmoothedWhitepointSumArr, 0.6)
    SmoothedWhitepointSumArr = t2.smooth(SmoothedWhitepointSumArr, 0.6)
    SmoothedWhitepointSumArr = t2.smooth(SmoothedWhitepointSumArr, 0.6)
    plt.plot(x, SmoothedWhitepointSumArr)
    plt.show()
            
    maxIndex1, maxIndex2, max1, max2 = t2.findMaxCouple(SmoothedWhitepointSumArr, 0.2)
    print "find max couple!"
    
    l, h = t2.findVerRange(SmoothedWhitepointSumArr, maxIndex1, 0.5)#垂直定位函数（已找到其中一点的情况下）
    print "alternative low and high edge: " + str(((l, h)))
        
    l = int(l - (h - l) * 0.1)
    h = int(h + (h - l) * 0.1) #竖直定位完成
    cropedImXbi = imXbi.crop((0, l, c - 1, h))
    cropedImXbi.show()
    m = int((l + h) / 2)
    lt, rt, fre = findHorRange(imXbi, m)
    outcome1 = (l, h, lt, rt, fre)
    ###########以下重复上面一段，对maxIndex2进行同样的操作
    l, h = t2.findVerRange(SmoothedWhitepointSumArr, maxIndex2, 0.5)#垂直定位函数（已找到其中一点的情况下）
    print "alternative low and high edge: " + str(((l, h)))
        
    l = int(l - (h - l) * 0.1)
    h = int(h + (h - l) * 0.1) #竖直定位完成
    #cropedImXbw = imXbw.crop((0, l, c - 1, h))
    #cropedImXbw.show()
    m = int((l + h) / 2)
    lt, rt, fre = findHorRange(imXbi, m)
    outcome2 = (l, h, lt, rt, fre)
    ########################################
#这里对outcome的选取考虑两个因素：fre和hsv蓝白比例。私以为第二个更重要
    outcome1 = expandPlateScope(outcome1, 0.4)
    outcome2 = expandPlateScope(outcome2, 0.4)
    plateIm1 = im.crop((outcome1[2], outcome1[0], outcome1[3], outcome1[1]))
    plateIm2 = im.crop((outcome2[2], outcome2[0], outcome2[3], outcome2[1]))
    
    h1, s1, v1 = myhsv.RGBtoHSV(plateIm1)
    h2, s2, v2 = myhsv.RGBtoHSV(plateIm2)
    
#蓝色车牌
#H值范围：190 ~ 245
#S值范围： 0.35 ~ 1
#V值范围： 0.3 ~ 1
    

    
    ratio1 = calculateBlueRatio(h1, s1, v1)
    ratio2 = calculateBlueRatio(h2, s2, v2)
    print ratio1, ratio2
    

    
    
#    if outcome1[4] > outcome2[4]:
#        outcome = outcome1
#    else:
#        outcome = outcome2
    
#    print outcome#(l, h, lt, rt, fre) vs (lt, l, rt, h)
    #cropedImFinal = im.crop((outcome[2], outcome[0], outcome[3], outcome[1]))
    #cropedImFinal.show()
    #车牌已定位，暂时跳过倾斜校正
    
    
   
#    plateIm = im.crop((outcome[2], outcome[0], outcome[3], outcome[1]))
#    plateImbw = plateIm.convert('L')
#    plateImbw.show()
#    plateImbi = t2.binaryzation(plateImbw, 220)
#    plateImbi.show()
    
#    os.makedirs("cars/" + name)#把车牌号存起来待用
#    plateImbi.save("cars/" + name + '/'+ name + ".bmp")
#    plateImbi.save("cars/" + name + '/'+ name + "bi.bmp")
#    plateIm.save("cars/" + name + '/'+ name + "Origin.jpg")
#    plateImbw.save("cars/" + name + '/'+ name + "bw.jpg")
    
    print "DONE@"

def expandPlateScope(outcome, percent):
    l, h, lt, rt, fre = outcome
    le = int(l - (h - l) * percent)
    he = int(h + (h - l) * percent)
    lte = int(lt - (rt - lt) * percent)
    rte = int(rt + (rt - lt) * percent)  
    outcomeE = (le, he, lte, rte, fre)#进行0.2的扩张边缘，以防车牌缺角
    return outcomeE

def calculateBlueRatio(h, s, v):
    r = float(len(h))
    c = len(h[1])
    count = 0
    for i in zip(h, s, v):
        if (i[0] >= 190 and i[0] <= 245 \
            and i[1] >= 0.35 and i[1] <= 1
            and i[2] >= 0.3 and i[2] <=1):
            count = count + 1
    return count / (r * c)        
    
#runFindPlate("car7")
      