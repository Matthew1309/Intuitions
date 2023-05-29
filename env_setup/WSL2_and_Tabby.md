--- 
title: "Linux on Windows" 
author: "Matthew Kozubov" 
date: "1/30/2022" 
---
# What is WSL2?
WSL2 is Window's way of getting linux as a seperate operating system on 
the same machine. You have to be careful and understand that it is rather 
finicky. The subsystem doesn't have the same permissions as the main 
system, and I have bumped into an issue where I was trying to delete 
something off of the main machine and it was giving cryptic answers. But 
in general it is pretty good :)
## Set up
For the most part follow this manuel installation tutorial with the 
dism.exe --install stuff: 
https://docs.microsoft.com/en-us/windows/wsl/install-win10 A struggle I 
remember is that I needed to toggle a button off, restart computer, toggle 
button on, restart and then it worked. 
https://github.com/Microsoft/WSL/issues/2982 Might need to do some stuff 
here: And specifically this command: 
https://pureinfotech.com/install-windows-subsystem-linux-2-windows-10/
	 ```wsl --set-default-version 2 wsl --set-version Ubuntu 2``` We 
can see the wsl version using:
	```wsl -l -v```
## Very annoying memory bug
When wsl starts devouring your memory use: 
https://itnext.io/wsl2-tips-limit-cpu-memory-when-using-docker-c022535faf6f
	```wsl --shutdown``` Edit .wslconfig file as directed in the link, 
mine looks like ```[wsl2] memory=3GB processors=4```
	
Additionally, Wsl2 still grabs a bunch of memory and doesn't let it go: 
https://devblogs.microsoft.com/commandline/memory-reclaim-in-the-windows-subsystem-for-linux-2/ 
this command on exit may help?
	```# echo 1 > /proc/sys/vm/compact_memory sudo sh -c 
	"/usr/bin/echo 1 > /proc/sys/vm/drop_caches"``` # This command 
	actually seemed to work
But it may need to be used in conjunction with: 
https://unix.stackexchange.com/questions/109496/echo-3-proc-sys-vm-drop-caches-permission-denied-as-root
	```sudo sh -c "/usr/bin/echo 1 > /proc/sys/vm/compact_memory"```
	
Put together: 
https://github.com/microsoft/WSL/issues/4166#issuecomment-628493643
Someone made an alias for drop_cache!!!
