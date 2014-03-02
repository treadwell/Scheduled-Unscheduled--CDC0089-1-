import processing as p
from datetime import datetime
import sqlite3
import os


def get_facility_db(path):
    '''retrieve data from database into Daily_Prodn objects'''
    facility_data_db = {}
    name = "facility_data.db"
    print "current working directory:", os.getcwd()
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
            d_value = p.Daily_Prodn(datetime.strptime(d[0], '%Y-%m-%d').date(), facility, d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8])
            facility_data_db[d_key] = d_value
    return facility_data_db

if __name__ == '__main__':
    print "------------------- Unit tests -------------------"
    path = "../test_db/"
    assert get_facility_db(path)[("GAH","2014-01-15")].sched == 4520

