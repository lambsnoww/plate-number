#-*-coding:utf-8-*-
'''
Created on 2016年5月16日
细化字符，提取特征

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

def thin(eng, name):#调用matlab的bwmorph对图像进行细化 and 保存为jpg格式
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

def getNumberOfVerticalLines(im):#返回有多少条竖直线，各有多长
#    im = Image.open(name + '.bmp')
    arr = np.array(im)
    r = len(arr)
    c = len(arr[0])
#    for i in range(r):
#        for j in range(c):
#            print arr[i][j],
#        print
    verThreshold = c * 4 / 7#12竖直方向假定有超过4/7长度便定义为有一条直线
    numOfLines = 0
    lines = [0 for i in range(3)]
    for i in range(c):
        count = 0
        for j in range(r):
            if arr[j][i] >= 200:
                count = count + 1
        if count >= verThreshold:
            numOfLines = numOfLines + 1
            if i >= 1 and i <= 4:
                lines[0] = count
            elif i >= 8 and i <= 12:
                lines[1] = count
            elif i >= 17 and i <= 22:
                lines[2] = count
    return (numOfLines, lines)

def getPointNumber(im):#返回（123叉点的个数数组， 3叉点的位置向量）
    imExpand = ImageOps.expand(im, 1, 0)
    arr = np.array(imExpand)
    r = len(arr)
    c = len(arr[0])
    count = [0 for i in range(4)]
    three = [(0, 0) for i in range(6)]
    for i in range(r):
        for j in range(c):
            if arr[i][j] > 200:
                count[0] = count[0] + 1
                neighbors = -1
                for l in range(-1, 2):
                    for k in range(-1, 2):
                        if arr[i + l][j + k] > 200:
                            neighbors = neighbors + 1
                count[neighbors] = count[neighbors] + 1
                if neighbors == 3:
                    three[count[3] - 1] = (i - 1, j - 1)#另忘了这里对图片expand了
    return (count, three)               

def getCircleNumber(count):#返回圆圈的个数
    e = (count[1] + 2 * count[2] + 3 * count[3]) / 2
    n = count[1] + count[2] + count[3]
    if e > n:
        return 2
    elif e == n:
        return 1
    elif e < n:
        return 0
    
def getNumberOfHorizontalLines(im):#返回多少条水平线，水平线各有多长
    arr = np.array(im)
    r = len(arr)
    c = len(arr[0])
    verThreshold = 11#水平方向假定有超过11长度便定义为有一条直线
    numOfLines = 0
    lines = [0 for i in range(3)]
    for i in range(r):
        count = 0
        for j in range(c):
            if arr[i][j] >= 200:
                count = count + 1
        if count >= verThreshold:
            numOfLines = numOfLines + 1
            if i >= 0 and i <= 3:
                lines[0] = count
            elif i >= 8 and i <= 12:
                lines[1] = count
            elif i >= 17 and i <= 22:
                lines[2] = count
    return (numOfLines, lines)

def getEdgePointsPosition(im):#返回左上、左下、右上、右下点的坐标
    arr = np.array(im)
    r = len(arr)
    c = len(arr[0])
    ret = [(0,0) for i in range(4)]
    for i in range(r):
        for j in range(c):
            if arr[i][j] > 200:
                ret[0] = (i, j)
                break
    for i in range(r):
        for j in range(c):
            if arr[r - 1 - i][j] > 200:
                ret[1] = (r - 1 - i, j)
                break
    for i in range(r):
        for j in range(c):
            if arr[i][c - 1 - j] > 200:
                ret[2] = (i, c - 1 - j)
                break
    for i in range(r):
        for j in range(c):
            if arr[r - 1 - i][c - 1 - j] > 200:
                ret[3] = (r - 1 - i, c - 1 - j)
                break
    return ret
    
    
if __name__ == "__main__":
    print "Initializing Matlab Engine"
    eng = matlab.engine.start_matlab()
    print "Initializing Complete!"
    name = 3
    thin(eng, name)
    im = Image.open(str(name) + ".jpg")
    verLines, lines = getNumberOfVerticalLines(im)
    print "vetical lines: " + str(verLines)
    print "vertical lines length: " + str(lines[0]),
    str(lines[1]), str(lines[2])
    horLines, lines = getNumberOfHorizontalLines(im)
    print "horizontal lines: " + str(horLines)
    print "horizontal lines length: " + str(lines[0]),
    str(lines[1]), str(lines[2])
    
    countList, threePos = getPointNumber(im)
    print "the num of points :",
    print countList[1], countList[2], countList[3]
    print "the three point pos: " + str(threePos)
    print "the circleNumber: ",
    print getCircleNumber(countList)
    print "the edge points position: ",
    print getEdgePointsPosition(im)


    
    
    