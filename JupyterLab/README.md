# Some useful Jupyterlab extensions
I liked 
1. jupyterlab-lsp [originally found at](https://stackoverflow.com/questions/58445239/jupyterlab-autocomplete-without-tab)
    1. Need to do a conda install of the jupyterlab-lsp: ```conda install -c conda-forge jupyterlab-lsp=3.10.2```
    1. (maybe not) ```conda install -c conda-forge python-language-server```. 
    1. ```conda install -c conda-forge jedi-language-server=0.21.0```. I've decided to use this because the pyls is pretty darn slow [this suggested jedi](https://stackoverflow.com/questions/65716529/slow-kite-autocomplete-in-jupyterlab); [this hinted that just installing would make it the default](https://github.com/pappasam/jedi-language-server/issues/55)
    1. in the advanced settings, do not turn on continous hinting, it is annoying. Tab will now work much much faster!
    1. The R-language server ```conda install -c conda-forge r-languageserver``` may be useful as well.


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
