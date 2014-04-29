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
        print "Running backlog warnings for", self.name, self.df['date'].iget(-1), "..."
        current_stats = {}
        for unit_type in ['dollars', 'lines', 'units', 'orders']:
            for statistic_type in ['new', 'ship', 'old', 'sched', 'unsched', 'fut', 'hold', 'in_process', 'ship_MA10']:
                statistic_name = statistic_type + '_' + unit_type
                statistic_value = self.df[statistic_name].iget(-1)
                current_stats[statistic_name] = statistic_value

        for unit_type in ['dollars', 'lines', 'units', 'orders']:
            backlog = current_stats['in_process_' + unit_type] / float(current_stats['ship_MA10_' + unit_type])

            if backlog > 3:
                print "\t", self.name, unit_type, "backlog > 3 days (", "{:4.2f}".format(backlog), "):"
                for statistic_type in [ 'in_process', 'sched','unsched', 'old','fut', 'hold','new', 'ship', 'ship_MA10']:
                    if statistic_type in ['sched', 'unsched', 'old','fut', 'hold']:
                        pre = '\t\t\t'
                    else:
                        pre = '\t\t'
                    print pre, statistic_type, ":", "{:4.2f}".format(current_stats[statistic_type + '_' + unit_type] / float(current_stats['ship_MA10_' + unit_type])), \
                    "days and", "{:6,.0f}".format(current_stats[statistic_type + '_' + unit_type]), unit_type
                print "\n"
                self.plot_trend('in_process' + '_' + unit_type)


        print "...backlog warnings for", self.name, "complete.\n"

    def summary(self):
        '''prints common summary statistics'''
        print "Running summary statistics for", self.name, self.df['date'].iget(-1), "..."

        for statistic in ['new_dollars', 'new_orders', 'new_lines', 'new_units', 'units_per_line', 'lines_per_order', 'dollars_per_unit', 'dollars_per_order']:
            if statistic in ['new_dollars', 'new_orders', 'new_lines', 'new_units']:
                format_string = "{:6,.0f}"
            else:
                format_string = "{:4.1f}"
            split_statistic = statistic.split('_')
            print_title = " ".join([split_statistic[0].title()] + split_statistic[1:])

            if print_title == "New dollars":
                print_title = print_title + ' ($m)'
            print "\t", print_title+":", format_string.format(self.df[statistic].iget(-1))

        print "...summary statistics for", self.name, "complete.\n"

    def generate_weekly_forecast(self, statistic):
        ''' Generate a weekly forecast of the selected statistic using a simple YTD change from prior year to
            the current year. This won't work for the first week of the year'''

        current_year = datetime.date.isocalendar(self.df.date.iget(-1))[0]
        latest_iso_week = datetime.date.isocalendar(self.df.date.iget(-1))[1]
        latest_full_week = max(1, latest_iso_week-1)


        # calculate YTD sum of target statistic for prior and current year

        YTD_sums = [self.df[(self.df.year == y) & (self.df.week_num < latest_full_week)][statistic].sum() for y in [current_year - 1, current_year]]


        growth = YTD_sums[1]/ float(YTD_sums[0])  # growth is the quotient of the two

        # aggregate prior year data by week

        weekly_prior_year = self.df[(self.df.year == current_year-1)].groupby('week_num')[statistic].aggregate(np.sum)

        # generate forecast (this should really only be for current week forward)

        forecast = weekly_prior_year.apply(lambda x: x * growth)

        # generate plot of actual through current week - 1 and forecast for the rest of the year

        return forecast

    def plot_ytd_comparison(self, statistic):
        '''plots current year ytd versus full year prior year'''

        current_year = datetime.date.isocalendar(self.df.date.iget(-1))[0]
        latest_iso_week = datetime.date.isocalendar(self.df.date.iget(-1))[1]

        daily = [self.df[(self.df.year == y)] for y in [current_year - 1, current_year]] # build list of 2 df's filtered by year
        weekly = [d.groupby('week_num')[statistic].aggregate(np.sum) for d in daily] # accumulate weekly data for each
        combined = pd. concat(weekly, axis=1) # combines the list items into a single data frame
        combined.columns = ['2013', '2014'] # renames the columns (they're named the same)

        # add cumsums and delete base year columns
        remaining_cols = []
        for col in [column for column in combined]:  # iterates over column names to add cumsums
             combined['cum_' + col] = combined[col].cumsum()
             remaining_cols.append('cum_' + col)
        combined = combined[remaining_cols]

        # print comparison statistics

        latest_full_week = combined.ix[latest_iso_week-1]  #  current week usually isn't comparable. Take prior week.
        growth = latest_full_week[1]/ latest_full_week[0]
        print "Growth vs prior year in", statistic,"at", self.name, ":", "{:.1%}".format(growth)
        
        # plot
        combined.plot()
        plt.title("YTD " + statistic + " in " + self.name)
        plt.ylabel('$000')
        plt.show()  


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

    #print Gahanna.df['day_of_year'].tail()

    Gahanna.summary()

    Gahanna.generate_weekly_forecast('new_dollars')

    Gahanna.warnings()

    Groveport = Facility("GRO", facility_data_db)
    Groveport.warnings()

    Ashland = Facility("ASH", facility_data_db)
    Ashland.warnings()

    #print Gahanna.generate_weekly_forecast('new_dollars')

    #Gahanna.plot_ytd_comparison('new_dollars')
    #Gahanna.plot_ytd_comparison('new_orders')
    Gahanna.plot_ytd_comparison('new_units')
    #Gahanna.plot_ytd_comparison('new_lines')





