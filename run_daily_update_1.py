import scripts.processing as p
import scripts.db_maintenance as db_m

''' This script compares the data in files against the data in the db and updates
    the db with new or missing data'''

path_to_db = "./db/"

print "Pre-update records"
print db_m.count_db_records_1(path_to_db)

p.incr_db_update_1()

print "Post-update records"
print db_m.count_db_records_1(path_to_db)