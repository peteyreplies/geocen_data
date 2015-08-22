'''a work script to rename files from muckrock's convention to something
usable in Dedoose 

by @peteyreplies

'''

##import libraries 
import os
import shutil

##where are the files, & where do they need to be? 
base_dir = '../../DATADUMP/GeoCen/Test_Docs'
new_dir = '../../DATADUMP/GeoCen/Renamed_Docs'

##define some functions
def return_contents(dir_path):
	'''takes a string of a filepath and returns a list of its contents'''
	contents = []
	for o in os.listdir(dir_path):
		contents.append(o)
	for n in contents:
		if '.DS_Store' in n:
			contents.remove(n)
	return contents

def check_incoming(response_path):
	'''checks if a document is incoming by reading first line for outgoing message
	if it is incoming, return true; else, false'''



def copy_file(response_path, entity_name, r):
	'''takes 3 strings: file dir, entity name, and filename, prepends 
	   entity name to file name, and then copies to renamed folder'''

	new_location = new_dir + '/' + entity_name + '_' + r
	shutil.copy(response_path,new_location)
	print entity_name + '_' + r + 'copied successfully'

##main loop 
 
#find each category of response 
response_categories = return_contents(base_dir)
for c in response_categories:
	cat_dir = base_dir + '/' + c
	responding_entities = return_contents(cat_dir)

	#find each entity within each category 
	for e in responding_entities:
		#get the name of the entity
		entity_dir = cat_dir + '/' + e
		entity_name = e[7:-5]
		entity_responses = return_contents(entity_dir)
		
		#find each response within each entity 
		for r in entity_responses:
			response_path = entity_dir + '/' + r

		#if it's a PDF, copy it 
		if 'pdf' in r[-3:]:
			copy_file(response_path, entity_name, r)

		#if it's an incoming txt file, copy it 
		if check_incoming(response_path):
			copy_file(response_path, entity_name, r)






