import processing as p
import output_db as o_db
### Output Layer ###

def display_fac(facility,date):  
    '''outputs tab-separated data for cut-and-paste to spreadsheet'''
    f = facility_data[(facility,date)]
    return '\t'.join([str(f.new), str(f.sched), str(f.unsched), str(f.ship), str(f.susp), str(f.old), str(f.future), str(f.hold)])

def cvs_fac(facility,date):  
    '''outputs csv data in list to drive automatic insertion to spreadsheet
        insertion in fac_to_csv function'''
    f = facility_data[(facility,date)]
    return [f.new, f.sched,	f.unsched, f.ship, f.susp, f.old, f.future, f.hold ]

def fac_to_screen(date):
    ''' combines output from all facilities for cust and paste to spreadsheet'''
    print date, display_fac('GAH', date), display_fac('ASH', date), display_fac('GRO', date)

def fac_to_csv(date):
    ''' combines output from all facilities and automatically inserts them into a spreadsheet'''
    save_filename = 'Scheduled Unscheduled.csv'
    csvRow = [date] + cvs_fac('GAH', date) + cvs_fac('ASH', date) + cvs_fac('GRO', date)
    myfile = open(path + save_filename,'a')
    writer = csv.writer(myfile)
    writer.writerow(csvRow)
    myfile.close()
    print date, "data saved to file:", save_filename







### ------------------------- Output Unit Tests  ------------------------- 

if __name__ == '__main__':
    print "------------------- Unit tests -------------------"
    facility_data = {}
    date = "1970-01-01"
    new = 1000
    sched = 1000
    unsched = 2000
    ship = 3000
    susp = 50
    old = 100
    future = 200
    hold = 300
    for location in ["GAH", "ASH", "GRO"]:
        facility_data[(location,date)] = p.Daily_Prodn(date, location, new, sched,
                 unsched, ship, susp, old, future, hold)
    print "Test objects:\n"
    print facility_data, "\n"
    
    assert display_fac("GAH",date) == "1000\t1000\t2000\t3000\t50\t100\t200\t300"
    assert cvs_fac("GAH", date) == [1000, 1000, 2000, 3000, 50, 100, 200, 300]
    assert o_db.insert_tuple("GAH",date) == ('1970-01-01', 1000, 1000, 2000, 3000, 50, 100, 200, 300)