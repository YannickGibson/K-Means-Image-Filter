# K-Means-Image-Filter
Color segmentation for images

## Input
<img src="https://user-images.githubusercontent.com/57909721/80402033-93515980-88bd-11ea-8a66-1bc224a6c2c3.jpg" width="400" />

## Result
<img src="https://user-images.githubusercontent.com/57909721/80402265-f642f080-88bd-11ea-8e22-5dd1816653e6.jpg" width="400" />


## Code
Note: `img.show()` will display the image by your default image viewing program.  
  
```python
from filter import k_means

img = k_means("originals/balls.jpg", k=6)
img.show()
```
### Saving
```python
img.save("example/destination")
```
