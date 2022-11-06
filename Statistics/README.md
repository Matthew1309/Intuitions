# In ```t-Test.ipynb``` I walk through the process of doing a **Two sample t-test**
This was a real life scenerio I ran into at work. I had about 30 bulk RNA sequencing samples that I deconvoluted, and got celltype proportion estimates. The question became: do the proportions of different celltypes change between control and HFpEF phenotype? This type of problem set up is perfect for a several statistical techniques that deal with comparing the means of different groups:
* Two sample t-test
* Two sample wilcoxon test
The choice of which test to use depends on what assumptions the user wants to make. In this tutorial we will use the t-test, but it would've been just as easy (and probably more correct) to use the wilcoxon.
