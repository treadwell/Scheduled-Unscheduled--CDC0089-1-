import scripts.processing as p
import scripts.input_db as i_db
import os
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# ------ Get facility data from database ------

path = './db/'
facility_data_db = i_db.get_facility_db(path)

# ------------- Build Facility Objects --------------

Gahanna = p.Facility("GAH", facility_data_db)
Ashland = p.Facility("ASH", facility_data_db)
Groveport = p.Facility("GRO", facility_data_db)
Ryerson = p.Facility("RYE", facility_data_db)
DeSoto = p.Facility("DES", facility_data_db)
TotalDomestic = p.Facility("TOT", facility_data_db)

start = datetime.date(2013,1,1)
end = datetime.date(2013,12,31)

print start
print end


def rolling_n_variance(facility, statistic, n):
	today = datetime.date.today()
	#print today
	thirty_days_ago = datetime.date.today() + datetime.timedelta(-30)
	#print thirty_days_ago
	last_year_today = datetime.date.today() + datetime.timedelta(-365)
	#print last_year_today
	last_year_thirty_days_ago = datetime.date.today() + datetime.timedelta(-365) + datetime.timedelta(-30)
	#print last_year_thirty_days_ago
	CY = facility.df[statistic][(TotalDomestic.df.date >= thirty_days_ago) & (TotalDomestic.df.date <= today)].sum()
	#print CY
	PY = facility.df[statistic][(TotalDomestic.df.date >= last_year_thirty_days_ago) & (TotalDomestic.df.date <= last_year_today)].sum()
	#print PY
	return float(CY)/PY

print rolling_n_variance(Ashland, "new_dollars", 30)

print "2013 Domestic Dollars ($m):", format(TotalDomestic.df["new_dollars"][(TotalDomestic.df.date >= start) & (TotalDomestic.df.date <= end)].sum(), ",")
print "2013 Domestic New Units:", format(TotalDomestic.df["new_units"][(TotalDomestic.df.date >= start) & (TotalDomestic.df.date <= end)].sum(), ",")
print "2013 Domestic Sched Units:", format(TotalDomestic.df["sched_units"][(TotalDomestic.df.date >= start) & (TotalDomestic.df.date <= end)].sum(), ",")

print"\n2013 Gahanna Dollars ($m):", format(Gahanna.df["new_dollars"][(Gahanna.df.date <= end) & (Gahanna.df.date >= start) ].sum(), ",")

print "2013 Gahanna Sched Units:", format(Gahanna.df["sched_units"][(Gahanna.df.date >= start) & (Gahanna.df.date <= end)].sum(), ",")
print "2013 Groveport Sched Units:", format(Groveport.df["sched_units"][(Groveport.df.date >= start) & (Groveport.df.date <= end)].sum(), ",")
print "2013 Ashland Sched Units:", format(Ashland.df["sched_units"][(Ashland.df.date >= start) & (Ashland.df.date <= end)].sum(), ",")

print "Ashland change in rolling 30 scheduled units", rolling_n_variance(Ashland, "sched_units", 30)

# rng = pd.date_range(start, end)

# print rng

# print TotalDomestic.df["new_dollars"].rng
