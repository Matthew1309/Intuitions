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
parser.add_argument('-i1', '--input_file1', default="BME163_Input_Data_5.psl")
parser.add_argument('-i2', '--input_file2', default="BME163_Input_Data_6.psl")
parser.add_argument('-g', '--input_genome', default="gencode.vM12.annotation.gtf")
parser.add_argument('-s', '--style_sheet', default='BME163')#'C:\\Users\\mattk\\Desktop\\BME163\\Assignments\\BME163')#
parser.add_argument('-o', '--output_file', default="Kozubov_Matthew_BME163_Assignment_Final.png")

# there are multiple ways you can access your arguments
# you can put all of the arguments into one variable like this:
args = parser.parse_args()
# which can then be accessed like this:
input_file = args.input_file1
input_file2 = args.input_file2
input_genome = args.input_genome
style_sheet = args.style_sheet
output_file = args.output_file

plt.style.use(style_sheet)

#######################################################################
#######################################################################

figureWidth=10# inches
figureHeight=5 # inches

plt.figure(figsize=(figureWidth,figureHeight))

panelWidth=10
panelHeight=1.25

relativePanelWidth=panelWidth/figureWidth
relativePanelHeight=panelHeight/figureHeight


##########################################################################
########### Panel creations ##############################################

#             left,bottom,width,height
panel3=plt.axes([0,0.05,relativePanelWidth,relativePanelHeight])

#             left,bottom,width,height
panel2=plt.axes([0,0.35,relativePanelWidth,relativePanelHeight])

#             left,bottom,width,height
panel1=plt.axes([0,0.65,relativePanelWidth,relativePanelHeight])

##########################################################################
################## Data Reader ###########################################
target = ['chr7', 45232945, 45240000]
#target = ['chr5', 24685973, 24710000]

desiredChromosome = target[0]
sectionStart = target[1]
sectionEnd = target[2]

def readData(input_file):
	readList = []
	with open(input_file, 'r') as inFile:
		for numLines, line in enumerate( inFile.readlines() ) :
			if True: #numLines % 1 == 0:
				contentList = line.strip().split('\t')
				chromosome=contentList[13]
				start=int(contentList[15])
				end=int(contentList[16])
				blockstarts=np.array( contentList[20].split(',')[:-1], dtype=int )
				blockwidths=np.array( contentList[18].split(',')[:-1], dtype=int )
				if chromosome == desiredChromosome and (sectionStart<start<sectionEnd or sectionStart<end<sectionEnd):
					read=[chromosome,start,end,blockstarts,blockwidths, False]
					readList.append(read)

		return readList

def readGTFData(input_file):
	gtfDict={}
	transcriptList = []
	with open(input_file) as inFile:
		for line in inFile.readlines():
			if line[0] != '#':
				a = line.strip().split('\t')
				chromosome=a[0]
				type1 = a[2]
				if type1 in ['exon', 'CDS']:
					start=int(a[3])
					end=int(a[4])
					transcript=a[8].split(' transcript_id "')[1].split('"')[0]
					if transcript not in gtfDict:
						gtfDict[transcript] = []
					gtfDict[transcript].append([chromosome,start,end,type1])
		
		for transcript,parts in gtfDict.items():
			starts = []
			ends = []

			blockstarts=[]
			blockwidths=[]
			types=[]
			for part in parts:
				chromosome = part[0]
				starts.append(part[1])
				ends.append(part[2])
				blockstarts.append(part[1])
				blockwidths.append(part[2]-part[1])
				types.append(part[3])

			if chromosome == desiredChromosome and (sectionStart<min(starts)<sectionEnd or sectionStart<max(ends)<sectionEnd):
				transcriptList.append([chromosome, min(starts), max(ends), blockstarts, blockwidths, False, types])
		#      [Chromosome, Start, End, Blockstarts, Blockwidths, placedStatus, typeOfBigBox]
		return transcriptList


##########################################################################
################## Nanopore plotter ######################################
def plotNanoporeReads(panel, readList, target):
	genome_chromosome, genome_start, genome_end = target[0], target[1], target[2]
	intron_size = 0.1
	exon_size = 0.6
	shift = exon_size/2 - intron_size/2
	bottom=1
	color = (0,0,0)

	for read in readList:
		chromosome,start,end,blockstarts,blockwidths=read[0], read[1], read[2], read[3], read[4]
		if chromosome==genome_chromosome:
			if genome_start<start<genome_end or genome_start<end<genome_end:
				rectangle=mplpatches.Rectangle( [start,bottom+shift],end-start,intron_size,
					facecolor=color,
					edgecolor='black',
					linewidth=0)
				panel.add_patch(rectangle)

				for index in np.arange(0,len(blockstarts), 1):
					blockstart=blockstarts[index]
					blockwidth=blockwidths[index]
					
					rectangle2=mplpatches.Rectangle( [blockstart,bottom],blockwidth,exon_size,
							facecolor=color,
							edgecolor='red',
							linewidth=0)
					panel.add_patch(rectangle2)

				bottom+=1


	return bottom
##########################################################################
################## Aligned plotter #######################################
def plotIlluminaReads(panel, readList):
	'''
	Give this a sorted (by start position) file of psl formatted 
	illumina sequencing readsand a panel, and it will plot them there.
	It returns the final bottom size for ylim_high
	'''
	intron_size = 0.1
	exon_size = 0.6
	CDS_size = 0.3
	shift = exon_size/2 - intron_size/2
	shift_CDS = exon_size/2 - CDS_size/2
	bottom=1
	color = (0,0,0)

	for bottom in range(1,len(readList),1):
		#need to find the first unplaced element in readList to place at the 
		#new Y-position


		lastPlaced = readList[0]
		for read in readList:
			chromosome,start,end,blockstarts,blockwidths,placedStatus=read[0], read[1], read[2], read[3], read[4], read[5]
			if not placedStatus:
				lastPlaced = read
				# Placing the introns
				rectangle=mplpatches.Rectangle( [start,bottom+shift],end-start,intron_size,
					facecolor=color,
					edgecolor='black',
					linewidth=0)
				panel.add_patch(rectangle)

				for index in np.arange(0,len(blockstarts), 1):
					blockstart=blockstarts[index]
					blockwidth=blockwidths[index]
					try:
						blocktype = read[6]
						if blocktype[index] == 'exon':
							rectangle2=mplpatches.Rectangle( [blockstart,bottom+shift_CDS],blockwidth,CDS_size,
								facecolor=color,
								edgecolor='red',
								linewidth=0)
							panel.add_patch(rectangle2)
						else:
							rectangle3=mplpatches.Rectangle( [blockstart,bottom],blockwidth,exon_size,
								facecolor=color,
								edgecolor='red',
								linewidth=0)
							panel.add_patch(rectangle3)

					except IndexError:
						# Adds the not gtf stuff
						rectangle2=mplpatches.Rectangle( [blockstart,bottom],blockwidth,exon_size,
								facecolor=color,
								edgecolor='red',
								linewidth=0)
						panel.add_patch(rectangle2)

				read[5] = True
				break

		for read in readList:
			chromosome,start,end,blockstarts,blockwidths,placedStatus=read[0], read[1], read[2], read[3], read[4], read[5]
			if not placedStatus: # if not yet placed, consider it
				if start > lastPlaced[2]:
					rectangle=mplpatches.Rectangle( [start,bottom+shift],end-start,intron_size,
						facecolor=color,
						edgecolor='black',
						linewidth=0)
					panel.add_patch(rectangle)

					for index in np.arange(0,len(blockstarts), 1):
						blockstart=blockstarts[index]
						blockwidth=blockwidths[index]
						
						try:
							blocktype = read[6]
							if blocktype[index] == 'exon':
								rectangle2=mplpatches.Rectangle( [blockstart,bottom+shift_CDS],blockwidth,CDS_size,
									facecolor=color,
									edgecolor='red',
									linewidth=0)
								panel.add_patch(rectangle2)
							else:
								rectangle3=mplpatches.Rectangle( [blockstart,bottom],blockwidth,exon_size,
									facecolor=color,
									edgecolor='red',
									linewidth=0)
								panel.add_patch(rectangle3)

						except IndexError:
							# Adds the not gtf stuff
							rectangle2=mplpatches.Rectangle( [blockstart,bottom],blockwidth,exon_size,
									facecolor=color,
									edgecolor='red',
									linewidth=0)
							panel.add_patch(rectangle2)

					read[5] = True
					lastPlaced = read

		#Checks to see if all the reads were placed
		if all(x[5] for x in readList):
			break


	return bottom

##########################################################################
################## Main ##################################################
##
# Nanopore
##
#                                                Sort by end
data = sorted( readData(input_file), key=lambda x: x[2])#lambda x: x[2]-x[1]
bottom = plotNanoporeReads(panel3, data, target)

##
# Illumina
##
#                                              Sort by end position
data = sorted(readData(input_file2), key=lambda x: x[2])
#print(target[0], min(x[1] for x in data), max(x[2] for x in data))
bottom_ill = plotIlluminaReads(panel2, data)

##
# Genome browser
##
#                                             Sort by end position
data = sorted( readGTFData(input_genome), key=lambda x: x[2])
bottom_gtf = plotIlluminaReads(panel1, data)



##########################################################################
########### Panel adjustments ##############################################

xlim_low = target[1] ; xlim_high = target[2]
ylim_low = 0 ; ylim_high = 1.1*bottom

panel3.set_xlim(xlim_low,xlim_high)
panel3.set_ylim(ylim_low,ylim_high)

panel3.tick_params(bottom=False, labelbottom=False,
	left=False, labelleft=False,
	right=False, labelright=False,
	top=False, labeltop=False)
panel3.set_xticks(np.arange(xlim_low, xlim_high, 50000))

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

xlim_low = target[1] ; xlim_high = target[2]
ylim_low = 0 ; ylim_high = 1.16*bottom_ill

panel2.set_xlim(xlim_low,xlim_high)
panel2.set_ylim(ylim_low,ylim_high)

panel2.tick_params(bottom=False, labelbottom=False,
	left=False, labelleft=False,
	right=False, labelright=False,
	top=False, labeltop=False)

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

xlim_low = target[1] ; xlim_high = target[2]
ylim_low = 0 ; ylim_high = 1.17*bottom_gtf

panel1.set_xlim(xlim_low,xlim_high)
panel1.set_ylim(ylim_low,ylim_high)

panel1.tick_params(bottom=False, labelbottom=False,
	left=False, labelleft=False,
	right=False, labelright=False,
	top=False, labeltop=False)

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Gets rid of strange matplotlib scientific notation
panel3.ticklabel_format(useOffset=False, style='plain')
panel2.ticklabel_format(useOffset=False, style='plain')
plt.ticklabel_format(useOffset=False, style='plain')

##########################################################################
########### Printing stuff ###############################################


plt.savefig(output_file, dpi=1200)
#plt.show()

