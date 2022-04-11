import matplotlib.pyplot as plt 
import matplotlib.patches as mplpatches
import numpy as np 

plt.figure( figsize=(1,1) )

panel1=plt.axes( [0.1,0.1,0.5,0.5] )
panel1.spines[["top","bottom"]].set_linewidth(2)

plt.show()