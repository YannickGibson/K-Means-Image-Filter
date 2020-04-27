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
center_colors = ["red","green","orange","blue","hotpink","darkviolet","darkgray","peru"]# For some reason 'darkgray' is not darker than 'gray' lmao check docs
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


def compare_groups(g1, g2):

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

def create_plot(name):
    fig = pyplot.figure(name)
    ax = Axes3D(fig)

    # Step of axises
    ax.set_xticks(list(range(0,256+1,64)))
    ax.set_yticks(list(range(0,256+1,64)))
    ax.set_zticks(list(range(0,256+1,64)))
    ax.view_init(azim=-130,elev=30)
    return ax

def generate_centers(k):
    centers = ([],[],[])
    for _ in range(k):
        centers[0].append(random.randint(0,255))
        centers[1].append(random.randint(0,255))
        centers[2].append(random.randint(0,255))
    return centers

def k_means(file_name, k, plot_final = False, plot_steps = False, logs = False):#using K-Means algorithm
    if k <= 0:
        raise Exception("Number of colors must be greater than 0")
   

    recenter_count = 0
    img = Image.open(file_name)
    pixels = list(img.getdata())
    distinct = len(set(pixels))
    if k >= distinct:
        raise Exception("Number of colors '{}' must be smaller than number of distinct colors in entered image '{}'".format(k, distinct))
    width, height = img.size

    if logs:
        print("Aplying '{}-Color Filter' on {}x{} image '{}'".format(k, width, height, file_name))

    has_transparency =  file_name.split('.')[ -1 ] == "png"

    #data preparation
    img_rgbs = ([],[],[])
    for pixel in pixels:
        img_rgbs[0].append(pixel[0])
        img_rgbs[1].append(pixel[1])
        img_rgbs[2].append(pixel[2])
    #
    centers = generate_centers(k)

    groups_temp = []
    groups = None
    recenter_cycles = 0
    while True:
        # Reset groups
        groups = [([],[],[],[]) for _ in range(k)]

        center_alone_indexes = []


        


        #GROUPING pixels
        for order, pix in enumerate(pixels):# 
            if has_transparency and pix[3] == 0:
                continue
            min_dist_index = 0
            smallest_dist = -1
            for _k in range(0,k):
                curr_vector = (centers[0][_k] - pix[0], centers[1][_k] - pix[1], centers[2][_k] - pix[2])
                curr_dist = math.sqrt(curr_vector[0]*curr_vector[0] + curr_vector[1]*curr_vector[1] + curr_vector[2]*curr_vector[2])
                if curr_dist < smallest_dist or smallest_dist == -1:
                    smallest_dist = curr_dist
                    min_dist_index = _k

            groups[min_dist_index][0].append(pix[0])
            groups[min_dist_index][1].append(pix[1])
            groups[min_dist_index][2].append(pix[2])
            groups[min_dist_index][3].append(order)

        #Trying to asign ALONE center points
        for _k in range(k):
            group_length = len(groups[_k][0])
            if group_length == 0:
                center_alone_indexes.append(_k)
            else:#recentering here
                x_sum = sum(groups[_k][0])
                y_sum = sum(groups[_k][1])
                z_sum = sum(groups[_k][2])
                centers[0][_k] = int(x_sum / group_length)
                centers[1][_k] = int(y_sum / group_length)
                centers[2][_k] = int(z_sum / group_length)

        if len(center_alone_indexes) != 0:
            generate_centers(k)
            recenter_count = len(center_alone_indexes)
            new_centers = generate_centers(recenter_count)
            for i, c_ind in enumerate(center_alone_indexes):
                centers[0][c_ind] = new_centers[0][i]
                centers[1][c_ind] = new_centers[1][i]
                centers[2][c_ind] = new_centers[2][i]
            
            if logs:
                print("Asigning " + str(recenter_count) + " alone center color" + ("" if recenter_count==1 else "s") )

            continue#repeat WhileLoop from start

        

        # If groups didn't change after 'Recentering' -> We quit the loop
        # Always check if recentering changed, so this if is never true on first iteration 
        if len(groups_temp) != 0:
            
            if (logs):
                print("Points of groups are recentered: " + str(recenter_cycles))

            if compare_groups(groups, groups_temp): # groups_temp == groups:
                break
        groups_temp = copy.deepcopy(groups)


        recenter_cycles += 1

        
        if plot_steps == True:
            ax = create_plot(name="Cycles: " + str(recenter_cycles))
            for g in range(len(groups)):
                ax.scatter(groups[g][0], groups[g][1], groups[g][2], marker='o', s=50, c=center_colors[g % COLOR_LENGTH], alpha=0.05)
                ax.scatter(centers[0][g], centers[1][g], centers[2][g], s=3000, c=center_colors[g % COLOR_LENGTH], alpha=0.8)#just a point

            pyplot.show()




    if plot_final or plot_steps:
        ax = create_plot(name="Finished | Cycles: " + str(recenter_cycles))
        for g in range(len(groups)):
            ax.scatter(groups[g][0], groups[g][1], groups[g][2], marker='o', s=50, c=center_colors[g], alpha=0.05)
            ax.scatter(centers[0][g], centers[1][g], centers[2][g], s=3000, c=center_colors[g], alpha=0.8)#just a point
        pyplot.show()
    data = None

    if has_transparency:
        data = np.zeros( (height,width,4), dtype=np.uint8 )#3 means RGB

        for k in range(k):
            for order in groups[k][3]:#fourth is for order
                color = (centers[0][k], centers[1][k], centers[2][k], 255)#255 for opacity
                data[order//width,order%width] = color#going from top to bottom, then x++
    else:
        data = np.zeros( (height,width,3), dtype=np.uint8 )#3 means RGB

        for k in range(k):
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



    file_name = "carti_what.jpg"
    ori_folder = "originals"
    original_dest = os.path.join(ori_folder,file_name)
    save_folder = "saves"
    k = 4

    start_time = time.time()
    img = k_means(original_dest, k, logs=True, plot_steps=False)
    time_elapsed = time.time() - start_time
    print("Execution time: %s" % display_time(round(time_elapsed)))
    

    # What a mess lol
    sub_split = file_name.split('.')
    sub_folder_name = "_".join( (".".join(sub_split[:-1]), sub_split[-1]) )
    sub_folder_path = os.path.join(save_folder, sub_folder_name)
    if not os.path.exists(sub_folder_path):
        os.makedirs(sub_folder_path)
        shutil.copy(original_dest, sub_folder_path)
    splitted = file_name.split(".")
    prefix, postfix = ".".join(splitted[:-1]), splitted[-1]
    _new_file_name = "{}_x{}".format(prefix, k)
    new_file_path = os.path.join(sub_folder_path, _new_file_name)
    if os.path.exists(new_file_path + "." + postfix):
        i=1
        while os.path.exists(new_file_path + "_{}.{}".format(i, postfix)):
            i += 1
        new_file_path = new_file_path + "_" + str(i)

    save_path = os.path.join(new_file_path + "." + postfix)
    img.show()
    ret = img.save(save_path)


if __name__ == "__main__":
    for _ in range(1):
        main()