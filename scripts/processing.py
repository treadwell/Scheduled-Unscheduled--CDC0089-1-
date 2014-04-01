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
    
    ## cast index to datetime; not automatically a datetime for some reason
    df.index = pd.to_datetime(df.date)
    df = df.sort(['date'])

    df['year'] = df["date"].apply(lambda x: datetime.date.isocalendar(x)[0])
    df['week_num'] = df["date"].apply(lambda x: datetime.date.isocalendar(x)[1])
    df['week_day'] = df["date"].apply(lambda x: datetime.date.isocalendar(x)[2])
    df['day_of_year'] = df['date'].apply(lambda d: d.toordinal() - datetime.date(d.year, 1, 1).toordinal() + 1)
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
    df['units_per_line'] = pd.rolling_mean(df.new_units, 10) / pd.rolling_mean(df.new_lines, 10)
    df['lines_per_order'] = pd.rolling_mean(df.new_lines, 10) / pd.rolling_mean(df.new_orders, 10)
    df['dollars_per_unit'] = pd.rolling_mean(df.new_dollars, 10) / pd.rolling_mean(df.new_units, 10) * 1000
    df['dollars_per_order'] = pd.rolling_mean(df.new_dollars, 10) / pd.rolling_mean(df.new_orders, 10) * 1000
  
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
        stat_smooth = pd.rolling_median(self.df[statistic], 10)
        #plt.plot(stat_smooth, label = 'rolling({k})'.format(k=statistic))
        stat_smooth.plot(label = 'rolling({k})'.format(k=statistic))
        plt.title(statistic + " in " + self.name)
        plt.legend(loc = "best")
        plt.show()

    def plot_dual(self, statistic1, statistic2):
        '''Plots trends of two specified statistics over time on the same axis'''
        self.df[statistic1].plot()
        self.df[statistic2].plot()
        plt.title(self.name)
        plt.legend()
        plt.show()

    def plot_stats(self):
        '''Plots units and dollar trends of major facility stats in a lattice plot'''
        plot_list= [self.df.new_units, self.df.new_dollars,self.df.ship_units, self.df.ship_dollars, \
              self.df.old_units, self.df.old_dollars, self.df.backlog_units, self.df.backlog_dollars]
        height = len(plot_list) / 2
        length = 2
        # add subplot titles and spacing

        for i, statistic in enumerate(plot_list):
            plt.subplot(height*100 + length*10 + (i+1))
            print 
            statistic.plot() 
            plt.title(statistic.name)
        plt.subplots_adjust(hspace= 1.5)
        plt.suptitle(self.name)
        plt.show()

    def warnings(self):
        '''identifies potential warning conditions'''
        # Backlogs
        print "running backlog warnings for", self.name, self.df['date'].iget(-1), "..."
        if self.df['backlog_dollars'].iget(-1) > 3:
            print "\t", self.name, "dollar backlog > 3 days (", "{:4.2f}".format(self.df['backlog_dollars'].iget(-1)), "):"
            print "\t\tIn process dollars:", self.df['in_process_dollars'].iget(-1)
            print "\t\t\tNew:", self.df['new_dollars'].iget(-1), "{:10.2f}".format(self.df['new_dollars'].iget(-1) / self.df['ship_MA10_dollars'].iget(-1))
            print "\t\t\tOld:", self.df['old_dollars'].iget(-1)
            print "\t\t\tSched:", self.df['sched_dollars'].iget(-1)
            print "\t\t\tUnsched:", self.df['unsched_dollars'].iget(-1)
            print "\t\t\tFuture:", self.df['fut_dollars'].iget(-1)
            print "\t\t\tHold:", self.df['hold_dollars'].iget(-1)
            print "\t\tMA dollar shipping:", self.df['ship_MA10_dollars'].iget(-1)
            self.plot_dual("in_process_dollars", "ship_MA10_dollars")
        if self.df['backlog_lines'].iget(-1) > 3:
            print "\t", self.name, "line backlog > 3 days (", "{:4.2f}".format(self.df['backlog_lines'].iget(-1)), ")"
            print "\t\tIn process lines:", self.df['in_process_lines'].iget(-1)
            print "\t\t\tNew:", self.df['new_lines'].iget(-1)
            print "\t\t\tOld:", self.df['old_lines'].iget(-1)
            print "\t\t\tSched:", self.df['sched_lines'].iget(-1)
            print "\t\t\tUnsched:", self.df['unsched_lines'].iget(-1)
            print "\t\t\tFuture:", self.df['fut_lines'].iget(-1)
            print "\t\t\tHold:", self.df['hold_lines'].iget(-1)
            print "\t\tMA line shipping:", self.df['ship_MA10_lines'].iget(-1)
            self.plot_dual("in_process_lines", "ship_MA10_lines")
        if self.df['backlog_units'].iget(-1) >3: 
            print "\t", self.name, "unit backlog > 3 days (", "{:4.2f}".format(self.df['backlog_units'].iget(-1)), ")"
            print "\t\tIn process units:", self.df['in_process_units'].iget(-1)
            print "\t\t\tNew:", self.df['new_units'].iget(-1)
            print "\t\t\tOld:", self.df['old_units'].iget(-1)
            print "\t\t\tSched:", self.df['sched_units'].iget(-1)
            print "\t\t\tUnsched:", self.df['unsched_units'].iget(-1)
            print "\t\t\tFuture:", self.df['fut_units'].iget(-1)
            print "\t\t\tHold:", self.df['hold_units'].iget(-1)
            print "\t\tMA unit shipping:", self.df['ship_MA10_units'].iget(-1)
            self.plot_dual("in_process_units", "ship_MA10_units")
        print "backlog warnings for", self.name, "complete.\n"

    def summary(self):
        '''prints common summary statistics'''
        print "running summary statistics for", self.name, self.df['date'].iget(-1), "..."
        print "\tNew dollars:", self.df.new_dollars.iget(-1)
        print "\tNew orders:", self.df.new_orders.iget(-1)
        print "\tNew lines:", self.df.new_lines.iget(-1)
        print "\tNew units:", self.df.new_units.iget(-1)
        

        print "\tUnits per line:", self.df['units_per_line'].iget(-1)
        print "\tLines per order:", self.df['lines_per_order'].iget(-1)
        print "\tDollars per unit:", self.df['dollars_per_unit'].iget(-1)
        print "\tDollars per order:", self.df['dollars_per_order'].iget(-1)
        print "summary statistics for", self.name, "complete.\n"

    def generate_weekly_forecast(self, statistic):
        ''' Generate a weekly forecast of the selected statistic using a simple YTD change from 2013 to
            the current year. This won't work for the first week of the year'''
        latest_iso_week = datetime.date.isocalendar(self.df.date.iget(-1))[1]
        year = datetime.date.isocalendar(self.df.date.iget(-1))[0]

        # calculate cumulative statistic for YTD 2013

        ytd_2013 = self.df[(self.df.week_num < latest_iso_week) & (self.df.year == 2013)][statistic].sum()

        # calculate cumulative statistic for current year

        ytd_current = self.df[(self.df.week_num < latest_iso_week) & (self.df.year == year)][statistic].sum()


        growth = float(ytd_current) / ytd_2013

        # aggregate base data by week

        weekly_2013 = self.df[(self.df.year == 2013)].groupby('week_num')[statistic].aggregate(np.sum)

        # generate forecast

        forecast = weekly_2013.apply(lambda x: x * growth)

        return forecast    

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

    print Gahanna.df['week_day'].tail()
    print Gahanna.df['day_of_year'].tail()

    g = Gahanna.df

   

    print Gahanna.generate_weekly_forecast('new_dollars')





