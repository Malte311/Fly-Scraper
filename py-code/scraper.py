import datetime
import json
import os
import random
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_info(flight):
	url = 'https://www.google.de/flights#flt=/m/03hrz.FNC.2020-05-03*FNC./m/03hrz.2020-05-31;c:EUR;e:1;sd:1;t:f'
	chrome_options = Options()
	#chrome_options.add_argument("--headless")
	driver = webdriver.Chrome(executable_path='drivers/chromedriver', options=chrome_options)

	try:
		driver.get(url)

		set_travellers(driver, int(flight['travellers']))

		print("Sleeping")
		time.sleep(120)

		set_cabin(driver, flight['cabin'])

		results = []
		flights = driver.find_elements_by_css_selector('.gws-flights-results__itinerary-card')
		for flightRes in flights:
			print(flightRes.text)
			resObj = {}
			data = re.split('[\n\r]+', flightRes.text)
			resObj['airline'] = data[1]
			resObj['duration'] = data[2]
			resObj['stops'] = data[4]
			resObj['stay'] = data[5]
			resObj['price'] = data[6]
			results.append(resObj)

		put_info(flight, results)
		
	except Exception:
		put_info(flight, {}) # mark as not successful
		raise Exception(f'No success for flight id {flight["id"]}')
	finally:
		driver.close()

def set_travellers(driver, travellers):
	menu = driver.find_elements_by_css_selector('.gws-flights-form__menu-label')

	time.sleep(0.2)
	menu[1].click() # Number of travellers

	time.sleep(0.2)
	inc = driver.find_element_by_css_selector('.gws-flights-widgets-numberpicker__flipper-increment')
	for _i in range(travellers - 1):
		parent = inc.find_element_by_xpath('..')
		parent.click()
		time.sleep(0.4)
	
	time.sleep(0.2)
	driver.find_element_by_css_selector('.gws-flights__dialog-primary-button').click()

	time.sleep(0.2)

def set_cabin(driver, cabin_str):
	menu = driver.find_elements_by_css_selector('.gws-flights-form__menu-label')

	time.sleep(0.2)
	menu[2].click() # Cabin class

	time.sleep(0.2)
	cabin = driver.find_elements_by_css_selector('.X4hwq.flt-subhead2')		
	cabin[map_cabin(cabin_str)].click()

	time.sleep(0.2)

def map_cabin(cabin_str):
	if 'first class' in cabin_str.lower():
		return 3
	elif 'business class' in cabin_str.lower():
		return 2
	elif 'premium economy' in cabin_str.lower():
		return 1
	else:
		return 0

def put_info(flight, info):
	file_name = path_prefix() + str(flight['id']) + '.json'
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
	log_file = path_prefix() + 'log.log'
	timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
	if not os.path.isfile(log_file):
		with open(log_file, 'w+') as file:
			file.write(f'{timestamp} \r\n {msg} \r\n')
	else:
		with open(log_file, 'a') as file:
			file.write(f'{timestamp} \r\n {msg} \r\n')

def path_prefix():
	if os.environ.get('PROD') == 'prod':
		return '../php-code/data/'
	else:
		return '../data/'