from datetime import datetime
import sqlite3


def get_facility_db(path, cls):
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
            d_value = cls(datetime.strptime(d[0], '%Y-%m-%d').date(), facility, d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8])
            facility_data_db[d_key] = d_value
    return facility_data_db
