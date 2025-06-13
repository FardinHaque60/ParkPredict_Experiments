# experiments
this directory contains all the experiments for predicting fullness given a time

## experiment set up
experiments are set up by loading data, training models, and performing inferences. experiments compare the models performance when trained on the entire data set vs. partitions. training data includes 2 features (timestamp, fullness). models predict fullness based solely on timestamp. experiments use models that include:
- knn
- random forest
- guassion regression
- decision tree regression
- sinusoidal regression
<br> still need to do: 
- support vector regression 
- bayesian regression
- generalized additive model

## performance measure
r^2 will be the primary metric in determining how well the prediction is doing and how it can be used to compare model performance from the experiments. RMSE and MAE will additionally be used

## model validation
models will be compared against the entire dataset to see how well it does on it but also on chosen test and validation data points

## future
future experiments may be conducted to make a prediction model for the inverse problem: predicting the first time a given fullness will appear