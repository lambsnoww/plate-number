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
    sampleSize = 1000
    train = [[0 for i in range(15)] for j in range(sampleSize)]
    label = [0 for i in range(sampleSize)]
    predictInput = [0 for i in range(15)]
    fnn = buildNetwork(16, 4, 1, bias = True)
    fnn.activate([1 for i in range(16)])
    ds = SupervisedDataSet(16, 1)
    for i in range(len(train)):
        ds.addSample(train[i], label[i])
        
    trainer = BackpropTrainer(fnn, ds)
    print "start the training..."
    trainer.trainUntilConvergence()
    
    print "start returning the result"
    print fnn.activate(predictInput)#进行预测
    
    






