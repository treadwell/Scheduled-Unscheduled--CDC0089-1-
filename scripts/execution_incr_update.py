from AAA_sched_unsched import *
from processing import *

''' This script compares the data in files versus the data in the db and updates
    the db with new or missing data'''

path_to_db = "../db/"

print "Pre-update records"
print count_db_records(path_to_db)

incr_db_update()

print "Post-update records"
print count_db_records(path_to_db)