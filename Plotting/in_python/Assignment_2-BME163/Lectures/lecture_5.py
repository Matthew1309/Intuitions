import matplotlib.pyplot as plt 
import matplotlib.patches as mplpatches
import numpy as np 
import time
import scipy.stats as stats


plt.style.use('C:\\Users\\mattk\\Desktop\\BME163\\Assignments\\BME163')


figureWidth=11
figureHeight=4

plt.figure(figsize=(figureWidth,figureHeight))


panelWidth=1.5
panelHeight=1.5

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

#mean,std,number of points
xList=np.random.normal(120,20,10000)
yList1=np.random.normal(120,20,10000)
yList2=xList
yList3=xList**10
yList4=np.sin(xList)

xShift=0.1
for yList in [yList1,yList2,yList3,yList4]:
	panel1=plt.axes([xShift,0.1,relativePanelWidth,relativePanelHeight])
	xShift+=0.2
	panel1.plot(xList,yList,
	marker='o',
	markerfacecolor=(0,0,0),
	markeredgecolor='black',
	markersize=1,
	markeredgewidth=0,
	linewidth=0,
	alpha=0.1)
	panel1.text(0,0, "r="+str(round(stats.spearmanr(xList,yList)[0],3)))
	panel1.set_xlim(0,max(xList))
	panel1.set_ylim(0,max(yList))


panel2=plt.axes([0.1,0.5,0.8,relativePanelHeight])
panel2.bar(3,np.average(yList1),width=0.5,
	facecolor='grey',
	edgecolor='black',
	linewidth=0.1,
	yerr=np.std(yList1))

panel1.tick_params(bottom=True, labelbottom=True,
	left='on', labelleft=True,
	right=True, labelright=False,
	top=False, labeltop=False)

#plt.savefig('Vollmers_Lecture1.png', dpi=300)
plt.show()