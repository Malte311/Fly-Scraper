import json
import os
import random
import sys
import time
import traceback
from scraper import create_date
from scraper import get_info
from scraper import write_log

DATA_FILE = '../data/entries.json'

def run_scraper():
	global DATA_FILE

	if len(sys.argv) < 2 or not os.path.isfile(DATA_FILE):
		exit()
	
	session_count = 0
	session_limit = int(sys.argv[1])
	with open(DATA_FILE, 'r') as file:
		data = json.load(file)
		for flight in data:
			if session_count >= session_limit:
				break

			try:
				if not is_done(flight['id']):
					get_info(flight)
					session_count += 1
					time.sleep(random.randint(20, 60))
			except Exception:
				write_log(f'Error for id {str(flight["id"])}: \r\n {str(traceback.format_exc())}')

def is_done(id):
	file_name = str(id) + '.json'

	if not os.path.isfile(file_name):
		return False

	with open(file_name, 'r') as file:
		data = json.load(file)
		today = create_date()
		return today in data

if __name__ == '__main__':
	run_scraper()