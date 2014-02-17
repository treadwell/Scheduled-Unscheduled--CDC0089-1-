import sqlite3
from processing import *



def get_facility_db(path):  
    '''retrieve data from database into Facility objects'''
    facility_data_db = {}
    name = "facility_data.db"
    conn = sqlite3.connect(path + name)
    c = conn.cursor()
    for f in ["Gahanna", "Ashland", "Groveport"]:
        if f == "Gahanna":
            facility = "GAH"
        elif f == "Ashland":
            facility = "ASH"
        else:
            facility = "GRO"
        c.execute("Select * from " + f)
        data = c.fetchall()
        for d in data:
            d_key = (facility, str(d[0]))
            d_value = Facility(str(d[0]), facility, d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8])
            facility_data_db[d_key] = d_value
    return facility_data_db