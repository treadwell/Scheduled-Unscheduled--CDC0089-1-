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

print "2013 Domestic Dollars ($m):", format(TotalDomestic.df["new_dollars"][(TotalDomestic.df.date >= start) & (TotalDomestic.df.date <= end)].sum(), ",")
print "2013 Domestic New Units:", format(TotalDomestic.df["new_units"][(TotalDomestic.df.date >= start) & (TotalDomestic.df.date <= end)].sum(), ",")
print "2013 Domestic Sched Units:", format(TotalDomestic.df["sched_units"][(TotalDomestic.df.date >= start) & (TotalDomestic.df.date <= end)].sum(), ",")

print"\n2013 Gahanna Dollars ($m):", format(Gahanna.df["new_dollars"][(Gahanna.df.date <= end) & (Gahanna.df.date >= start) ].sum(), ",")

print "2013 Gahanna Sched Units:", format(Gahanna.df["sched_units"][(Gahanna.df.date >= start) & (Gahanna.df.date <= end)].sum(), ",")
print "2013 Groveport Sched Units:", format(Groveport.df["sched_units"][(Groveport.df.date >= start) & (Groveport.df.date <= end)].sum(), ",")
print "2013 Ashland Sched Units:", format(Ashland.df["sched_units"][(Ashland.df.date >= start) & (Ashland.df.date <= end)].sum(), ",")

# rng = pd.date_range(start, end)

# print rng

# print TotalDomestic.df["new_dollars"].rng
