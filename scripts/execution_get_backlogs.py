from input_db import *
from processing import *

# Calculate facility backlogs
path = '../db/'
facility_data_db = get_facility_db(path)
#print facility_data_db


print calc_facility_backlog("GAH", facility_data_db)
print calc_facility_backlog("ASH", facility_data_db)
print calc_facility_backlog("GRO", facility_data_db)

# Other things to look at:
#  ratio of unscheduled to scheduled (is work being pulled fast enough to keep up with backlog)
#  instantaneous backlog
#  smoothed backlog (more responsive than MA10). Use Loess?
#  trend in shipping, backlog, in process, new