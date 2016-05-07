'''a script to merge more public data into the 'main' datasets as we go along 

by @peteyreplies
'''

import csv 
from collections import OrderedDict

#files and filders
new_file = '2011-school-universe-data.csv' 
base_path = '../RESOURCES/geocen/'
f = open('../DATADUMP/GeoCen/merged_public_data.csv','w')

#first, load csvs into list of dicts 
main_data = []
main_entities = csv.DictReader(open(base_path + 'alabama_main_data.csv', 'rU'))
for m in main_entities: 
	main_data.append(m)

new_data = []
new_data_entities = csv.DictReader(open(base_path + new_file, 'rU'))
for n in new_data_entities:
	new_data.append(n)

#loop thru muckrock list 
for d in main_data:
	if d['agency_type'] == 'School District':
		match = [y for y in new_data if y['LEAID'] == d['fedID']]
		d['mls-ala'] = match[0]['LIBSPE']
		d['total_librarians'] = int(match[0]['LIBSPE']) + int(match[0]['LIBSUP'])
	else:
		pass

        f = open('../DATADUMP/GeoCen/merged_public_data.csv','a')
        orderedEntity = OrderedDict(sorted(d.items()))
        DW = csv.DictWriter(f,orderedEntity.keys())
        if f.tell() == 0:
            DW.writer.writerow(orderedEntity.keys())
            DW.writer.writerow(orderedEntity.values())
        else:
            DW.writer.writerow(orderedEntity.values())

        print 'written data for entity ' + d['agency_name'].encode('ascii')

