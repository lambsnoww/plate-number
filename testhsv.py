#-*-coding:utf-8-*-
'''
Created on 2016年5月19日

@author: linxue
'''

import Image, ImageDraw, ImageOps
import mytoolshsv as mh

def printa(a):
    r = len(a)
    c = len(a[0])
    for i in range(r):
        for j in range(c):
            print a[i][j],
        print
        
if __name__ == '__main__':
    im = Image.open("cat.jpg")
    im.show()
    h, s, v = mh.RGBtoHSV(im)
    a = 171
    b = 183
    print (h[a][b],s[a][b], v[a][b])#已试验两个，符合，网址：http://www.csgnetwork.com/csgcolorsel4.html

