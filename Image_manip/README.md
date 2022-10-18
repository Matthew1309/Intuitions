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