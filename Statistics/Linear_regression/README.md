# Entry 1: Inuition via simple simple problem?
I thought of how to test out linear regression explaination. Two question survey
"are you a boy?" yes, no; and "do you like firetrucks?" yes, no; with the goal of figuring 
out if this person is a boy or a girl. Plot this where Q1 is X-axis, Y-axis is Q2, and color
by actual gender. How do we draw a line through this data to always classify girls from boys,
and how much variation is explained by each question. Is this a good mock problem?

# Entry 2: Using the EDXWELCOME problem
I have been following a course called "An Introduction to Statistical Learning, with Applications in R (Second Edition)" (James, Witten, Hastie, Tibshirani - Springer 2021). This textbook is available at https://www.statlearning.com/. They actually provide some datasets, and give hints to some R programming languages.

That being said, I think I would like to do some of this in Python and use my matplotlib skills to make plots like the ones in StatQuest https://www.youtube.com/watch?v=PaFPbb66DxQ.

# Classification_Iris
I added this intitially to practice linear regression, but I now realize this is actually a classification problem! I suppose I should actually follow along with the Hastie-Tibshirani video examples and make an R module for true LR.

First thing I did here was plot the corr-scat-plots like they did in the tutorial. I really like this representation!

# Predicting_classes_from_gene_expression.ipynb
I read in my dataset from GSE76118 to practice using Lasso as a logit multiclass classifier. Seems to have worked pretty
easily. I haven't tested it on out of dataset samples, but I worry there may be some issues. I read in normalized data of the gene counts, and I'm wondering if it may be a better move to read in raw counts, and then make a standardizable way of normalization, so that any future dataset can be normalized in a similar manner.

In the edX course they talk about normalizing to standard deviation (can that work here?) How does seurat normlazation work?