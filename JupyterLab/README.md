# Jupyterlab tips
1. [Shift-Tab] will display a 'small help' window

# Some useful Jupyterlab extensions
<details open>
  <summary>Click me</summary>
  
I liked 
1. jupyterlab-lsp [originally found at](https://stackoverflow.com/questions/58445239/jupyterlab-autocomplete-without-tab)
    1. Need to do a conda install of the jupyterlab-lsp: ```conda install -c conda-forge jupyterlab-lsp=3.10.2```
    1. (maybe not) ```conda install -c conda-forge python-language-server```. 
    1. ```conda install -c conda-forge jedi-language-server=0.21.0```. I've decided to use this because the pyls is pretty darn slow [this suggested jedi](https://stackoverflow.com/questions/65716529/slow-kite-autocomplete-in-jupyterlab); [this hinted that just installing would make it the default](https://github.com/pappasam/jedi-language-server/issues/55)
    1. in the advanced settings, do not turn on continous hinting, it is annoying. Tab will now work much much faster!
    1. The R-language server ```conda install -c conda-forge r-languageserver``` may be useful as well.

</details>


# Instructions to help set up an R ipython kernal
<details open>
  <summary>Click me</summary>
    
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

## Getting an R session on my jupyter lab
1. Make your R env using Rstudio. Do not make an R env using conda! It is awful and rarely works!
2. Make sure `install.packages("IRkernel")` has been run.
3. Run `conda create --name <"name-of-env">` then `conda activate <"name-of-env">`.
4. cd into `~/.local/share/jupyter/kernels` and make a directory with the name-of-env, then cd into it.
5. Make a file called `kernel.json` and put 
```
{"argv": 
     ["path/to/Rstudio/created/R",
         "--slave",
         "-e",
         "IRkernel::main()",
         "--args",
         "{connection_file}"],
 "display_name":"Name we want to display in jupyter-R 4.2.0",
 "language":"R"
}
```
6. Done! Restart jupyter lab with the refresh button to get this working, but now we have a jupyter lab that has the power to run the exact env that is in our Rstudio!
    
</details>

# Instructions for enabling line specific execution
<details open>
  <summary>Click me</summary>
    
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

</details>
    
# Day to day jupyter lab on a server
<details open>
  <summary>Click me</summary>
    
I mainly followed this tutorial: https://towardsdatascience.com/how-to-connect-to-jupyterlab-remotely-9180b57c45bb

I ran ```screen``` to enter a detachable state. 

Then I ran something along the lines of
> ```jupyter lab --no-browser --ip "*" --notebook-dir <full path to the directory you want this in> --port=<your port number>```

I don't fully remember the details, but the ```--no-browser``` lets this
run on a server, and I don't remember what the ```--ip "*"``` does.

The current password for my Jupyters is Tenaya2021, and I have two
running on ports 1999 and 1998 for my public and private SCAN projects.


---

If you get an R kernal going and don't like that images in the output are tiny/unscrollable
```options(repr.plot.width=8, repr.plot.height=3)``` command found https://blog.revolutionanalytics.com/2015/09/resizing-plots-in-the-r-kernel-for-jupyter-notebooks.html
was incredibly helpful.
---

## Trouble shooting
If the command runs fine on the server, but jupyter lab doesn't show up on the browser, the issue is likely the server's firewall. Farshad somehow got around it and
opened me the 1999 port. This thread https://github.com/jupyter/docker-stacks/issues/639 highlights the issue after the port was opened up. For some reason I was
getting an Error 500. To get around this I needed to set a new config by running ```jupyter server --generate-config``` which replaces the old config file, then 
```jupyter server password``` lets your reset the password. After these actions my jupyter lab worked great again.
    
</details>
