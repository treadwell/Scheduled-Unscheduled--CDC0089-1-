import sqlite3

def fac_to_db(facility, date, facility_data):
    '''updates data from all files in a directory to a database'''
    name = "facility_data_1.db"
    path = "./db/"
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
        
    if facility == "GAH":
        table = "Gahanna"
    elif facility == "ASH":
        table = "Ashland"
    elif facility == "GRO":
        table = "Groveport"
    elif facility == "RYE":
        table = "Ryerson"
    elif facility == "DES":
        table = "DeSoto"
    elif facility == "TOT":
        table = "Total"
    else:
        raise UnsupportedFacilityException
        
    # create table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS ''' + table + schema)
    
    c.execute("INSERT INTO " + table + " VALUES " + str(insert_tuple(facility,date, facility_data)))
    conn.commit()
    conn.close()
    return


def insert_tuple(facility,date, facility_data):
    '''Creates a tuple of facility data for insertion into a database'''
    f = facility_data[(facility,date)]
    return (f.date, f.new_orders, f.new_lines, f.new_units, f.new_dollars, \
               f.sched_orders, f.sched_lines, f.sched_units, f.sched_dollars, \
               f.unsched_orders, f.unsched_lines, f.unsched_units, f.unsched_dollars, \
               f.ship_orders, f.ship_lines, f.ship_units, f.ship_dollars, \
               f.susp_orders, f.susp_lines, f.susp_units, f.susp_dollars, \
               f.old_orders, f.old_lines, f.old_units, f.old_dollars, \
               f.fut_orders, f.fut_lines, f.fut_units, f.fut_dollars, \
               f.hold_orders, f.hold_lines, f.hold_units, f.hold_dollars)

