import matplotlib.pyplot as plt 
import matplotlib.patches as mplpatches
import numpy as np 
import matplotlib.image as mpimg


plt.style.use('C:\\Users\\mattk\\Desktop\\BME163\\Assignments\\BME163')

figureWidth=8.5
figureHeight=3

plt.figure(figsize=(figureWidth,figureHeight))


panelWidth=3
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


A=mpimg.imread("../A_small.png")
T=mpimg.imread("../T_small.png")
G=mpimg.imread("../G_small.png")
C=mpimg.imread("../C_small.png")


for x in np.arange(-10,10,1):
	#												[left, right, bottom, top]
	panel2.imshow(A, aspect='auto', origin='upper', extent=[x,x+1,0,1])
	panel2.imshow(T, aspect='auto', origin='upper', extent=[x,x+1,1,1.5])
	panel2.imshow(G, aspect='auto', origin='upper', extent=[x,x+1,1.5,1.75])
	panel2.imshow(C, aspect='auto', origin='upper', extent=[x,x+1,1.75,2])

panel2.plot([2,2],[1,2], marker='o', markersize=5, mfc='black',mew=0, linewidth=0)
panel2.set_xlim(-10,10)
panel2.set_ylim(0,2)

#plt.savefig('Vollmers_Lecture1.png', dpi=300)
plt.show()