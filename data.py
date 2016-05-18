#-*-coding:utf-8-*-
'''
Created on 2016年5月18日

@author: linxue
'''
import thinner
import Image, ImageDraw, ImageOps
import numpy as np
import mytools as t1
import mytools2 as t2
import matlab
import matlab.engine

noCircleChars = ['1', '2', '3', '5', '7', 'C', 'E', \
    'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'S', \
    'T', 'U', 'V', 'W', 'X', 'Y', 'Z']#23个
oneCircleChars = ['0', '4', '6', '9', 'A', 'D', \
                  'P', 'Q', 'R']#9个
twoCircleChars = ['8', 'B']#2个

def getTrainingData(chars):
    l = len(chars) * 50
    train = [[0 for i in range(16)] for j in range(l)]
    for char in chars:
        for i in range(50):
            imstr = 'CharSamples/%c/%d'%(char, i + 1)
            im = Image.open(imstr + ".png")
            imbw = t2.binaryzationpng(im, 200)
            imbwrz = imbw.resize((20, 22))
            imbwrz.save(imstr + "rz.jpg")
            
            eng = matlab.engine.start_matlab()
            thinner.thin(eng, imstr + "rz", 'jpg')
            imthin = Image.open(imstr + "rz.jpg")
            imthin.show()

getTrainingData(noCircleChars)
    