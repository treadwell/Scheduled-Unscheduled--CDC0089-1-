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
        # self.in_process = sched + unsched + old + future + hold
        ## should not be calculated when the object is built

    def _get_in_process(self):
        # class properties/methods that start with underscore are private
        return sum([self.sched, self.unsched, self.old, self.future, self.hold])

    in_process = property(_get_in_process)
  
    # in_process = property(_get_in_process, _set_in_process)
    # foo.in_process -> will call foo._get_in_process() and return its result
    ### getting:
    # >>> foo.in_process
    # 123 ## "get" a result
    # >>> foo.in_process = 456
    # # no result; "setting" the variable
    # foo.in_process = 123 -> will run foo._set_in_process(123), not return anything
    

    def __repr__(self):
        return str(self.__dict__)

    # __str__ = __repr__ ## uncomment this if printing doesn't work well 

class Daily_Prodn_1(object):
    def __init__(self, date, location, new_orders, new_lines, new_units, new_dollars,    
               sched_orders, sched_lines, sched_units, sched_dollars,  
               unsched_orders, unsched_lines, unsched_units, unsched_dollars,
               ship_orders, ship_lines, ship_units, ship_dollars,   
               susp_orders, susp_lines, susp_units, susp_dollars,   
               old_orders, old_lines, old_units, old_dollars,    
               fut_orders, fut_lines, fut_units, fut_dollars,    
               hold_orders, hold_lines, hold_units, hold_dollars):
        
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
        #assert location in ('GAH', 'ASH', 'GRO', 'RYE', 'DES', "TOT")
        self.new_orders = new_orders
        self.new_lines = new_lines
        self.new_units = new_units
        self.new_dollars = new_dollars
        self.sched_orders = sched_orders
        self.sched_lines = sched_lines
        self.sched_units = sched_units
        self.sched_dollars = sched_dollars
        self.unsched_orders = unsched_orders
        self.unsched_lines = unsched_lines
        self.unsched_units = unsched_units
        self.unsched_dollars = unsched_dollars
        self.ship_orders = ship_orders
        self.ship_lines = ship_lines
        self.ship_units = ship_units
        self.ship_dollars = ship_dollars
        self.susp_orders = susp_orders
        self.susp_lines = susp_lines
        self.susp_units = susp_units
        self.susp_dollars = susp_dollars
        self.old_orders = old_orders
        self.old_lines = old_lines
        self.old_units = old_units
        self.old_dollars = old_dollars
        self.fut_orders = fut_orders
        self.fut_lines = fut_lines
        self.fut_units = fut_units
        self.fut_dollars = fut_dollars
        self.hold_orders = hold_orders
        self.hold_lines = hold_lines
        self.hold_units = hold_units
        self.hold_dollars = hold_dollars

    def _get_in_process_orders(self):
        # class properties/methods that start with underscore are private
        return sum([self.sched_orders, self.unsched_orders, self.old_orders, self.fut_orders, self.hold_orders])
    in_process_orders = property(_get_in_process_orders)

    def _get_in_process_lines(self):
        # class properties/methods that start with underscore are private
        return sum([self.sched_lines, self.unsched_lines, self.old_lines, self.fut_lines, self.hold_lines])
    in_process_lines = property(_get_in_process_lines)

    def _get_in_process_units(self):
        # class properties/methods that start with underscore are private
        return sum([self.sched_units, self.unsched_units, self.old_units, self.fut_units, self.hold_units])
    in_process_units = property(_get_in_process_units)

    def _get_in_process_dollars(self):
        # class properties/methods that start with underscore are private
        return sum([self.sched_dollars, self.unsched_dollars, self.old_dollars, self.fut_dollars, self.hold_dollars])
    in_process_dollars = property(_get_in_process_dollars)


  
    # in_process = property(_get_in_process, _set_in_process)
    # foo.in_process -> will call foo._get_in_process() and return its result
    ### getting:
    # >>> foo.in_process
    # 123 ## "get" a result
    # >>> foo.in_process = 456
    # # no result; "setting" the variable
    # foo.in_process = 123 -> will run foo._set_in_process(123), not return anything
    

    def __repr__(self):
        return str(self.__dict__)

    # __str__ = __repr__ ## uncomment this if printing doesn't work well 
        

def create_data_frame(facility, facility_data_db):
    '''Creates data frames of facility data'''
    facility_list = [[f.date, f.location, f.new, f.sched,
                 f.unsched, f.ship, f.susp, f.old, f.future, f.hold, f.in_process] 
                 for f in facility_data_db.values() if f.location == facility]
    df = pd.DataFrame(facility_list, columns=['date', 'location', 'new', 'sched',
                 'unsched', 'ship', 'susp', 'old', 'future', 'hold', 'in_process'])
    # index on date?
    df.index = df['date']
    df = df.sort(['date'])
    return df        


class Facility(object):
    def __init__(self, name, data_dict):
        # build the data frame here
        self.name = name
        self.df = create_data_frame(name, data_dict)
        self.df['new_col'] = self.df['old'] + self.df['new']
        
        facility_list = [value for value in data_dict.values() if value.location == name]
        for i, date_object in enumerate(facility_list):
            if i > 10:
                cumsum, cumcount = 0, 0
                for j in xrange(0,9):
                    if facility_list[i-j].ship >0:
                        cumsum += facility_list[i-j].ship
                        cumcount += 1
                # this should be in a higher object or a separate list or smth
                date_object.ship_MA10 = int(cumsum/cumcount)
            else:
                date_object.ship_MA10 = 0
        
def incr_db_update():
    '''Compares records in a database with data available from a directory and updates
    the missing data in the database.'''
    # retrieve db records
    facility_data_db = i_db.get_facility_db('./db/')

    # retrieve data from files
    facility_data = i_files.read_dir('./data/')

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

def plot_facility_trends(facility, statistic):
    '''Plots trends of specified statistic over time in a specified facility'''
    # Accept only "GAH", "ASH", "GRO"
    assert facility in ["GAH", "GRO", "ASH"]
    assert statistic in ['new', 'sched', 'unsched', 'ship', 'susp', 'old', 'future', 'hold', 'in_process']
    # Cycle through facility_data_db, pulling values for facility into a list
    path = './db/'
    facility_data_db = i_db.get_facility_db(path)
    df = create_data_frame(facility, facility_data_db)
    df[statistic].plot()
    plt.title(statistic + " in " + facility)

    plt.show()





if __name__ == '__main__':
    print "------------------- Unit tests -------------------"
    #plot_facility_trends("ASH", "new")
    # path = '../db/'
    # facility_data_db = i_db.get_facility_db(path)
    # df = create_data_frame("ASH", facility_data_db)
    #df.index = df['date']
    # print df
    # print df.head()
    # print df.tail()
    # df['hold'].plot()

    # plt.show()

    
# debug backlogs

    path = '../db/'
    facility_data_db = i_db.get_facility_db(path)
    ASH_today = calc_facility_backlog("ASH", facility_data_db)
    print "ASH new:", ASH_today.new, "sched:", ASH_today.sched,  "backlog:", ASH_today.backlog



