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
#print test.groupby('week_num')['new_dollars'].aggregate(np.sum)
#print test.groupby('week_day')['new_dollars'].aggregate(np.average)

latest_iso_day = test.date.iget(-1)
latest_iso_week = datetime.date.isocalendar(test.date.iget(-1))[1]

print "latest day:", latest_iso_day
print "latest week:", latest_iso_week

# cut down to current week only

ytd_2013_new_dollars = test[(test.week_num <= latest_iso_week - 1) & (test.year == 2013)].new_dollars.sum()

print "YTD 2013 new dollars:", ytd_2013_new_dollars

ytd_2014_new_dollars = test[(test.week_num <= latest_iso_week - 1) & (test.year == 2014)].new_dollars.sum()

print "YTD 2014 new dollars:", ytd_2014_new_dollars

growth = float(ytd_2014_new_dollars) / ytd_2013_new_dollars

print growth

# annual_groups = test_through_current_week.groupby('year')

# # calculate weekly cumulative for each annual group

# for name, annual_group in annual_groups:
# 	annual_weekly = annual_group.groupby('week_num')['new_dollars'].aggregate(np.sum)
# 	YTD = sum(annual_weekly)

# 	print name, annual_weekly
# 	print "sum:", name, YTD


# # calc a ytd sum through the previous week
# weekly = test.groupby('week_num')['new_dollars'].aggregate(np.sum)  # this has 2 years of data all munged together in it

# print type(weekly)
# print len(weekly)

# print "Series name:", weekly.name
# #annual_groups = weekly.groupby('year')

# print weekly.head()

# cumsum_by_week = weekly.cumsum()

# print cumsum_by_week.head()
# #weekly = g = df.groupby('A')

# #  group by year, then do cumsum by week

# #In [16]: g.cumsum()
# # do it for 2013 and for 2014

# # make a multiplier

# apply the multiplier for the next 4 (or howerver many) weeks
