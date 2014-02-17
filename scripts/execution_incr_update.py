from AAA_sched_unsched import *

path_to_db = "../db/"

print "Pre-update records"
print count_db_records(path_to_db)

incr_db_update()

print "Post-update records"
print count_db_records(path_to_db)