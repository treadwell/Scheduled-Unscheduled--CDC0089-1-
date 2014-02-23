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
    
def read_file(path, filename):
    '''Parses text file, creating dictionary of Daily_Prodn objects'''
    file_data = {}
    with open(path + filename) as f:
        # alternative: pull things directly by line number
        lines = list(f)

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


if __name__ == '__main__':
    path = "../test_data/"
    facility_data = read_dir(path)
    assert len(facility_data) == 78

    filename = "CDC0089 01-01-14.txt"
    facility_data = {}

    info = read_file(path, filename)
    assert info[('ASH', '2014-01-01')].sched == 49


    