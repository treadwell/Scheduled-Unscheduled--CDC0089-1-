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


latest_iso_day = test.date.iget(-1)

# def generate_weekly_forecast(dataframe, statistic):
# 	''' Generate a weekly forecast of the selected statistic using a simple YTD change from 2013 to
# 	    the current year. This won't work for the first week of the year'''
# 	latest_iso_week = datetime.date.isocalendar(dataframe.date.iget(-1))[1]
# 	year = datetime.date.isocalendar(self.df.date.iget(-1))[0]

# 	# calculate cumulative statistic for YTD 2013

# 	ytd_2013 = self.df[(self.df.week_num < latest_iso_week) & (self.df.year == 2013)][statistic].sum()

# 	# calculate cumulative statistic for current year

# 	ytd_current = self.df[(self.df.week_num < latest_iso_week) & (self.df.year == year)][statistic].sum()


# 	growth = float(ytd_current) / ytd_2013

# 	# aggregate base data by week

# 	weekly_2013 = self.df[(self.df.year == 2013)].groupby('week_num')[statistic].aggregate(np.sum)

# 	# generate forecast

# 	forecast = weekly_2013.apply(lambda x: x * growth)

# 	return forecast


# plot multiple stats ytd against each other

# aggregate data by week into new data frame, index by week in a dataframe

# weekly['2013_new'] = pd.Dataframe(test[(test.year == 2013)].groupby('week_num')['new_dollars'].aggregate(np.sum))
# weekly['2014_new'] = test[(test.year == 2014)].groupby('week_num')['new_dollars'].aggregate(np.sum)

# cum_ytd_2013_new_dollars = test[(test.year == 2013)].new_dollars.cumsum()
# cum_ytd_2014_new_dollars = test[(test.year == 2014)].new_dollars.cumsum()

# cum_ytd_2013_new_dollars.plot()
# cum_ytd_2014_new_dollars.plot()
# plt.legend()
# plt.show()

# split into years

data_2013 = test[(test.year == 2013)]

print data_2013.new_dollars.tail()

weekly_2013 = data_2013.groupby('week_num')['new_dollars'].aggregate(np.sum)

print weekly_2013.tail()

data_2014 = test[(test.year == 2014)]

weekly_2014 = data_2014.groupby('week_num')['new_dollars'].aggregate(np.sum)

print weekly_2014.tail()

combined = pd.concat([weekly_2013, weekly_2014], axis=1)

combined.columns = ['2013', '2014']

combined['cum_2013']=combined['2013'].cumsum()

combined['cum_2014']=combined['2014'].cumsum()

print combined.head(20)

columns = ['cum_2013', 'cum_2014']

combined = combined[columns]

combined.plot()

plt.show()




weekly_groups = test.groupby(['year','week_num'])

grouped = weekly_groups.new_dollars.aggregate(np.sum)
#print grouped








# calculate daily cumulative for each annual group and plot

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
