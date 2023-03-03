# 3/3/2023
I learned this at Tenaya from Farshad Farshidfar.
You go into commandline and write the following:

"CMD"
```
cd /opt/R/4.2.0/bin/
/opt/R/4.2.0/bin/R
```

Then this will boot up an R session that will resemble the console log of
Rstudio in your terminal window. This is now a functional R env! Butttt
there is currently no packages. We fix that by doing:

"R"
```
.libPaths("/opt/R/4.2.0/lib/R/library")
```

Now stuff is pointed to and we can hook up the packages as usual by doing

"R"
'''
suppressWarnings(library("ggplot"))
suppressWarnings(library("Seurat"))
'''

And now, just like in Rstudio, you can paste line by line the commands you
want :)
