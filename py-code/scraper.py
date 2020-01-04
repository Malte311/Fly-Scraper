import datetime
import json
import os
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

USER_AGENTS = [
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362',
	'Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0'
]

def get_info(flight, errCount = -1):
	global USER_AGENTS

	if errCount < 0:
		user_agent = random.choice(USER_AGENTS)
	elif errCount < len(USER_AGENTS):
		user_agent = USER_AGENTS[errCount]
	else:
		put_info(flight, {}) # mark as not successful
		raise Exception(f'No success for flight id {flight["id"]}')

	url = 'https://www.google.de/flights#flt=/m/03hrz.FNC.2020-01-20*FNC./m/03hrz.2020-01-24;c:EUR;e:1;sd:1;t:f'
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	driver = webdriver.Chrome(executable_path='drivers/chromedriver', options=chrome_options)

	try:
		driver.get(url)
		time.sleep(3)
		write_log(driver.find_element_by_class_name('gws-flights-results__price'))
		
	except Exception:
		errCount += 1
		time.sleep(random.randint(15, 45))
		get_info(flight, errCount)
	finally:
		driver.close()

def put_info(flight, info):
	file_name = '../data/' + str(flight['id']) + '.json'
	if not os.path.isfile(file_name):
			data = {}
	else:
		with open(file_name, 'r') as file:
			data = json.load(file)

	today = create_date()
	data[today] = info
	with open(file_name, 'w+') as file:
		json.dump(data, file, indent=4, sort_keys=True)

def create_date():
	now = datetime.datetime.now()
	today = f'{now.year}-{str(now.month).zfill(2)}-{str(now.day).zfill(2)}'
	return today

def write_log(msg):
	log_file = '../data/log.log'
	timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
	if not os.path.isfile(log_file):
		with open(log_file, 'w+') as file:
			file.write(f'{timestamp} \r\n {msg} \r\n')
	else:
		with open(log_file, 'a') as file:
			file.write(f'{timestamp} \r\n {msg} \r\n')