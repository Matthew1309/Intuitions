import matplotlib.pyplot as plt 
import matplotlib.patches as mplpatches
import numpy as np 
import time
import scipy.stats as stats


plt.style.use('C:\\Users\\mattk\\Desktop\\BME163\\Assignments\\BME163')


figureWidth=4
figureHeight=4

plt.figure(figsize=(figureWidth,figureHeight))


panelWidth=2
panelHeight=2

relativePanelWidth=panelWidth/figureWidth
relativePanelHeight=panelHeight/figureHeight
######################################################################
######################################################################
'''
#             left,bottom,width,height
panel1=plt.axes([0.1,0.1,relativePanelWidth,relativePanelHeight])
panel2=plt.axes([0.4,0.1,relativePanelWidth,relativePanelHeight])
panel3=plt.axes([0.7,0.1,relativePanelWidth,relativePanelHeight])
'''

xList=[1,3,5,7]
yList = [1,3,5,7]

panel1=plt.axes([0.2,0.2,relativePanelWidth,relativePanelHeight])
panel1.plot(xList,yList,linewidth=0, marker='o', mew=0,mfc='black',ms=1)

panel1.text(1,1,'test1')
panel1.text(3,3,'test1')
panel1.text(5,5,r'test1$^\mathrm{poop}$')
panel1.text(7,7,'test1', va='top', ha='right')

panel1.tick_params(bottom=True, labelbottom=True,
	left='on', labelleft=True,
	right=True, labelright=False,
	top=False, labeltop=False)

panel1.set_xlabel(r'line$_{whatever}$')
#plt.savefig('Vollmers_Lecture1.png', dpi=300)
plt.show()