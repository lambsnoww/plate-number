#-*-coding:utf-8-*-
'''
Created on 2016年5月1日

@author: linxue
'''
import sys, os
import Image, ImageDraw, ImageOps
import numpy
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
import plateOperation as po
import plateOperation as po
import scipy
from pybrain.structure import FeedForwardNetwork
from pybrain.structure import LinearLayer, SigmoidLayer 
from sklearn import datasets, linear_model
from pybrain.structure import RecurrentNetwork
from pybrain.structure import FullConnection
import matlab
import matlab.engine
import time


def run():
    name = "car7" 
    
    rf.runFindPlate(name)
    imQueue = po.runGetCharacter(name)
    
    imQueue2 = Queue.Queue(-1)
    for elem in imQueue:
        im = elem.resize((32, 64))#调整字符尺寸
        im.show()
        imQueue2.put(im)

def ffn():  
    n = FeedForwardNetwork()
    inLayer = LinearLayer(2)
    hiddenLayer = SigmoidLayer(3)
    outLayer = LinearLayer(1)
    
    n.addInputModule(inLayer)
    n.addModule(hiddenLayer)
    n.addOutputModule(outLayer)
    
    in_to_hidden = FullConnection(inLayer, hiddenLayer)
    hidden_to_out = FullConnection(hiddenLayer, outLayer)
    
    n.addConnection(in_to_hidden)
    n.addConnection(hidden_to_out)
    
    n.sortModules()
    

    #print "activate"
    n.activate([1,2])#必须要print才打印
    print n
    #print in_to_hidden.params

    
    
    
    
    
        
#ffn()

        
        