import scripts.processing as p
import scripts.input_db as i_db
import os
import pandas as pd

# Calculate facility backlogs

#print os.getcwd()
path = './db/'
facility_data_db = i_db.get_facility_db_1(path)
#print facility_data_db


#print GAH_today.date
print "----------"
#print "GAH new:", GAH_today.new_dollars, "in process:", GAH_today.in_process_dollars, "sched:", GAH_today.sched_dollars,  "backlog:", GAH_today.backlog_dollars
#print "ASH new:", ASH_today.new_dollars, "in process:", ASH_today.in_process_dollars, "sched:", ASH_today.sched_dollars,  "backlog:", ASH_today.backlog_dollars
#print "GRO new:", GRO_today.new_dollars, "in process:", GRO_today.in_process_dollars, "sched:", GRO_today.sched_dollars,  "backlog:", GRO_today.backlog_dollars
#print "RYE new:", RYE_today.new_dollars, "in process:", RYE_today.in_process_dollars, "sched:", RYE_today.sched_dollars,  "backlog:", RYE_today.backlog_dollars


Gahanna = p.Facility("GAH", facility_data_db)
Ashland = p.Facility("ASH", facility_data_db)
Groveport = p.Facility("GRO", facility_data_db)
Ryerson = p.Facility("RYE", facility_data_db)
#DeSoto = p.Facility("DES", facility_data_db)
TotalDomestic = p.Facility("TOT", facility_data_db)

print "Gahanna backlogs:"
print "Dollar backlog: ", Gahanna.df['backlog_dollars'].iget(-1)
print "Line backlog: ", Gahanna.df['backlog_lines'].iget(-1) 
print "Unit backlog: ", Gahanna.df['backlog_units'].iget(-1) 
print "----------"
print "Ashland backlogs:"
print "Dollar backlog: ", Ashland.df['backlog_dollars'].iget(-1)
print "Line backlog: ", Ashland.df['backlog_lines'].iget(-1) 
print "Unit backlog: ", Ashland.df['backlog_units'].iget(-1) 
print "----------"
print "Groveport backlogs:"
print "Dollar backlog: ", Groveport.df['backlog_dollars'].iget(-1)
print "Line backlog: ", Groveport.df['backlog_lines'].iget(-1) 
print "Unit backlog: ", Groveport.df['backlog_units'].iget(-1) 

Gahanna.plot_trend("backlog_dollars")
Gahanna.plot_trend("backlog_lines")

Ashland.plot_trend("backlog_dollars")
Ashland.plot_trend("backlog_lines")
Ashland.plot_trend("backlog_units")

Groveport.plot_trend("backlog_dollars")
Groveport.plot_trend("backlog_lines")

#print Gahanna.df['backlog_dollars'].last()  # syntax for last item in a dataframe

# Other things to look at:
#  ratio of unscheduled to scheduled (is work being pulled fast enough to keep up with backlog)
#  instantaneous backlog
#  smoothed backlog (more responsive than MA10). Use Loess?
#  trend in shipping, backlog, in process, new versus prior year
#  backlog at max production - what's the best way to determine this?  How much can you ramp up a facility in one day?

