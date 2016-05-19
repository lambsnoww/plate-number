#-*-coding:utf-8-*-
'''
Created on 2016年5月19日

@author: linxue
'''
import numpy as np
import Image, ImageDraw, ImageOps, colorsys
from ensurepip import __main__

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
            max = findMaxArr(a)
            if max == -1:
                h[i][j] = 0
            elif max == 0 and g >= b:
                h[i][j] = 60 * (g - b) / (a[max] - min(a))
            elif max == 0 and g < b:
                h[i][j] = 60 * (g - b) / (a[max] - min(a)) + 360
            elif max == 1:
                h[i][j] = 60 * (b - r) / (a[max] - min(a)) + 120
            elif max == 2:
                h[i][j] = 60 * (r - g) / (a[max] - min(a)) + 240
            
            if max(a) == 0:
                s[i][j] = 0
            else:
                s[i][j] = 1 - min(a) / max(a)
            
            v[i][j] = max(a)
            
    return (h, s, v)
       

def findMaxArr(arr):
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


            

if __name__ == "__main__":
    
    im = Image.open("CarPhotos/1.jpg")
    arr = np.array(im)
    imout = HSVColor(im)
    imout.show()
#    print len(arr), len(arr[0]), len(arr[0][0])