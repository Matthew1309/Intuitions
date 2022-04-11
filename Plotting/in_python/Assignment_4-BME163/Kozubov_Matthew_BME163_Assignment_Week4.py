import matplotlib.pyplot as plt 
import matplotlib.patches as mplpatches
import numpy as np 
import argparse
import time
# usage: python Assignment1.py -o firstAssignment.png
starttime = time.time()

parser=argparse.ArgumentParser()

# define your arguments
parser.add_argument('-i', '--input_file', default="BME163_Input_Data_3.txt")
parser.add_argument('-s', '--style_sheet', 'BME163')#default='C:\\Users\\mattk\\Desktop\\BME163\\Assignments\\BME163'
parser.add_argument('-o', '--output_file', default="Kozubov_Matthew_BME163_Assignment_Week4.png")

# there are multiple ways you can access your arguments
# you can put all of the arguments into one variable like this:
args = parser.parse_args()
# which can then be accessed like this:
input_file = args.input_file
style_sheet = args.style_sheet
output_file = args.output_file

plt.style.use(style_sheet)

#######################################################################
#######################################################################

figureWidth=7# inches
figureHeight=3 # inches

plt.figure(figsize=(figureWidth,figureHeight))

panelWidth=5
panelHeight=2
relativePanelWidth=panelWidth/figureWidth
relativePanelHeight=panelHeight/figureHeight


##########################################################################
########### Main panel placement #########################################

#             left,bottom,width,height
panel1=plt.axes([0.1,0.2,relativePanelWidth,relativePanelHeight])

panel1.tick_params(bottom=True, labelbottom=True,
	left=True, labelleft=True,
	right=False, labelright=False,
	top=False, labeltop=False)


xlim_low = 0.25 ; xlim_high = 11.75
ylim_low = 75 ; ylim_high = 100

panel1.set_xlim(xlim_low,xlim_high)
panel1.set_ylim(ylim_low,ylim_high)

xTickLabels = [ x for x in range(1,11)]
xTickLabels.append('>10')

panel1.set_xticks([x for x in range(1,12)])
panel1.set_xticklabels(xTickLabels)

panel1.set_xlabel(r'Subread Coverage')
panel1.set_ylabel(r'Identity %')

##########################################################################
########### Converting Figure distances into inches ######################
################## Pseudo-code ###########################################
"""
def pseudo-code():
	# The inital figureWidth and figureHeight variables are in inches.
	# Everything loaded in the .axes() is relative to that.

	# Therefore to get into inches we multiply the values we 
	# see by figureWidth and figureHeight

	# Therefore anything within a panel can be converted
	# back to inches by this simple multiplication.

	# A panel that is 1 by 1 has points at (0,0) and (0,1)

	# We can calculate the point to point distance using a function
	def eukDistance(coor1, coor2):
		'''Returns the Euclidean distance between any two n-dimensional points'''
		try:
			print(coor2[1] - coor1[1], coor2[0] - coor1[0])
			angle = np.arctan( (coor2[1] - coor1[1])/(coor2[0] - coor1[0]) ) *180/np.pi
		except ZeroDivisionError:
			if coor2[1] - coor1[1] > 0:
				angle = 270
			elif coor2[1] - coor1[1] < 0:
				angle = 90
			else:
				angle=None

		distance = np.sqrt( sum( (var2-var1)**2 for var1,var2 in zip(coor1,coor2) ) )

		return distance, angle

	# Because my current plot is between zero and 1 it is easy to
	# convert from plot to inches, just multiply whatever value I
	# have by my figure sizes.

	point1 = [1,1]
	point2 = [0,0]

	x = [1,0]
	y = [1,0]

	panelExample = panel1=plt.axes([0.5,0.5,relativePanelWidth,relativePanelHeight])
	panelExample.plot(x,y, marker='o')

	xlim_low = 0 ; xlim_high = 2
	ylim_low = 0 ; ylim_high = 100

	xscalar = xlim_high - xlim_low
	yscalar = ylim_high - ylim_low

	panelExample.set_xlim(xlim_low,xlim_high)
	panelExample.set_ylim(ylim_low,ylim_high)

	# In general I think imma need to break my distance into x and y
	# components, and divide each of those by the x and y limits to 
	# get stuff in terms of 1 unit, from there multiply each component
	# by their corresponding figureWidth or figureHeight to get inches.

	# The issue is how do I break my Euclidean distance into components.
	# Naw lets just do what we did above, but just return the components
	# way simpler

	def components(coor1, coor2):
		'''Returns the components as a list [x,y,z,...]'''
		return [ abs(var2-var1) for var1,var2 in zip(coor1,coor2) ]

	print(eukDistance(point1,point2 ))
	print(components(point1, point2))

	distances = components(point1, point2)

	# Okay now that I have the components of the distances
	# between two points, lets convert them into inches using our predefined scalars

	relativePanelXDistance = distances[0]/xscalar
	relativePanelYDistance = distances[1]/yscalar

	# This gets them between zero and one
	print(relativePanelXDistance, relativePanelYDistance)

	# Okay this looks like it works! Well now that we have
	# the relative panel distance lets convert it to 
	# inches by multiplying the relavent x,y by the panel sizes. 

	inchesPanelXDistance = relativePanelXDistance * panelWidth
	inchesPanelYDistance = relativePanelYDistance * panelHeight

	print(inchesPanelXDistance, inchesPanelYDistance)
	 
	# It doesn't actually matter how big the figure is lol

	# Okay lets put this all into a function


def distance_in_inches(point1, point2, panel,
					actualPanelHeight=panelHeight, actualPanelWidth=panelWidth):
	'''Returns the distance between two points on a panel in inches'''
	
	def components(coor1, coor2):
		'''Returns the components as a list [x,y,z,...]'''
		return [ abs(var2-var1) for var1,var2 in zip(coor1,coor2) ]
	def hypot(comp1, comp2):
		'''Returns the hypotenus'''
		return np.sqrt( comp1**2 + comp2**2 )

	#xscalar = xlim_high - xlim_low
	#yscalar = ylim_high - ylim_low

	xscalar = float(panel.viewLim.x1) - float(panel.viewLim.x0)
	yscalar = float(panel.viewLim.y1) - float(panel.viewLim.y0)

	distances = components(point1, point2)

	inchesPanelXDistance = distances[0]/xscalar * actualPanelWidth
	inchesPanelYDistance = distances[1]/yscalar * actualPanelHeight

	return hypot(inchesPanelYDistance, inchesPanelXDistance)

"""
##########################################################################
########### Parsing BME163_Input_Data_3 ##################################

groupNumber = []
YData = []

with open(input_file) as file:
	for i,line in enumerate(file.readlines()):
		bigName, numberICareAbout, others1, others2, other3 = line.split('\t')

		groupNumber.append( bigName.split('_')[3] )
		YData.append( numberICareAbout )


groupNumber = np.array(groupNumber, dtype=int) 
YData = np.array(YData, dtype=float)

indicies = YData.argsort()

sortedYData = YData[indicies]
sortedGroupNumber = groupNumber[indicies]



# groupNumber has the catagorical x-data 
# YData contains the actual numbers we care about

# Lets put the YData into a dictionary

catagoricalData = {1:[], 2:[], 3:[], 4:[], 5:[],
					6:[], 7:[], 8:[], 9:[], 10:[], 11:[]}


for i,number in enumerate(sortedGroupNumber):
	try:
		catagoricalData[sortedGroupNumber[i]].append(sortedYData[i])
	except KeyError:
		catagoricalData[11].append( sortedYData[i] )


##########################################################################
########### Lets enact the program for one catagory ######################
#
##########################################################################
########### Swarm class ##################################################
"""
class Custom_Swarm_Plot_old():
	def __init__(self, YData, XLocation, panel, actualPanelHeight=2, actualPanelWidth=5, markersize=1):
		self.YData = sorted( YData )
		self.XLocation = XLocation
		self.panel = panel
		self.actualPanelHeight = actualPanelHeight
		self.actualPanelWidth = actualPanelWidth
		self.markersize = markersize

		self.minDist = markersize/72
		self.pointShift = self.minDist/5

	def distance_in_inches(self, point1, point2):
		'''Returns the distance between two points on a panel in inches'''
	
		def components(coor1, coor2):
			'''Returns the components as a list [x,y,z,...]'''
			return [ abs(var2-var1) for var1,var2 in zip(coor1,coor2) ]
		def hypot(comp1, comp2):
			'''Returns the hypotenus'''
			return np.sqrt( comp1**2 + comp2**2 )

		#xscalar = xlim_high - xlim_low
		#yscalar = ylim_high - ylim_low

		xscalar = float(self.panel.viewLim.x1) - float(self.panel.viewLim.x0)
		yscalar = float(self.panel.viewLim.y1) - float(self.panel.viewLim.y0)

		distances = components(point1, point2)

		inchesPanelXDistance = distances[0]/xscalar * self.actualPanelWidth
		inchesPanelYDistance = distances[1]/yscalar * self.actualPanelHeight

		return hypot(inchesPanelYDistance, inchesPanelXDistance)

	def which_points_to_check2(self, xcoor, listOfPlacedPoints):
		'''Returns a list in the shape of [(),(),()...]'''
		superRelevantPointList = []
		for relevantPoint in listOfPlacedPoints:
				if self.distance_in_inches( (xcoor,0), (relevantPoint[0],0) ) < self.minDist:
					superRelevantPointList.append(relevantPoint)

		return superRelevantPointList


	def which_points_to_check(self, ycoor, listOfPlacedPoints):
		'''Returns a list in the shape of [(),(),()...]'''
		relevantPointList = []
		for point2 in listOfPlacedPoints:
			if self.distance_in_inches( (0,ycoor), (0,point2[1]) ) < self.minDist:
				relevantPointList.append(point2)

		return relevantPointList

	def data_for_plotting(self):
		# populate the pointsList with our first point
		pointYList = [self.YData.pop()]
		# populate the pointsList with our first point
		pointXList = [self.XLocation]

		# loop through points
		for i, yCoor in enumerate(self.YData):
			
			xCoor = self.XLocation
			xCoor1 = xCoor
			xCoor2 = xCoor

			relevantPointList = self.which_points_to_check( yCoor, zip(pointXList, pointYList))
			relevantPointList1 = self.which_points_to_check2( xCoor1, relevantPointList )
			relevantPointList2 = self.which_points_to_check2( xCoor2, relevantPointList )
			#if i == 50:
			#	break
			#	print( yCoor, len(relevantPointList) ) 

			while any( [self.distance_in_inches( pt, (xCoor1, yCoor) ) < self.minDist for pt in relevantPointList1] ) \
					and \
					any( [self.distance_in_inches( pt, (xCoor2, yCoor) ) < self.minDist for pt in relevantPointList2] ):
				xCoor1 += self.pointShift
				xCoor2 -= self.pointShift
				relevantPointList1 = self.which_points_to_check2( xCoor1, relevantPointList )
				relevantPointList2 = self.which_points_to_check2( xCoor2, relevantPointList )

			if any( [self.distance_in_inches( pt, (xCoor1, yCoor) ) < self.minDist for pt in relevantPointList1] ):
				xCoor = xCoor2
			else:
				xCoor = xCoor1

			pointYList.append(yCoor)
			pointXList.append(xCoor)

		return pointXList, pointYList

	def __str__(self):
		return "Data for column {0}".format( self.XLocation )
"""

class Custom_Swarm_Plot():
	def __init__(self, YData, XLocation, panel, actualPanelHeight=2, actualPanelWidth=5, markersize=1):
		self.YData = sorted( YData )
		self.XLocation = XLocation
		self.panel = panel
		self.actualPanelHeight = actualPanelHeight
		self.actualPanelWidth = actualPanelWidth
		self.markersize = markersize

		self.minDist = markersize/72
		self.pointShift = self.minDist/5


		self.xscalar = float(self.panel.viewLim.x1) - float(self.panel.viewLim.x0)
		self.yscalar = float(self.panel.viewLim.y1) - float(self.panel.viewLim.y0)

	def distance_in_inches(self, point1, point2):
		'''Returns the distance between two points on a panel in inches'''
		inchesPanelXDistance = (point1[0]-point2[0])/self.xscalar * self.actualPanelWidth
		inchesPanelYDistance = (point1[1]-point2[1])/self.yscalar * self.actualPanelHeight

		return np.sqrt(inchesPanelYDistance**2 + inchesPanelXDistance**2)

	def which_points_to_check(self, ycoor, listOfPlacedPointsY, listOfPlacedPointsX):
		'''Returns a list in the shape of [(),(),()...]'''
		relevantPointList = []
		for i,point in enumerate(listOfPlacedPointsY):
			if abs( (ycoor-point)/self.yscalar * self.actualPanelHeight ) < self.minDist:
				relevantPointList.append( (listOfPlacedPointsX[i],point))
			#else:
			#	break

		return relevantPointList

	def data_for_plotting(self):
		# populate the pointsList with our first point
		pointYList = [self.YData.pop()]
		# populate the pointsList with our first point
		pointXList = [self.XLocation]

		lenRelevant = 0
		lenWhole = 0
		# loop through points
		for yCoor in self.YData:
			
			xCoor = self.XLocation
			xCoor1 = xCoor
			xCoor2 = xCoor

			relevantPointList = self.which_points_to_check( yCoor, pointYList, pointXList )

			#print(len(relevantPointList), len(pointYList))
			lenRelevant += len(relevantPointList)
			lenWhole += len(pointYList)

			while any( self.distance_in_inches( pt, (xCoor1, yCoor) ) < self.minDist for pt in relevantPointList ) \
					and \
					any( self.distance_in_inches( pt, (xCoor2, yCoor) ) < self.minDist for pt in relevantPointList ):
				xCoor1 += self.pointShift
				xCoor2 -= self.pointShift

			if any( self.distance_in_inches( pt, (xCoor1, yCoor) ) < self.minDist for pt in relevantPointList ):
				xCoor = xCoor2
			else:
				xCoor = xCoor1

			pointYList.append(yCoor)
			pointXList.append(xCoor)
		#print(lenRelevant, lenWhole)

		return pointXList, pointYList

	def __str__(self):
		return "Data for column {0}".format( self.XLocation )
def custom_boxplot(YData, panel, XLocation=1, actualPanelHeight=2, actualPanelWidth=5, width=0.8):
		median = np.median(YData)
		panel.plot([XLocation-width/2, XLocation+width/2], (median, median), linewidth=1, color='red')



def plotSwarm(subsetSize=1000):
	for catagory, Ydata in catagoricalData.items():
		markerSize = 0.55

		try:
			YData1 = list( np.random.choice(Ydata,subsetSize,replace=False) )#catagoricalData[1]#[0::300]
		except ValueError:
			print("listToLong")
			YData1 = list( np.random.choice(Ydata,len(Ydata),replace=False) )
		YData1.sort()
		
		swarmPlotObject = Custom_Swarm_Plot(YData=YData1, XLocation=catagory , markersize=markerSize,panel=panel1)
		print(swarmPlotObject)

		starttime = time.time()
		pointXList,pointYList = swarmPlotObject.data_for_plotting()
		endtime = time.time()
		print(endtime-starttime)

		panel1.plot(pointXList,pointYList, marker='o', linewidth=0, markersize=markerSize, markeredgewidth=0, color=(0,0,0))
		custom_boxplot(YData1, panel1, XLocation=catagory)


plotSwarm()
dataMedian = 95
panel1.plot([xlim_low, xlim_high], 2*[dataMedian], dashes=[1,2,2,2], lw=0.5, c=(0,0,0))


##########################################################################
########### Printing stuff ###############################################


plt.savefig(output_file, dpi=600)
#plt.show()

