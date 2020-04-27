from PIL import Image
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
import random
import math
import os
import shutil
import numpy as np
import copy

from matplotlib.colors import TABLEAU_COLORS
from matplotlib.colors import get_named_colors_mapping

colors = list(map(lambda x: x.split(':')[1],TABLEAU_COLORS.keys()))
centerColors = ["red","green","orange","blue","hotpink","darkviolet","darkgray","peru"]# For some reason 'darkgray' is not darker than 'gray' lmao check docs
groupColors = ["darkred","darkgreen","darkorange","darkblue","mediumvioletred","indigo","dimgrey","saddlebrown"]
rndColor = lambda : random.choice(colors)
COLOR_LENGTH = len(colors)

#Removal of wierd margin
###patch start### https://stackoverflow.com/a/16496436/11776868 
from mpl_toolkits.mplot3d.axis3d import Axis
if not hasattr(Axis, "_get_coord_info_old"):
    def _get_coord_info_new(self, renderer):
        mins, maxs, centers, deltas, tc, highs = self._get_coord_info_old(renderer)
        mins += deltas / 4
        maxs -= deltas / 4
        return mins, maxs, centers, deltas, tc, highs
    Axis._get_coord_info_old = Axis._get_coord_info  
    Axis._get_coord_info = _get_coord_info_new
###patch end###

ax = None


def compareGroups(g1, g2):

    # k is the color_group of group
    for k in range(len( g1 )):

        # Components are 0: Red, 1: Green, 2: Blue, 3: Order in image
        for component_type_index in range(len( g1[k] )):

            # If N of colors in g1.a != N of colors in g2.a
            if len(g1[k][component_type_index]) != len(g2[k][component_type_index]):
                pass
                #return False

            for comp_index in range(len( g1[k][component_type_index] )):


                
                """ print("----1----")
                print(g1)
                print("----2----")
                print(g2)
                print("----3----")
                return True """
                comp1 = g1[k][component_type_index][comp_index]

                comp2 = g2[k]\
                [component_type_index]\
                [comp_index]
                """  
                try:
                    comp2 = g2[k]\
                    [component_type_index]\
                    [comp_index]
                except:
                    print(len(g1[k][component_type_index]), len(g2[k][component_type_index]), comp_index)
                    import sys
                    raise Exception(sys.exc_info()) """

                # Comparing component int values
                if comp1 != comp2:
                    return False

    return True

def createPlot(name):
    fig = pyplot.figure(name)
    ax = Axes3D(fig)

    # Step of axises
    ax.set_xticks(list(range(0,256+1,64)))
    ax.set_yticks(list(range(0,256+1,64)))
    ax.set_zticks(list(range(0,256+1,64)))
    ax.view_init(azim=-130,elev=30)
    return ax

def generateCenters(K):
    centers = ([],[],[])
    for k in range(K):
        centers[0].append(random.randint(0,255))
        centers[1].append(random.randint(0,255))
        centers[2].append(random.randint(0,255))
    return centers

def simplify(fileName, colorsK, showPlotFinish = False, showPlotSteps = False, logs = False):#using K-Means algorithm
    if colorsK <= 0:
        raise Exception("Number of colors must be greater than 0")
   

    recenterCount = 0
    img = Image.open(fileName)
    pixels = list(img.getdata())
    distinct = len(set(pixels))
    if colorsK >= distinct:
        raise Exception("Number of colors '{}' must be smaller than number of distinct colors in entered image '{}'".format(colorsK, distinct))
    width, height = img.size

    if logs:
        print("Aplying '{}-Color Filter' on {}x{} image '{}'".format(colorsK, width, height, fileName))

    hasTransparency = len(pixels[0]) == 4

    #data preparation
    imgRGBs = ([],[],[])
    for pixel in pixels:
        imgRGBs[0].append(pixel[0])
        imgRGBs[1].append(pixel[1])
        imgRGBs[2].append(pixel[2])
    #
    centers = generateCenters(colorsK)

    groupsTemp = []
    groups = None
    recenter_cycles = 0
    while True:
        # Reset groups
        groups = [([],[],[],[]) for _ in range(colorsK)]

        centerAloneIndexes = []


        


        #GROUPING pixels
        for order, pix in enumerate(pixels):# 
            if hasTransparency and pix[3] == 0:
                continue
            minDistIndex = 0
            smallestDist = -1
            for k in range(0,colorsK):
                currVector = (centers[0][k] - pix[0], centers[1][k] - pix[1], centers[2][k] - pix[2])
                currDist = math.sqrt(currVector[0]*currVector[0] + currVector[1]*currVector[1] + currVector[2]*currVector[2])
                if currDist < smallestDist or smallestDist == -1:
                    smallestDist = currDist
                    minDistIndex = k

            groups[minDistIndex][0].append(pix[0])
            groups[minDistIndex][1].append(pix[1])
            groups[minDistIndex][2].append(pix[2])
            groups[minDistIndex][3].append(order)

        #Trying to asign ALONE center points
        for k in range(colorsK):
            groupLength = len(groups[k][0])
            if groupLength == 0:
                centerAloneIndexes.append(k)
            else:#recentering here
                xSum = sum(groups[k][0])
                ySum = sum(groups[k][1])
                zSum = sum(groups[k][2])
                centers[0][k] = int(xSum / groupLength)
                centers[1][k] = int(ySum / groupLength)
                centers[2][k] = int(zSum / groupLength)

        if len(centerAloneIndexes) != 0:
            generateCenters(colorsK)
            groups = [([],[],[],[]) for _ in range(colorsK)]
            recenterCount = len(centerAloneIndexes)
            newCenters = generateCenters(recenterCount)
            for i, cInd in enumerate(centerAloneIndexes):
                centers[0][cInd] = newCenters[0][i]
                centers[1][cInd] = newCenters[1][i]
                centers[2][cInd] = newCenters[2][i]
            
            if logs:
                print("Asigning " + str(recenterCount) + " ALONE center color" + ("" if recenterCount==1 else "s") )

            continue#repeat WhileLoop from start

        

        # If groups didn't change after 'Recentering' -> We quit the loop
        # Always check if recentering changed, so this if is never true on first iteration 
        if len(groupsTemp) != 0:
            
            if (logs):
                print("Points of groups are recentered: " + str(recenter_cycles))

            if compareGroups(groups, groupsTemp): # groupsTemp == groups:
                break
        groupsTemp = copy.deepcopy(groups)


        recenter_cycles += 1

        
        if showPlotSteps == True:
            ax = createPlot(name="Cycles: " + str(recenter_cycles))
            for g in range(len(groups)):
                ax.scatter(groups[g][0], groups[g][1], groups[g][2], marker='o', s=50, c=centerColors[g % COLOR_LENGTH], alpha=0.05)
                ax.scatter(centers[0][g], centers[1][g], centers[2][g], s=3000, c=centerColors[g % COLOR_LENGTH], alpha=0.8)#just a point

            pyplot.show()




    if showPlotFinish:
        ax = createPlot(name="Finished | Cycles: " + str(recenter_cycles))
        for g in range(len(groups)):
            ax.scatter(groups[g][0], groups[g][1], groups[g][2], marker='o', s=50, c=centerColors[g], alpha=0.05)
            ax.scatter(centers[0][g], centers[1][g], centers[2][g], s=3000, c=centerColors[g], alpha=0.8)#just a point
        pyplot.show()
    data = None

    if hasTransparency:
        data = np.zeros( (height,width,4), dtype=np.uint8 )#3 means RGB

        for k in range(colorsK):
            for order in groups[k][3]:#fourth is for order
                color = (centers[0][k], centers[1][k], centers[2][k], 255)#255 for opacity
                data[order//width,order%width] = color#going from top to bottom, then x++
    else:
        data = np.zeros( (height,width,3), dtype=np.uint8 )#3 means RGB

        for k in range(colorsK):
            for order in groups[k][3]:#fourth is for order
                color = (centers[0][k], centers[1][k], centers[2][k])
                data[order//width,order%width] = color#going from top to bottom, then x++

    

    return Image.fromarray(data)


# Sidenote: jpg applies antialiasing automaticaly after i save the "im"
def main():
    import time

    def display_time(seconds):
        minutes = seconds // 60
        if minutes != 0:
            seconds %= 60
            hours = minutes // 60
            if hours != 0:
                minutes %= 60
                return "{}hours {}minutes {}seconds".format(hours, minutes, seconds)
            return "{}minutes {}seconds".format(minutes, seconds)
        return "{}seconds".format(seconds)



    fileName = "water_drop.jpg"
    ori_folder = "originals"
    original_dest = os.path.join(ori_folder,fileName)
    save_folder = "saves"
    K = 3

    start_time = time.time()
    img = simplify(original_dest, K, logs=True, showPlotSteps=True)
    timeElapsed = time.time() - start_time
    print("Execution time: %s" % display_time(round(timeElapsed)))
    

    # What a mess lol
    sub_split = fileName.split('.')
    subFolderName = "_".join( (".".join(sub_split[:-1]), sub_split[-1]) )
    subFolderPath = os.path.join(save_folder, subFolderName)
    if not os.path.exists(subFolderPath):
        os.makedirs(subFolderPath)
        shutil.copy(original_dest, subFolderPath)
    splitted = fileName.split(".")
    prefix, postfix = ".".join(splitted[:-1]), splitted[-1]
    newFileName = "{}x{}".format(prefix, K)
    newFilePath = os.path.join(subFolderPath, newFileName)
    if os.path.exists(newFilePath + "." + postfix):
        i=1
        while os.path.exists(newFilePath + "_{}.{}".format(i, postfix)):
            i += 1
        newFilePath = newFilePath + "_" + str(i)

    save_path = os.path.join(newFilePath + "." + postfix)
    ret = img.save(save_path)
    img.show()


if __name__ == "__main__":
    for _ in range(1):
        main()