# Bklas
All scripts expect the relevant data files in the data directory. A caching feature is used for ease of use. To use this the first time running the program set the `makeData` variable to `True`. This will create a csv files(cache). Next time when running the same program these files can be used as a cache can by setting the `makeData` to `False`. 

# Installation
All scripts should be run with a modern version of Python 3 (3.9 or higher is prefered). \
Some scripts require extra dependencies. Make sure to install all required ones from the requirements.txt. 
```
pip3 install -r requirements.txt
```