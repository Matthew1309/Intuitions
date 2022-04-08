# Instructions to help set up an R ipython kernal
https://stackoverflow.com/questions/56460834/how-to-run-a-single-line-or-selected-code-in-a-jupyter-notebook-or-jupyterlab-ce
This seems like a healful way to create an Rstudio like python kernal.

```Settings --> Advanced Settings Editor --> JSON Settings Editor```
then copy and paste this:
```{
            "command": "notebook:run-in-console",
            "keys": [
                "Ctrl Shift Enter"
            ],
            "selector": ".jp-Notebook.jp-mod-editMode"
},```

Walking through step by step needs to be worked through,
but a nice jupyter notebook with R functionality has been installed
and seems to be working nicely!

The yml file stats.yml contains the necessary jupyter and R packages to make this work.

# In ```t-Test.ipynb``` I walk through the process of doing a **Two sample t-test**
This was a real life scenerio I ran into at work. I had about 30 bulk RNA sequencing samples that I deconvoluted, and got celltype proportion estimates. The question became: do the proportions of different celltypes change between control and HFpEF phenotype? This type of problem set up is perfect for a several statistical techniques that deal with comparing the means of different groups:
* Two sample t-test
* Two sample wilcoxon test
The choice of which test to use depends on what assumptions the user wants to make. In this tutorial we will use the t-test, but it would've been just as easy (and probably more correct) to use the wilcoxon.