import matplotlib.pyplot as plt 
import matplotlib.patches as mplpatches
import numpy as np 
import time
import scipy.stats as stats


plt.style.use('C:\\Users\\mattk\\Desktop\\BME163\\Assignments\\BME163')


def permutationTest(yList1, yList2):
	'''Perform MC permutation test to see if two distributions are different'''
	difference = np.abs( np.average(yList1) - np.average(yList2) )
	combinedList = np.concatenate((yList1, yList2), axis=None)
	bigger=0
	for iteration in range(0,10000,1):
		np.random.shuffle(combinedList)
		newList1 = combinedList[:len(yList1)]
		newList2 = combinedList[len(yList1):]
		newDifference = np.abs( np.average(newList1) - np.average(newList2) )
		if newDifference >= difference:
			bigger+=1
	print(iteration)
	return bigger/(iteration+1)


figureWidth=10
figureHeight=5

plt.figure(figsize=(figureWidth,figureHeight))


panelWidth=5
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

#mean,std,number of points
xList=np.random.normal(120,20,10000)
yList1=np.random.normal(120,20,10000)
yList2=xList
yList3=xList**10
yList4=np.sin(xList)
yList5 = np.random.normal(30,20,10000)
yList6 = np.concatenate([yList1,yList5],axis=None)
yList7 = np.random.normal(125,100,20000)
yList8 = np.random.normal(125,100,20000)

panel2=plt.axes([0.2,0.5,relativePanelWidth,relativePanelHeight])
xmin = 0; xmax=10
ymin=min(yList6)*1.1; ymax=max(yList6) * 1.1


panel2.boxplot([yList6, yList7, yList8],positions=[5, 6, 7],widths=0.5)
vp=panel2.violinplot([yList6, yList7, yList8],positions=[5,6,7],widths=0.5)
for body in vp['bodies']:
	body.set(facecolor='grey',edgecolor='black',linewidth=0.5,alpha=0.5)
for lines in ['cmaxes', 'cmins', 'cbars']:
	vp[lines].set(linewidth=0)

print(np.average(yList6), np.average(yList8))
for x in range(0,10):
	print(permutationTest(yList6, yList8))



panel2.set_xlim(xmin,xmax)
panel2.set_ylim(ymin,ymax)

#plt.savefig('Vollmers_Lecture1.png', dpi=300)
#plt.show()