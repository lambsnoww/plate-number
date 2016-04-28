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
from itertools import count
from _Res import Count1Resources


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

def findHorRange(im, ind):
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

            if flag == False:
#                print "first enter" + str(i)
                count = 1
                flag = True
                startIndex = i
                endIndex = i
                continue
            elif flag == True:
#                print "second enter" + str(i)
                if (i - endIndex) <= interval:
                    endIndex = i
                    if i > 0:
                        if imArr[ind][i - 1] == 0:
                            count = count + 1
                    continue
                elif (i - endIndex) > interval:
#                    print "first come out" + str(i)
                    item = [startIndex, endIndex, count]
                    findList.append(item)
                    flag = True
                    count = 1
                    startIndex = i
                    endIndex = i
                    
                    continue
        else:
            if i == c - 1 and  (i - endIndex) > interval:
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
    image.show()
    return image

def getConnectedSetInfo(im):#对一个二值图像，找连通集，并进行逐点标记
    arr = np.array(im)
#    print arr
    r = len(arr)
    c = len(arr[0])
    brr = [[0 for i in range(c)] for j in range(r)]
    count = 0
    for i in range(r):
        for j in range(c):
            if arr[i][j] > 0 and brr[i][j] == 0:
                count = count + 1
                markConnectedSet(arr, brr, i, j, count)
                print "count = "+ str(count)
            else:
                continue
    return (brr, count)
                
def markConnectedSet(arr, brr, i, j, count):#递归地标记连通集????这里的递归太深了，不能用，换别的方法
#    print (i, j),
    r = len(arr)
    c = len(arr[0])
    if arr[i][j] == 0:
        return
    elif brr[i][j] > 0:
        return
    brr[i][j] = count#其它情况即有图像，而并未mark标记的点，进行一个递归的mark
    if i - 1 > 0:
        if j - 1 >= 0:
            markConnectedSet(arr, brr, i - 1, j - 1, count)
        if j + 1 < c:
            markConnectedSet(arr, brr, i, j + 1, count)
        markConnectedSet(arr, brr, i - 1, j, count)
    if j - 1 >= 0:
        markConnectedSet(arr, brr, i, j - 1, count)
    if j + 1 < c:
        markConnectedSet(arr, brr, i, j + 1, count)
    if i + 1 < r:
        if j - 1 >= 0:
            markConnectedSet(arr, brr, i + 1, j - 1, count)
        if j + 1 < c:
            markConnectedSet(arr, brr, i, j + 1, count)
        markConnectedSet(arr, brr, i + 1, j, count)
    return

def getConnectedSetInfo2(im):
  
    im = ImageOps.expand(im, 2, 0)#这里expand了2个像素，为什么是两个呢？一会儿你就知道了
    arr = np.array(im)
    print "print expanded arr: "
    printArr(arr)
    r = len(arr)
    c = len(arr[0])
    for i in range(r):
        for j in range(c):
            if arr[i][j] == 255:
                for s in range(-1, 2):
                    for t in range(-1, 2):
                        if arr[i + s][j + t] == 0:
                            arr[i + s][j + t] = 100#arr这个由图像得来的数组居然存不了-1！-1当作255存了
#                            printArr(arr)
#                            print "  *" * 50,
#                            print " **" * 50,
#                            print "***" * 50,
#                            print "  *" * 50,
#                            print " **" * 50,
#                            print "***" * 50
    brr = [[0 for i in range(c)] for j in range(r)]
    count = 0
    for i in range(r):
        for j in range(c):
            if arr[i][j] == 100 and arr[i + 1][j] == 255:
                count = count + 1
                while(True):
                    brr[i + 1][j] = count
                    

def printArr(arr):
    r = len(arr)
    c = len(arr[0])
    for i in range(r):
        for j in range(c):
            print "%3d" % arr[i][j],
        print
                

im = Image.open("car8.jpg")#原图
imOrigin = Image.open("car8.jpg")
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
#plt.show()



                
                
                
                
                
                

maxIndex1, maxIndex2, max1, max2 = t2.findMaxCouple(SmoothedWhitepointSumArr, 0.2)
print "find max couple!"

l, h = t2.findVerRange(SmoothedWhitepointSumArr, maxIndex1, 0.5)#垂直定位函数（已找到其中一点的情况下）
print "alternative low and high edge: " + str(((l, h)))
    
l = int(l - (h - l) * 0.1)
h = int(h + (h - l) * 0.1) #竖直定位完成
#cropedImXbw = imXbw.crop((0, l, c - 1, h))
#cropedImXbw.show()
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
if outcome1[4] > outcome2[4]:
    outcome = outcome1
else:
    outcome = outcome2

print outcome#(l, h, lt, rt, fre) vs (lt, l, rt, h)
#cropedImFinal = im.crop((outcome[2], outcome[0], outcome[3], outcome[1]))
#cropedImFinal.show()
#车牌已定位，下面进行倾斜校正


l, h, lt, rt, fre = outcome
le = int(l - (h - l) * 0.4)
he = int(h + (h - l) * 0.4)
lte = int(lt - (rt - lt) * 0.4)
rte = int(rt + (rt - lt) * 0.4)



outcomeE = (le, he, lte, rte)#进行0.2的扩张边缘，以防车牌缺角
cropedImFinal = im.crop((outcomeE[2], outcomeE[0], outcomeE[3], outcomeE[1]))
#imForAdj.show()
#imForAdj = im.crop((outcome[2], outcome[0], outcome[3], outcome[1]))
#imForAdj = t2.binaryzation(imForAdj, 120)#二值化
###################倾斜校正开始



#每次膨胀后，删除面积小于阀值的连通集（作为噪声）——这个思路先放放

#while True:
#    imForAdj = expand(imForAdj, 1, 0)
#    brr, count = getConnectedSetInfo(imForAdj)
#        deleteNoise(imForAdj)
#    for i in range(len(brr)):
#            for j in range(len(brr[0])):
#                print brr[i][j],
#            print
#    break
    

#imForAdj = expand(imForAdj, 1, 0)
#imForAdj.show()
bor = int((rt - lt) * 0.4)
im = cropedImFinal
im = im.convert('L')
#im = t2.findEdge(im)[2]#xy方向的变化都加入
im = t2.binaryzation(im, 120)
im = expand(im, 0, 2)
#brr, count = getConnectedSetInfo(im)
#for i in range(len(brr)):
#    for j in range(len(brr[0])):
#        print "%4d" % brr[i][j],
#   print
#print "How many connected set? " + str(count)

im = expand(im, 1, 3)

brr, count = getConnectedSetInfo2(im)

print "2*How many connected set? " + str(count)

######################################################
#如果找出来的“车牌”比例不对，我们有理由相信，之前的二选一，选错了，回去选另一个
#scaleTmp = float(h - l) / (rt - lt)
#scale = ((440.0/140) * 0.8, (440.0/140) * 1.2)
#if (scaleTmp > scale[1] or scaleTmp < scale[0]):
#    if plateIndex == maxIndex1:
#        plateIndex = maxIndex2
#    else:
#        plateIndex = maxIndex1
######################以下为重复代码：
#l, h = t2.findVerRange(SmoothedWhitepointSumArr, plateIndex, 0.5)#垂直定位函数（已找到其中一点的情况下）
#print l, h
    
#l = int(l - (h - l) * 0.1)
#h = int(h + (h - l) * 0.1) #竖直定位完成
#cropedImXbw = imXbw.crop((0, l, c - 1, h))
#cropedImXbw.show()
#m = int((l + h) / 2)
#lt, rt, fre = findHorRange(imXbi, m)
###########################################
















print "DONE@"
