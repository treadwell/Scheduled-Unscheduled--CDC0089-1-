import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import processing as p
import output_db as o_db
import input_db as i_db
import input_files as i_files
import datetime

import sklearn

path = '../db/'
facility_data_db = i_db.get_facility_db(path)

# ------------- Build Facility Objects --------------
Gahanna = p.Facility("GAH", facility_data_db)

print Gahanna.df['ship_dollars'].tail()