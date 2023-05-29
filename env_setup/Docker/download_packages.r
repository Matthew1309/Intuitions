setwd("/home/rstudio/") 

packages <- readRDS("/app/currentEnvPackages.rds") 
my_packages <- library()$results[,1] 
`%!in%` <- Negate(`%in%`)

# install and load the package manager
if (!requireNamespace("BiocManager", quietly = TRUE)){ install.packages("BiocManager")
}
# Install the packages
if (!requireNamespace(packages$packages, quietly = TRUE)){ BiocManager::install(unique(packages$packages[packages$packages %!in% my_packages]), ask = F, force = T)
}
