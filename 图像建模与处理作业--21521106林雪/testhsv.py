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

def binaryzation(im, n):
    source = im.split()
    cols = list(im.size)[0]
    rows = list(im.size)[1]
    newIm = Image.new('1', (cols, rows))
    draw = ImageDraw.Draw(newIm)
    a = 0
    for i in range(0, rows):
        for j in range(0, cols):
            a = source[0].getpixel((j, i))
            if a > n:
                a = 1
            else:
                a = 0
            draw.point([j, i], a)
    del draw
    return newIm
    
if __name__ == '__main__':
    im = Image.open("cat.jpg")
    im.show()
    imBw = im.convert('L')
    imBw.show()
    imBi = binaryzation(imBw, 200)
    imBi.show()
#    h, s, v = mh.RGBtoHSV(im)
#    a = 171
#    b = 183
#    print (h[a][b],s[a][b], v[a][b])#已试验两个，符合，网址：http://www.csgnetwork.com/csgcolorsel4.html

