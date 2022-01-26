# Entry 1: Stat Quest t-Test
I would like to follow along with his example by using a real life 
example from GSE155882. This is a single cell dataset that has 4
conditions: control, TAC, TAC+JQ1, TAC+JQ1 withdrawn. Well I could make
a matrix of <br>


[200 most variable genes x 10 cells from each condition, from each cluster(1000 cells)] + 
the associated meta data<br>


With this we can follow along with 
https://www.youtube.com/watch?v=NF5_btOaCig&t=428s, and hopefully get a much
better understanding of t-Tests!


Here is the code I used to make it
## R file "Make a seurat object into toy CSV files"
```
###
# Making small toy dataset
###
seurat.fibrosis <- readRDS("/SRA_store/shared/repo/disco/sc_resources/public_datasets/GSE155882/scripts/intermediate_seurat/integrated/integrated_sham_TAC_unannotated_2021-11-24.rds")

# Lets look at our object and remember what it is about
DimPlot(seurat.fibrosis, group.by="assay.ident")
colnames(seurat.fibrosis@meta.data)
# [1] "orig.ident"             "nCount_RNA"             "nFeature_RNA"          
# [4] "percent.mt"             "integrated_snn_res.0.1" "seurat_clusters"       
# [7] "assay.ident"

# Genes we want to grab
top.variable.genes <- head(VariableFeatures(seurat.fibrosis), 200)
top.variable.genes <- c(top.variable.genes, 'Meox1')

# Cells we want to grab
random.20.TAC.cells <- subset(x = seurat.fibrosis[,seurat.fibrosis[['assay.ident']]=='TAC'], downsample = 50)
random.20.control.cells <- subset(x = seurat.fibrosis[,seurat.fibrosis[['assay.ident']]=='sham'], downsample = 50)

# Looking at our current haul
DimPlot(random.20.control.cells) + DimPlot(random.20.TAC.cells)
FeaturePlot(seurat.fibrosis, features = 'Meox1', split.by = 'assay.ident')

# Lets grab the counts and data
# Counts
hist(random.20.TAC.cells@assays$RNA@counts['Ccl21a',])
VlnPlot(random.20.control.cells, features = 'Ccl21a')

hist(random.20.TAC.cells@assays$RNA@counts['Meox1',])
VlnPlot(random.20.control.cells, features = 'Meox1')

matrix.control.cell.counts <- as.matrix(random.20.control.cells@assays$RNA@counts[top.variable.genes,])
dim(matrix.control.cell.counts)
# [1] 201 700

matrix.TAC.cell.counts <- as.matrix(random.20.TAC.cells@assays$RNA@counts[top.variable.genes,])
dim(matrix.TAC.cell.counts)
# [1] 201 641

matrix.cell.counts <- cbind(matrix.control.cell.counts, matrix.TAC.cell.counts)
dim(matrix.cell.counts)
# [1]  201 1341

# Normalized data
hist(random.20.TAC.cells@assays$RNA@data['Ccl21a',])
VlnPlot(random.20.control.cells, features = 'Ccl21a')

hist(random.20.TAC.cells@assays$RNA@data['Meox1',])
VlnPlot(random.20.control.cells, features = 'Meox1')

matrix.control.cell.data <- as.matrix(random.20.control.cells@assays$RNA@data[top.variable.genes,])
dim(matrix.control.cell.data)
# [1] 201 700

matrix.TAC.cell.data <- as.matrix(random.20.TAC.cells@assays$RNA@data[top.variable.genes,])
dim(matrix.TAC.cell.data)
# [1] 201 641

matrix.cell.data <- cbind(matrix.control.cell.data, matrix.TAC.cell.data)
dim(matrix.cell.data)
# [1]  201 1341

# Grabbing the meta data for the cells I just got
seurat.fibrosis.small <- subset(seurat.fibrosis, cells = colnames(matrix.cell.data))
matrix.cell.meta.data <- seurat.fibrosis.small@meta.data


# Writing data to files
write.table(matrix.cell.counts, 
            file = './intermediate_misc/fibrosis_toy_counts.csv',
            sep=',')
write.table(matrix.cell.data, 
            file = './intermediate_misc/fibrosis_toy_data.csv',
            sep=',')
write.table(matrix.cell.meta.data, 
            file = './intermediate_misc/fibrosis_toy_meta_data.csv',
            sep=',')
###
# End of making small toy dataset
###
```