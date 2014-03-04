import scripts.processing as p
import scripts.input_db as i_db
import os
import pandas as pd

# Calculate facility backlogs

#print os.getcwd()
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
Groveport.warnings()
Ryerson.warnings()
TotalDomestic.warnings()

# add plotting of relevant charts when warning is triggered


# ------------- Plot basic trends --------------

Gahanna.plot_trend("new_dollars")

Ashland.plot_trend("new_dollars")
Ashland.plot_trend("new_units")

Groveport.plot_trend("new_dollars")
Groveport.plot_trend("new_units")
