# header.R
# usage in other scripts: source("path/header.R")

library(tidyr)
library(plyr)
library(Seurat)
library(data.table) # for fread import
library(reticulate)
library(ggplot2)
#remotes::install_github("davidsjoberg/ggsankey")
library(ggsankey)

library(corrplot)
library(Matrix)
library(hypeR)
library(reshape2)
library(patchwork)
library(SeuratDisk)
library(openxlsx)
library(Hmisc)
library(cowplot)
library(future)
library(readxl)
library(rgl)
library(dplyr)
library(rstatix)
library(tradeSeq)
library(tibble)
library(DESeq2)

library(scales)
library(pals)
library(dendextend)

#library(monocle)

#library(tradeSeq)
library(BiocParallel)
library(RhpcBLASctl)
library(TimeSeriesExperiment)
library(doMC)


## Load package
library(igraph)
library(ggraph)

library(pracma)
library(extraDistr) # multivariate hypergeom

# Decontamination https://genomebiology.biomedcentral.com/articles/10.1186/s13059-020-1950-6
library("celda")
library("scater")
library(matrixStats)

library(ComplexHeatmap)

library(ramify)
library(devtools)

#install.packages("wordcloud")
#install.packages("RColorBrewer")
#install.packages("wordcloud2")
#install.packages("tm")

# From https://towardsdatascience.com/create-a-word-cloud-with-r-bde3e7422e8a
library(tm)
library(wordcloud2)
library(wordcloud)
library(RColorBrewer)

# From https://cran.r-project.org/web/packages/ggwordcloud/vignettes/ggwordcloud.html
# install.packages("ggwordcloud")
library(ggwordcloud)


# Gene ontology following the video here: https://www.youtube.com/watch?v=JPwdqdo_tRg
library(clusterProfiler)
library(AnnotationDbi)
#library(EnsDb.Hsapiens.v86)
#BiocManager::install("EnsDb.Mmusculus.v79")
library(EnsDb.Mmusculus.v79)
# BiocManager::install("org.Mm.eg.db")
library(org.Mm.eg.db)

###
# Helper functions
###
outersect <- function(x, y) {
  sort(c(setdiff(x, y),
         setdiff(y, x)))
}

fun.root.feature <- function(seurat.obj, root.name){
  both.treat <- rownames(seurat.obj)[grepl(root.name, rownames(seurat.obj))]
  return(both.treat)
  
}
fun.map.labels <- function(query, reference, meta2trans, meta2trans.names = F, test.k.weight = F, k.weight = 50){
  # If the user doesn't specify the meta2trans.names, then it is assumed it is the same as the 
  # meta2trans
  if(is.logical(meta2trans.names)){meta2trans.names = meta2trans}
  
  # This pulls out the reference meta data in a way that is
  # usable by the functions down below.
  for.refdata <- as.list(reference[[meta2trans]])
  # Default number of k.neighbors. Note: if this number is too
  # high, the function will error! By default we aren't testing
  # this, but flip the test.k.weight switch to test.
  user.input.k <- k.weight
  
  print('Finding Transfer Anchors')
  heart.anchors <- FindTransferAnchors(reference = reference, 
                                       query = query,
                                       npcs = 30,
                                       dims = 1:30, 
                                       reference.reduction = "pca", 
                                       project.query = T,
                                       normalization.method = 'SCT', 
                                       query.assay = 'integrated')
  print('Done Finding Transfer Anchors')
  
  # This subfunction hasn't been implemented yet
  # I need to figure out how to ask it to test one
  # particular label transfer if the user doesn't 
  # specify.
  if(test.k.weight) {
    print("Shouldn't be entering this test.k.weight quite yet")
    # optimizing the k.weight
    # Here we need to make sure that if the k is 
    # too high, it doesn't throw an error that cannot
    # be skipped over.
    list.of.plots <- list()
    list.of.plot.labels <- list()
    k.to.test <- linspace(5,40,n = 6)
    for(i in 1:6){
      k.weight <- k.to.test[i]
      predictions <- TransferData(anchorset = heart.anchors,
                                  refdata = for.refdata,
                                  dims = 1:30, k.weight = k.weight)
      
      if(length(list.of.tranfer.meta) > 1){
        seurat.query$test <- predictions$auth.labels$predicted.id
      }
      else{
        seurat.query$test <- predictions$predicted.id
      }
      
      list.of.plots[[i]] <- DimPlot(seurat.query, group.by = "test", cols = 'glasbey')
      list.of.plot.labels[[i]] <- paste0("k.weight: ",k.weight)
      seurat.query$test <- NULL
    }
    print(paste0("Saving k.weight optimization plot to: ", "./figures/QC/", Sys.Date(), "/k_weight_opt_tranferData.png"))
    plot.k.weight <- plot_grid(plotlist=list.of.plots, labels=list.of.plot.labels); plot.k.weight
    ggsave(plot.k.weight, filename = 'k_weight_opt_tranferData.png', path = paste0("./figures/QC/transferData/", Sys.Date()), units = 'in', width = 12, height = 8)
    
    # Asking user for their prefered K value based on the plot.k.weight produced.
    user.input.k <- as.integer(readline(prompt="Enter the number for k, default is 50: "))
  }
  
  print('Predicting reference labels on query')
  # If you run across Error in idx[i, ] <- res[[i]][[1]], it means 
  # that the data is too sparse, need to lower k.weight
  predictions <- TransferData(anchorset = heart.anchors, 
                              refdata = for.refdata,
                              dims = 1:30, k.weight = user.input.k)
  
  if(length(meta2trans) > 1){
    
    query <- AddMetaData(
      object = query,
      metadata = lapply(predictions, FUN = function(x){return(x$predicted.id)}),
      col.name = meta2trans.names
    )
  }
  else{
    query[[meta2trans.names]] <- predictions$predicted.id
  }
  
  return(query)
}


fun.dict.substitute <- function(list.of.keys, key.value.pairs) {
  # R doesn't have a nice easy, naitive way to replace values via
  # a key:value pair relationship. IE if I have stuff in one column
  # but I wanna transform each into another one, what do I do? Easy
  # in python, quite a pain here.
  
  # Input: list("A", "B", "A", "C"), list("name1": "A", "name2":"B", "name3":"C")
  # Output: list("name1", "name2", "name1", "name3")
  
  # Examples:
  # list.of.keys <- c("A", "B", "A", "C")
  # key.value.pairs <- c("A", "B", "C")
  # names(key.value.pairs) <- c("name1", "name2", "name3")
  # Help: https://stackoverflow.com/questions/35636315/replace-values-in-a-dataframe-based-on-lookup-table
  # Made on 3/25/2022 by Matthew Kozubov
  
  ### This is a redundancy of an existing R package called zeallot
  # c(transcripts, t2g) %<-% genomes[match(species, genomes$species),c("transcripts", "tx2")]
  # (Thank you Farshad!)
  
  return( names(key.value.pairs)[match(list.of.keys, key.value.pairs)] )
  
}


fun.stacked.bar.plot <- function(obj, on.y = 'exp.assay', on.x = 'seurat_clusters', round2 = 2){
  # I want a measure of whether the differences we see
  # are statistically significant. We need to make sure
  # that there are no just zero columns!
  dat <- as.data.frame(as.matrix(ftable(obj[[on.y]], obj[[on.x]])))
  is.contingency.significant <- chisq.test(dat)$p.value
  
  # Unfortuanately this can only be done one at a time
  # The [[]] are needed to actually select assay
  df1 = subset(obj@meta.data, select = c(on.x,on.y))
  #df1$percentage <- rep(1/dim(df1)[1], dim(df1)[1])
  
  # The coloring is weird, that is what df.colors and the next two lines are for
  df.box.plot <- df1
  # Okay, so we make the colors the names, and the object we want to 
  # assign that color the value.
  df.colors <- unique(df.box.plot[[on.y]])
  names(df.colors) <- glasbey(length(unique(df.box.plot[[on.y]])))
  # The scale_fill_manual is how we need to color
  # and the aes_string is so that the variable expands
  # and isn't taken literally. I also need the paste
  # with backticks because R cannot handle dashes in gene names 
  # https://stackoverflow.com/questions/48651370/dash-in-column-name-yields-object-not-found-error
  # HERE IS HOW TO ADD NUMBERS SHOWING PERCENTS!!! https://stackoverflow.com/questions/59444265/percentages-for-geom-text-in-stacked-barplot-with-counts
  return(ggplot(df.box.plot, aes_string(x=on.x, fill = on.y), add=c('jitter')) + 
           geom_bar(position="fill") + theme_bw() + 
           scale_fill_manual(values = names(df.colors)) + 
           geom_text(aes(label = scales::percent(round(..count../tapply(..count.., ..x.. ,sum)[..x..], round2))),
                     colour='#FFFFFF', size = 4,
                     position = position_fill(vjust = 0.5),
                     stat = "count") +
           theme(axis.text.x = element_text(angle = 40, vjust = 1, hjust=1, lineheight = 0.75, size = 11),
                 axis.text.y = element_text(family = "Arial", size = 10, face = "plain", color = "black"),
                 plot.title = element_text(hjust = 0.5),
                 legend.text = element_text(family = "Arial", size = 12, face = "plain", color = "black"),
                 panel.grid.major = element_blank(), panel.grid.minor = element_blank()) + 
           ggtitle(paste0("Cluster proportions (Chi-sqr-pvalue: ",format(round(is.contingency.significant, 3), scientific = TRUE),"): \n",
                          paste(round(table(obj[[on.y]])/
                                        sum(table(obj[[on.y]])),round2), 
                                collapse=" "))))
}

# change split.by to NULL not F
fun.boxplot <- function(obj, gene, assay = 'RNA', split.by = F, group.by = 'seurat_clusters', coef = 1.5){
  # Unfortuanately this can only be done one at a time
  # The [[]] are needed to actually select assay
  df1 = t(obj@assays[[assay]][gene,])
  df2 = obj@meta.data
  df3 = merge(x=df1, y=df2, by = 'row.names')
  rownames(df3) <- df3$Row.names
  df3$Row.names <- NULL
  
  # If user provides a column to split by, we will color by the split.by
  # else, we color by the group.by
  if(is.character(split.by)){ # if(!is.null(split.by)
    # The coloring is weird, that is what df.colors and the next two lines are for
    df.box.plot <- df3[,c(gene, group.by, split.by)]
    # I changed the way naming is handled so the order of labels isn't weird.
    df.colors <- unique(df.box.plot[[split.by]])
    names(df.colors) <- glasbey(length(unique(df.box.plot[[split.by]])))
    
    df.box.plot$colors <- sapply(df.box.plot[[split.by]], FUN = function(x) df.colors[x])
    
    # The scale_fill_manual is how we need to color
    # and the aes_string is so that the variable expands
    # and isn't taken literally. I also need the paste
    # with backticks because R cannot handle dashes in gene names 
    # https://stackoverflow.com/questions/48651370/dash-in-column-name-yields-object-not-found-error
    return(ggplot(df.box.plot, aes_string(x=group.by, y=paste0("`", gene, "`"), fill = split.by), add=c('jitter')) + 
             geom_boxplot(coef = coef) + theme_bw() + scale_fill_manual(breaks = df.colors, values = names(df.colors)) + 
             theme(axis.text.x = element_text(angle = 40, vjust = 1, hjust=1, lineheight = 0.75, size = 11),
                   axis.text.y = element_text(family = "Arial", size = 10, face = "plain", color = "black"),
                   plot.title = element_text(hjust = 0.5),
                   legend.text = element_text(family = "Arial", size = 12, face = "plain", color = "black"),
                   panel.grid.major = element_blank(), panel.grid.minor = element_blank()))
  }
  # This is if the user doesn't provide a split by, I'm not sure how to make this code more
  # compact, and I don't super care about efficiency or anything.
  else{
    df.box.plot <- df3[,c(gene, group.by)]
    df.colors <- unique(df.box.plot[[group.by]])
    names(df.colors) <- glasbey(length(unique(df.box.plot[[group.by]])))
    df.box.plot$colors <- sapply(df.box.plot[[group.by]], FUN = function(x) df.colors[x])
    
    return(ggplot(df.box.plot, aes_string(x=group.by, y=paste0("`", gene, "`"), fill = group.by), add=c('jitter')) + 
             geom_boxplot() + theme_bw() + scale_fill_manual(breaks = df.colors, values = names(df.colors)) + 
             theme(axis.text.x = element_text(angle = 40, vjust = 1, hjust=1, lineheight = 0.75, size = 11),
                   axis.text.y = element_text(family = "Arial", size = 10, face = "plain", color = "black"),
                   plot.title = element_text(hjust = 0.5),
                   legend.text = element_text(family = "Arial", size = 12, face = "plain", color = "black"),
                   panel.grid.major = element_blank(), panel.grid.minor = element_blank()))
  }
}


fun.ftable.heatmap <- function(cat1, cat2){
  heatmap.data <- as.matrix(ftable(cat1,cat2))
  return(heatmap(t(t(heatmap.data)/colSums(heatmap.data)), Rowv = NA, Colv = NA, scale='column'))
}


fun.find.all.markers <- function(seurat.obj, path.marker.list=NA,
                                 sort.metric = 'avg_log2FC',
                                 all.path.csv,
                                 all.path.figure,
                                 all.name.figure,
                                 all.log.thresh=0.1, all.n=10, all.group.by='exp.assay',all.min.pct=0, find.assay='SCT', viz.assay='RNA', disp.max=10, disp.min=-2.5,
                                 factor.order = NULL,
                                 recorrect_umi = F,
                                 height = 20, width = 19) {
  # So I want to give the log.threshold
  # The path to put the CSV
  # the number of genes to plot
  # and the ident to group by.
  
  # The passed seurat object should already have the idents changed to what we want them
  # to be.
  print('Setting Idents')
  Idents(seurat.obj) <- seurat.obj@meta.data[,all.group.by]
  if(is.na(path.marker.list)){
    log.thresh = all.log.thresh#0.7
    
    print('Finding all markers (might take a while)')
    # I need to explicitly state the assay to use and the slot to use
    markers.seurat.cm <- FindAllMarkers(object=seurat.obj, only.pos = T, 
                                        logfc.threshold = log.thresh, min.pct = all.min.pct, recorrect_umi = recorrect_umi, slot = "data", assay=find.assay,
                                        test.use = 'wilcox', 
    )
    
    # I want to add the Wilcox ranking system that Farshad likes
    markers.seurat.cm$p_val_adj_corr <-  markers.seurat.cm$p_val_adj + 2.225074e-308
    markers.seurat.cm$wilcox <- -log10(markers.seurat.cm$p_val_adj_corr) * sign(markers.seurat.cm$avg_log2FC)
    
    
    # In order to create a directory, if it doesn't already exist
    ifelse(!dir.exists(file.path(dirname(all.path.csv))), dir.create(file.path(dirname(all.path.csv)), recursive = T), F)
    
    print(paste0('Writing marker file to: ', all.path.csv))
    write.csv(markers.seurat.cm, all.path.csv, row.names = TRUE)
    
    # to bring order
    if(!is.null(factor.order)){
      markers.seurat.cm$cluster <- factor(markers.seurat.cm$cluster, levels=factor.order, 
                                          ordered = T)
    }
  }
  else{
    markers.seurat.cm <- read.table(path.marker.list,sep=',', header=T, row.names = 1)
    if(!is.null(factor.order)){
      markers.seurat.cm$cluster <- factor(markers.seurat.cm$cluster, levels=factor.order, 
                                          ordered = T)
    }
    }
  
  print(paste0('all.n: ', all.n, " sort.metric: ", sort.metric))
  # Thank you to https://stackoverflow.com/questions/61016504/using-a-string-for-variable-name-in-dplyr-top-n
  # For helping me with the !!sym(), this allows the user passed sort.metric
  # to actually be used!
  markers.seurat.cm %>%
    dplyr::group_by(cluster) %>%
    dplyr::top_n(n = all.n, wt = !!sym(sort.metric)) -> top10
  top10 <- top10[order(top10$cluster, -top10[,sort.metric]),]
  
  print(paste0("Making heatmap with ",all.n," genes per div, and saving to: ", all.path.figure))
  plot.farshad.heatmap <- DoHeatmap(seurat.obj, features = top10$gene,group.by=all.group.by, assay=viz.assay, slot = "scale.data", disp.max=disp.max, disp.min=disp.min) +
    theme(text = element_text(size = 25)) #+ 
  #scale_fill_gradientn(colors = c("#352A87","#33B7A0","#F9FB0E")); plot.farshad.heatmap
  ggsave(all.name.figure, plot.farshad.heatmap, 
         path=all.path.figure, width = width, 
         height = height, units = 'in', limitsize = FALSE)
  
  return(markers.seurat.cm)
  
}


fun.find.markers <- function(seurat.obj,path.marker.list=NA,
                             ident.1,
                             ident.2,
                             sort.metric = 'avg_log2FC',
                             all.path.csv,
                             all.path.figure,
                             all.name.figure,
                             all.log.thresh=0.1, min.diff.pct = -Inf, all.n=10, all.group.by='exp.assay',all.min.pct=0, find.assay='SCT', viz.assay='RNA', disp.max=10, disp.min=-2.5,
                             factor.order = NULL,
                             recorrect_umi = F,
                             parallel=F,
                             height = 20,
                             width = 19
){
  if(is.na(path.marker.list)){
    log.thresh = all.log.thresh
    print(paste0("Finding markers between ", ident.1, " and ", ident.2))
    if(parallel){print('Parallel');plan("multiprocess", workers = 4)}
    markers.seurat.cm <- FindMarkers(object=seurat.obj, only.pos = F, 
                                     logfc.threshold = all.log.thresh, test.use = 'wilcox',
                                     ident.1 = ident.1, ident.2 =ident.2 , 
                                     group.by = all.group.by, min.pct=all.min.pct, assay=find.assay, slot='data', 
                                     recorrect_umi=F, min.diff.pct = min.diff.pct)
    
    print('done finding markers')
    plan("sequential")
    # In order to create a directory, if it doesn't already exist
    ifelse(!dir.exists(file.path(dirname(all.path.csv))), dir.create(file.path(dirname(all.path.csv)), recursive = T), F)
    
    # I want to add the Wilcox ranking system that Farshad likes
    markers.seurat.cm$p_val_adj_corr <-  markers.seurat.cm$p_val_adj + 2.225074e-308
    markers.seurat.cm$wilcox <- -log10(markers.seurat.cm$p_val_adj_corr) * sign(markers.seurat.cm$avg_log2FC)
    
    # Adding mean/grouping to the matrix
    #mean.per.group <- AverageExpression.matt(seurat.obj, fun = 'mean', assay='RNA',slot = 'data', group.by = all.group.by, genes = rownames(markers.seurat.cm))
    #colnames(mean.per.group) <- paste(colnames(mean.per.group),"RNA",sep="_")
    #markers.seurat.cm <- cbind(markers.seurat.cm, mean.per.group)
    # 
    # mean.per.group <- AverageExpression.matt(seurat.obj, fun = 'mean', assay='SCT',slot = 'data', group.by = all.group.by, genes = rownames(markers.seurat.cm))
    # colnames(mean.per.group) <- paste(colnames(mean.per.group),"SCT",sep="_")
    # markers.seurat.cm <- cbind(markers.seurat.cm, mean.per.group)
    
    mean.per.group <- AverageExpression.matt(seurat.obj, fun = 'mean', assay=find.assay,slot = 'data', group.by = all.group.by, genes = rownames(markers.seurat.cm))
    colnames(mean.per.group) <- paste(colnames(mean.per.group),find.assay,sep="_")
    markers.seurat.cm <- cbind(markers.seurat.cm, mean.per.group)
    
    
    
    print(paste0('Writing marker file to: ', all.path.csv))
    write.csv(markers.seurat.cm, all.path.csv, row.names = TRUE)
  }
  else{
    markers.seurat.cm <- read.table(path.marker.list,sep=',', header=T, row.names = 1)
    if(!is.null(factor.order)){
      markers.seurat.cm$cluster <- factor(markers.seurat.cm$cluster, levels=factor.order, 
                                          ordered = T)
    }
  }
  
  
  # Getting genes into order of avg_log2FC like in seurat tutorials
  key.genes <- rownames(markers.seurat.cm[order(markers.seurat.cm[,sort.metric], decreasing = T),])
  how.many <- all.n
  print(paste0("Creating heatmap in: ", all.name.figure))
  plot.farshad.heatmap <- DoHeatmap(seurat.obj,
                                    features = c(key.genes[0:how.many],rev(key.genes[(length(key.genes)-how.many):length(key.genes)])),
                                    group.by=all.group.by, slot = 'scale.data', disp.max=disp.max, disp.min=disp.min, assay=viz.assay) + 
    theme(text = element_text(size = 25)) #+ 
  #scale_fill_gradientn(colors = coolwarm(3)); plot.farshad.heatmap#c("#352A87","#33B7A0","#F9FB0E")
  ggsave(all.name.figure, plot.farshad.heatmap, path=all.path.figure, width = width, height = height, units = 'in')
  
  return(markers.seurat.cm)
}

fun.ftable.with.margins <- function(obj1, obj2) {
  # Pass this in: 
  # seurat.cm.ml@meta.data$tradeseq.lineages, seurat.cm.ml@meta.data$tissue_small
  table.tradeseq.lin.vs.tissue <- as.matrix(ftable(obj1, obj2)); table.tradeseq.lin.vs.tissue
  table.tradeseq.lin.vs.tissue <-rbind(table.tradeseq.lin.vs.tissue, colSums(table.tradeseq.lin.vs.tissue))
  table.tradeseq.lin.vs.tissue <-cbind(table.tradeseq.lin.vs.tissue, rowSums(table.tradeseq.lin.vs.tissue))
  return(table.tradeseq.lin.vs.tissue)
}

# Make sure path.cardiomyocyte.figures doesn't end with a "/"
graphs.I.would.want <- function(seurat.cm.sub, path.cardiomyocyte.figures) {
  # Basic clusters and meta data on UMAP
  plot.final.dimplot <- DimPlot(seurat.cm.sub, reduction='umap', cols='glasbey', label=T, label.size=7); plot.final.dimplot # Visualization
  ggsave(paste0("dimplot_", Sys.Date(), ".png"), plot.final.dimplot, path=path.cardiomyocyte.figures, width = 6, height = 6, units = 'in')
  plot.final.dimplot <- DimPlot(seurat.cm.sub, reduction='umap', cols='glasbey', group.by='exp.assay'); plot.final.dimplot # Visualization
  ggsave(paste0("dimplot_exp_assay_", Sys.Date(), ".png"), plot.final.dimplot, path=path.cardiomyocyte.figures, width = 7.5, height = 6, units = 'in')
  plot.final.dimplot <- DimPlot(seurat.cm.sub, reduction='umap', cols='glasbey', group.by='orig.ident'); plot.final.dimplot # Visualization
  ggsave(paste0("dimplot_orig_ident_", Sys.Date(), ".png"), plot.final.dimplot, path=path.cardiomyocyte.figures, width = 7, height = 6, units = 'in')
  
  # Additional QC plot
  plot.final.dimplot <- FeaturePlot(seurat.cm.sub, features = "nCount_RNA", max.cutoff = 30000) | seurat.cm.sub@meta.data %>% ggplot(aes(color=seurat_clusters, x=nCount_RNA, fill=seurat_clusters)) + geom_density(alpha=0.2) + scale_x_log10() + theme_classic() + ylab("Cell density") + geom_vline(xintercept=500)
  ggsave(paste0("dimplot_nCount_QC_", Sys.Date(), ".png"), plot.final.dimplot, path=path.cardiomyocyte.figures, width = 13, height = 6, units = 'in')
  
  # Stacked 1
  plot.final.dimplot <- fun.stacked.bar.plot(seurat.cm.sub, on.x = 'exp.assay', on.y = 'seurat_clusters', round2=4) | 
    DimPlot(seurat.cm.sub, cols='glasbey')
  ggsave(paste0("stacked_barplot_exp.assay_clusters_", Sys.Date(), ".png"), plot.final.dimplot, path=path.cardiomyocyte.figures, width = 17, height = 17, units = 'in')
  
  # Stacked 2
  plot.final.dimplot <- fun.stacked.bar.plot(seurat.cm.sub, on.x = 'seurat_clusters', on.y ='exp.assay', round2=4) | 
    DimPlot(seurat.cm.sub, cols='glasbey')
  ggsave(paste0("stacked_barplot_clusters_exp.assay_", Sys.Date(), ".png"), plot.final.dimplot, path=path.cardiomyocyte.figures, width = 20, height = 7, units = 'in')
  
  # Stacked 3
  plot.final.dimplot <- fun.stacked.bar.plot(seurat.cm.sub, on.x = 'seurat_clusters', on.y = 'orig.ident', round2=4) | 
    DimPlot(seurat.cm.sub, cols='glasbey')
  ggsave(paste0("stacked_barplot_clusters_orig.ident_", Sys.Date(), ".png"), plot.final.dimplot, path=path.cardiomyocyte.figures, width = 20, height = 9, units = 'in')
  
  
  
  
  # More complicated "Split.by" graphs
  plot.final.dimplot <- DimPlot(seurat.cm.sub, split.by = 'seurat_clusters', group.by='orig.ident', cols='glasbey'); plot.final.dimplot # Visualization
  ggsave(paste0("dimplot_orig_ident_splitby_clusters_", Sys.Date(), ".png"), plot.final.dimplot, path=path.cardiomyocyte.figures, width = 20, height = 6, units = 'in')
  png(paste0(path.cardiomyocyte.figures,"/heatmap_cluster_comp_orig.ident_", Sys.Date(), ".png"), 
      width = 1800, height = 1000, res=220)
  fun.ftable.heatmap(seurat.cm.sub@meta.data$orig.ident,seurat.cm.sub@meta.data$seurat_clusters)#heatmap(as.matrix(ftable(seurat.cm.sub@meta.data$orig.ident, seurat.cm.sub@meta.data$seurat_clusters)), Rowv = NA, Colv = NA, scale='column')
  dev.off()
  
  plot.final.dimplot <- DimPlot(seurat.cm.sub, split.by = 'seurat_clusters', group.by='exp.assay', cols='glasbey'); plot.final.dimplot # Visualization
  ggsave(paste0("dimplot_expassay_splitby_clusters_", Sys.Date(), ".png"), plot.final.dimplot, path=path.cardiomyocyte.figures, width = 20, height = 6, units = 'in')
  png(paste0(path.cardiomyocyte.figures,"/heatmap_cluster_comp_exp.assay_", Sys.Date(), ".png"), 
      width = 1800, height = 1000, res=220)
  fun.ftable.heatmap(seurat.cm.sub@meta.data$exp.assay,seurat.cm.sub@meta.data$seurat_clusters)#heatmap(as.matrix(ftable(seurat.cm.sub@meta.data$exp.assay, seurat.cm.sub@meta.data$seurat_clusters)), Rowv = NA, Colv = NA, scale='column')
  dev.off()
  
  # QC violin plot of mito
  plot.vln.plot <- VlnPlot(seurat.cm.sub, features = 'percent.mt', cols = glasbey(16)); plot.vln.plot
  ggsave(paste0("vlnplot_mt_percent_clusters_", Sys.Date(), ".png"), plot.vln.plot, 
         path=path.cardiomyocyte.figures, width = 10, height = 6, units = 'in')
  
  # QC feature plot of mito
  plot.final.dimplot <- FeaturePlot(seurat.cm.sub, features='percent.mt'); plot.final.dimplot # Visualization
  ggsave(paste0("dimplot_mt-percent_", Sys.Date(), ".png"), plot.final.dimplot, path=path.cardiomyocyte.figures, width = 6, height = 6, units = 'in')
  
}

fun.seurat.2feature.plot <- function(seurat.obj, 
                                     interesting.genes, 
                                     path.2feature,
                                     width=12, height=7){
  plot.cell.types.cardio.fibro <- FeaturePlot(object=seurat.obj, # Wow huge thank you here https://github.com/satijalab/seurat/issues/2400
                                              features=interesting.genes, 
                                              pt.size = 1.7) & 
    scale_colour_gradientn(colours = kovesi.rainbow(10))
  interesting.genes <- paste0(interesting.genes, collapse = '_')
  ggsave(paste0("emb_comp_trab_split_", interesting.genes, "_CMFB_audit_", Sys.Date(), ".png"), 
         plot.cell.types.cardio.fibro, 
         path=path.2feature, width = width, height = height, units = 'in')
  
}

`%!in%` <- Negate(`%in%`)

AverageExpression.matt <- function(seurat.obj, 
                                   fun = 'mean', ...,
                                   slot = 'counts',
                                   assay='RNA',
                                   group.by='seurat_clusters', 
                                   genes=c('DCN', "GSN", "TNNT2")){
  # Give a seurat object, and calculate different variations of summary
  # statistics. For example mean, or median. We can choose different slots
  # like counts, data, etc. We can also choose what to group.by.
  final_obj <- list()
  iter <- unique(seurat.obj@meta.data[,group.by])
  iter <- sort(iter)
  
  for(i in 1:length(iter)){
    cells.post.category.filter <- rownames(seurat.obj@meta.data)[seurat.obj@meta.data[,group.by] == iter[i]]
    thing <- slot(seurat.obj@assays[[assay]], slot)[genes, cells.post.category.filter]
    summarized.category <- apply(thing, MARGIN = 1, FUN = fun, ...)
    final_obj[[i]] <- summarized.category
  }
  final_obj <- data.frame(final_obj)
  colnames(final_obj) <- iter
  return(final_obj)
}

fun.pseudobulk.heatmap <- function(obj, gene.list, group.by='exp.assay', disp = 0.3, write.nums = F, text.size=6, assay='RNA', slot='scale.data', round_to=3){
  # Usage: fun.pseudobulk.heatmap(seurat.cm.i, gene.list = plot.genes, disp = 0.7)
  # This won't work for a single gene because of how my AverageExpression.matt
  # function works unfortunately.
  
  # At somepoint it might be nice to give the user control over the title, or 
  # somehow pretty it up like the seurat heatmap.
  data.real <- AverageExpression.matt(obj, fun = 'mean', slot=slot, genes=gene.list, group.by = group.by, assay=assay)
  
  data.real$genes <- factor(rownames(data.real), levels = rev(gene.list), ordered=T)
  data.real <- melt(data.real, 
                    id.vars = c("genes"), 
                    variable.name = "condition")
  
  
  if(!write.nums){
    return(ggplot(data.real, aes(condition, genes, fill= value)) + 
             geom_tile() +
             scale_fill_gradientn(colors = PurpleAndYellow(100), limits=c(-disp,disp), oob=squish) +
             scale_x_discrete(position = "top") +
             labs(x = "condition means") +
             theme(axis.text = element_text(size = 20))) 
  }
  else{
    return(ggplot(data.real, aes(condition, genes, fill= value)) + 
             geom_tile() +
             scale_fill_gradientn(colors = PurpleAndYellow(100), limits=c(-disp,disp), oob=squish) +
             geom_text(aes(label = round(value, digits = round_to)), color = "white", size = text.size) +
             scale_x_discrete(position = "top") +
             labs(x = "condition means") +
             theme(axis.text = element_text(size = 20))) 
  }
  
}


ARI.matt <- function(cat1, cat2){
  # Given two vectors with categories (the row order should be ensured by the user)
  # the contingency table is produced, and the Adjusted Rand index is calculated.
  # https://en.wikipedia.org/wiki/Rand_index and https://davetang.org/muse/2017/09/21/adjusted-rand-index/
  # helped produce this.
  
  # The output is a single value. A value of 1 inidicates perfect re-clusterability.
  # A value of near zero indicates virtually random assortment.
  
  # Example usage: ARI.matt(seurat.obj111@meta.data$seurat_clusters, seurat.obj222@meta.data$seurat_clusters)
  # Example output: 1
  
  contingency.table.wiki <- as.data.frame(fun.ftable.with.margins(cat1, cat2))
  colnames(contingency.table.wiki)[length(colnames(contingency.table.wiki))] <- 'aSums'
  rownames(contingency.table.wiki)[length(rownames(contingency.table.wiki))] <- 'bSums'
  
  nij <- contingency.table.wiki[1:dim(contingency.table.wiki)[1]-1, 1:dim(contingency.table.wiki)[2]-1]
  nij <- as.vector(as.matrix(nij))
  ai <- as.vector(contingency.table.wiki[1:(dim(contingency.table.wiki)[1]-1),'aSums'])
  bj <- as.vector(contingency.table.wiki['bSums',1:(dim(contingency.table.wiki)[2]-1)])
  n.choose.2 <- choose(sum(nij), 2)
  
  sum.choose <- function(vector.int, k=2){
    # Helper function for calculating the sum of 
    # a list of "chooses"
    sum(sapply(vector.int, FUN = choose, k=k))
  }
  
  numerator <- sum.choose(nij) - (sum.choose(ai) * sum.choose(bj))/n.choose.2
  denominator <- 0.5*(sum.choose(ai) + sum.choose(bj)) - (sum.choose(ai) * sum.choose(bj))/n.choose.2
  
  ARI <- numerator/denominator
  return(ARI)
}


fun.GSEA.wordcloud <- function(GSEA.table, min.GSEA.entries=10, max.Q=0.75, n.genes=30){
  # Given one of Reva's GSEA Tables, generate a WordCloud of the genes
  # associated with the GSEA terms.
  
  # For future use. If we have an error regarding n.genes,
  # That may be because the while loops got to too high of a 
  # Q.val without selecting any suitable pathways. We need to increase
  # the max Q.val.
  
  # Increasing n.genes increases how many genes we show on the
  # canvas.
  fun.generate.wordcloud <- function(df.with.csv.genes, which.rows, n.genes ){
    # Helper function. Given the cleaned up dataframe and logical vector
    # of which rows to grab, generate the wordcloud.
    
    # Makes a nice vector of the genes we have
    vector.of.csv.genes <- unlist(sapply(df.with.csv.genes$Leading.edge.genes[which.rows], 
                                         FUN=function(x){
                                           lapply(strsplit(x, ","), FUN=trimws)
                                         }))
    names(vector.of.csv.genes) <- NULL
    
    # This is pulled from 
    docs <- Corpus(VectorSource(vector.of.csv.genes))
    dtm <- TermDocumentMatrix(docs) 
    matrix <- as.matrix(dtm) 
    words <- sort(rowSums(matrix),decreasing=TRUE) 
    df <- data.frame(word = names(words),freq=words)
    
    # To make this actually return an object, I had
    # to resort to using the ggplot2 wordcloud implementation
    # https://cran.r-project.org/web/packages/ggwordcloud/vignettes/ggwordcloud.html
    df$prop <- df$freq/sum(df$freq)
    df.top <- df[df$prop > quantile(df$prop, 1-(n.genes/dim(df)[1])),]
    df.top <- df.top %>%
      mutate(angle = 90 * sample(c(0, 1), n(), replace = TRUE, prob = c(60, 40)))
    
    # If you wanna change the palette or how many colors
    # there are, adjust the color.choice and divisions
    # Make sure to change the for loop if you change the 
    # num of divisions.
    df.top <- df.top[order(-df.top$freq),]
    color.choice <- brewer.set1(5)
    colors <- rep(0,dim(df.top)[1])
    for(i in 1:5){
      chunk.size <- ceiling(dim(df.top)[1]/5)
      start.ind <- chunk.size * (i-1)
      if(start.ind == 0){start.ind = 1}
      end.ind <- chunk.size * (i)
      colors[start.ind:end.ind+1] <- color.choice[i]
    }
    df.top$color <- colors[1:dim(df.top)[1]]
    
    ggplot(df.top, aes(label=toupper(word),
                       size=freq, 
                       angle=angle, 
                       color=color)) +
      geom_text_wordcloud() +
      scale_size_area(max_size = 10) +
      theme_minimal()
  }
  
  message('Making the RANK ordering column')
  GSEA.table$RANK <- sign(GSEA.table$NES) * GSEA.table$Q.value
  up.sig.count <- 0
  down.sig.count <- 0 
  Q.val <- 0.05
  message("Selecting significantly upregulated pathways")
  while((Q.val < max.Q) & (up.sig.count < min.GSEA.entries)) {
    message(paste0("Qval: ", Q.val, " ;; selected ", up.sig.count, " pathways"))
    up.sig <- GSEA.table$RANK > 0 & abs(GSEA.table$RANK) < Q.val
    up.sig.count <- sum(up.sig)
    Q.val = Q.val + 0.05
  }
  message(paste0("Qval: ", Q.val, " ;; selected ", up.sig.count, " pathways"))
  
  Q.val <- 0.05
  message("Selecting significantly downregulated pathways")
  while(Q.val < max.Q & down.sig.count < min.GSEA.entries) {
    message(paste0("Qval: ", Q.val, " ;; selected ", down.sig.count, " pathways"))
    down.sig <- GSEA.table$RANK < 0 & abs(GSEA.table$RANK) < Q.val
    down.sig.count <- sum(down.sig)
    Q.val <- Q.val + 0.05
  }
  message(paste0("Qval: ", Q.val, " ;; selected ", down.sig.count, " pathways"))
  
  return(list(fun.generate.wordcloud(GSEA.table, up.sig, n.genes), fun.generate.wordcloud(GSEA.table, down.sig, n.genes)))
  
}

fun.GO.wordcloud <- function(GSEA.table, min.GSEA.entries=10, max.Q=0.05, n.genes=30, split.char =','){
  # Given one of Reva's GSEA Tables, generate a WordCloud of the genes
  # associated with the GSEA terms.
  
  # For future use. If we have an error regarding n.genes,
  # That may be because the while loops got to too high of a 
  # Q.val without selecting any suitable pathways. We need to increase
  # the max Q.val. This can also be caused if n.genes > the genes found
  # but I added an if statement that should make this not an issue.
  
  # Something like this may be necessary: GO_results$Leading.edge.genes <- GO_results$geneID
  # if you don't want to actually change the plotting function itself.
  
  # Increasing n.genes increases how many genes we show on the
  # canvas.
  fun.generate.wordcloud <- function(df.with.csv.genes, which.rows, n.genes, split.char =',' ){
    # Helper function. Given the cleaned up dataframe and logical vector
    # of which rows to grab, generate the wordcloud.
    
    # Makes a nice vector of the genes we have
    vector.of.csv.genes <- unlist(sapply(df.with.csv.genes$Leading.edge.genes[which.rows], 
                                         FUN=function(x){
                                           lapply(strsplit(x, split.char), FUN=trimws)
                                         }))
    names(vector.of.csv.genes) <- NULL
    
    # This is pulled from 
    docs <- Corpus(VectorSource(vector.of.csv.genes))
    dtm <- TermDocumentMatrix(docs) 
    matrix <- as.matrix(dtm) 
    words <- sort(rowSums(matrix),decreasing=TRUE) 
    df <- data.frame(word = names(words),freq=words)
    
    # To make this actually return an object, I had
    # to resort to using the ggplot2 wordcloud implementation
    # https://cran.r-project.org/web/packages/ggwordcloud/vignettes/ggwordcloud.html
    df$prop <- df$freq/sum(df$freq)
    if(n.genes > dim(df)[1]){n.genes = dim(df)[1]}
    df.top <- df[df$prop > quantile(df$prop, 1-(n.genes/dim(df)[1])),]
    df.top <- df.top %>%
      mutate(angle = 90 * sample(c(0, 1), n(), replace = TRUE, prob = c(60, 40)))
    
    # If you wanna change the palette or how many colors
    # there are, adjust the color.choice and divisions
    # Make sure to change the for loop if you change the 
    # num of divisions.
    df.top <- df.top[order(-df.top$freq),]
    color.choice <- brewer.set1(5)
    colors <- rep(0,dim(df.top)[1])
    for(i in 1:5){
      chunk.size <- ceiling(dim(df.top)[1]/5)
      start.ind <- chunk.size * (i-1)
      if(start.ind == 0){start.ind = 1}
      end.ind <- chunk.size * (i)
      colors[start.ind:end.ind+1] <- color.choice[i]
    }
    df.top$color <- colors[1:dim(df.top)[1]]
    
    ggplot(df.top, aes(label=toupper(word),
                       size=freq, 
                       angle=angle, 
                       color=color)) +
      geom_text_wordcloud() +
      scale_size_area(max_size = 10) +
      theme_minimal()
  }
  
  message('Making the RANK ordering column')
  GSEA.table$RANK <- GSEA.table$p.adjust
  up.sig.count <- 0
  Q.val <- 1e-5
  message("Selecting significant terms")
  while((Q.val < max.Q) & (up.sig.count < min.GSEA.entries)) {
    message(paste0("Qval: ", Q.val, " ;; selected ", up.sig.count, " pathways"))
    up.sig <- GSEA.table$RANK > 0 & abs(GSEA.table$RANK) < Q.val
    up.sig.count <- sum(up.sig)
    Q.val = Q.val + 0.001
  }
  #print(up.sig)
  message(paste0("Qval: ", Q.val, " ;; selected ", up.sig.count, " pathways"))
  
  return( fun.generate.wordcloud(GSEA.table, up.sig, n.genes, split.char=split.char) )
  
}


fun.match.replace <- function(from.df, into.df, match.col=NULL, replace.col){
  # # My testing
  # set.seed(124)
  # exp1 <- data.frame('a'=c(1:5),
  #                    'b'=sample(c("A","B","C"),5,replace = T )); exp1
  # 
  # exp2 <- data.frame('a'=c(2,5),
  #                    'b'=c('X', "Y")); exp2
  # 
  # exp1$b[!is.na(match(exp1$a, exp2$a))] <- exp2$b
  # 
  # # pseudocode: given the column we want to match by
  # # we will match from ___ into ___ and replace the into
  # # values with from.
  # 
  # # from exp2 match a into exp1. Replace exp1 'b' with exp2 'b'.
  # 
  # fun.match.replace(exp2, exp1, 'a', 'b')
  # 
  # rownames(exp1) <- exp1$a; exp1$a <- NULL; exp1
  # rownames(exp2) <- exp2$a; exp2$a <- NULL; exp2
  # 
  # fun.match.replace(from.df=exp2, into.df=exp1, replace.col = 'b')
  
  # Gotta make sure that match.col is unique!
  into.df.2 <- into.df
  # If the user doesn't give us a matching column, check the rownames.
  if(!is.null(match.col)){
    into.df.2[!is.na(match(into.df.2[,match.col], from.df[,match.col])), replace.col] <- from.df[,replace.col]
  }
  else{
    into.df.2[!is.na(match(rownames(into.df.2), rownames(from.df))), replace.col] <- from.df[,replace.col]
  }
  return(into.df.2[,replace.col])
}

###
# End of helper functions
###




