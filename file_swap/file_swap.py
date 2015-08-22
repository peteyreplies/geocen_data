'''a work script to rename files from muckrock's convention to something
usable in Dedoose 

by @peteyreplies

'''

#import libraries 
import os

#where are the files? 
base_dir = '../../RESOURCES/GeoCen_Test_Docs' 

def return_subdirs(dir_path):
	'''takes a string of a filepath and returns a list of subfolders'''
	subdirs = []
	for o in os.listdir(dir_path):
		subdirs.append(o)
	subdirs.remove('.DS_Store')
	return subdirs




#loop through each category, finding responding entities 
for c in response_categories:
	responding_entities = []
	this_cat = original_docs + '/' + c



