# Bklas
All scripts expect the relevant data files in the data directory. A caching feature is used for ease of use. To use this the first time running the program set the `makeData` variable to `True`. This will create a csv files(cache). Next time when running the same program these files can be used as a cache can by setting the `makeData` to `False`. 

# Installation
All scripts should be run with a modern version of Python 3 (3.9 or higher is prefered). \
Some scripts require extra dependencies. Make sure to install all required ones from the requirements.txt. 
```
pip3 install -r requirements.txt
```

# Plots folder:
- main folder: contains all stats(total release, score, price)
- release folder: contains only release stats
- score folder: contains only score stats
- score folder: contains only score stats
- regression folder: contains regression for genres

# Statistics folder:
t-test.csv:
Show t-test results. Includes genres, t-statistic, p-value, slopes

slope.txt:
Results for total amount of increases and decreases in slopes(amount of games released) and the degree of increase:
- increase more than 0.02 large increase in slope; 
- increase between 0 and 0.02 small increase in slope; 
- increase between -0.02 and 0 small decrease in slope; 
- increase more than -0.02 large decrease in slope; 

scores.txt:
Results for total amount of increases and decreases for score
- increase more than 5 large increase in scores; 
- increase between 0 and 5 small increase in scores; 
- increase between -5 and 0 small decrease in scores; 
- increase more than -5 large decrease in scores; 

price.txt:
Results for total amount of increases and decreases for price
- increase more than 10 large increase in prices; 
- increase between 0 and 10 small increase in prices; 
- increase between -10 and 0 small decrease in prices; 
- increase more than -10 large decrease in prices; 