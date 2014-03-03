import re
import os
from datetime import datetime
from re import sub
import processing as p
### Input Layer ###

facility_names = {"GAH":"Gahanna", "ASH":"Ashland", "GRO":"Groveport"}
# order_types gives the line location of the various order type data
order_types = {'new':11, 'sched':36, 'unsched':49, 'ship':60, 'susp':63, 'old':66, 'future':67, 'hold':68}
order_type_names = ['new', 'sched', 'unsched', 'ship', 'susp', 'old', 'future', 'hold']
# L-names gives the column location of facility dollar fields
L_names = {'GAH':[52,60], 'ASH':[90,96], 'GRO':[126,132]} 
    
def read_dir(path):
    '''Retrieves correct files from directory into a list'''
    facility_data = {}
    files = os.listdir(path)
    data_files = [file for file in files if 'CDC0089' in file]
    for file in data_files:
        file_data = read_file(path, file)
        facility_data.update(file_data)
    return facility_data

def read_dir_1(path):
    '''Retrieves correct files from directory into a list'''
    facility_data = {}
    files = os.listdir(path)
    data_files = [file for file in files if 'CDC0089' in file]
    for file in data_files:
        file_data = read_file_1(path, file)
        facility_data.update(file_data)
    return facility_data
    
def read_file(path, filename):
    '''Parses text file, creating dictionary of Daily_Prodn objects'''
    file_data = {}
    with open(path + filename) as f:
        # alternative: pull things directly by line number
        lines = list(f)

    assert "GAHANNA" in lines[5]
    assert "ASHLAND" in lines[5]
    assert "GROVEPORT" in lines[5]
    #assert "DESOTO" in lines[5]
    assert "RYERSON" in lines[74]
    assert "TOTAL NEW ORDERS" in lines[11]
    assert "TOTAL SCHEDULED ORDERS" in lines[36]
    assert "TOTAL UNSCHEDULED ORDERS" in lines[49]
    assert "TOTAL SHIPMENT CONFIRM" in lines[60]
    assert "SUSPENDED SHIPMENTS" in lines[63]
    assert "OLD INPROCESS (INP)" in lines[66]
    assert "FUTURE DATED" in lines[67]
    assert "HOLDS / ERRORS" in lines[68]

    date = str([word for word in lines[1].split() if '/' in word]).strip("[]\'")
    date = datetime.strptime(date, '%m/%d/%y')
    date = date.strftime('%Y-%m-%d')
    

    for L in L_names.keys():  # cycle through the locations, sequence doesn't matter
        order_type_data = []
        order_type_data_1 = []

        for o in order_type_names:  # cycle through order_types.  Sequence matters, necessitating a separate list
            order_type_data.append(lines[order_types[o]][L_names[L][0]:L_names[L][1]].replace(' ', ''))
	    
        for d in order_type_data:
            if d == '':
                order_type_data_1.append(0)
            else:
                order_type_data_1.append(int(sub(r'[^\d.]', '', d)))

        file_data[(L,date)] = p.Daily_Prodn(date, L, *order_type_data_1)

    return file_data

def read_file_1(path, filename):
    '''Parses text file, creating dictionary of Daily_Prodn objects including
    orders, lines, units and dollars'''
    file_data = {}
    with open(path + filename) as f:
        # alternative: pull things directly by line number
        lines = list(f)

    zone_layout = {"zone1":{"line":5, "col_start":28, "col_end":61}, 
                   "zone2":{"line":5, "col_start":64, "col_end":97},
                   "zone3":{"line":5, "col_start":100, "col_end":133},
                   "zone4":{"line":74, "col_start":28, "col_end":61},
                   "zone5":{"line":74, "col_start":64, "col_end":97},
                   "zone6":{"line":74, "col_start":100, "col_end":133},
                   "zone7":{"line":143, "col_start":28, "col_end":69}}

    offsets = {"new_orders":     {"lines":6,  "cols":0, "chars":6},
               "new_lines":      {"lines":6,  "cols":7, "chars":7},
               "new_units":      {"lines":6,  "cols":16, "chars":9},
               "new_dollars":    {"lines":6,  "cols":25, "chars":7},
               "sched_orders":   {"lines":31, "cols":0, "chars":6},
               "sched_lines":    {"lines":31, "cols":7, "chars":7},
               "sched_units":    {"lines":31, "cols":16, "chars":9},
               "sched_dollars":  {"lines":31, "cols":25, "chars":7},
               "unsched_orders": {"lines":44, "cols":0, "chars":6},
               "unsched_lines":  {"lines":44, "cols":7, "chars":7},
               "unsched_units":  {"lines":44, "cols":16, "chars":9},
               "unsched_dollars":{"lines":44, "cols":25, "chars":7},
               "ship_orders":    {"lines":55, "cols":0, "chars":6},
               "ship_lines":     {"lines":55, "cols":7, "chars":7},
               "ship_units":     {"lines":55, "cols":16, "chars":9},
               "ship_dollars":   {"lines":55, "cols":25, "chars":7},
               "susp_orders":    {"lines":58, "cols":0, "chars":6},
               "susp_lines":     {"lines":58, "cols":7, "chars":7},
               "susp_units":     {"lines":58, "cols":16, "chars":9},
               "susp_dollars":   {"lines":58, "cols":25, "chars":7},
               "old_orders":     {"lines":61, "cols":0, "chars":6},
               "old_lines":      {"lines":61, "cols":7, "chars":7},
               "old_units":      {"lines":61, "cols":16, "chars":9},
               "old_dollars":    {"lines":61, "cols":25, "chars":7},
               "fut_orders":     {"lines":62, "cols":0, "chars":6},
               "fut_lines":      {"lines":62, "cols":7, "chars":7},
               "fut_units":      {"lines":62, "cols":16, "chars":9},
               "fut_dollars":    {"lines":62, "cols":25, "chars":7},
               "hold_orders":    {"lines":63, "cols":0, "chars":6},
               "hold_lines":     {"lines":63, "cols":7, "chars":7},
               "hold_units":     {"lines":63, "cols":16, "chars":9},
               "hold_dollars":   {"lines":63, "cols":25, "chars":7}}
    
    statistic_names = ["new_orders", "new_lines", "new_units", "new_dollars",    
               "sched_orders", "sched_lines", "sched_units", "sched_dollars",  
               "unsched_orders", "unsched_lines", "unsched_units", "unsched_dollars",
               "ship_orders", "ship_lines", "ship_units", "ship_dollars",   
               "susp_orders", "susp_lines", "susp_units", "susp_dollars",   
               "old_orders", "old_lines", "old_units", "old_dollars",    
               "fut_orders", "fut_lines", "fut_units", "fut_dollars",    
               "hold_orders", "hold_lines", "hold_units", "hold_dollars"]

    zone_map = {}

    for zone in ["zone1", "zone2", "zone3", "zone4", "zone5", "zone6", "zone6", "zone7"]:
        zone_area = lines[zone_layout[zone]['line']][zone_layout[zone]['col_start']:zone_layout[zone]['col_end']]
        if "GAHANNA" in zone_area:
            zone_map[zone]="GAH"
        elif "ASHLAND" in zone_area:
            zone_map[zone]="ASH"
        elif "DESOTO" in zone_area:
            zone_map[zone]="DES"   
        elif "GROVEPORT" in zone_area:
            zone_map[zone]="GRO"
        elif "RYERSON" in zone_area:
            zone_map[zone]="RYE"
        elif "GRAND" in zone_area:
            zone_map[zone]="TOT"
        else:
            pass

    #print zone_map

    date = str([word for word in lines[1].split() if '/' in word]).strip("[]\'")
    date = datetime.strptime(date, '%m/%d/%y')
    date = date.strftime('%Y-%m-%d')

    file_data = {}

    for zone in zone_map.keys():
        statistic_data = []
        statistic_data_1 = []
        for s in statistic_names:
            if zone == 'zone7' and 'ord' in s:
                col_start = 30
                col_end = 39
            elif zone == 'zone7' and 'lin' in s:
                col_start = 40
                col_end = 48
            elif zone == 'zone7' and 'uni' in s:
                col_start = 49
                col_end = 60
            elif zone == 'zone7' and 'dol' in s:
                col_start = 61
                col_end = 68
            else:
                col_start = zone_layout[zone]["col_start"] + offsets[s]["cols"]
                col_end =  col_start + offsets[s]["chars"]
            
            line_no = zone_layout[zone]["line"] + offsets[s]["lines"]

            #statistic_data.append((line_no, col_start, col_end))
            #statistic_data.append(lines[line_no])
            statistic_data.append(lines[line_no][col_start:col_end].replace(' ', ''))

        for d in statistic_data:
            if d == '':
                statistic_data_1.append(0)
            else:
                statistic_data_1.append(int(sub(r'[^\d.]', '', d)))

        file_data[(zone_map[zone],date)] = p.Daily_Prodn_1(date, zone_map[zone], *statistic_data_1)

    # for s in statistic_names:
    
    a = file_data[('GAH',date)].new_orders
    b = file_data[('ASH',date)].new_orders
    c = file_data[('GRO',date)].new_orders
    d = file_data[('RYE',date)].new_orders
    if ('DES',date) in file_data.keys():
        e =  file_data[('DES',date)].new_orders
    else:
        e = 0
    f = file_data[('TOT',date)].new_orders
    assert file_data[('TOT',date)].new_orders == a + b + c + e

    return file_data

if __name__ == '__main__':
    path = "../test_data/"
    facility_data = read_dir(path)
    assert len(facility_data) == 78

    filename = "CDC0089 01-01-14.txt"
    facility_data = {}

    info = read_file(path, filename)
    print info
    assert info[('ASH', '2014-01-01')].sched == 49

    print "------------------------"
    filename = "CDC0089 01-02-14.txt"
    facility_data = {}

    info = read_file_2(path, filename)
    print "GAH ------------------------"
    print info[('GAH','2014-01-02')]
    print "ASH ------------------------"
    print info[('ASH','2014-01-02')]
    print "GRO ------------------------"
    print info[('GRO','2014-01-02')]
    print "RYE ------------------------"
    print info[('RYE','2014-01-02')]
    print "TOT ------------------------"
    print info[('TOT','2014-01-02')]

    print info[('GAH','2014-01-02')].new_orders

  


    