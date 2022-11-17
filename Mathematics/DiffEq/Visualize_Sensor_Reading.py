# Usage: Make sure humidityTempSensor.ino is running on the arduino
# conda activate arduino
# python Visualize_Sensor_Reading.py

########################################################################
# # Visualizing Sensor Readings
# I am following Peter Kazarinoff's [How to make animated plots with Matplotlib and Python](https://pythonforundergradengineers.com/live-plotting-with-matplotlib.html) tutorial.

# ## Pseudocode
# 1. Make 2 plots, one for humidity and one for temperature
# 1. Set the serial arduino COM
# 1. Make animate function
#     1. Read the serial input
#     1. Clean up the serial input
#     1. Split the input in two
#         1. Append the first value to a temperature list
#         1. Append the second value to a humidity list
#     1. Keep only the first 100 points
# 1. ser.close()
# 1. Write temp list to a file
# 1. Write humid list to a file
############################################################################

# live_plot_sensor.py
import time
from datetime import date
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from functools import reduce
from statistics import mean
import pandas as pd
import argparse


today = date.today().strftime("%m/%d/%y").replace("/", "_")

# Recieve CMD input from user
parser = argparse.ArgumentParser(description = "Description for my parser")
parser.add_argument("-e", "--example", help = "Example input -- python Visualize_Sensor_Reading.py -s 'file_to_save.txt'", required = False, default = "")
parser.add_argument("-s", "--save", help = "Save Argument -- name of file", required = False, default = f"temp_humidity_{today}.txt")
argument = parser.parse_args()

# animation function
def animate(i, data_temp, data_humid, ser):  
    # Read arduino output into a list
    b = ser.readline()
    string_n = b.decode()
    string = string_n.rstrip()
    try:
        temp, humid = string.split(' ')
        fltT = float(temp)
        fltH = float(humid)
        data_temp.append(fltT)
        data_humid.append(mean(data_humid[-5:] + [fltH]))
        data_time.append(time.ctime())
    except:
        pass
    # Limit the data list to 100 values
    data_temp = data_temp[-100:]
    data_humid = data_humid[-100:]
    
    # clear the last frame and draw the next frame
    axT.clear()
    axT.plot(data_temp, c='red')
    # Format plot
    axT.set_ylim([0, 30])
    axT.set_title("Temperature Reading Live Plot")
    axT.set_ylabel("Celcius")
    axT.grid(visible=True, color='grey', linewidth=1, linestyle='-')
    
    # clear the last frame and draw the next frame
    axH.clear()
    axH.plot(data_humid, c='blue')
    # Format plot
    axH.set_ylim([30, 100])
    axH.set_title("Humidity Reading Live Plot")
    axH.set_ylabel("%RH")
    
    return(axT, axH)

# create empty list to store data
# create figure and axes objects
data_temp = []
data_humid = []
data_time = []
fig, (axT, axH) = plt.subplots(nrows=1, ncols=2, figsize=[10,5])
fig.tight_layout(pad=5.0)

# set up the serial line
ser = serial.Serial('COM3', 9600) # change COM# if necessary
time.sleep(2)
print(ser.name)

# run the animation and show the figure
ani = animation.FuncAnimation(fig, animate, frames=100, fargs=(data_temp, data_humid, ser), interval=500) # Call animate every 500ms
plt.show()

# Once user closes the plot, save the data to a file
df = pd.DataFrame({'Temp':data_temp,'Humidity':data_humid, "Time":data_time})
df.to_csv(argument.save, sep=',', index=False)

# after the window is closed, close the serial line
ser.close()
print("Serial line closed")