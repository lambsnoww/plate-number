#-*-coding:utf-8-*-
'''
Created on 2016年5月19日

@author: linxue
'''
import numpy as np
import Image, ImageDraw, ImageOps, colorsys
from ensurepip import __main__
import mytools2 as t2

def RGBtoHSV(im):
    arr = np.array(im)
    row = len(arr)
    col = len(arr[0])
    h = [[0 for i in range(col)] for j in range(row)]
    s = [[0 for i in range(col)] for j in range(row)]
    v = [[0 for i in range(col)] for j in range(row)]
    
    for i in range(row):
        for j in range(col):
            a = [elem / 255. for elem in arr[i][j]]
            r, g, b = a
            maxIndex = findmaxArr(a)
            if maxIndex == -1:
                h[i][j] = 0
            elif maxIndex == 0 and g >= b:
                h[i][j] = 60 * (g - b) / (a[maxIndex] - min(a))
            elif maxIndex == 0 and g < b:
                h[i][j] = 60 * (g - b) / (a[maxIndex] - min(a)) + 360
            elif maxIndex == 1:
                h[i][j] = 60 * (b - r) / (a[maxIndex] - min(a)) + 120
            elif maxIndex == 2:
                h[i][j] = 60 * (r - g) / (a[maxIndex] - min(a)) + 240
            
            if max(a) == 0:
                s[i][j] = 0
            else:
                s[i][j] = 1 - min(a) / max(a)
            
            v[i][j] = max(a)
            
    return (h, s, v)
       

def findmaxArr(arr):
    if arr[0] == arr[1] and arr[1] == arr[2]:
        return -1
    if arr[0] > arr[1]:
        if arr[0] > arr[2]:
            return 0
        else:
            return 2
    elif arr[1] < arr[2]:
        return 2
    else:
        return 1

#蓝色车牌
#H值范围：190 ~ 245
#S值范围： 0.35 ~ 1
#V值范围： 0.3 ~ 1
def findBlueareaFromIm(im):
    h, s, v = RGBtoHSV(im)
    r = len(h)
    c = len(h[0])
    arr = [[0 for i in range(c)] for j in range(r)]
    for i in range(r):
        for j in range(c):
            if h[i][j] >= 190 and h[i][j] <= 245:
                arr[i][j] = 255
            else:
                arr[i][j] = 0
    scopeIm = t2.getBiIm(arr)
    scopeIm.show()
    return scopeIm
            

if __name__ == "__main__":
    
    im = Image.open("CarPhotos/1.jpg")
    arr = np.array(im)
    h, s, v = RGBtoHSV(im)
    print h
    print s
    print v
#    print len(arr), len(arr[0]), len(arr[0][0])