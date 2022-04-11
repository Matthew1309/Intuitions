import matplotlib.pyplot as plt 
import matplotlib.patches as mplpatches
import numpy as np 
import argparse
import time
import os
import matplotlib.image as mplimage
# usage: python Assignment1.py -o firstAssignment.png
starttime = time.time()

parser=argparse.ArgumentParser()

# define your arguments
parser.add_argument('-i', '--input_file', default="BME163_Input_Data_4.txt")#BME163_Input_Data_4.txt
parser.add_argument('-s', '--style_sheet', default='BME163')#'C:\\Users\\mattk\\Desktop\\BME163\\Assignments\\BME163')#
parser.add_argument('-o', '--output_file', default="Kozubov_Matthew_BME163_Assignment_Week6.png")

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

figureWidth=5# inches
figureHeight=3 # inches

plt.figure(figsize=(figureWidth,figureHeight))

panelWidth=0.75
panelHeight=2.5

relativePanelWidth=panelWidth/figureWidth
relativePanelHeight=panelHeight/figureHeight


##########################################################################
########### Panel 1 placement ############################################

#             left,bottom,width,height
panel1=plt.axes([0.1,0.1,relativePanelWidth,relativePanelHeight])

panel1.tick_params(bottom=True, labelbottom=True,
	left=True, labelleft=True,
	right=False, labelright=False,
	top=False, labeltop=False)

xlim_low = -1.5 ; xlim_high = 22.5
ylim_low = 0 ; ylim_high = 1262

panel1.set_xlim(xlim_low,xlim_high)
panel1.set_ylim(ylim_low,ylim_high)

xTicks = [3*x for x in range(0,8)]
yTicks = [200*x for x in range(0,7)]

panel1.set_xticks(xTicks)
panel1.set_yticks(yTicks)

xTickLabels = [0,'',6,'',12,'',18]

panel1.set_xticklabels(xTickLabels)

panel1.set_xlabel('CT')
panel1.set_ylabel(r'Number of genes')



##########################################################################
################## Data Reader ###########################################
datatable = []
sortby = []
with open(input_file, 'r') as inFile:

	colNames = inFile.readline()

	for line in inFile.readlines():
		dataline = np.array( line.split('\t')[4:12], dtype=int )
		normalized_dataline = 100*( (np.array(dataline, dtype=int) - int(min(dataline)))/(int(max(dataline)) - int(min(dataline))) )
		#print( list(normalized_dataline) )
		#normalized_dataline = np.append( normalized_dataline, float(line.split('\t')[13]))

		datatable.append(list(normalized_dataline))
		sortby.append( float(line.split('\t')[13] ))
		#print(list( normalized_dataline) )
		#break

	sorted_datatable = [dataline for dataline, sort_el in sorted(zip(datatable, sortby), key=lambda pair: pair[1], reverse=True)]
#sorted_datatable = sorted(datatable, key=lambda x: x[-1], reverse=True)
#print(sorted_datatable[0])

yellow=[255/255,225/255,40/255]
blue=[56/255,66/255,157/255]

R=np.linspace(yellow[0], blue[0], 101)
G=np.linspace(yellow[1], blue[1], 101)
B=np.linspace(yellow[2], blue[2], 101)

bottom = ylim_low
left = xlim_low

bottom_change = 1
left_change = 3


for row in sorted_datatable:
	left = xlim_low
	#row = row[0:-1]
	#print(row)

	for column in row:
		#print(type(column))
		column = int(column)
		rectangle=mplpatches.Rectangle( [left,bottom],3,1,
			facecolor=( R[column],G[column],B[column] ),
			edgecolor='black',
			linewidth=0)
		panel1.add_patch(rectangle)

		left += left_change
	bottom += bottom_change


##########################################################################
########### Printing stuff ###############################################


plt.savefig(output_file, dpi=600)
#plt.show()

