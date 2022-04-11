import matplotlib.pyplot as plt 
import matplotlib.patches as mplpatches
import numpy as np 


plt.style.use('C:\\Users\\mattk\\Desktop\\BME163\\Assignments\\BME163')


figureWidth=4
figureHeight=2

plt.figure(figsize=(figureWidth,figureHeight))


panelWidth=3
panelHeight=1.5

relativePanelWidth=panelWidth/figureWidth
relativePanelHeight=panelHeight/figureHeight


#             left,bottom,width,height
panel1=plt.axes([0.1,0.1,relativePanelWidth,relativePanelHeight])

xList=[2,5,3]
yList=[10,1,100]
panel1.plot(xList,yList,marker='o',markerfacecolor=(0,0,0),
	markeredgecolor='black', markersize=13, markeredgewidth=0,
	linewidth=0)

rectangle=mplpatches.Rectangle( [0.1,0.1],2,0.5 ,
	facecolor='red',
	edgecolor='black',
	linewidth=0)
panel1.set_xticks([3.5])
panel1.set_xticklabels(['dragon'])

panel1.tick_params(bottom=True, labelbottom=True,
	left='on', labelleft=True,
	right=True, labelright=False,
	top=False, labeltop=False)
panel1.set_xlim(0,10)
panel1.set_ylim(0,120)
#plt.savefig('Vollmers_Lecture1.png', dpi=300)
plt.show()