#-*-coding:utf-8-*-
'''
Created on 2016年5月19日

@author: linxue
'''
import Image, ImageDraw, ImageOps
import mytools, mytools2, mytools3
import mytoolshsv as mh

def getChars():
    im = Image.open("CarPhotos/246.jpg")#未通过:3,678(白牌)2(颜色不蓝)
#    im = mytools.preprocess(im)#滤波+锐化+直方均衡化
    imOut = mytools3.runFindPlate(im)
    imOut.show()
    #下面进行一次HSV检验
    scopeIm = mh.findBlueareaFromIm(imOut)
    print "tt"

getChars()