# K-Means-Image-Filter
Color segmentation for images

## Input
<img src="https://user-images.githubusercontent.com/57909721/80402033-93515980-88bd-11ea-8a66-1bc224a6c2c3.jpg" width="400" />

## Result
### K=3
<img src="https://user-images.githubusercontent.com/57909721/80428537-5ea7c700-88ea-11ea-8ade-8bf2ee5a74b6.jpg" width="400" />  

### K=4
<img src="https://user-images.githubusercontent.com/57909721/80428653-a9294380-88ea-11ea-9c48-6564fa2283da.jpg" width="400" />  

### K=7
<img src="https://user-images.githubusercontent.com/57909721/80427522-3ae38180-88e8-11ea-9da3-fc308c4efe9c.jpg" width="400" />  

## Code
Note: `img.show()` will display the image by your default image viewing program.  
  
```python
from filter import k_means

img = k_means("originals/balls.jpg", k=7)
img.show()
```
### Saving
```python
img.save("example/destination")
```
