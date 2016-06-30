#!/usr/bin/env python

import sys
import os
import readline
import requests

def usage():
	print """
	Usage: rampup_pause [TEST_ID]
	"""
# see https://a.blazemeter.com/api/latest/explorer for info
def start_test(test_id):
	r = requests.get('https://a.blazemeter.com/api/latest/tests/' + test_id + '/start',
		headers={'x-api-key': api_key})
	return(r.json())

def pause_test_rampup(master_id):
	r = requests.post('https://a.blazemeter.com/api/masters/' + str(master_id) + '/rampup/pause', 
		headers={'x-api-key': api_key})
	return r.text


if __name__ == "__main__":
	test_id = sys.argv[1]
	api_key = os.environ['BLAZEMETER_API_KEY']

	response = start_test(test_id)
	master_id = response['result']['id']

	raw_input("Press any key to stop rampup and hold traffic at current level.")
	print pause_test_rampup(master_id)
