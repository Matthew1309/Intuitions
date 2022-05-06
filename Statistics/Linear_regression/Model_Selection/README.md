# 5/6/2022
I have finished the model selection portion of the edX statistical learning course.
I applied the information I learned to a dataset from work where I am trying to model cardiac development. I wanted to note that in the course they didn't cover how to extract information and make predictions using their identified best models using the ```regsubsets``` and ```glmnet``` functions.

### Making predictions using the best forward selection model
First thing you must do is save the object to an RDS file. In my case I called it ```10f_CV_forwadsel_atria_2022-05-06.rds```. When you read this file in, you also need to note the results of the 10-fold CV when chosing the best model. In my case it was model 13, which containted the 13 most informative genes.

Once you have this object read in, you need to make sure the ```library(leaps)``` package is loaded in. Copy over our predict.regsubset convenience function. Extract the most gene names that went into making the fit. Cut the full dataset to just these genes as our columns. Then run the ```predict.regsubset(fit, as.matrix(new.data), idOfBestModel)``` command. Thats it! That is how we make a new prediction.

### Making predictins using the best Lasso model
Similar to forward selection, you need to save the file. In my case I called it ```lasso_fit_atria_2022-05-06.rds```. When you read the file in, you once again need to note the best values of lambda that resulted from the CV. These can be found by looking at ```lasso.cv$lambda.1se``` or ```lasso.cv$lambda.min```. The 1se value is a harsher model that is 1 standard error away from the best value.

With these values, we can extract the names of the genes that fit the model from ```lasso.obj$beta@Dimnames[[1]]```, subset our validation set to just these columns, and run a prediction using the ```predict.glmnet(lasso.obj, as.matrix(new.data), s=lasso.cv$lambda.min)``` function. For this to work make sure that the ```library(glmnet)``` command has been run.

