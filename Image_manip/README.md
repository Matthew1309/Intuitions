# Purpose
Here I will summarize some of the image manipulation techniques I have learned.

1. To convert pdfs to pngs or svgs we can use inkscape. For example the command ```inkscape --export-area-drawing --export-type=png --export-margin=1 .pdf"``` will convert a png to a specified pdf. Just give it the PDF name at the
.pdf part. We learned this in Kevin Karplus's Analog Electronics class
1. To resize images and make them more managable we can use python or the commandline
    1. Python is pretty darn simple. From the comment by [Goncalo](https://superuser.com/questions/646896/how-to-change-dpi-of-a-png-file-in-command-line-without-imagemagick) we can enter the following 
    
        ```
        from PIL import Image
        im = Image.open("in.png")
        nx, ny = im.size
        im2 = im.resize((int(nx*1.5), int(ny*1.5)), Image.BICUBIC)
        im2.save("out.png")
        ```
    1. I don't remember how, but with inkscape it seems the commandline can let you choose DPI and size of export. Or maybe it isn't the commandline and is the actual inkscape application.
   1. Visualize it in markdown with `<img src="Lap_table_small.png" width="100" height=" 100">`
   
## Full Python workflow
```
import matplotlib.image as mpimg
img=mpimg.imread('basic_grav_model.png')
plt.minorticks_on()
imgplot = plt.imshow(img)

from PIL import Image
im = Image.open("basic_grav_model.png")

top = 60
bottom = 460
left = 200
right = 600

im1 = im.crop((left, top, right, bottom))
nx, ny = im1.size; print(nx, ny)
# Shows the image in image viewer
im1

im2 = im1.resize((int(nx*0.25), int(ny*0.25)), Image.BICUBIC)
im2.save("out.png")
```

## Cropping in python
If we want to see the dimensions of the image we can use
```
import matplotlib.image as mpimg
img=mpimg.imread('basic_grav_model.png')
imgplot = plt.imshow(img)
```
    
    
## Using inkscape
1. We can open up an image by going file --> open then navigate to the file we want to edit. 
1. The editor will open your image. Generally I like to clip off whitespace, and to do that select the rectangle tool, make a rectangle around the area we want to keep.
1. Select rectangle first, image second.
1. In the top menu click object --> clip --> set
1. Now our image is smaller. To export it in the right hand menu select export as to set a destination. Then make sure to click export selected items only. Done.
