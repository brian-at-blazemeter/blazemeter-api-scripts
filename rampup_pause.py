#!/usr/bin/env python

import sys
import os
import readline
import requests
import json

def usage():
	print """
	Usage: rampup_pause [TEST_ID]
	"""

class BlazeMeterTest:
	api_key = os.environ['BLAZEMETER_API_KEY']

	def __init__ (self, filename):
		self.filename = filename
		# see https://guide.blazemeter.com/hc/en-us/articles/207421775-Create-a-Test for info
		self.test_spec = {
	    	"projectId": 40325,
	    	"configuration": {
	        	"dedicatedIpsEnabled": False,
	        	"location": "us-west-1",
	        	"concurrency": 150,
	        	"plugins": {
	        	    "splitCSV": {
	        	        "enabled": False
	        	    },
	        	    "reportEmail": {
	        	        "enabled": True
	        	    },
	            	"jmeter": {
	            	    "override": {
	            	        "duration": 10,
	            	        "rampup": 600,
	            	        "threads": None,
	            	        "iterations": -1
	            	    },
	            	    "filename": self.filename,
	            	    "version": "2.13blazemeter"
	            	}
	        	},
	        	"type": "jmeter",
	        	"serverCount": None
	    	},
	    	"name": "Auto-generated rampup_pause test"
		}

		# see https://a.blazemeter.com/api/latest/explorer for info
		r = requests.post('https://a.blazemeter.com/api/latest/tests',
			data=json.dumps(self.test_spec),
			headers={'x-api-key': self.api_key})
		self.test_id = str(r.json()['result']['id'])


	def add_file_to_test(self):
		self.add_resp = requests.post('https://a.blazemeter.com/api/latest/tests/' + self.test_id + '/files', 
			files={'file': open(self.filename, 'rb')},
			headers={'x-api-key': self.api_key})
		print self.add_resp.text

	def start_test(self):
		r = requests.get('https://a.blazemeter.com/api/latest/tests/' + self.test_id + '/start',
			headers={'x-api-key': self.api_key})
		return(r.json())

	def pause_test_rampup(self, master_id):
		r = requests.post('https://a.blazemeter.com/api/latest/masters/' + str(master_id) + '/rampup/pause', 
			headers={'x-api-key': self.api_key})
		return r.text


if __name__ == "__main__":
	try:
		b = BlazeMeterTest(sys.argv[1])
	except Exception as e:
		print e
		usage()
		exit()

	b.add_file_to_test()

	response = b.start_test()
	master_id = response['result']['id']

	raw_input("Started test with master id" + str(master_id) + 
		".  \nPress any key to stop rampup and hold traffic at current level.")
	print b.pause_test_rampup(master_id)
