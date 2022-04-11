import matplotlib.pyplot as plt 
import matplotlib.patches as mplpatches
import numpy as np 
import matplotlib.image as mpimg

plt.style.use('C:\\Users\\mattk\\Desktop\\BME163\\Assignments\\BME163')

figureWidth=8.5
figureHeight=3

plt.figure(figsize=(figureWidth,figureHeight))


panelWidth=1.5
panelHeight=1.5

relativePanelWidth=panelWidth/figureWidth
relativePanelHeight=panelHeight/figureHeight


#             left,bottom,width,height
panel1=plt.axes([0.1,0.1,relativePanelWidth,relativePanelHeight])
panel2=plt.axes([0.5,0.1,relativePanelWidth,relativePanelHeight])


xList=[2,5,3]
yList=[10,1,100]
panel1.plot(xList,yList,marker='o',markerfacecolor='red',
	markeredgecolor='black', markersize=13, markeredgewidth=0,
	linewidth=0)

rectangle=mplpatches.Rectangle( [0.1,0.1],2,0.5 ,
	facecolor='red',
	edgecolor='black',
	linewidth=0)

panel2.add_patch(rectangle)
#plt.savefig('Vollmers_Lecture1.png', dpi=300)
plt.show()