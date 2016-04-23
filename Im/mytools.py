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

#锥形滤波 & 拉普拉斯锐化 & 直方图均衡化

def userFilter(im, mode):#锥形滤波+拉普拉斯锐化
    tm = np.array([(1,2,1),(2,4,2),(1,2,1)],float)
    tm2 = np.array([(0,-1,0),(-1,5,-1),(0,-1,0)],float)
    
    tm = tm / 16
    draw = ImageDraw.Draw(im)
    source = im.split()
    pointColor = [0,0,0]
    for i in range(0, list(im.size)[0]):
        for j in range(0, list(im.size)[1]):
            if (i >= 1) and (j >= 1) and (i+2 <= list(im.size)[0]) and (j+2 <= list(im.size)[1]):
                for t in range(0,3):
                    imarray = np.array([(source[t].getpixel((i-1,j-1)),\
                                       source[t].getpixel((i-1,j)),\
                                       source[t].getpixel((i-1,j+1))),\
                                      (source[t].getpixel((i,j-1)),\
                                       source[t].getpixel((i,j)),\
                                       source[t].getpixel((i,j+1))),\
                                      (source[t].getpixel((i+1,j-1)),\
                                       source[t].getpixel((i+1,j)),\
                                       source[t].getpixel((i+1,j+1)))],float)
#                    print imarray
                    if mode == "filter":
                        pointColor[t] = arraySum(imarray * tm)
                    else:
                        if mode == "sharpen":
                            pointColor[t] = arraySum(imarray * tm2)
                    
                point = [i,j]
#               print (pointColor[0], pointColor[1], pointColor[2])
#                print t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t
#                print pointColor[t], source[t].getpixel((i,j))
                draw.point(point, (pointColor[0], pointColor[1], pointColor[2]))
            elif (i+2) == list(im.size)[0] and (j+2) == list(im.size)[1]:
                break
            else:
                continue
    del draw
    return im
                    
def arraySum(arr):
    sum = 0.0
    for i in range(0,len(arr)):
        for j in range(0,len(arr[0])):
            sum += arr[i][j]
            
    return int(sum)
                    
def hist(im):#直方图均衡化
    arr0 = [0.0] * 256
    arr1 = [0.0] * 256
    arr2 = [0.0] * 256

    source = im.split()
    draw = ImageDraw.Draw(im)
    for i in range(0, list(im.size)[0]):
        for j in range(0, list(im.size)[1]):
            iGray = source[0].getpixel((i,j))
            arr0[iGray] = arr0[iGray] + 1
            iGray = source[1].getpixel((i,j))
            arr1[iGray] = arr2[iGray] + 1
            iGray = source[2].getpixel((i,j))
            arr2[iGray] = arr2[iGray] + 1
                

    for i in range(1, 256):
        arr0[i]  = arr0[i] + arr0[i - 1]
        arr1[i]  = arr1[i] + arr1[i - 1]
        arr2[i]  = arr2[i] + arr2[i - 1]
            
                
    for i in range(0, list(im.size)[0]):
        for j in range(0, list(im.size)[1]):
            point = [i,j]
            r = source[0].getpixel((i,j))
            g = source[1].getpixel((i,j))
            b = source[2].getpixel((i,j))
            draw.point(point, ((int)(arr0[r]/arr0[255]*255), \
                               (int)(arr1[g]/arr1[255]*255), \
                               (int)(arr2[b]/arr2[255]*255)))
    del draw
    return im
    

    
    
