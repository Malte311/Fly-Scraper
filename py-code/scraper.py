import datetime
import json
import os
import random
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

SLEEP_TIME = 0.4

def get_info(flight):
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	driver = webdriver.Chrome(executable_path='drivers/chromedriver', options=chrome_options)

	try:
		driver.get('https://www.google.de/flights')

		set_travellers(driver, int(flight['travellers']))
		set_cabin(driver, flight['cabin'])
		set_from(driver, flight['from'])
		set_to(driver, flight['to'])
		set_depart_and_return(driver, flight['depart'], flight['return'])

		put_info(flight, fetch_results(driver))
		
	except Exception:
		put_info(flight, []) # mark as not successful
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

def set_depart_and_return(driver, depart_date, return_date):
	datepicker = driver.find_elements_by_css_selector('.gws-flights-form__input-target')[2]
	parent = datepicker.find_element_by_xpath('..')

	time.sleep(SLEEP_TIME)
	parent.click()

	time.sleep(SLEEP_TIME)
	inputs = driver.find_elements_by_css_selector('.qCutsdOnIDY__date-input')
	for i in range(2):
		if i == 0:
			date = depart_date
		else:
			date = return_date
	
		time.sleep(SLEEP_TIME)
		inputs[i].click()
		time.sleep(SLEEP_TIME)
		inputs[i].send_keys(Keys.CONTROL + 'a')
		time.sleep(SLEEP_TIME)
		inputs[i].send_keys(Keys.DELETE)
		time.sleep(SLEEP_TIME)
		inputs[i].send_keys(date)
		time.sleep(SLEEP_TIME)
		inputs[i].send_keys(Keys.ENTER)
		time.sleep(SLEEP_TIME)

	driver.find_element_by_css_selector('.eE8hUfzg9Na__overlay').find_element_by_xpath('..').click()
	
	time.sleep(SLEEP_TIME)

def fetch_results(driver):
	time.sleep(1)

	results = []
	flights = driver.find_elements_by_css_selector('.gws-flights-results__result-item')
	for flightRes in flights:
		resObj = {}
		data = re.split('[\n\r]+', flightRes.text)

		for i in range(0, len(data)):
			if re.search(r'^([^0-9]*)$', data[i]) and not 'airlines' in resObj:
				resObj['airlines'] = data[i].split(',')
				continue
			if re.search(r'(\d* Min|\d* h \d* Min)', data[i]) and not 'duration' in resObj:
				resObj['duration'] = duration_str_to_mins(data[i])
				continue
			if re.search(r'(.*stop|\d* Stopp.)', data[i]) and not 'stops' in resObj:
				if re.search(r'(.*stop)', data[i]):
					resObj['stops'] = str(0) # Match for "Nonstop"
				else:
					resObj['stops'] = re.search(r'\d* Stopp.', data[i]).group().strip()
				continue
			if re.search(r'\d*\.?\d* €{1}', data[i]) and not 'price' in resObj:
				resObj['price'] = re.sub('€', '', data[i]).strip()
				continue
		
		results.append(resObj)

	return results

def duration_str_to_mins(duration_str):
	mins = int(re.search(r'\d*', duration_str.split('h')[1].strip()).group())
	hours = int(re.search(r'\d*', duration_str.split('h')[0].strip()).group())
	
	return 60 * hours + mins

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