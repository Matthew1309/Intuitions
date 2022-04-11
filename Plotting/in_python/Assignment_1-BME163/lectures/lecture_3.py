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

# xList=[2,5,3]
# yList=[10,1,100]
# panel1.plot(xList,yList,marker='o',markerfacecolor=(0,0,0),
# 	markeredgecolor='black', markersize=13, markeredgewidth=0,
# 	linewidth=0)

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
panel1.set_xlim(0,100)
panel1.set_ylim(0,120)
#plt.savefig('Vollmers_Lecture1.png', dpi=300)
plt.show()