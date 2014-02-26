import pandas as pd
import matplotlib.pyplot as plt
import output_db as o_db
import input_db as i_db
import input_files as i_files

### Processing Layer ###

class Daily_Prodn(object):
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
        self.location = location
        assert location in ('GAH', 'ASH', 'GRO')
        self.new = new
        self.sched = sched
        self.unsched = unsched
        self.ship = ship
        self.susp = susp
        self.old = old
        #assert old > susp
        self.future = future
        self.hold = hold
        self.in_process = sched + unsched + old + future + hold
    
    def __repr__(self):
        return str(self.__dict__)

    # __str__ = __repr__ ## uncomment this if printing doesn't work well 

def incr_db_update():
    '''Compares records in a database with data available from a directory and updates
    the missing data in the database.'''
    # retrieve db records
    facility_data_db = i_db.get_facility_db('../db/')

    # retrieve data from files
    facility_data = i_files.read_dir('../data/')

    # determine missing records from database
    missing_records = list(set(facility_data.keys())-set(facility_data_db.keys()))
    print missing_records

    # updates db with missing records
    for r in missing_records:
        o_db.fac_to_db(r[0],r[1], facility_data)
        
    # checks
        assert len(facility_data_db) + len(missing_records) == len(facility_data)

def calc_facility_backlog(facility, facility_data_db):
    '''Calculates backlog in a facility over time and returns most recent backlog'''
    # Accept only "GAH", "ASH", "GRO"
    # Cycle through facility_data_db, pulling values for facility into a list
    facility_list = [value for value in facility_data_db.values() if value.location == facility]
    
    # calculate the orders in process
    #for date_object in facility_list:
    #    date_object.in_process = date_object.sched + date_object.unsched + date_object.old + date_object.future + date_object.hold
  
    # order the list by date
    facility_list.sort(key=lambda x: x.date)
    
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

def plot_facility_trends(facility, facility_data_db):
    '''Plots trends of processing, MA processing, orders in process and shipping over time'''
    # Accept only "GAH", "ASH", "GRO"
    # Cycle through facility_data_db, pulling values for facility into a list
    facility_list = [value for value in facility_data_db.values() if value.location == facility]
    
    # calculate the orders in process
    for date_object in facility_list:
        date_object.in_process = date_object.sched + date_object.unsched + date_object.old + date_object.future + date_object.hold
  
    # order the list by date
    facility_list.sort(key=lambda x: x.date)
    for d in facility_list:
        print d.date, d.ship

def create_data_frame(facility, facility_data_db):
    '''Creates data frames of facility data'''
    facility_list = [[f.date, f.location, f.new, f.sched,
                 f.unsched, f.ship, f.susp, f.old, f.future, f.hold, f.in_process] 
                 for f in facility_data_db.values() if f.location == facility]
    df = pd.DataFrame(facility_list, columns=['date', 'location', 'new', 'sched',
                 'unsched', 'ship', 'susp', 'old', 'future', 'hold', 'in_process'])
    # index on date?
    return df



if __name__ == '__main__':
    print "------------------- Unit tests -------------------"
    path = '../db/'
    facility_data_db = i_db.get_facility_db(path)
    df = create_data_frame("GAH", facility_data_db)
    print df.head()
    df['in_process'].plot()

    plt.show()



