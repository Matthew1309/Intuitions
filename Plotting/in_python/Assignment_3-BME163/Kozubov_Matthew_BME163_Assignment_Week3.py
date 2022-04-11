import matplotlib.pyplot as plt 
import matplotlib.patches as mplpatches
import numpy as np 
import argparse
# usage: python Assignment1.py -o firstAssignment.png

parser=argparse.ArgumentParser()

# define your arguments
parser.add_argument('-i', '--input_file', default="BME163_Input_Data_2.txt")
parser.add_argument('-s', '--style_sheet', default='C:\\Users\\mattk\\Desktop\\BME163\\Assignments\\BME163')#'BME163'
parser.add_argument('-o', '--output_file', default="Kozubov_Matthew_BME163_Assignment_Week3.png")

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

figureWidth=3
figureHeight=3

plt.figure(figsize=(figureWidth,figureHeight))

panelWidth=2
panelHeight=2
relativePanelWidth=panelWidth/figureWidth
relativePanelHeight=panelHeight/figureHeight


##########################################################################
########### Main panel placement #########################################

#             left,bottom,width,height
panel1=plt.axes([1/6,1/6,relativePanelWidth,relativePanelHeight])


panel1.tick_params(bottom=True, labelbottom=True,
	left=True, labelleft=True,
	right=False, labelright=False,
	top=False, labeltop=False)

panel1.set_xlim(-12,12)
panel1.set_ylim(0,60)

panel1.set_xticks([-10,-5,0,5,10])

panel1.set_xlabel(r'log$_\mathrm{2}$(fold change)')
panel1.set_ylabel(r'-log$_\mathrm{10}$(p-value)')

#
##########################################################################
########### Parsing BME163_Input_Data_1 ##################################

geneName = []
runXData = []
runYData = []
with open(input_file) as file:
	for i,line in enumerate(file.readlines()):
		gene = line.rstrip().split('\t')[0]
		log2 = line.rstrip().split('\t')[1] 
		log10 = line.rstrip().split('\t')[2]
		
		geneName.append(gene)
		if log2 == 'NA':
			runXData.append(0.)
		else:
			runXData.append( float(log2) )

		if log10 == 'NA':
			runYData.append(1.)
		else:
			runYData.append( float(log10) )

runXData = np.array(runXData, dtype=float)
runYData = np.array(runYData, dtype=float)

runYData = -np.log10(runYData)


##########################################################################
########### Getting black and red points #################################
runXBlackData = []
runYBlackData = []

runXRedData = []
runYRedData = []

for i,x in enumerate( zip(runYData,runXData,geneName) ):
	y,x,name = x
	if 2**np.abs(x) > 10 and (y > 8):
		runXRedData.append( runXData[i] )
		runYRedData.append( runYData[i] )

	if x < np.log2(10) and (y > 30):
		panel1.text(x,y,'{0} '.format(name), va='center', ha='right', fontsize = 6)
	else:
		runXBlackData.append( runXData[i] )
		runYBlackData.append( runYData[i] )


##########################################################################
########### Plotting main panel ##########################################

panel1.scatter(runXBlackData,runYBlackData,marker='o',
		s=2, c=[(0,0,0)], linewidth=0)

panel1.scatter(runXRedData,runYRedData,marker='o',
		s=2, c=[(1,0,0)], linewidth=0)


##########################################################################
########### Printing stuff ###############################################

plt.savefig(output_file, dpi=600)
#plt.show()