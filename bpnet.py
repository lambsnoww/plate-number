#-*-coding:utf-8-*-
'''
Created on 2016年5月17日
建立BP网络，并进行分类

@author: linxue
'''
import sys, os
import Image, ImageDraw, ImageOps
import numpy as np
import colorsys
import matplotlib.pyplot as plt
import mytools as t1
import mytools2 as t2
from itertools import count
from _Res import Count1Resources
from __builtin__ import False
import refa as rf
import collections
import matlab
import matlab.engine
import thinner
from pybrain.structure import FeedForwardNetwork
from pybrain.structure import LinearLayer, SigmoidLayer
from pybrain.structure import FullConnection
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers.backprop import BackpropTrainer

if __name__ == "__main__":
    fnn = buildNetwork(16, 21, 23, bias = True)
    fnn.activate([1 for i in range(16)])
    ds = SupervisedDataSet(16, 23)
    for i in range(len(train)):
        ds.addSample(train[i], label[i])
    #trainer = BackpropTrainer(fnn, ds, momentum = 0.1, verbose = True, weightdecay = 0.01)
    trainer = BackpropTrainer(fnn, ds)
    print "start the training..."
    #trainer.trainEpochs(epochs = 500)#利用低度下降法训练500次
    trainer.trainUntilConvergence()
    
    print "start returning the result"
    print fnn.activate((x1, x2, x3, x4, x5, x6, x7, x8, x9,\
                        x10, x11, x12, x13, x14, x15, x16))#进行预测
    
    






