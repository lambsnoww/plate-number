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
from itertools import count
from _Res import Count1Resources
import Queue
from __builtin__ import False
import refa as rf
import collections

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
        
        
       

plateImbi = Image.open("car4.bmp")
arr = np.array(plateImbi)
#print arr
plateEdge =  rf.findPlateEdge(plateImbi)

r = list(plateImbi.size)[1]
c = list(plateImbi.size)[0]
flag = False
for i in range(r):
    if plateEdge[i] >= 7 and flag == False:
        s = i
        e = i
        flag = True
    elif plateEdge[i] < 7 and flag == True:
        e = i - 1
        break
print "the scope of the characters is: "
print (s, e)
plateImbiCroped = plateImbi.crop((0, s, list(plateImbi.size)[0], e + 1))
plateImbiCroped.show()#经过水平切割后的车牌，下面进行垂直切割
r = list(plateImbiCroped.size)[1]
c = list(plateImbiCroped.size)[0]


verlen = e - s#车牌竖直长度
charArr = rf.getWhitepointSumArr(plateImbiCroped, 'c')
rf.drawWaveByRow(charArr, 100)
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

myqueueForCharacter = collections.deque()
lastElem = setInfo.__getitem__(0)

  
        
        

for elem in setInfo:
    s, e, dis = elem
    im = plateImbiCroped.crop((s, 0, e + 1, r))#注意crop是不包含结尾的
    myqueueForCharacter.append(im)
if len(myqueueForCharacter) > 7:
    myqueueForCharacter.pop()
if len(myqueueForCharacter) > 7:
    myqueueForCharacter.popleft()
    
#maxInterval = 0
#for i in range(len(setInfo)):
#    if i == 0 or i == len(setInfo) - 1:
#        continue
#    if elem[2] > maxInterval:
#        maxInterval = elem[2]

#if len(myqueueForCharacter) > 7 and maxInterval < lower:
#    for i in range(len(myqueueForCharacter)):
#        elem = myqueueForCharacter.popleft()
#        if i == 2:
#            continue
#        else:
#            myqueueForCharacter.append(elem)#去掉中间那个点
    
print "*****" + str(len(myqueueForCharacter))
for elem in myqueueForCharacter:
    elem.show()




    

