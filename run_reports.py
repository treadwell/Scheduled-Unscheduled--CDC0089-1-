import scripts.processing as p
import scripts.input_db as i_db
import os
import pandas as pd
import matplotlib.pyplot as plt

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

# ------------- Print warnings --------------

Gahanna.warnings()
Ashland.warnings()
Ashland.plot_trend('in_process_dollars')
Groveport.warnings()
Ryerson.warnings()
TotalDomestic.warnings()

#Ryerson.plot_dual("in_process_dollars", "ship_MA10_dollars")
#Ryerson.plot_trend('ship_dollars')

# ------------- Plot basic trend panels --------------

#Gahanna.plot_stats()
#Ashland.plot_stats()
#Groveport.plot_stats()
#Ryerson.plot_stats()

# -------------- Plot basic summary stats ---------------
Gahanna.summary()
Ashland.summary()
Groveport.summary()
Ryerson.summary()
TotalDomestic.summary()

# -------------- Plot YTD comparisons ---------------

Gahanna.plot_ytd_comparison('new_dollars')
Gahanna.plot_ytd_comparison('new_orders')
Gahanna.plot_ytd_comparison('new_lines')
Gahanna.plot_ytd_comparison('new_units')
print "-----------------"
Ashland.plot_ytd_comparison('new_dollars')
Ashland.plot_ytd_comparison('new_orders')
Ashland.plot_ytd_comparison('new_lines')
Ashland.plot_ytd_comparison('new_units')
print "-----------------"
Groveport.plot_ytd_comparison('new_dollars')
Groveport.plot_ytd_comparison('new_orders')
Groveport.plot_ytd_comparison('new_lines')
Groveport.plot_ytd_comparison('new_units')
print "-----------------"
Ryerson.plot_ytd_comparison('new_dollars')
Ryerson.plot_ytd_comparison('new_orders')
Ryerson.plot_ytd_comparison('new_lines')
Ryerson.plot_ytd_comparison('new_units')
