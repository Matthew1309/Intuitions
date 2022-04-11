import matplotlib.pyplot as plt 
import matplotlib.patches as mplpatches
import numpy as np 
import time

plt.style.use('C:\\Users\\mattk\\Desktop\\BME163\\Assignments\\BME163')


figureWidth=7
figureHeight=2

plt.figure(figsize=(figureWidth,figureHeight))


panelWidth=1.5
panelHeight=1.5

relativePanelWidth=panelWidth/figureWidth
relativePanelHeight=panelHeight/figureHeight
######################################################################
######################################################################

#             left,bottom,width,height
panel1=plt.axes([0.1,0.1,relativePanelWidth,relativePanelHeight])
panel2=plt.axes([0.4,0.1,relativePanelWidth,relativePanelHeight])
panel3=plt.axes([0.7,0.1,relativePanelWidth,relativePanelHeight])


blue=(0,0,1)
red=(1,0,0)
green=(0,1,0)
yellow=(1,1,0)
black=(0,0,0)
white=(1,1,1)


R=np.linspace(yellow[0],blue[0],101)
G=np.linspace(yellow[1],blue[1],101)
B=np.linspace(yellow[2],blue[2],101)
print(R)

#mean,std,number of points
xList=np.random.normal(120,20,10000)
yList=np.random.normal(120,20,10000)

start=time.time()
panel1.plot(xList,yList,
	marker='o',
	markerfacecolor=(0,0,0),
	markeredgecolor='black',
	markersize=1,
	markeredgewidth=0,
	linewidth=0,
	alpha=0.1)
end=time.time()

duration=end-start
print("plot",duration)

sizes=[]
colors=[]
start=time.time()
for i in range(0,len(xList),1):
	xValue=xList[i]
	yValue=yList[i]
	sizes.append(xValue)
	colors.append( (xValue/255,yValue/255,1-(xValue/255) ) )

	panel2.plot(xValue,yValue,
	marker='o',
	markerfacecolor=(xValue/255,yValue/255,1-(xValue/255)),
	markeredgecolor='black',
	markersize=1,
	markeredgewidth=0,
	linewidth=0,
	alpha=0.7)
end=time.time()

duration=end-start
print("plot",duration)

start=time.time()
panel3.scatter(xList,yList,
				s=sizes,
				facecolor=colors,
				linewidth=0,
				alpha=0.2)
end=time.time()

duration=end-start
print("plot",duration)

xHisto,bins=np.histogram(xList,range(0,250,10))
print(xHisto,bins)

for i in range(0,len(xHisto),1):
	bottom=0
	left=bins[i]
	width=bins[i+1]-left
	height=xHisto[i]
	rectangle=mplpatches.Rectangle( [left,bottom],width,height,
		facecolor=( 0.3,0.3,0.3 ),
		edgecolor='black',
		linewidth=0.1)
	panel1.add_patch(rectangle)


for i in range(0,101,1):
	rectangle=mplpatches.Rectangle( [i,0],1,120,
		facecolor=( R[i],G[i],B[i] ),
		edgecolor='black',
		linewidth=0)
	panel1.add_patch(rectangle)

panel1.set_xticks([3.5])
panel1.set_xticklabels(['dragon'])

panel1.tick_params(bottom=True, labelbottom=True,
	left='on', labelleft=True,
	right=True, labelright=False,
	top=False, labeltop=False)

for panel in [panel1,panel2,panel3]:
	panel.set_xlim(0,250)
	panel.set_ylim(0,250)

panel1.set_ylim(0,1.1*max(xHisto))
#plt.savefig('Vollmers_Lecture1.png', dpi=300)
plt.show()