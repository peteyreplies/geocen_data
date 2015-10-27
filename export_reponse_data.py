'''a script that talks to the muckrock api and tries to get a lot of 
communication data. 

first 40 lines or so are ripped right from https://github.com/MuckRock/API-examples/blob/master/export_all_user_requests.py
as of 10/27/2015

rest by @peteyreplies'''

#!/usr/bin/env python2
# -- coding: utf-8 --

import utils
import urllib, os, json, datetime, requests, urlparse
from datetime import datetime, timedelta, date
import time    
import csv 
from collections import OrderedDict

#set muckrock params 
api_url = utils.API_URL
token = utils.get_api_key()
headers = utils.get_headers(token)

username = raw_input('Username: ')
next_url = api_url + "foia/?user=" + username
current_page = 0

#erase prior csv if it exists
f = open('../DATADUMP/GeoCen/response_data.csv','w')

while next_url:
    # we use next_url because the API results are paginated
    r = requests.get(next_url, headers=headers)
    data = r.json()
    next_url = data['next']

    # measures progress by page, not by result
    current_page += 1
    total_pages = (data['count'] / 20.0)
    utils.display_progress(current_page, total_pages)

    for result in data['results']:
        #get the id of the first result 
        request_id = result['id']
        print "Working on request " + str(request_id)
        
        # get the first result
        ##get the API url of the result 
        request_url = api_url + 'foia/%d/' % request_id
        print request_url
        ##get the data within the request & convert from json to dict 
        request = requests.get(request_url, headers=headers)
        print request
        request_data = request.json()

        #grab submission time & timestamp 
        initial_submit_date = request_data['date_submitted'].encode('ascii')
        initial_submit_stamp = time.mktime(time.strptime(initial_submit_date, '%Y-%m-%d'))

        ##create dict for this entity interaction & seed w/ initial data
        ##we will write this one later  
        thisEntity = {
        				'request_id':request_id,
        				'request_url':request_url,
        				'muckrock_status':request_data['status'].encode('ascii'),
        				'initial_submit_date':initial_submit_date,
        }

        # get agency second
        agency_url = api_url + 'agency/%d/' % request_data['agency']
        agency = requests.get(agency_url , headers=headers)
        agency_data = agency.json()
        tempAgency = {
        				'agency_name':agency_data['name'].encode('ascii'),
        				'agency_id':agency_data['id'],
        				'agency_jurisdiction':agency_data['jurisdiction'],
        				'agency_type':agency_data['types'][0].encode('ascii'),
        				'agency_address':agency_data['address'].encode('ascii'),
        				'agency_phone':str(agency_data['phone']).encode('ascii'),
        }
        thisEntity.update(tempAgency)


        # get communications third
        communications = request_data['communications']
        i = 0 
        any_response_received = False 
        for c in communications:
        	firstResponse = {
        		'first_response_date':'',
        		'first_responder_name':'',
        		'requests_until_first_response':'',
        		'days_until_first_respone':'',
        		}
        	if c['response'] == False:
        		i = i + 1
        		continue
        	else:
        		any_response_received = True
        		first_response_datestamp = time.mktime(time.strptime(c['date'].encode('ascii')[0:10], '%Y-%m-%d'))
        		delta = (datetime.fromtimestamp(first_response_datestamp).date() - datetime.fromtimestamp(initial_submit_stamp).date()).days
        		firstResponse = {
        		'first_response_date':c['date'].encode('ascii')[0:10],
        		'first_responder_name':c['from_who'].encode('ascii'),
        		'requests_until_first_response':i,
        		'days_until_first_response':delta,
        		}
        		break

        thisEntity.update(firstResponse)
        num_responses = 0
        num_files = 0  
        for c in communications:
        	if c['response']:
        		num_responses = num_responses + 1
        		num_files = num_files + len(c['files'])

        thisEntity['total_communications'] = len(communications)
        thisEntity['any_response_received'] = any_response_received
        thisEntity['total_num_responses'] = num_responses
        thisEntity['total_files_received'] = num_files
				
        #write dict to csv 
        f = open('../DATADUMP/GeoCen/response_data.csv','a')
        orderedEntity = OrderedDict(sorted(thisEntity.items()))
        DW = csv.DictWriter(f,orderedEntity.keys())
        if f.tell() == 0:
            DW.writer.writerow(orderedEntity.keys())
            DW.writer.writerow(orderedEntity.values())
        else:
            DW.writer.writerow(orderedEntity.values())

        print 'written data for entity ' + agency_data['name'].encode('ascii')