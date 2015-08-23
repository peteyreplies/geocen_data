'''a work script to rename files from muckrock's convention to something
usable in Dedoose 

by @peteyreplies

'''

##import libraries 
import os										#to walk dirs 
import shutil									#to copy command 

##where are the files, & where do they need to be? 
base_dir = '../../../../Desktop/scratch/GeoCen/old_docs'
new_dir = '../../../../Desktop/scratch/GeoCen/renamed_docs'

##define some functions
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


def copy_file(response_path, entity_name, r):
	'''takes 3 strings: file dir, entity name, and filename, prepends 
	   entity name to file name, and then copies to renamed folder'''

	new_location = new_dir + '/' + entity_name + '_' + r
	shutil.copy(response_path,new_location)
	#print entity_name + '_' + r + ' copied successfully'

##main loop 
 

#find each entity within each category 
i = 0 

responding_entities = return_contents(base_dir)
for e in responding_entities:
	#get the name of the entity
	entity_dir = base_dir + '/' + e
	entity_name = e[7:-1]

	#debug statement 
	print 'working within entity ' + entity_name
	
	#find each response within each entity
	entity_responses = return_contents(entity_dir) 
	for r in entity_responses:
		response_path = entity_dir + '/' + r

		#debug statement 
		i = i + 1
		print 'working on document ' + str(i) + ': ' + entity_name + '_' + r

		#if it's not a text file, copy it, saving just the title of the doc  
		if 'txt' not in r[-3:]:
			copy_file(response_path, entity_name, r.split()[-1])
		#if it's an incoming txt file, copy it 
		elif check_incoming(response_path):
			copy_file(response_path, entity_name, r)

print 'finished processing ' + str(i) + ' documents' 




