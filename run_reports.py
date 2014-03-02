import scripts.processing as p
import scripts.input_db as i_db
import os

# Calculate facility backlogs
path = '../db/'
facility_data_db = i_db.get_facility_db(path)
#print facility_data_db

GAH_today = p.calc_facility_backlog("GAH", facility_data_db)
ASH_today = p.calc_facility_backlog("ASH", facility_data_db)
GRO_today = p.calc_facility_backlog("GRO", facility_data_db)

print GAH_today.date
print "----------"
print "GAH new:", GAH_today.new, "in process:", GAH_today.in_process, "sched:", GAH_today.sched,  "backlog:", GAH_today.backlog
print "ASH new:", ASH_today.new, "in process:", ASH_today.in_process, "sched:", ASH_today.sched,  "backlog:", ASH_today.backlog
print "GRO new:", GRO_today.new, "in process:", GRO_today.in_process, "sched:", GRO_today.sched,  "backlog:", GRO_today.backlog


p.plot_facility_trends("GAH", "new")
p.plot_facility_trends("GRO", "new")
p.plot_facility_trends("ASH", "new")

# Other things to look at:
#  ratio of unscheduled to scheduled (is work being pulled fast enough to keep up with backlog)
#  instantaneous backlog
#  smoothed backlog (more responsive than MA10). Use Loess?
#  trend in shipping, backlog, in process, new versus prior year
#  backlog at max production - what's the best way to determine this?  How much can you ramp up a facility in one day?


