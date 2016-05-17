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

n = FeedForwardNetwork()
inLayer = LinearLayer(16, name = 'Input')
hiddenLayer = SigmoidLayer(4, name = 'Hidden')#5-14都试下
outLayer = LinearLayer(1, name = 'Output')

n.addInputModule(inLayer)
n.addModule(hiddenLayer)
n.addOutputModule(outLayer)

in_to_hidden = FullConnection(inLayer, hiddenLayer)
hidden_to_out = FullConnection(hiddenLayer, outLayer)
n.addConnection(in_to_hidden)
n.addConnection(hidden_to_out)

n.sortModules()

print n

print n.activate([1 for i in range(16)])

print in_to_hidden.params
print hidden_to_out.params
print n.params


