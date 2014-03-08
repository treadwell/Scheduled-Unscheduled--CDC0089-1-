import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import output_db as o_db
import input_db as i_db
import input_files as i_files
import datetime

### Processing Layer ###

class Daily_Prodn(object):
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
        

def create_data_frame_1(facility, facility_data_db):
    '''Creates data frames of facility data'''
    facility_list = [[f.date, f.location, f.new_orders, f.new_lines, f.new_units, f.new_dollars, \
               f.sched_orders, f.sched_lines, f.sched_units, f.sched_dollars, \
               f.unsched_orders, f.unsched_lines, f.unsched_units, f.unsched_dollars, \
               f.ship_orders, f.ship_lines, f.ship_units, f.ship_dollars, \
               f.susp_orders, f.susp_lines, f.susp_units, f.susp_dollars, \
               f.old_orders, f.old_lines, f.old_units, f.old_dollars, \
               f.fut_orders, f.fut_lines, f.fut_units, f.fut_dollars, \
               f.hold_orders, f.hold_lines, f.hold_units, f.hold_dollars] 
                 for f in facility_data_db.values() if f.location == facility]
    df = pd.DataFrame(facility_list, columns=['date', 'location', 'new_orders', 'new_lines', 'new_units', 'new_dollars',    
               'sched_orders', 'sched_lines', 'sched_units', 'sched_dollars',  
               'unsched_orders', 'unsched_lines', 'unsched_units', 'unsched_dollars',
               'ship_orders', 'ship_lines', 'ship_units', 'ship_dollars',   
               'susp_orders', 'susp_lines', 'susp_units', 'susp_dollars',   
               'old_orders', 'old_lines', 'old_units', 'old_dollars',    
               'fut_orders', 'fut_lines', 'fut_units', 'fut_dollars',    
               'hold_orders', 'hold_lines', 'hold_units', 'hold_dollars'])
    # index on date?
    df.index = df['date']
    df = df.sort(['date'])
    df['weekday'] = df['date'].apply(lambda d: datetime.datetime.weekday(d))
    df['ship_MA10_orders'] = pd.rolling_quantile(df['ship_orders'], 5, 0.75)
    df['ship_MA10_lines'] = pd.rolling_quantile(df['ship_lines'], 5, 0.75)
    df['ship_MA10_units'] = pd.rolling_quantile(df['ship_units'], 5, 0.75)
    df['ship_MA10_dollars'] = pd.rolling_quantile(df['ship_dollars'],5, 0.75)
    df['in_process_orders'] = df['sched_orders'] + df['unsched_orders'] + df['old_orders'] + df['fut_orders'] + df['hold_orders']
    df['in_process_lines'] = df['sched_lines'] + df['unsched_lines'] + df['old_lines'] + df['fut_lines'] + df['hold_lines']
    df['in_process_units'] = df['sched_units'] + df['unsched_units'] + df['old_units'] + df['fut_units'] + df['hold_units']
    df['in_process_dollars'] = df['sched_dollars'] + df['unsched_dollars'] + df['old_dollars'] + df['fut_dollars'] + df['hold_dollars']
    df['backlog_orders'] = df['in_process_orders'].div(df['ship_MA10_orders'])
    df['backlog_lines'] = df['in_process_lines'].div(df['ship_MA10_lines'])
    df['backlog_units'] = df['in_process_units'].div(df['ship_MA10_units'])
    df['backlog_dollars'] = df['in_process_dollars'].div(df['ship_MA10_dollars'])
  
    return df        


class Facility(object):
    def __init__(self, name, data_dict):
        # build the data frame here
        self.name = name
        self.df = create_data_frame_1(name, data_dict)
        #self.df['new_col'] = self.df['old'] + self.df['new']
    
    def plot_trend(self, statistic):
        '''Plots trends of specified statistic over time in a specified facility'''
        self.df[statistic].plot()
        plt.title(statistic + " in " + self.name)
        plt.show()

    def plot_dual(self, statistic1, statistic2):
        '''Plots trends of specified statistic over time in a specified facility'''
        self.df[statistic1].plot()
        self.df[statistic2].plot()
        plt.title(self.name)
        plt.legend()
        plt.show()

    def warnings(self):
        '''identifies potential warning conditions'''
        # Backlogs
        print "running backlog warnings for", self.name, "..."
        if self.df['backlog_dollars'].iget(-1) > 3:
            print self.name, "dollar backlog > 3 days (", self.df['backlog_dollars'].iget(-1), ")"
            self.plot_dual("in_process_dollars", "ship_MA10_dollars")
        if self.df['backlog_lines'].iget(-1) > 3:
            print self.name, "line backlog > 3 days (", self.df['backlog_lines'].iget(-1), ")"
            self.plot_dual("in_process_lines", "ship_MA10_lines")
        if self.df['backlog_units'].iget(-1) >3: 
            print self.name, "unit backlog > 3 days (", self.df['backlog_units'].iget(-1), ")"
            self.plot_dual("in_process_units", "ship_MA10_units")
        print "backlog warnings for", self.name, "complete."
        

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

# ------------- Build Facility Objects --------------
    Gahanna = Facility("GAH", facility_data_db)

    print Gahanna.df['ship_dollars'].tail()
    print Gahanna.df['ship_MA10_dollars'].tail()

    g = Gahanna.df

    weekday_groups = g.groupby(g.weekday)

    for name, group in weekday_groups:
        #group.new_dollars.plot()
        #plt.plot(group.new_dollars, label = name)
        group.smooth = pd.rolling_mean(group.new_dollars, window = 10)
        plt.plot(group.smooth, label = 'rolling({k})'.format(k=name))

    plt.legend(loc = "best")
    plt.show()

    ### version 2
    # grouped = g.groupby(g.weekday)

    # for name, group in grouped:
    #     group.new_dollars.plot()
        

    #plt.legend()
    # plt.show()

    ### version 3
    grouped = g.groupby(g.weekday)

    L = len(grouped)
    height = 2
    length = (L+1)//2
    
    for i, (name, group) in enumerate(grouped):
        plt.subplot(height*100 + length*10 + (i+1))
        ## should probably be done as string concatenation
        group.new_dollars.plot()
        

    # http://matplotlib.org/examples/pylab_examples/anscombe.html

    #plt.legend()
    plt.show()


