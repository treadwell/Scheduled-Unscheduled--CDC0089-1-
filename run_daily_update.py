import scripts.processing as p
import scripts.db_maintenance as db_m

''' This script compares the data in files against the data in the db and updates
    the db with new or missing data'''

path_to_db = "./db/"

print "Count of records before the update"
print db_m.count_db_records(path_to_db)

p.incr_db_update()

print "Count of records after the update"
print db_m.count_db_records(path_to_db)