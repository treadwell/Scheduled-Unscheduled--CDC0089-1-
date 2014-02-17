### Output Layer ###

def display_fac(facility,date):  
    '''outputs tab-separated data for cut-and-paste to spreadsheet'''
    f = facility_data[(facility,date)]
    return '\t'.join([str(f.new), str(f.sched), str(f.unsched), str(f.ship), str(f.susp), str(f.old), str(f.future), str(f.hold)])

def cvs_fac(facility,date):  
    '''outputs csv data in list to drive automatic insertion to spreadsheet
        insertion in fac_to_csv function'''
    f = facility_data[(facility,date)]
    return [f.new, f.sched,	f.unsched, f.ship, f.susp, f.old, f.future, f.hold ]

def fac_to_screen(date):
    ''' combines output from all facilities for cust and paste to spreadsheet'''
    print date, display_fac('GAH', date), display_fac('ASH', date), display_fac('GRO', date)

def fac_to_csv(date):
    ''' combines output from all facilities and automatically inserts them into a spreadsheet'''
    save_filename = 'Scheduled Unscheduled.csv'
    csvRow = [date] + cvs_fac('GAH', date) + cvs_fac('ASH', date) + cvs_fac('GRO', date)
    myfile = open(path + save_filename,'a')
    writer = csv.writer(myfile)
    writer.writerow(csvRow)
    myfile.close()
    print date, "data saved to file:", save_filename



def fac_to_db(facility, date):
    '''updates data from all files in a directory to a database'''
    name = "facility_data.db"
    path = "../db/"
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
        raise UnsupportedFacility
        
    # create table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS ''' + table + schema)
    
    c.execute("INSERT INTO " + table + " VALUES " + str(insert_tuple(facility,date)))
    conn.commit()
    conn.close()
    return

def insert_tuple(facility,date):
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

def incr_db_update():
    '''Compares records in a database with data available from a directory and updates
    the missing data in the database.  This supercedes the bulk update approach above.'''
    # retrieve db records
    get_facility_db('../db/')

    # retrieve data from files
    read_dir('../data/')

    # determine missing records from database
    missing_records = list(set(facility_data.keys())-set(facility_data_db.keys()))
    print missing_records

    # updates db with missing records
    for r in missing_records:
        fac_to_db(r[0],r[1])
        
    # checks
        assert len(facility_data_db) + len(missing_records) == len(facility_data)

### ------------------------- Output Unit Tests  ------------------------- 

if __name__ == '__main__':
    print "------------------- Unit tests -------------------"
    date = "1970-01-01"
    new = 1000
    sched = 1000
    unsched = 2000
    ship = 3000
    susp = 50
    old = 100
    future = 200
    hold = 300
    for location in ["GAH", "ASH", "GRO"]:
        facility_data[(location,date)] = Facility(date, location, new, sched,
                 unsched, ship, susp, old, future, hold)
    print "Test objects:\n"
    print facility_data, "\n"
    
    assert display_fac("GAH",date) == "1000\t1000\t2000\t3000\t50\t100\t200\t300"
    assert cvs_fac("GAH", date) == [1000, 1000, 2000, 3000, 50, 100, 200, 300]
    assert insert_tuple("GAH",date) == ('1970-01-01', 1000, 1000, 2000, 3000, 50, 100, 200, 300)