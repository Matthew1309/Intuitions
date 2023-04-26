# 4/26/2023
I believe some python tips may be useful to note:
1. To see all functions for an object use `dir(obj)`
1. To get just attributes use obj.__dict__ (note it may not always work)
1. For pandas we have
	1. df.describe()
	1. df.shape
	1. df.head()
	1. df.dtypes()

# 4/21/2023
I made a script to easily pull pdfs and htmls of pubmed articles. Perhaps this will be useful in the future for a machine
learning project to produce a large language model to help me in understanding biology better :)

# 6/22/2022
I've had the issue where I'm given two matricies, one with data and one with meta
data for the columns. The issue is how to group the data.matrix based on the info
contained within the meta.matrix!


Today in R I learned of two ways: one using ```tapply```, and the other using ```purrrlyr```.
Apparently python pandas can also somewhat do this: https://stackoverflow.com/questions/20905713/equivalent-of-rs-tapply-in-python-pandas


However, all these methods seem to work off of the same core concept. The concept that the initial data.matrix
shaped like n x m (n=rows, m=columns) and the meta.matrix shaped like m x g (m=rows, 
g=groups/columns), can be simply combined by transposing the data.matrix into m x n, then
appending/indexing by the meta.matrix.


I like the tapply because you can see what is happening; I don't understand ```purrrlyr```,
so I won't attempt to explain the code. Here is the apply method:
```
apply(data.matrix, 2, FUN=function(x){
		tapply(x, meta.data[,<column of interest>], mean, na.rm=T)})
```

This goes column by column ```apply(,2,)``` passing each column to ```tapply```.
```tapply``` somehow maps the column to the column found in meta.data we selected,
then it simply knows that we need to group by the factors found in meta.data, and
take the mean.

## Simple as this!
