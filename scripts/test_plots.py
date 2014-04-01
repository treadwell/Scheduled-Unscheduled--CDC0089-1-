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

Gahanna = p.Facility("GAH", facility_data_db)

print Gahanna.df['week_day'].tail()
print Gahanna.df['day_of_year'].tail()

g = Gahanna.df

Gahanna.plot_trend("new_orders")
Gahanna.plot_stats()

weekday_groups = g.groupby(g.week_day)

for name, group in weekday_groups:
    #group.new_dollars.plot()
    #plt.plot(group.new_dollars, label = name)
    group.smooth = pd.rolling_mean(group.new_dollars, window = 10)
    plt.plot(group.smooth, label = 'rolling({k})'.format(k=name))

plt.legend(loc = "best")
plt.show()

### version 2
# grouped = g.groupby(g.week_day)

# for name, group in grouped:
#     group.new_dollars.plot()
    

#plt.legend()
# plt.show()

### version 3
grouped = g.groupby(g.week_day)

L = len(grouped)
height = 2
length = (L+1)//2

for i, (name, group) in enumerate(grouped):
    plt.subplot(height*100 + length*10 + (i+1))
    ## should probably be done as string concatenation
    group.new_dollars.plot()
    

# http://matplotlib.org/examples/pylab_examples/anscombe.html

#plt.legend()
plt.show()