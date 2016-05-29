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
import mytools3 as t3
from itertools import count
from _Res import Count1Resources
import Queue
from __builtin__ import False
import collections
import matlab
import matlab.engine



def getSetInfo(arr):
    l = len(arr)
    flag = False
    start = end = 0
    setDist = 0
#    myqueue = Queue.Queue(-1)
    myqueue = collections.deque()
    for i in range(l):
        if flag == False and arr[i] > 0:
            flag = True
            setDist = i - end - 1
            start = end = i
        elif flag == True and arr[i] > 0:
            end = i
        elif flag == True and arr[i] == 0:
            flag = False
            myqueue.append((start, end, setDist))
    if arr[l - 1] > 0:
        myqueue.append((start, end, setDist))
    return myqueue

#def charDivide(im, queue):
#    arr = np.array(im)
#    diviedeQueue = Queue.Queue(-1)#容量为7
#    for i in range():
        
def runGetCharacter(plateImbi):
#    plateImbi = Image.open("cars/" + name + "/" + name + ".bmp")        
#    plateImbw = Image.open("cars/" + name + "/" + name + "bw.jpg")        
#    plateImOrigin = Image.open("cars/" + name + "/" + name + "Origin.jpg")        
    arr = np.array(plateImbi)
    t3.printArr(arr)
    plateRow = len(arr)
    plateCol = len(arr[0])
    plateColTheory = int(float(plateRow) * 440 / 90)
    #print arr
    plateEdge =  t3.findPlateEdge(plateImbi)
    print "plate Edge : ",
    print plateEdge
    r = list(plateImbi.size)[1]
    c = list(plateImbi.size)[0]
    flag = False
    s = e = 0
    for i in range(r):
        if plateEdge[i] >= 9 and flag == False:
            s = i
            e = i
            flag = True
        elif plateEdge[i] < 9 and flag == True:
            e = i - 1
            break
    print "the scope of the characters is: "
    print (s, e)
    #水平下刀切割
    plateImbiCroped = plateImbi.crop((0, s, list(plateImbi.size)[0], e + 1))
#    plateImbwCroped = plateImbw.crop((0, s, list(plateImbw.size)[0], e + 1))
#    plateImCroped = plateImOrigin.crop((0, s, list(plateImbw.size)[0], e + 1))
    
#    plateImbiCroped.show()#经过水平切割后的车牌，下面进行垂直切割
    plateImbiCroped.save("plateBi.bmp")
    r = list(plateImbiCroped.size)[1]
    c = list(plateImbiCroped.size)[0]
    
    
    verlen = e - s#车牌竖直长度
    charArr = t3.getWhitepointSumArr(plateImbiCroped, 'c')
#    t3.drawWaveByRow(charArr, 100)#这里的代码有问题，被0除
    setInfo = getSetInfo(charArr)
    print "set count: " + str(len(setInfo))
    
    for elem in setInfo:
        start, end, setDist = elem
        print (start, end, setDist),
    
    widestInterval = float(verlen) * 34 / 90#最长的字符间隔的像素值（理论值）
    print widestInterval#为了去除那个圆点（以及其它单独噪声），最小宽度 < 阈值1 and totalCount < 阈值2，后面再做
    
    
    lower = int(widestInterval * (1 - 0.2))
    higher = int(widestInterval * (1 + 0.2))
    print [lower, widestInterval, higher]
    
    bimyqueueForCharacter = collections.deque()
#    bwmyqueueForCharacter = collections.deque()
#    ormyqueueForCharacter = collections.deque()
#    lastElem = setInfo.__getitem__(0)
  
    for elem in setInfo:
        s, e, dis = elem
        imbi = plateImbiCroped.crop((s, 0, e + 1, r))#注意crop是不包含结尾的
#        imbw = plateImbwCroped.crop((s, 0, e + 1, r))#注意crop是不包含结尾的
#        im = plateImCroped.crop((s, 0, e + 1, r))#注意crop是不包含结尾的
        bimyqueueForCharacter.append(imbi)
#        bwmyqueueForCharacter.append(imbw)
#        ormyqueueForCharacter.append(im)

    while len(bimyqueueForCharacter) > 7:
        ind = findImWithMinWidth(bimyqueueForCharacter)
        popInd(bimyqueueForCharacter, ind)

#    os.mkdir("cars/" + name + '/bi')
#    os.mkdir("cars/" + name + '/bw')
#    os.mkdir("cars/" + name + '/origin')
#    print "*****" + str(len(bimyqueueForCharacter))
#    i = 0
#    for elem in bimyqueueForCharacter:
#        i = i + 1
#        elem.save("cars/" + name + "/bi/" + str(i) + ".bmp")
#    i = 0
#    for elem in bwmyqueueForCharacter:
#        i = i + 1
#        elem.save("cars/" + name + "/bw/" + str(i) + ".jpg")
#    i = 0
#    for elem in ormyqueueForCharacter:
#        i = i + 1
#        elem.save("cars/" + name + "/origin/" + str(i) + ".jpg")
    i = 1
    for elem in bimyqueueForCharacter:
#        imtmp = elem.resize((20, 22))
        imtmp = t2.binaryzation(elem, 180)
        imtmp.save(str(i) + ".bmp")
        i = i + 1

def findImWithMinWidth(dq):
    minWidth = 300
    for i in range(dq.__len__()):
        im = dq.popleft()
#        arr = np.array(im)
#        t3.printArr(arr)
        dq.append(im)
#        print "minWidthNow = %d, cols = %d; "%(minWidth, list(im.size)[1])
        if minWidth > list(im.size)[0]:#im.size先列后行，注意了
            minWidth = list(im.size)[0]
            minIndex = i
    print "minIndex = %d, minWidth = %d; "%(minIndex,minWidth)
    return minIndex

def popInd(dq, ind):
    for i in range(dq.__len__()):
        im = dq.popleft()
        if i == ind:
            continue
        else:
            dq.append(im)
                   

