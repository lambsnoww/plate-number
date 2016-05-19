#-*-coding:utf-8-*-
'''
Created on 2016年5月19日

@author: linxue
'''
import Image, ImageDraw, ImageOps
import mytools, mytools2, mytools3

def getChars():
    im = Image.open("CarPhotos/1.jpg")
#    im = mytools.preprocess(im)#滤波+锐化+直方均衡化
    mytools3.runFindPlate(im)
    print "tt"

getChars()