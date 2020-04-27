from filter import k_means

# Settings 'showPlotFinish' or 'showPlotFinish' to True is not recommended for images with more than 250*250 pixels
img = k_means("originals/balls.jpg", k=6)
img.show()




