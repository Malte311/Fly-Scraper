import datetime
import json
import os
import random
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

SLEEP_TIME = 0.4

def get_info(flight):
	chrome_options = Options()
	#chrome_options.add_argument("--headless")
	driver = webdriver.Chrome(executable_path='drivers/chromedriver', options=chrome_options)

	try:
		driver.get('https://www.google.de/flights')

		#set_travellers(driver, int(flight['travellers']))
		#set_cabin(driver, flight['cabin'])
		#set_from(driver, flight['from'])
		#set_to(driver, flight['to'])
		set_depart(driver, flight['depart'])
		#set_return(driver, flight['return'])

		print("Sleeping")
		time.sleep(120)

		put_info(flight, fetch_results(driver))
		
	except Exception:
		put_info(flight, {}) # mark as not successful
		raise Exception(f'No success for flight id {flight["id"]}')
	finally:
		driver.close()

def set_travellers(driver, travellers):
	menu = driver.find_elements_by_css_selector('.gws-flights-form__menu-label')

	time.sleep(SLEEP_TIME)
	menu[1].click() # Number of travellers

	time.sleep(SLEEP_TIME)
	inc = driver.find_element_by_css_selector('.gws-flights-widgets-numberpicker__flipper-increment')
	for _i in range(travellers - 1):
		parent = inc.find_element_by_xpath('..')
		parent.click()
		time.sleep(SLEEP_TIME)
	
	time.sleep(SLEEP_TIME)
	driver.find_element_by_css_selector('.gws-flights__dialog-primary-button').click()

	time.sleep(SLEEP_TIME)

def set_cabin(driver, cabin_str):
	menu = driver.find_elements_by_css_selector('.gws-flights-form__menu-label')

	time.sleep(SLEEP_TIME)
	menu[2].click() # Cabin class

	time.sleep(SLEEP_TIME)
	cabin = driver.find_elements_by_css_selector('.X4hwq.flt-subhead2')		
	cabin[map_cabin(cabin_str)].click()

	time.sleep(SLEEP_TIME)

def map_cabin(cabin_str):
	if 'first class' in cabin_str.lower():
		return 3
	elif 'business class' in cabin_str.lower():
		return 2
	elif 'premium economy' in cabin_str.lower():
		return 1
	else:
		return 0

def set_from(driver, origin_airport):
	airport = driver.find_element_by_css_selector('.gws-flights-form__input-target')
	parent = airport.find_element_by_xpath('..')

	time.sleep(SLEEP_TIME)
	parent.click()

	time.sleep(SLEEP_TIME)
	input_field = driver.find_element_by_id('sb_ifc50').find_element_by_xpath(".//*")
	time.sleep(SLEEP_TIME)
	input_field.clear()
	time.sleep(SLEEP_TIME)
	input_field.send_keys(origin_airport)

	time.sleep(SLEEP_TIME)
	airport_result = driver.find_element_by_css_selector('.fsapp-option-content')
	time.sleep(SLEEP_TIME)
	airport_result.click()
	
	time.sleep(SLEEP_TIME)

def set_to(driver, dest_airport):
	airport = driver.find_elements_by_css_selector('.gws-flights-form__input-target')[1]
	parent = airport.find_element_by_xpath('..')

	time.sleep(SLEEP_TIME)
	parent.click()

	time.sleep(SLEEP_TIME)
	input_field = driver.find_element_by_id('sb_ifc50').find_element_by_xpath(".//*")
	time.sleep(SLEEP_TIME)
	input_field.clear()
	time.sleep(SLEEP_TIME)
	input_field.send_keys(dest_airport)

	time.sleep(SLEEP_TIME)
	airport_result = driver.find_element_by_css_selector('.fsapp-option-content')
	time.sleep(SLEEP_TIME)
	airport_result.click()

	time.sleep(SLEEP_TIME)

def set_depart(driver, depart_date):
	datepicker = driver.find_element_by_css_selector('.gws-flights-form__input-target')
	parent = datepicker.find_element_by_xpath('..')
	parent.click()
	time.sleep(SLEEP_TIME)

def set_return(driver, return_date):
	time.sleep(SLEEP_TIME)

def fetch_results(driver):
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

	return results

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