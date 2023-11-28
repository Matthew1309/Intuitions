# Purpose
Here I will summarize some of the image manipulation techniques I have learned.

1. To convert pdfs to pngs or svgs we can use inkscape. For example the command ```inkscape --export-area-drawing --export-type=png --export-margin=1 .pdf"``` will convert a png to a specified pdf. Just give it the PDF name at the
.pdf part. We learned this in Kevin Karplus's Analog Electronics class. 
There are other inputs to that like `inkscape in.svg --export-type=png -o out.png -h HEIGHT -w WIDTH`.

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

## A gimp tutorial for batch resizing images I found on my laptop
http://warunapw.blogspot.com/2010/01/batch-resize-images-in-gimp.html

From this link they use a language called Scheme, which I installed with
Tabby using sudo apt-get scm blah blah.

I think I will use the first option where they simply overwrite the photos
with the sized down gimp photos.

I need to put the script into ~/.gimp-/scripts/ directory for this to work.
I actually put it into "/mnt/c/Documents and Settings/mattk/Application Data/GIMP/2.10/scripts"
so lets hope this works.

Didn't work so I'mma put it into "/mnt/c/Program Files/GIMP 2/share/gimp/2.0/scripts" because 
https://daviesmediadesign.com/how-to-install-scripts-in-gimp-3-easy-steps/ told me too.

That was a whole process because this folder apparently doesn't respond to sudo, so I had
to open gitbash as administrator then make the file in there. WTF. Then the gimp wasn't in my
PATH so I added it (it is in /mnt/c/Program\ Files/Gimp \2/bin/). 

Command:
	`gimp-2.10.exe -i -b '(batch-resize "*.JPG" 604 453)' -b '(gimp-quit 0)'`

