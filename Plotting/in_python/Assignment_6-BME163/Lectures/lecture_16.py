import matplotlib.pyplot as plt 
import matplotlib.patches as mplpatches
import numpy as np 
import matplotlib.image as mpimg


plt.style.use('C:\\Users\\mattk\\Desktop\\BME163\\Assignments\\BME163')

figureWidth=4
figureHeight=4

plt.figure(figsize=(figureWidth,figureHeight))


panelWidth=3
panelHeight=3

relativePanelWidth=panelWidth/figureWidth
relativePanelHeight=panelHeight/figureHeight


#             left,bottom,width,height
panel1=plt.axes([0.1,0.1,relativePanelWidth,relativePanelHeight])

def plot_triangle(point1, point2, point3, color=(0,0,0)):
	xList = np.linspace(point2[0],point2[0],500)
	yList = np.linspace(point2[1], point3[1], 500)

	for index in np.arange(0, len(xList), 1):
		xvalue = xList[index]
		yvalue = yList[index]
		panel1.plot([xvalue, point1[0]], [yvalue,point1[1]],
			marker='o',
			markerfacecolor=color,
			markeredgecolor='black',
			markersize=0,
			markeredgewidth=0,
			color=color,
			linewidth=0.25)

point1 = (0,3)
point2 = (4,7)
point3 = (9,9)

color = (58/255,66/255,156/255)

point4=(3,1)
point5=(5,5)
point6=(8,8)

plot_triangle(point1, point2, point3, color)
plot_triangle(point4, point5, point6, "black")

panel1.tick_params(bottom=False, labelbottom=False,
	left=False, labelleft=False,
	right=False, labelright=False,
	top=False, labeltop=False)

#plt.savefig('Vollmers_Lecture1.png', dpi=300)
plt.show()