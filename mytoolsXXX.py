#-*-coding:utf-8-*-
'''
Created on 2016年5月23日
膨胀与腐蚀，目的是定位车牌、消除噪声，并对三个候选车牌进行筛选

@author: linxue
'''
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
import Image, ImageDraw, ImageOps
import mytools as t1
import mytools2 as t2
import mytools3 as t3


def expand(im):

    im.show()
    arr = np.array(im)
    r = len(arr)
    c = len(arr[0])
    brr = [[0 for i in range(c)] for j in range(r)]
    for i in range(r):
        for j in range(c):
            if arr[i][j] > 0:
                brr[i][j] = 1
            else:
                brr[i][j] = 0
    open_arr = ndimage.binary_opening(brr)
#    print len(open_arr)
#    print len(open_arr[0])
#    print len(open_arr[0][0])
#    arr2 = [[0 for i in range(c)] for j in range(r)]
#    for i in range(r):
#        for j in range(c):
#            arr2[i][j] = open_arr[i][j][0]
    imOpen = t2.getBiIm(arr2)
    imOpen.show()
    eroded_arr = ndimage.binary_erosion(open_arr)
    arr2 = [[0 for i in range(r)] for j in range(c)]
    for i in range(r):
        for j in range(c):
            print eroded_arr[i][j]
            arr2[i][j] = eroded_arr[i][j][0]
    imEroded = t2.getBiIm(arr2)
    imEroded.show()
    
if __name__ == '__main__':
    im = Image.open("CarPhotos/4.jpg")
    im = t3.runFindPlate(im)
    imBw = im.convert('L')
    imBi = t2.binaryzation(imBw, 160)
    imBi.save("BiArea/1.bmp")
    imBi.show()    
    expand(im)
    