import matplotlib.pyplot as plt 
import matplotlib.patches as mplpatches
import numpy as np 
import argparse
# usage: python Assignment1.py -o firstAssignment.png

parser=argparse.ArgumentParser()

# define your arguments
parser.add_argument('-i', '--input_file')
parser.add_argument('-s', '--style_sheet', default='BME163')
parser.add_argument('-o', '--output_file', default="pwetty_wainbow_gwid.png")

# there are multiple ways you can access your arguments
# you can put all of the arguments into one variable like this:
args = parser.parse_args()
# which can then be accessed like this:
input_file = args.input_file
style_sheet = args.style_sheet
output_file = args.output_file

plt.style.use(style_sheet)


figureWidth=3.42
figureHeight=2

plt.figure(figsize=(figureWidth,figureHeight))

panelWidth=1
panelHeight=1

relativePanelWidth=panelWidth/figureWidth
relativePanelHeight=panelHeight/figureHeight

##########################################################################
########### panel 1 ######################################################

#             left,bottom,width,height
panel1=plt.axes([0.1,0.2,relativePanelWidth,relativePanelHeight])

panel1.tick_params(bottom=False, labelbottom=False,
	left=False, labelleft=False,
	right=False, labelright=False,
	top=False, labeltop=False)


number_of_dots=25
xList=[np.cos(x) for x in np.linspace(start=0,stop=np.pi/2, num=number_of_dots)]
yList=[np.sin(x) for x in np.linspace(start=0,stop=np.pi/2, num=number_of_dots)]

for x,y in zip(xList,yList):
	panel1.plot(x,y,marker='o',markerfacecolor=(x,x,x),
		markeredgecolor='black', markersize=2, markeredgewidth=0,
		linewidth=0)



##########################################################################
########### panel 2 ######################################################

panel2=plt.axes([0.55,0.2,relativePanelWidth,relativePanelHeight])


panel2.tick_params(bottom=False, labelbottom=False,
	left=False, labelleft=False,
	right=False, labelright=False,
	top=False, labeltop=False)

number_of_squares = 10
rectangeWidth = 1/number_of_squares
rectangeHeight = 1/number_of_squares
for x in np.linspace(0,0.9,number_of_squares):
	for y in np.linspace(0,0.9,number_of_squares):          
		rectangle=mplpatches.Rectangle( [x,y],rectangeWidth,rectangeHeight,
			facecolor=( x,y,1 ),
			edgecolor='black',
			linewidth=1)
		panel2.add_patch(rectangle)


panel2.set_xlim(0,1)
panel2.set_ylim(0,1)


##########################################################################
########### Printing stuff ###############################################

plt.savefig(output_file, dpi=600)
#plt.show()