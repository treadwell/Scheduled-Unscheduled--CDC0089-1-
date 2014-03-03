import scripts.processing as p
import scripts.input_db as i_db
import os

# Calculate facility backlogs

print os.getcwd()
path = './db/'
facility_data_db = i_db.get_facility_db_1(path)
#print facility_data_db

GAH_today = p.calc_facility_backlog_1("GAH", facility_data_db)
ASH_today = p.calc_facility_backlog_1("ASH", facility_data_db)
GRO_today = p.calc_facility_backlog_1("GRO", facility_data_db)
RYE_today = p.calc_facility_backlog_1("RYE", facility_data_db)

print GAH_today.date
print "----------"
print "GAH new:", GAH_today.new_dollars, "in process:", GAH_today.in_process_dollars, "sched:", GAH_today.sched_dollars,  "backlog:", GAH_today.backlog_dollars
print "ASH new:", ASH_today.new_dollars, "in process:", ASH_today.in_process_dollars, "sched:", ASH_today.sched_dollars,  "backlog:", ASH_today.backlog_dollars
print "GRO new:", GRO_today.new_dollars, "in process:", GRO_today.in_process_dollars, "sched:", GRO_today.sched_dollars,  "backlog:", GRO_today.backlog_dollars
print "RYE new:", RYE_today.new_dollars, "in process:", RYE_today.in_process_dollars, "sched:", RYE_today.sched_dollars,  "backlog:", RYE_today.backlog_dollars


p.plot_facility_trends_1("GAH", "backlog_dollars")
p.plot_facility_trends_1("GAH", "new_dollars")
p.plot_facility_trends_1("GRO", "new_dollars")
p.plot_facility_trends_1("ASH", "new_dollars")
p.plot_facility_trends_1("RYE", "new_dollars")

# Other things to look at:
#  ratio of unscheduled to scheduled (is work being pulled fast enough to keep up with backlog)
#  instantaneous backlog
#  smoothed backlog (more responsive than MA10). Use Loess?
#  trend in shipping, backlog, in process, new versus prior year
#  backlog at max production - what's the best way to determine this?  How much can you ramp up a facility in one day?

