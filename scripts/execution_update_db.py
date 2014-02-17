from AAA_sched_unsched import *

#  update data from directory
path_to_db = '../db/'
path_to_data = '../data/'
#wipe_tables()
get_facility_db(path_to_db)
read_dir(path_to_data)
populate_database()
print len(set(facility_data.keys())-set(facility_data_db.keys())), "records updated"
