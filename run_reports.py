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
Groveport.warnings()
Ryerson.warnings()
TotalDomestic.warnings()

# ------------- Plot basic trend panels --------------

#Gahanna.plot_stats()
#Ashland.plot_stats()
#Groveport.plot_stats()

# -------------- Plot basic summary stats ---------------
Gahanna.summary()
Ashland.summary()
Groveport.summary()
Ryerson.summary()
TotalDomestic.summary()