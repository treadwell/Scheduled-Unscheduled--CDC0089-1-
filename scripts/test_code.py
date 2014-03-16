import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import processing as p
import output_db as o_db
import input_db as i_db
import input_files as i_files
import datetime

import sklearn
from statsmodels.tsa.arima_model import ARIMA as a

path = '../db/'
facility_data_db = i_db.get_facility_db(path)

# ------------- Build Facility Objects --------------
Gahanna = p.Facility("GAH", facility_data_db)

print Gahanna.df['ship_dollars'].tail()

test = Gahanna.df['new_dollars']

# MA_length = 2
# Gahanna.df["MA_control"] = pd.rolling_mean(test, MA_length)

# print Gahanna.df["MA_control"]
## cast index to datetime; not automatically a datetime for some reason
test.index = pd.to_datetime(test.index)

#test = test[-100:] # speed up ARIMA calculations for testing

p, d, q = 7, 2, 0
model = a(test, (p, d, q))
x = model.fit()
MA = x.predict()


Gahanna.df = Gahanna.df[d:] # slice the entire data frame first; can't slice one col
Gahanna.df["MA"] = MA

#assert L == len(Gahanna.df["new_dollars"])
# Gahanna.df = Gahanna.df[MA_length:] # drop NaN's from MA_control
                                    #so plot_dual doesn't fail

### make sure plot_dual handles NaN's, and also accounts for mis-matched lengths
### (either with a better error or with automatic trimming)

# Gahanna.plot_dual("MA", "MA_control")
Gahanna.plot_dual("MA", "new_dollars")    

