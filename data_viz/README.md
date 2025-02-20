## data visualization
this directory contains files needed to make plots with [scraped data](https://drive.google.com/drive/folders/1XgHf5oBGeM3tbPtI-WzvOpNLY5MvlX3g?usp=sharing)

TODO sarvy:
- get started on making plots from scraped data 
- popular libraries for plotting data points are `matplotlibs`, `numpy`, `scikit`, and `pandas` look to utilize these when making plots
- update requirements by using `pip freeze > requirements.txt` if you install any python packages
- brainstorm what plots you will make 
    * (understand the data first, what will you plot garages vs. fullness, etc.)
- think about interesting ways to represent the data such that we can initially spot out trends with the naked eye 
    * (i.e. make a plot for fullness from monday -  friday, make a plot for specific times of the day, etc.)
- the stats/ ml model we use for prediction will only perform as well as our data. we have to model our data and tell it to look for certain areas/ patterns in 
particular to ensure that it makes the best predictions
- data modeling/ pattern recognition in this step is important and we'll spend time making different plots to get a feel for the data
- we should also keep track of trends/ patterns like 
    * parking not being full on fridays because less people have class
    * tuesday/ thursday have similar parking fullness
    * monday/ wednesday have similar parking status since those two pairs people have the same class repeated
stuff like that. Save this in a `.txt` file or something in this directory just to keep a log of our brainstorms