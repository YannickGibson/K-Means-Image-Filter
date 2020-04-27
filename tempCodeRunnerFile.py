
    for k in range(colorsK):
        for order in groups[k][3]:#fourth is for order
            color = (centers[0][k], centers[1][k], centers[2][k],255)
            data[order//width,order%width] = color#going from top to bottom, then x++