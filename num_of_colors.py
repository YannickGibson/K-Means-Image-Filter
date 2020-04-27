
def n_distinct(l):
    color_composition = {}

    #this
    ''' for c in pixels:
        if c not in color_composition:
            color_composition.append(c) '''
    #or this solution... this shows why structures are better, its like 100x times faster!!
    #color_composition = set(pixels)
    #also dicts are seemingly having same speed than sets, 'in' for dict(keys) is also like 100x faster than list
    for c in l:
        if c not in color_composition:
            color_composition[c] = True
    return len(color_composition)
    

def main():
    from PIL import Image
    filePath = "originals/bruh.jpg"
    #filePath = "saves/hi homer_jpg/hi homerx2.jpg" # buncho collors
    #filePath = "saves/hi homer_png/hi homerx2.png" # two colors
    im = Image.open(filePath)
    pixels = list(im.getdata())

    number = n_distinct(pixels)

    print("The image is made of {} colors".format(number))

main()
