import matplotlib.pyplot as plt 
import matplotlib.patches as mplpatches
import numpy as np 
import argparse
# usage: python Assignment1.py -o firstAssignment.png

parser=argparse.ArgumentParser()

# define your arguments
parser.add_argument('-i', '--input_file', default="BME163_Input_Data_1.txt")
parser.add_argument('-s', '--style_sheet', default='BME163')#'C:\\Users\\mattk\\Desktop\\BME163\\Assignments\\BME163'
parser.add_argument('-o', '--output_file', default="Kozubov_Matthew_BME163_Assignment_Week2.png")

# there are multiple ways you can access your arguments
# you can put all of the arguments into one variable like this:
args = parser.parse_args()
# which can then be accessed like this:
input_file = args.input_file
style_sheet = args.style_sheet
output_file = args.output_file

plt.style.use(style_sheet)


figureWidth=5
figureHeight=2

plt.figure(figsize=(figureWidth,figureHeight))

panelWidth=1
panelHeight=1
relativePanelWidth=panelWidth/figureWidth
relativePanelHeight=panelHeight/figureHeight

sidePanelWidth = 0.25
sidePanelHeight = 1
relativeSidePanelWidth=sidePanelWidth/figureWidth
relativeSidePanelHeight=sidePanelHeight/figureHeight

topPanelWidth = 1
topPanelHeight = 0.25
relativeTopPanelWidth=topPanelWidth/figureWidth
relativeTopPanelHeight=topPanelHeight/figureHeight


##########################################################################
########### Main panel placement #########################################

#             left,bottom,width,height
panel1=plt.axes([0.14,0.15,relativePanelWidth,relativePanelHeight])
panel2=plt.axes([0.54,0.15,relativePanelWidth,relativePanelHeight])

for panel in [panel1,panel2]:
	panel.tick_params(bottom=True, labelbottom=True,
		left=False, labelleft=False,
		right=False, labelright=False,
		top=False, labeltop=False)

	panel.set_xlim(0,15)
	panel.set_ylim(0,15)

##########################################################################
########### side panel placement #########################################

#             left,bottom,width,height
sidePanel1=plt.axes([0.076,0.15,relativeSidePanelWidth,relativeSidePanelHeight])
sidePanel2=plt.axes([0.476,0.15,relativeSidePanelWidth,relativeSidePanelHeight])

for panel in [sidePanel1,sidePanel2]:
	panel.tick_params(bottom=True, labelbottom=True,
		left=True, labelleft=True,
		right=False, labelright=False,
		top=False, labeltop=False)

	panel.set_xlim(20,0)
	panel.set_ylim(0,15)

##########################################################################
########### top panel placement ##########################################

#             left,bottom,width,height
topPanelBottom = 0.685
topPanel1=plt.axes([0.14,topPanelBottom,relativeTopPanelWidth,relativeTopPanelHeight])
topPanel2=plt.axes([0.54,topPanelBottom,relativeTopPanelWidth,relativeTopPanelHeight])

for panel in [topPanel1,topPanel2]:
	panel.tick_params(bottom=False, labelbottom=False,
		left=True, labelleft=True,
		right=False, labelright=False,
		top=False, labeltop=False)

	panel.set_xlim(0,15)
	panel.set_ylim(0,20)

##########################################################################
########### Parsing BME163_Input_Data_1 ##################################

runXData = []
runYData = []
with open(input_file) as file:
	for i,line in enumerate(file.readlines()):
		runXData.append(np.log2(int(line.rstrip().split('\t')[1]) + 1))
		runYData.append(np.log2(int(line.rstrip().split('\t')[2]) + 1))

##########################################################################
########### Plotting main panel ##########################################

panel1.scatter(runXData,runYData,marker='o',
		s=2, c=[(0,0,0)], alpha=0.1, linewidth=0)

##########################################################################
########### Plotting top panel ###########################################

topHist = np.histogram(runXData, np.arange(0,15.5,0.5))
heights = [np.log2(x+1) for x in topHist[0]]
bins = topHist[1]
#print(heights)

#loops 30 times
for i in range( 0,len(heights) ):
	bottom = 0
	left = bins[i]
	width = bins[i+1] - left
	height = heights[i]

	#print(f'[{left},{bottom}],{width} ,{height}')
	rectangle=mplpatches.Rectangle( [left,bottom],width,height,
			facecolor=( 0.5,0.5,0.5 ),
			edgecolor='black',
			linewidth=.1)
	topPanel1.add_patch(rectangle)
	rectangle=mplpatches.Rectangle( [left,bottom],width,height,
		facecolor=( 0.5,0.5,0.5 ),
		edgecolor='black',
		linewidth=.1)
	topPanel2.add_patch(rectangle)

##########################################################################
########### Plotting side panel ##########################################

topHist = np.histogram(runYData, np.arange(0,15.5,0.5))
heights = [np.log2(x+1) for x in topHist[0]]
bins = topHist[1]
#print(heights)

#loops 30 times
for i in range( 0,len(heights) ):
	bottom = bins[i]
	left = 0
	width = heights[i]
	height = bins[i+1] - bottom

	#print(f'[{left},{bottom}],{width} ,{height}')
	rectangle=mplpatches.Rectangle( [left,bottom],width,height,
			facecolor=( 0.5,0.5,0.5 ),
			edgecolor='black',
			linewidth=.1)
	sidePanel1.add_patch(rectangle)
	rectangle=mplpatches.Rectangle( [left,bottom],width,height,
			facecolor=( 0.5,0.5,0.5 ),
			edgecolor='black',
			linewidth=.1)
	sidePanel2.add_patch(rectangle)

##########################################################################
########### Panel 2 heatmap guide ########################################

# making the color label panel
#             		left,bottom,width,height
colorPanel=plt.axes([0.8,0.15,0.4*relativeSidePanelWidth,relativeSidePanelHeight])
colorPanel.tick_params(bottom=False, labelbottom=False,
						left=True, labelleft=True,
						right=False, labelright=False,
						top=False, labeltop=False)
colorPanel.set_yticks([0,10,20])
colorPanel.set_yticklabels(['0','10','>20'])

numberOfBlocks = 20
colorPanel.set_xlim(0,1)
colorPanel.set_ylim(0,numberOfBlocks)

for i in range(0,numberOfBlocks+1):

	rectangle=mplpatches.Rectangle( [0,i],1,1,
		facecolor=( (20-i)/20, (20-i)/20, (20-i)/20 ),
		edgecolor='black',
		linewidth=0)
	colorPanel.add_patch(rectangle)

##########################################################################
########### Panel 2 heatmap plot #########################################


def custom2DHisto(yAxis, xAxis, resolution=50, xLength=15, yLength=0):
	''' 
	Perform the 1D histogram binning to get the ranges. 
	Loop through data and assign each pair of points 
	to a box counter
		  x---x---x
		y 5   0   0
		|
		y 8   9   2
		|
		y 3   0   5
	Return this list of lists to be looped over in a double 
	for loop, also give x and y dimensions of the squares.

	return listOfLists, xDim, yDim
	'''

	if not yLength:
		yLength=xLength
	numberOfBlocks = xLength
	resolution=resolution+1

	xDim = np.linspace(0,xLength)[0]
	yDim = np.linspace(0,yLength)[0]

	xHeights,xBins = np.histogram(xAxis, np.linspace(0,numberOfBlocks,resolution))
	yHeights,yBins = np.histogram(runYData, np.linspace(0,numberOfBlocks,resolution))

	listOfCounts = [[0 for i in range( len(xBins)) ] for j in range( len(yBins) )]


	# Want to iterate over the x,y dataset together and put them into the appropriate bins.
	for x,y in zip(xAxis, yAxis):
		whereToCount = [0,0]
		# Looking through the xBins to see where the x-coor belongs
		for i, xDivider in enumerate(xBins):
			# trick is we would place into i-1 position of listOfCounts
			if x < xDivider:
				whereToCount[0] = i-1
				break
			elif x == xDivider and i == len(xBins)-1:
				whereToCount[0] = i-1
				break
			elif x == xDivider:
				whereToCount[0] = i
				break

		# Looking through the yBins to see where teh y-coor belongs
		for i, yDivider in enumerate(yBins):
			# trick is we would place into i-1 position of listOfCounts
			if y < yDivider:
				whereToCount[1] = i-1
				break
			elif y == yDivider and i == len(xBins)-1:
				whereToCount[1] = i-1
				break
			elif y == yDivider:
				whereToCount[1] = i
				break

		# increment the number of points in this square
		listOfCounts[ whereToCount[0] ][ whereToCount[1] ] += 1


	return (listOfCounts, xDim, yDim, xBins, yBins, xHeights, yHeights)

	
dataForPlotting, xDim, yDim, xBins, yBins, xHeights, yHeights = custom2DHisto(runYData, runXData, resolution=60)

for i in range(0,len(xHeights)):
	for j in range(0,len(yHeights)):
		bottom = yBins[j]
		left = xBins[i]
		width = xBins[i+1]-left
		height = yBins[j+1]-bottom

		if dataForPlotting[i][j] > 20:
			colorTuple = (0,0,0)
		else:
			thing = ( 20-dataForPlotting[i][j] )/20
			colorTuple = (thing,thing,thing)

		rectangle=mplpatches.Rectangle( [left,bottom],width,height,
				facecolor=colorTuple,
				edgecolor='black',
				linewidth=0)
		panel2.add_patch(rectangle)

##########################################################################
########### Printing stuff ###############################################

plt.savefig(output_file, dpi=600)
#plt.show()