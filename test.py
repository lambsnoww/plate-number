#-*-coding:utf-8-*-

'''
Created on 2016年4月28日

@author: linxue
'''
import Image, ImageDraw
import numpy as np
#说明图片打开之后，并不是按引用传递，改一下就全改了的！

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
                    
def getConnectedSetInfo3(im):#queue实现有误
    im = ImageOps.expand(im, 1, 0)
    arr = np.array(im)
    r = len(arr)
    c = len(arr[0])
    brr = [[0 for i in range(c)] for j in range(r)]
    count = 0
    myqueue = Queue.LifoQueue(maxsize = -1)
    for i in range(r):
        for j in range(c):
            if arr[i][j] > 0 and brr[i][j] ==  0:
                count = count + 1
                brr[i][j] = count
                myqueue.put((i, j))
                while(myqueue.not_empty):
                    p, q = myqueue.get()
                    if arr[p][q - 1] > 0 and brr[p][q - 1] == 0:
                        brr[p][q - 1] = count
                        myqueue.put((p, q - 1))
                    if arr[p + 1][q] > 0 and brr[p + 1][q] == 0:
                        brr[p + 1][q] = count
                        myqueue.put((p + 1, q))
                    if arr[p][q + 1] > 0 and brr[p][q + 1] == 0:
                        brr[p][q + 1] = count
                        myqueue.put((p, q + 1))
                    if arr[p - 1][q] > 0 and brr[p - 1][q] == 0:
                        brr[p - 1][q] = count
                        myqueue.put((p - 1, q))
    printArr(brr)
    return (brr, count)