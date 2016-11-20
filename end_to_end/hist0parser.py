from PIL import Image
from scipy import signal, ndimage
import json
import numpy as np
import matplotlib.pyplot as plt
import sys, math
import timeit
#import peakutils

def get_smooth_hist(xlist, sigma, N=100):
    '''return normalized sigma-smoothed histogram of xlist'''
    x, X = min(xlist), max(xlist)
    step = float(X-x)/N
    gauss = np.arange(-sigma, +sigma, step)
    gauss = np.exp(-np.multiply(gauss, gauss) / (2*sigma))
    convo = np.convolve(xlist, gauss)
    convo = convo[len(gauss)//2:][:len(xlist)]
    convo /= np.sum(convo)
    return convo

def peak_cwt(mylist, w, size):
    mylist = get_smooth_hist(mylist, 5, size)
    mylist = ndimage.filters.gaussian_filter1d(mylist, 4)
    columnList = signal.find_peaks_cwt(mylist, np.arange(1,w))
    return columnList

def peak_origin(mylist):
    columnList = []
    l = len(mylist)
    for index, obj in enumerate(mylist):
        if index < (l - 2) and float(obj) > 0:
            if (mylist[index+2] / float(obj) > 1.1):
                columnList.append(index)
    return columnList

def remove_duplicate(l):
    pre = l[0]
    ans = []
    ans.append(l[0])
    for i, v in enumerate(l):
        if (v - pre >= 20):
            ans.append(v)
        pre = v
    return ans

def peak_var(mylist, nstd):
    dmylist = np.diff(mylist)
    dmylist = [abs(x) for x in dmylist]
    avg = np.average(dmylist)
    std = np.std(dmylist)
    ans = []
    for i,v in enumerate(dmylist):
        if v > avg + std * nstd or v < avg - std * nstd:
            ans.append(i)
    ans = remove_duplicate(ans)
    return ans

def peak_dog(mylist):
    return []

def generateJSON(ansList):
    anns = []
    idd = 0
    for value in ansList:
        fromx = value[0]
        endx = value[1]
        rowList = value[2]

        for i in range(0, len(rowList)-1):
            height = rowList[i+1] - rowList[i]
            if (height < 300):
                anns.append({"class": "title",
                          "height": height,
                          "id": str(idd),
                          "type": "rect",
                          "width": endx - fromx,
                          "x": fromx,
                          "y": rowList[i]})
                idd += 1
            else:
                anns.append({"class": "article",
                          "height": height,
                          "id": str(idd),
                          "type": "rect",
                          "width": endx - fromx,
                          "x": fromx,
                          "y": rowList[i]})
                idd += 1
    seg = [{
            "annotations": anns,
          }]
    return seg


def main():
    start = timeit.default_timer()
    outfolder, imagename, xmlname,outname = sys.argv[1:5]
    outname = outfolder + '/' + outname.split('/')[-1]

    methodName = "var"
    img = Image.open(imagename)
    img = img.convert('L')

    size = width, height = img.size
    # print size
    columnList = []
    ansList = []

    if methodName == 'original':

        bw = img.point(lambda x:0 if x<190 else 225, '1')
        bw.show()
        px = bw.load()
        mylist = []
        for x in range(width):
            vs = 0
            for y in range(height):
                vs += px[x, y] / 225
            mylist.append(vs)

        fig = plt.gcf()
        plt.plot(mylist)

        columnList = peak_origin(mylist)

        # print columnList
        for xi in columnList:
            plt.axvline(x=xi, color='red')

        for i in range(0, len(columnList)-1):
            fromx = columnList[i]
            endx = columnList[i+1]
            secondaryList = []
            # print fromx, endx

            for y in range(height):
                hs = 0
                for x in range(fromx, endx):
                    hs += px[x, y]
                secondaryList.append(hs)

            rowList = peak_origin(secondaryList)
            ansList.append([fromx, endx, rowList])

    # Continuous Wavelet Analysis
    if methodName == 'cwt':
        bw = np.asarray(img).copy()
        bw[bw <  190] = 0
        bw[bw >= 190] = 1
        vertical_histogram = np.sum(bw, axis=0)
        mylist = list(vertical_histogram)

        fig = plt.gcf()
        plt.plot(mylist)

        columnList = peak_cwt(mylist, width/8, width)
        # print columnList
        for xi in columnList:
            plt.axvline(x=xi, color='red')

        for i in range(0, len(columnList)-1):
            fromx = columnList[i]
            endx = columnList[i+1]
            secondaryList = []
            # print fromx, endx

            horizontal_histogram = np.sum(bw[:, fromx:endx], axis=1)

            secondaryList = list(horizontal_histogram)
            rowList = peak_cwt(secondaryList, height/4, height)

            ansList.append([fromx, endx, rowList])

    # variance
    if methodName == 'var':

        bw = np.asarray(img).copy()
        bw[bw <  190] = 0
        bw[bw >= 190] = 1

        # testlist = get_smooth_hist(list(np.sum(bw, axis=1)), 20, height)
        # plt.clf()
        # fig = plt.gcf()
        # plt.plot(testlist)
        #
        # # for xi in rowList:
        # #     plt.axvline(x=xi, color='red')
        # plt.show()


        mylist = list(np.sum(bw, axis=0))
        mylist = get_smooth_hist(mylist, 5, width)

        columnList = peak_var(mylist, 2)
        # print columnList

        for i in range(0, len(columnList)-1):
            fromx = columnList[i]
            endx = columnList[i+1]

            horizontal_histogram = list(np.sum(bw[:, fromx:endx], axis=1))
            horizontal_histogram = get_smooth_hist(horizontal_histogram, 4, height)
            rowList = peak_var(horizontal_histogram, 1.2)

            # print fromx, endx
            # plt.clf()
            # fig = plt.gcf()
            # plt.plot(horizontal_histogram)
            #
            # for xi in rowList:
            #     plt.axvline(x=xi, color='red')
            # plt.show()

            ansList.append([fromx, endx, rowList])

    seg = generateJSON(ansList)
    with open(outname,'w') as f:
       json.dump(seg, f, indent=4)
    f.close()
if __name__=='__main__':
  main()
