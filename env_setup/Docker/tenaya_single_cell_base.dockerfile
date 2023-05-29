# Setting up this env will fairly nicely recreate 
# the R-env I used at Tenaya for single-cell analysis
# 2021-2023. It may be missing a couple of packages
# but the user can look in currentEnvPackages.rds
# too see what they may need.

# Use rocker/rstudio:4.0.5 as the base image
FROM rocker/rstudio:4.0.5

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
        libcurl4-openssl-dev \
        libssl-dev \
        libxml2-dev \
	libglpk-dev \
	libcairo2-dev \
	libxt-dev

# Read in the R packages installed on the server
COPY currentEnvPackages.rds /app/currentEnvPackages.rds
COPY download_packages.r /home/rstudio/download_packages.r

# Install R packages from CRAN and Bioconductor
RUN R -e "install.packages(c('tidyverse', 'devtools'))"
RUN R -e "if (!requireNamespace('BiocManager', quietly = TRUE)) install.packages('BiocManager')"
RUN R -e "install.packages('Seurat')"
RUN R -e "install.packages('openxlsx')"
RUN R -e "BiocManager::install('DESeq2', ask = FALSE)"
RUN R -e "install.packages('pals')"
# RUN R -e "BiocManager::install('BiocParallel')"
RUN R -e "BiocManager::install('ComplexHeatmap')"
RUN R -e "BiocManager::install('clusterProfiler')"
# RUN R -e "BiocManager::install('AnnotationDbi')"
RUN R -e "BiocManager::install('EnsDb.Mmusculus.v79')"
# RUN R -e "BiocManager::install('org.Mm.eg.db')"
RUN R -e "BiocManager::install('BiocNeighbors')"
RUN R -e "devtools::install_github('sqjin/CellChat')"
RUN R -e "install.packages('jaccard')"
RUN R -e "BiocManager::install('monocle')" 

# Expose the RStudio port (default is 8787)
EXPOSE 8787

# Start RStudio server
CMD ["/init"]
