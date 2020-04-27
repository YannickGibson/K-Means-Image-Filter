import filter

# Settings 'showPlotFinish' or 'showPlotFinish' to True is not recommended for images with more than 250*250 pixels
img = filter.simplify("originals/water_drop.jpg", 5, logs=True, showPlotFinish=True)

img.show()
