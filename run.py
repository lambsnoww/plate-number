#-*-coding:utf-8-*-
'''
Created on 2016年5月19日

@author: linxue
'''
import Image, ImageDraw, ImageOps
import mytools, mytools2, mytools3
import mytoolshsv as mh
import mytools4plateOperation as t4

def getChars():
    im = Image.open("Cars_small/1.jpg")
#    im = im.resize((326* 2, 244 * 2))
    #未通过:678(白牌)2，3(颜色不蓝)244，28(长宽比；建议如果两个ratio都超过70则比其它的比如fre)
    #11，12，17，22，36，37，40，44，45，48(没进入前三，待解决)
    #13，14，21(不全)24，31(报错)27(有两个车牌)
    #47(选错)
#    im = mytools.preprocess(im)#滤波+锐化+直方均衡化
    imOut = mytools3.runFindPlate(im)
#    imOut.show()
    #下面进行一次HSV检验
    scopeIm = mh.findBlueareaFromIm(imOut)
    
    print "Finished@run.getChars"

if __name__ == '__main__':
    getChars()
