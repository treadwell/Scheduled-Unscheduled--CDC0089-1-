import sqlite3
import input_db as i_db

### ------------------------- Database Maintenance Functions ------------------------- 

def wipe_tables():
    '''Wipes all tables in database. Used to clear duplicate records created during debugging.'''
    name = "facility_data.db"
    path = "../db/"
    schema = "(date integer, new integer, sched integer, unsched integer, ship integer, susp integer, old integer, future integer, hold integer)"
    conn = sqlite3.connect(path + name)
    c = conn.cursor()
	    
    for table in ["Gahanna", "Ashland", "Groveport"]:
        print "deleting:", table
        c.execute('''DROP table ''' + table)
        c.execute('''CREATE TABLE IF NOT EXISTS ''' + table + schema)
        
    conn.commit()
    conn.close()
    return

def wipe_tables_1():
    '''Wipes all tables in database. Used to clear duplicate records created during debugging.'''
    name = "facility_data_1.db"
    path = "../db/"
    schema = "(date integer, new_orders integer, new_lines integer, new_units integer, new_dollars integer, \
        sched_orders integer, sched_lines integer, sched_units integer, sched_dollars integer, \
        unsched_orders integer, unsched_lines integer, unsched_units integer, unsched_dollars integer, \
        ship_orders integer, ship_lines integer, ship_units integer, ship_dollars integer,  \
        susp_orders integer, susp_lines integer, susp_units integer, susp_dollars integer, \
        old_orders integer, old_lines integer, old_units integer, old_dollars integer,    \
        fut_orders integer, fut_lines integer, fut_units integer, fut_dollars integer,   \
        hold_orders integer, hold_lines integer, hold_units integer, hold_dollars integer)"
    conn = sqlite3.connect(path + name)
    c = conn.cursor()
        
    for table in ["Gahanna", "Ashland", "Groveport", "DeSoto", "Ryerson", "Total"]:
        print "deleting:", table
        c.execute('''DROP table ''' + table)
        c.execute('''CREATE TABLE IF NOT EXISTS ''' + table + schema)
        
    conn.commit()
    conn.close()
    return

def create_database_1():
    name = "facility_data_1.db"
    path = "../db/"
    schema = "(date integer, new_orders integer, new_lines integer, new_units integer, new_dollars integer, \
        sched_orders integer, sched_lines integer, sched_units integer, sched_dollars integer, \
        unsched_orders integer, unsched_lines integer, unsched_units integer, unsched_dollars integer, \
        ship_orders integer, ship_lines integer, ship_units integer, ship_dollars integer,  \
        susp_orders integer, susp_lines integer, susp_units integer, susp_dollars integer, \
        old_orders integer, old_lines integer, old_units integer, old_dollars integer,    \
        fut_orders integer, fut_lines integer, fut_units integer, fut_dollars integer,   \
        hold_orders integer, hold_lines integer, hold_units integer, hold_dollars integer)"
    conn = sqlite3.connect(path + name)
    c = conn.cursor()
        
    for table in ["Gahanna", "Ashland", "Groveport", "DeSoto", "Ryerson", "Total"]:
        print "creating:", table
        c.execute('''CREATE TABLE IF NOT EXISTS ''' + table + schema)
        
    conn.commit()
    conn.close()
    return

def count_db_records(path):
    '''Count records in the database to provide visual confirmation of update, etc.'''
    name = "facility_data.db"
    conn = sqlite3.connect(path + name)
    c = conn.cursor()
    record_count = 0
    for table in ["Gahanna", "Ashland", "Groveport"]:
        c.execute('''SELECT COUNT(*) FROM ''' + table)
        records = int(c.fetchall()[0][0])  # extracts the count from returned tuple inside list
        print table, "records: ", records
        record_count += records
    conn.commit()
    conn.close()

    return record_count

def count_db_records_1(path):
    '''Count records in the database to provide visual confirmation of update, etc.'''
    name = "facility_data_1.db"
    conn = sqlite3.connect(path + name)
    c = conn.cursor()
    record_count = 0
    for table in ["Gahanna", "Ashland", "Groveport", "DeSoto", "Ryerson", "Total"]:
        c.execute('''SELECT COUNT(*) FROM ''' + table)
        records = int(c.fetchall()[0][0])  # extracts the count from returned tuple inside list
        print table, "records: ", records
        record_count += records
    conn.commit()
    conn.close()

    return record_count

def check_db():
    '''Check database for quality, inconsistency, etc.'''
    # only one record per facility/date
    facility_data_db = i_db.get_facility_db('../db/')
    #print facility_data_db.keys()
    
    for facility in ["GAH", "GRO", "ASH"]:
        print facility
        facility_list = [key for key in facility_data_db.keys() if key[0] == facility]
        print len(facility_list)
        print len(set(facility_list))
        facility_list.sort(key=lambda x: x[1])
        for key in facility_list:
            print key
    # the counts from all tables match
    # reasonableness of the data

if __name__ == '__main__':
    print "------------------- Unit tests -------------------"
    check_db()

    create_database_1()

