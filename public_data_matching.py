'''a script to match library data taken from muckrock to public library/distract
data from the original exports

by @peteyreplies
'''

import csv 
from collections import OrderedDict

#files and filders 
base_path = '../RESOURCES/geocen/'
f = open('../DATADUMP/GeoCen/merged_public_data.csv','w')

#first, load csvs into list of dicts 
muckrock_data = []
muckrock_entities = csv.DictReader(open(base_path + 'muckrock_data.csv', 'rU'))
for m in muckrock_entities: 
	muckrock_data.append(m)

library_data = []
libraries = csv.DictReader(open(base_path + 'Alabama Public Libraries(IMLS).csv', 'rU'))
for l in libraries:
	library_data.append(l)

school_data = []
school_districts = csv.DictReader(open(base_path + 'Alabama Public School Districts(NCES).csv', 'rU'))
for s in school_districts:
	school_data.append(s)

#create translation tables 
locales = { 
			'11':'City, Large',
			'12':'City, Midsize',
			'13':'City, Small',
			'21':'Suburb, Large',
			'22':'Suburb, Midsize',
			'23':'Suburb, Small',
			'31':'Town, Fringe',
			'32':'Town, Distant',
			'33':'Town, Remote',
			'41':'Rural, Fringe',
			'42':'Rural, Distant',
			'43':'Rural, Remote',
			'M':'Missing',
			'N':'Not Applicable', 
}


#loop thru muckrock list 
for d in muckrock_data:
	#specify common fields up front 
	d['lat'] = ''			#latitude
	d['long'] = ''			#longitude 
	d['locale'] = ''		#federally defined locale type 
	d['cdcode'] = ''		#congressional district code 
	d['conum'] = ''			#ANSI County Code
	d['fedID'] = ''			#unique ID in associated dataset 
	d['total_librarians'] = ''	#num of total librarians; only available for libraries 
	d['computer_users']	= ''	#users of public computers per year; only available for libraries 


	#if it's a library, look in the library data 
	if d['agency_type'] == 'Library':
		#find matches based on zip and name 
		possible_matches = [y for y in library_data if y['ZIP_M'] == d['agency_zip'][:5]] 
		if len(possible_matches) == 1:
			lib_match = possible_matches[0]
		else:
			lib_match = [y for y in possible_matches if y['LIBNAME'].lower() == d['agency_name'].lower()][0]

		d['lat'] = lib_match['LATITUDE']
		d['long'] = lib_match['LONGITUD']
		d['locale'] = locales[lib_match['LOCALE']]
		d['cdcode'] = lib_match['CDCODE']
		d['conum'] = lib_match['FIPSPLAC']
		d['fedID'] = lib_match['FSCSKEY']
		d['total_librarians'] = lib_match['LIBRARIA']
		d['computer_users'] = lib_match['PITUSR']	 

	#otherwise, look in the school data 
	else:
		possible_matches = [y for y in school_data if y['MZIP'] == d['agency_zip'][:5]] 
		if len(possible_matches) == 1:
			school_match = possible_matches[0]
		else:
			school_match = [y for y in possible_matches if y['NAME'].lower() == d['agency_name'].lower()][0]
		d['lat'] = school_match['LATCOD']
		d['long'] = school_match['LONCOD']
		d['locale'] = locales[school_match['ULOCAL']]
		d['cdcode'] = school_match['CDCODE']
		d['conum'] = school_match['CONUM']
		d['fedID'] = school_match['LEAID']

        f = open('../DATADUMP/GeoCen/merged_public_data.csv','a')
        orderedEntity = OrderedDict(sorted(d.items()))
        DW = csv.DictWriter(f,orderedEntity.keys())
        if f.tell() == 0:
            DW.writer.writerow(orderedEntity.keys())
            DW.writer.writerow(orderedEntity.values())
        else:
            DW.writer.writerow(orderedEntity.values())

        print 'written data for entity ' + d['agency_name'].encode('ascii')

