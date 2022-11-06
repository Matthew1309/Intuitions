# Instructions to help set up an R ipython kernal
I used this to help guide me: https://stackoverflow.com/questions/68939097/how-to-use-different-versions-of-r-kernels-in-vs-code-jupyter-notebooks-when-usi
To find where the kernels are (in case of unusual path creation)
you can use the command ```jupyter kernelspec list```.


1. Make a conda env and get r-base
2. activate the environment
3. CD into `~/.local/share/jupyter/kernels` and make a new directory with the same name as your conda env
4. Create a file called `kernel.json` 
```
{"argv": 
        ["/SRA_store/shared/tools/mkozubov/miniconda3/envs/pcst/bin/R",
         "--slave",
         "-e",
         "IRkernel::main()",
         "--args",
         "{connection_file}"],
 "display_name":"Cytotalk-R 4.2.0",
 "language":"R"
}
``` 

fill the file with this, and make the R path the path to a specific conda R you want, and change the Cytotalk display name. 
5. Make sure that the conda env, PCST in my case, has the irkernel conda installed otherwise the kernel just wont connect!

# Instructions for enabling line specific execution
https://stackoverflow.com/questions/56460834/how-to-run-a-single-line-or-selected-code-in-a-jupyter-notebook-or-jupyterlab-ce
This seems like a healful way to create an Rstudio like python kernal.

```Settings --> Advanced Settings Editor --> JSON Settings Editor```
then copy and paste this:
```
{
            "command": "notebook:run-in-console",
            "keys": [
                "Ctrl Shift Enter"
            ],
            "selector": ".jp-Notebook.jp-mod-editMode"
},
```

Walking through step by step needs to be worked through,
but a nice jupyter notebook with R functionality has been installed
and seems to be working nicely!

The yml file stats.yml contains the necessary jupyter and R packages to make this work.

# In ```t-Test.ipynb``` I walk through the process of doing a **Two sample t-test**
This was a real life scenerio I ran into at work. I had about 30 bulk RNA sequencing samples that I deconvoluted, and got celltype proportion estimates. The question became: do the proportions of different celltypes change between control and HFpEF phenotype? This type of problem set up is perfect for a several statistical techniques that deal with comparing the means of different groups:
* Two sample t-test
* Two sample wilcoxon test
The choice of which test to use depends on what assumptions the user wants to make. In this tutorial we will use the t-test, but it would've been just as easy (and probably more correct) to use the wilcoxon.
