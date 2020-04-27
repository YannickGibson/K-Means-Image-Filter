# KMeans-Image-Filter
Color segmentation for images

## Input
<img src="https://user-images.githubusercontent.com/57909721/80402033-93515980-88bd-11ea-8a66-1bc224a6c2c3.jpg" width="400" />

## Result
<img src="https://user-images.githubusercontent.com/57909721/80402265-f642f080-88bd-11ea-8e22-5dd1816653e6.jpg" width="400" />


## Code
Note: `img.show()` will display the image by your default image viewing program.  
  
```python
import filter

img = filter.simplify("originals/balls.jpg", 6)
img.show()
```
### Saving
```python
img.save("example/destination")
```
