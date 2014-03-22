import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import processing as p
import output_db as o_db
import input_db as i_db
import input_files as i_files
import datetime


path = '../db/'
facility_data_db = i_db.get_facility_db(path)

# ------------- Build Facility Objects --------------
Gahanna = p.Facility("GAH", facility_data_db)

test = Gahanna.df

# print test.date.head()

test['week_num'] = test["date"].apply(lambda x: datetime.date.isocalendar(x)[1])
test['week_day'] = test["date"].apply(lambda x: datetime.date.isocalendar(x)[2])


# print test['week_num'].head()
# print test['week_day'].head()
print test.groupby('week_num')['new_dollars'].aggregate(np.sum)
print test.groupby('week_day')['new_dollars'].aggregate(np.average)
