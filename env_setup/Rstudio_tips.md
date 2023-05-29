# Tip 1: Restoring workspace taking a long time
<details>
  <summary>Expand</summary>
    
If your last logout contained a massive R object, and loading in the workspace
is taking forever, we can use the tip found here: https://docs.rstudio.com/ide/server-pro/1.4.869-4/r-sessions.html,
to get around this.

In the URL simply type ```/?restore_workspace=0``` after your normal URL. For
example my login URL will look like ```http://bioinformatics.tenaya.local:8787/?restore_workspace=0```.
    
</details>

# Tip 2: Passing variable into an R pipe
<details>
  <summary>Expand</summary>
    
This took forever to figure out but the secret is to wrap your variable in
```!!sym()```. Not sure why this works. Not sure how this works. But it worked
for this code

```
markers.seurat.cm %>% 
	dplyr::group_by(cluster) %>%
	dplyr::top_n(n = all.n, wt = !!sym(sort.metric)) -> top10
```
</details>
    
# Tip 3: Transfering R env to another device
* [Get your list of installed packages](https://rpubs.com/Mentors_Ubiqum/list_packages)
* [Installing the pulled list of packages](https://bioinformatics.stackexchange.com/questions/15259/installing-multiple-bioconductor-packages-at-once)

### Process

<details>
  <summary>Expand</summary>
    
**On the device that has the R env we want to copy write the following lines into a script.**
```
### List of all installed packages
my_packages <- library()$results[,1]

### We can list the libraries that are actually loaded doing
my_loaded_packages <- (.packages())

saveRDS(list(packages = my_packages, loaded.packages = my_loaded_packages), "./currentEnvPackages.rds")
```

**Then on the other device**

```
# Almost completely re-creates env of the server. It doesn't
# take care of non-CRAN packages, and sometimes needs a little 
# help from the user for several packages. Overall, this should
# work though.

setwd("C:/Users/mkozubov/OneDrive - Tenaya Therapeutics/Desktop/R_bio/local_SCAN/")

packages <- readRDS("./currentEnvPackages.rds")
my_packages <- library()$results[,1]
`%!in%` <- Negate(`%in%`)

# install and load  the package  manager
if (!requireNamespace("BiocManager", quietly = TRUE)){
  install.packages("BiocManager")
}

# Install the packages
if (!requireNamespace(packages$packages, quietly = TRUE)){
  BiocManager::install(unique(packages$packages[packages$packages %!in% my_packages]), ask = F, force = T)
}

install.packages("C:/Users/mkozubov/Downloads/pbkrtest/", repos = NULL, type = 'source')

devtools::install_github("sqjin/CellChat")
remotes::install_github('satijalab/seurat-wrappers')
devtools::install_github("davidsjoberg/ggsankey")
install.packages("C:/Users/mkozubov/Downloads/randomForest/", repos = NULL, type = 'source')
install.packages("C:/Users/mkozubov/Downloads/doMC/", repos = NULL, type = 'source') # Doesn't exist for windows :(


# load all at once
invisible(lapply(packages$loaded.packages, function(x){
  tryCatch({library(x, character.only=TRUE)}, 
           error = function(cond){
             message(paste0("Library load error in for package: ", x))
             message("here is the original message: ")
             message(cond)
             return(NA)
           })
  }))

print(paste0('Packages left to install: ', paste0(unique(packages$packages[packages$packages %!in% my_packages]), collapse = ", ")))
```
</details>

### Issues

<details>
  <summary>Expand</summary>
    
#### Manual installation of packages
[Manually downloading and installing packages in R link](https://stackoverflow.com/questions/14806705/manually-downloading-and-installing-packages-in-r) shows us how to manually download and install a package. 

I needed `pbkrtest` so I went to its website [here](https://cran.r-project.org/web/packages/pbkrtest/index.html) clicked on the Old sources: archive link, and found the one that works with my R version (in my case it was version 0.5.1.

I decompressed it using linux with this command `tar -xf pbkrtest_0.5.1.tar.gz` then entered `install.packages("C:/Users/mkozubov/Downloads/pbkrtest/", repos = NULL, type = 'source')` in R.

#### Rtools installation
I ran into an issue where ```Package installation freezed at lazy loading``` and at the top of my console I was getting a warning saying that I need a package called Rtools to install from not CRAN sources. Now this may be a windows specific error, so you may be having a different issue, but here is how I solved it.

So I had to manually go to the [Rtools website](https://cran.rstudio.com/bin/windows/Rtools/), find the package that associated with my R version (I have R 4.0.5 so I had to get Rtools40), and install it to my computer. I decided to manually put it into the same directory as my R-4.0.5 version: ```C:\Program Files\R\R-4.0.5\rtools40```. I then add the `rtools40\usr\bin` to my path manually by going to *edit the system env variables -> environment variables -> System variables: Path: click on edit -> New -> give it my path*. I restarted Rstudio, then typed Sys.which("make") which produced a weirdly formatted output of my path to the rtools40. Then I tested this by trying to do a `install.packages(ggplot2)` which still produced an error, albiet a different one saying `pillars` isn't available. So I did `install.packages(pillars)`, which now worked, and then repeated my ggplot2 install which finally worked!

Watch out, sometimes this new installation tool produces a popup in the background that wants a yes or no to continue, but it doesn't tell you it is there and is fairly subtle, so it looks like the install is frozen.

Also got 
```
ERROR: dependency 'testthat' is not available for package 'nloptr'
* removing 'C:/Users/mkozubov/OneDrive - Tenaya Therapeutics/Documents/R/win-library/4.0/nloptr'
ERROR: dependency 'testthat' is not available for package 'vdiffr'
* removing 'C:/Users/mkozubov/OneDrive - Tenaya Therapeutics/Documents/R/win-library/4.0/vdiffr'
ERROR: dependency 'nloptr' is not available for package 'lme4'
* removing 'C:/Users/mkozubov/OneDrive - Tenaya Therapeutics/Documents/R/win-library/4.0/lme4'
ERROR: dependencies 'pbkrtest', 'lme4' are not available for package 'car'
* removing 'C:/Users/mkozubov/OneDrive - Tenaya Therapeutics/Documents/R/win-library/4.0/car'
ERROR: dependencies 'car', 'emmeans' are not available for package 'FactoMineR'
* removing 'C:/Users/mkozubov/OneDrive - Tenaya Therapeutics/Documents/R/win-library/4.0/FactoMineR'
```
#### Incorrect placement of Rtools
This is a tough one because the processx simply refuses to install. I'm going to try and manually download and unpack it as shown here: https://stackoverflow.com/questions/14806705/manually-downloading-and-installing-packages-in-r.


Additional info on this error
```
"C:/Program Files/R/R-4.0.5/rtools40/mingw64/bin/"gcc  -O2 -Wall  -std=gnu99 -mfpmath=sse -msse2 -mstackrealign -Wall tools/px.c -o tools/px.exe
C:/Program Files/R/R-4.0.5/rtools40/mingw64/bin/../lib/gcc/x86_64-w64-mingw32/8.3.0/../../../../x86_64-w64-mingw32/bin/ld.exe: cannot find C:/Program: No such file or directory
C:/Program Files/R/R-4.0.5/rtools40/mingw64/bin/../lib/gcc/x86_64-w64-mingw32/8.3.0/../../../../x86_64-w64-mingw32/bin/ld.exe: cannot find Files/R/R-4.0.5/rtools40/mingw64/bin/../lib/gcc/x86_64-w64-mingw32/8.3.0/../../../../x86_64-w64-mingw32/lib/../lib/default-manifest.o: No such file or directory
collect2.exe: error: ld returned 1 exit status
make: *** [Makevars.win:18: tools/px.exe] Error 1
```
Fixing this issue, just re-download the Rtools40 and put them into the C: directory straight up. Change the path to still point into C:\rtools40\usr\bin, but this fixes the issue!

#### Straight up no doMC package for Windows

</details>
    
# Tip 4: Running an independant R-job on a server
<details>
  <summary>Expand</summary>
    
We can have an R job work independently of our Rstudio session on a server for when we have a large job that can just be run in the background. For this we would enter the following lines into the terminal.
```
cd /opt/R/4.2.0/bin/ 
/opt/R/4.2.0/bin/R
```
In this case the `/opt/R/4.2.0/bin/` could be specific to your individual R versions/environments we want our R to work in.

Then from inside R we would enter the following line to load the installed packages.
```
.libPaths("/opt/R/4.2.0/lib/R/library")
```

Note that we would still need to "library()" the code to make it accessible to our R session. The view in the terminal should look like the bottom left tab of an Rstudio session. You can paste large blocks of code and it will run it sequentially.

**Note** if you want this to run indefinetely, you could make a seperate screen in the terminal, then exit out with Ctrl-A + Ctrl-D. You can call "\<Rsession\>" whatever you want and don't need to include the brackets.

```
screen -S <Rsession>
```

To rejoin the session after exiting with Ctrl-A + Ctrl-D, type
```
screen -r <Rsession>
```
</details>
    
