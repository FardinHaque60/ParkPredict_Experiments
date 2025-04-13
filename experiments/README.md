# experiments
this directory contains all the experiments for predicting fullness given a time

## methods 
the following methods will be used to perform the experiments:
* sinusodial regression
* fourier series regression
* tree-based model (random forest, XGBoost, LightGBM)
* neural network (large dataset)
* gaussian process regression (small dataset)

## performance measure
RMSE will be used to determine how well the prediction is doing and how it can be used to compare model performance from the experiments.

## test validation
random data points will be chosen from the scraped data and model outputs will be compared with actual data point.

## future
future experiments will look to make a prediction model for the inverse problem: predicting the first time a given fullness will appear