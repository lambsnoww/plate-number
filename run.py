#-*-coding:utf-8-*-
'''
Created on 2016年5月19日

@author: linxue
'''
import Image, ImageDraw, ImageOps
import mytools as t1
import mytools2 as t2
import mytools3 as t3
import mytoolshsv as mh
import mytools4plateOperation as t4
import thinner
import numpy as np
import os

def getChars():
    im = Image.open("Cars_small/42.jpg")
    im = t1.preprocess(im)#滤波+锐化+直方均衡化
    imOut = t3.runFindPlate(im)
    imOut.show()#正确
    #下面进行一次HSV检验
#    scopeIm = mh.findBlueareaFromIm(imOut)
    imBw = imOut.convert('L')

    imBi = t2.binaryzation(imBw, 100)#当时第二个参数太大了
#    imBi.show()

    t4.runGetCharacter(imBi)
    print "Finished@run.getChars"
    
    thinner.saveThinnedImage(7)
    
    deleteIm()
    
    
def deleteIm():
    for i in range(7):
        filename = "%d.jpg"%(i+1)
        if os.path.exists(filename):
            os.remove(filename)
        filename = "%d.bmp"%(i+1)
        if os.path.exists(filename):
            os.remove(filename)
    filename = "plateBi.bmp"
    if os.path.exists(filename):
        os.remove(filename)

    

if __name__ == '__main__':
    getChars()
