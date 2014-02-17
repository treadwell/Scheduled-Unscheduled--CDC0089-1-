import re
import os
import csv
import sqlite3
from datetime import datetime
from re import sub

### Processing Layer ###

class Facility(object):
    def __init__(self, date, location, new, sched,
                 unsched, ship, susp, old, future, hold):
        
        # properties:
        # location: GAH, ASH, or GRO
        # date
        # new: new_orders
        # sched: scheduled orders
        # unsched: unscheduled orders
        # ship: ship confirms
        # susp: suspended orders
        # old: old in process
        # future: future orders
        # hold: hold or problem orders

        # can do arbitrary things with the input, like any fn
        # print date
        # date = datetime.datetime(date)
        
        # this is a schema

        self.date = date
        #  assert location in ('GAH', 'ASH', 'GRO')
        self.location = location
        self.new = new
        self.sched = sched
        self.unsched = unsched
        self.ship = ship
        self.susp = susp
        self.old = old
        self.future = future
        self.hold = hold
    
    def __repr__(self):
        return str(self.__dict__)

    # __str__ = __repr__ ## uncomment this if printing doesn't work well

def calc_facility_backlog(facility):
    '''Calculates backlog in a facility over time and returns most recent backlog'''
    # Accept only "GAH", "ASH", "GRO"
    # Cycle through facility_data_db, pulling values for facility into a list
    facility_list = [value for value in facility_data_db.values() if value.location == facility]
    
    # calculate the orders in process
    for date_object in facility_list:
        date_object.in_process = date_object.sched + date_object.unsched + date_object.old + date_object.future + date_object.hold
  
    # order the list by date
    facility_list.sort(key=lambda x: x.date)
    print "---------------------------"
    
    # calculate moving average processing (eliminating zeros)
    for i, date_object in enumerate(facility_list):
        if i > 10:
            cumsum = 0
            cumcount = 0
            for j in xrange(0,9):
                if facility_list[i-j].ship >0:
                    cumsum += facility_list[i-j].ship
                    cumcount += 1
            date_object.ship_MA10 = int(cumsum/cumcount)
        else:
            date_object.ship_MA10 = 0

    # calculate backlog
    for date_object in facility_list:
        if date_object.ship_MA10 >0:
            date_object.backlog = float(date_object.in_process)/date_object.ship_MA10
        elif date_object.ship > 0:
            date_object.backlog = float(date_object.in_process)/date_object.ship
        else:
            date_object.backlog = None
    
    return facility_list[-1]

def plot_facility_trends(facility):
    # print daily orders processed, MA processing, orders in process, backlog
    # plot all of that
    pass

### Input Layer ###

facility_names = {"GAH":"Gahanna", "ASH":"Ashland", "GRO":"Groveport"}
# order_types gives the line location of the various order type data
order_types = {'new':11, 'sched':36, 'unsched':49, 'ship':60, 'susp':63, 'old':66, 'future':67, 'hold':68}
order_type_names = ['new', 'sched', 'unsched', 'ship', 'susp', 'old', 'future', 'hold']
# L-names gives the column location of facility dollar fields
L_names = {'GAH':[52,60], 'ASH':[90,96], 'GRO':[126,132]} 
    
facility_data = {}
def read_file(path, filename):
    '''Parses text file, creating dictionary of Facility objects'''
    with open(path + filename) as f:
        # alternative: pull things directly by line number
        lines = list(f)

    assert "TOTAL NEW ORDERS" in lines[11]
    assert "TOTAL SCHEDULED ORDERS" in lines[36]
    assert "TOTAL UNSCHEDULED ORDERS" in lines[49]
    assert "TOTAL SHIPMENT CONFIRM" in lines[60]
    assert "SUSPENDED SHIPMENTS" in lines[63]
    assert "OLD INPROCESS (INP)" in lines[66]
    assert "FUTURE DATED" in lines[67]
    assert "HOLDS / ERRORS" in lines[68]

    date = str([word for word in lines[1].split() if '/' in word]).strip("[]\'")
    date = datetime.strptime(date, '%m/%d/%y')
    date = date.strftime('%Y-%m-%d')
    

    for L in L_names.keys():  # cycle through the locations, sequence doesn't matter
        order_type_data = []
        order_type_data_1 = []

        for o in order_type_names:  # cycle through order_types.  Sequence matters, necessitating a separate list
            order_type_data.append(lines[order_types[o]][L_names[L][0]:L_names[L][1]].replace(' ', ''))
	    
        for d in order_type_data:
            if d == '':
                order_type_data_1.append(0)
            else:
                order_type_data_1.append(int(sub(r'[^\d.]', '', d)))

        facility_data[(L,date)] = Facility(date, L, *order_type_data_1)

    return date, facility_data

#date, facility_data = read_file(path, filename)

def read_dir(path):
    '''Retrieves correct files from directory into a list'''
    files = os.listdir(path)
    data_files = [file for file in files if 'CDC0089' in file]
    for file in data_files:
        read_file(path, file)
    
facility_data_db = {}

def get_facility_db(path):  
    '''retrieve data from database into Facility objects'''
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
    path = "/users/kbrooks/Documents/MH/Projects/Metrics/Distribution/Scheduled Unscheduled (CDC0089-1)/"
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

def incr_db_update(path):
    '''Compares records in a database with data available from a directory and updates
    the missing data in the database.  This supercedes the bulk update approach above.'''
    # retrieve db records
    get_facility_db(path)

    # retrieve data from files
    read_dir(path)

    # determine missing records from database
    missing_records = list(set(facility_data.keys())-set(facility_data_db.keys()))
    print missing_records

    # updates db with missing records
    for r in missing_records:
        fac_to_db(r[0],r[1])
        
    # checks
        assert len(facility_data_db) + len(missing_records) == len(facility_data)

### ------------------------- Database Maintenance Functions ------------------------- 

def wipe_tables():
    '''Wipes all tables in database. Used to clear duplicate records created during debugging.'''
    name = "facility_data.db"
    path = "/users/kbrooks/Documents/MH/Projects/Metrics/Distribution/Scheduled Unscheduled (CDC0089-1)/"
    schema = "(date integer, new integer, sched integer, unsched integer, ship integer, susp integer, old integer, future integer, hold integer)"
    conn = sqlite3.connect(path + name)
    c = conn.cursor()
	    
    for table in ["Gahanna", "Ashland", "Groveport"]:
        print "deleting:", table
        c.execute('''DROP table ''' + table)
        c.execute('''CREATE TABLE IF NOT EXISTS ''' + table + schema)
        
    conn.commit()
    conn.close()
    return

def count_db_records(path):
    '''Count records in the database to provide visual confirmation of update, etc.'''
    name = "facility_data.db"
    conn = sqlite3.connect(path + name)
    c = conn.cursor()
    record_count = 0
    for table in ["Gahanna", "Ashland", "Groveport"]:
        c.execute('''SELECT COUNT(*) FROM ''' + table)
        records = int(c.fetchall()[0][0])  # extracts the count from returned tuple inside list
        print table, "records: ", records
        record_count += records
    conn.commit()
    conn.close()

    return record_count

def check_db():
    '''Check database for quality, inconsistency, etc.'''
    # only one record per facility/date
    # the counts from all tables match
    #
    pass

### ------------------------- Unit Test  ------------------------- 

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


