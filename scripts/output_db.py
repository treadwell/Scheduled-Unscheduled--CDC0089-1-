import sqlite3


def fac_to_db(facility, date, facility_data):
    '''updates data from all files in a directory to a database'''
    name = "facility_data.db"
    path = "./db/"
    schema = "(date integer, new integer, sched integer, unsched integer, ship integer, susp integer, old integer, future integer, hold integer)"
    conn = sqlite3.connect(path + name)
    c = conn.cursor()
	    
    if facility == "GAH":
        table = "Gahanna"
    elif facility == "ASH":
        table = "Ashland"
    elif facility == "GRO":
        table = "Groveport"
    else:
        raise UnsupportedFacilityException
        
    # create table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS ''' + table + schema)
    
    c.execute("INSERT INTO " + table + " VALUES " + str(insert_tuple(facility,date, facility_data)))
    conn.commit()
    conn.close()
    return

def insert_tuple(facility,date, facility_data):
    '''Creates a tuple of facility data for insertion into a database'''
    f = facility_data[(facility,date)]
    return (f.date, f.new, f.sched, f.unsched, f.ship, f.susp, f.old, f.future, f.hold)


# populate the database
def populate_database():
    '''Deprecated. Bulk update of database from a dictionary of facility-date objects'''
    dates = sorted(list(set([date for facility, date in facility_data.keys()])))
    locations = sorted(list(set([facility for facility, date in facility_data.keys()])))
    for date in dates:
        for location in locations:
            fac_to_db(location, date)    
    print "database update completed"