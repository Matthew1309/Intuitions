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
parser.add_argument('-i', '--input_file', default="Splice_Sequences.fasta")#BME163_Input_Data_4.txt
parser.add_argument('-s', '--style_sheet', default='BME163')#'C:\\Users\\mattk\\Desktop\\BME163\\Assignments\\BME163')
parser.add_argument('-o', '--output_file', default="Kozubov_Matthew_BME163_Assignment_Week5.png")
parser.add_argument('-p', '--pngs', default="bases\\")

# there are multiple ways you can access your arguments
# you can put all of the arguments into one variable like this:
args = parser.parse_args()
# which can then be accessed like this:
input_file = args.input_file
style_sheet = args.style_sheet
output_file = args.output_file
basesDirectory = args.pngs
A = ''
C = ''
G = ''
T = ''
for filename in os.listdir(basesDirectory):
	path_to_file = os.path.join(basesDirectory, filename)
	if filename[0] == 'A':
		A = mplimage.imread(path_to_file)
	elif filename[0] == 'C':
		C = mplimage.imread(path_to_file)
	elif filename[0] == 'G':
		G = mplimage.imread(path_to_file)
	elif filename[0] == 'T':
		T = mplimage.imread(path_to_file)
	else:
		pass
plt.style.use(style_sheet)

#######################################################################
#######################################################################

figureWidth=6# inches
figureHeight=3 # inches

plt.figure(figsize=(figureWidth,figureHeight))

panelWidth=2.4
panelHeight=1
relativePanelWidth=panelWidth/figureWidth
relativePanelHeight=panelHeight/figureHeight


##########################################################################
########### Panel 1 placement ############################################

#             left,bottom,width,height
panel1=plt.axes([0.0835,0.3,relativePanelWidth,relativePanelHeight])

panel1.tick_params(bottom=True, labelbottom=True,
	left=True, labelleft=True,
	right=False, labelright=False,
	top=False, labeltop=False)

xlim_low = -10 ; xlim_high = 10
ylim_low = 0 ; ylim_high = 2

panel1.set_xlim(xlim_low,xlim_high)
panel1.set_ylim(ylim_low,ylim_high)

xTickLabels = [-10, -5, 0, 5, 10]

panel1.set_xticks(xTickLabels)
#panel1.set_xticklabels(xTickLabels)

panel1.set_xlabel('Distance to\nSplice Site')
panel1.set_ylabel(r'Bits')

panel1.set_title("5'SS")

#Centerline
panel1.plot(2*[(xlim_low+xlim_high)/2],[ylim_low, ylim_high], c=(0,0,0), lw=0.51)

##########################################################################
########### Panel 2 placement ############################################

panel2=plt.axes([0.5665,0.3,relativePanelWidth,relativePanelHeight])

panel2.tick_params(bottom=True, labelbottom=True,
	left=False, labelleft=False,
	right=False, labelright=False,
	top=False, labeltop=False)


panel2.set_xlim(xlim_low,xlim_high)
panel2.set_ylim(ylim_low,ylim_high)

xTickLabels = [-10, -5, 0, 5, 10]

panel2.set_xticks(xTickLabels)
#panel1.set_xticklabels(xTickLabels)

panel2.set_xlabel('Distance to\nSplice Site')

panel2.set_title("3'SS")

#Center line
panel2.plot(2*[(xlim_low+xlim_high)/2],[ylim_low, ylim_high], c=(0,0,0), lw=0.51)

##########################################################################
################## Fasta Reader ##########################################
splice_junctions = {'5':[], '3':[]}
cooler_splice_junctions = {'5': {'-10':[], '-9':[],
								'-8':[], '-7':[],
								'-6':[], '-5':[],
								'-4':[], '-3':[],
								'-2':[], '-1':[],
								'0':[], '1':[],
								'2':[], '3':[],
								'4':[], '5':[],
								'6':[], '7':[],
								'8':[], '9':[],
								'10':[]	}, 
							'3':{'-10':[], '-9':[],
								'-8':[], '-7':[],
								'-6':[], '-5':[],
								'-4':[], '-3':[],
								'-2':[], '-1':[],
								'0':[], '1':[],
								'2':[], '3':[],
								'4':[], '5':[],
								'6':[], '7':[],
								'8':[], '9':[] } }

position_list = ['-10', '-9', '-8', '-7', '-6', '-5', '-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

with open(input_file, 'r') as fastaFile:

	header = fastaFile.readline()
	sequence = ''

	for line in fastaFile.readlines():
		if line[0] != '>':
			sequence += line.rstrip()
			for position,base in enumerate(sequence):
				cooler_splice_junctions[header[1]][str(position-10)].append(base)
		else:
			splice_junctions[header[1]].append(sequence)
			header = line
			sequence = ''


##########################################################################
########### Sequence logo math ###########################################
# The y-axis math thank you wikipedia "Sequence Logos"
# Ri = log2(4) - (Hi + en)
# 	Hi = -sum( baseFreq * log2(baseFreq) )
# 	en = small-sample correction
#		en = 1/ln2 * 3/(2*#ofsequences)

# Finally the Height of the letters is
# height = baseFreq * Ri
##########################################################################
##########################################################################

number_of_sequences = len(cooler_splice_junctions['5']['-10'])
en = ( 1/np.log(2) ) * ( 3/(2*number_of_sequences) )

heights_of_letters_5 = []
#every item is a position, within are 4 values for heights
#of letters in alphabetical order: A,C,G,T
for position in position_list:
	position_heights = []
	Hi = 0
	baseFreq_list = []
	for base in ['A','C','G','T']:
		baseFreq = cooler_splice_junctions['5'][position].count(base)/number_of_sequences
		baseFreq_list.append(baseFreq)
		Hi += baseFreq * np.log2(baseFreq)
	Hi = -Hi
	Ri = np.log2(4) - (Hi + en)
	baseFreq_list = list( np.array(baseFreq_list, dtype=float) * Ri )
	heights_of_letters_5.append(baseFreq_list)


number_of_sequences = len(cooler_splice_junctions['3']['-10'])
heights_of_letters_3 = []
#every item is a position, within are 4 values for heights
#of letters in alphabetical order: A,C,G,T
for position in position_list:
	position_heights = []
	Hi = 0
	baseFreq_list = []
	for base in ['A','C','G','T']:
		baseFreq = cooler_splice_junctions['3'][position].count(base)/number_of_sequences
		baseFreq_list.append(baseFreq)
		Hi += baseFreq * np.log2(baseFreq)
	Hi = -Hi
	Ri = np.log2(4) - (Hi + en)
	baseFreq_list = list( np.array(baseFreq_list, dtype=float) * Ri )
	heights_of_letters_3.append(baseFreq_list)

##########################################################################
########### Lets make the sequence logos I suppose #######################
# Structure of heights_of_letters_*
# -position
# 	-A,C,G,T
BASES = [A,C,G,T]

startLeft = xlim_low
x_move = (abs(xlim_low) + abs(xlim_high)) / len(position_list)
startRight = startLeft+x_move
startBottom = ylim_low

for position in heights_of_letters_5:
	sortedPosition = sorted( zip(BASES, position), key=lambda x: x[1] )
	for letter in sortedPosition:
	#														[left,right,bottom,top]
		panel1.imshow(letter[0], aspect='auto', origin='upper', extent = [startLeft,startRight,startBottom,startBottom + letter[1]])
		#print(startLeft, startRight, startBottom)
		startBottom = startBottom + letter[1]
	startLeft += x_move
	startRight += x_move
	startBottom = ylim_low

startLeft = xlim_low
x_move = (abs(xlim_low) + abs(xlim_high)) / len(position_list)
startRight = startLeft+x_move
startBottom = ylim_low

for position in heights_of_letters_3:
	sortedPosition = sorted( zip(BASES, position), key=lambda x: x[1] )
	for letter in sortedPosition:
	#														[left,right,bottom,top]
		panel2.imshow(letter[0], aspect='auto', origin='upper', extent = [startLeft,startRight,startBottom,startBottom + letter[1]])
		#print(startLeft, startRight, startBottom)
		startBottom = startBottom + letter[1]
	startLeft += x_move
	startRight += x_move
	startBottom = ylim_low


#panel1.plot([xlim_low, xlim_high], 2*[dataMedian], dashes=[1,2,2,2], lw=0.5, c=(0,0,0))


##########################################################################
########### Printing stuff ###############################################


plt.savefig(output_file, dpi=600)
#plt.show()

