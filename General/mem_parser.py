# free -g -s 10 | stdbuf -o0 awk '{ print $3 }' > memory_monitor.txt
import os
import matplotlib.pyplot as plt
import pandas as pd

filename = "intermediate_misc/memory_monitor_2.txt" 
seconds = 10

with open(filename) as file:
    mem_content = file.read()
    data = [mem_content.split("\n")[1::4],mem_content.split("\n")[2::4],[seconds*n for n in range(len(mem_content.split("\n")[2::4]))]]
    data = {'RAM': data[0],
           'Swap': data[1],
           't': data[2],
           'mem_total': [float(n)+float(m) for n,m in zip(data[0], data[1])]}
    df_mem_content = pd.DataFrame(data)

plt.xlabel("Time (h)")
plt.ylabel("Mem total (GB)")
plt.xticks([x for x in range(11)])
plt.plot(np.array(df_mem_content['t'])/3600,df_mem_content['mem_total'])
