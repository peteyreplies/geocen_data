'''a script to help organize the type and character of responses in the
geocen dataset. would be more elegant to do this via the API but it seems
broken; right now, relying on full exported corpus.''' 


import os										#to walk dirs 
import shutil									#to copy command 

i = 0 

##where are the files, & where do they need to be? 
base_dir = '../../../Desktop/scratch/GeoCen/old_docs'

def return_contents(dir_path):
	'''takes a string of a filepath and returns a list of its contents'''
	contents = []
	for o in os.listdir(dir_path):
		contents.append(o)
	for n in contents:
		if '.DS_Store' in n:
			contents.remove(n)
	#print 'walking ' + dir_path
	return contents

def check_incoming(response_path):
	'''checks if a document is incoming by reading first line for outgoing message
	if it is incoming, return true; else, false'''
	f = open(response_path)
	lines = f.read().splitlines()
	try:
		if lines[0] == '':
			del lines[0]
		#print 'checking ' + response_path + ' for incoming'
		return 'To Whom' not in lines[0]
	except IndexError: 
		pass

#main loop 
#find each entity within each category 
i = 0 

all_entities = []

responding_entities = return_contents(base_dir)
for e in responding_entities:
	#get the name of the entity
	entity_dir = base_dir + '/' + e
	entity_name = e[7:-1]

	#guess entity type 
	if 'Library' in entity_name:
		entity_type = 'Library'
	else:
		entity_type = 'School'

	#debug statement 
	print 'working within entity ' + entity_name
	
	#find each response within each entity and 
	entity_responses = return_contents(entity_dir)

	for r in entity_responses:
		response_path = entity_dir + '/' + r


