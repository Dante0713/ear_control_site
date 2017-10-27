import sqlite3
import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait



def turn_on_sql():
	conn = sqlite3.connect('../db.sqlite3')
	cursor = conn.cursor()
	return conn, cursor

def get_sql_current_max_id_and_time(cursor):
	last_info=cursor.execute('SELECT id, ear_time, s_year, s_month FROM ear_info ORDER by id desc').fetchone()
	if last_info is None:
		return 0, None, None, None
	else:
		return int(last_info[0]), last_info[1], int(last_info[2]), int(last_info[3])

def store_data_from_earthquake_website(cursor):
	url = 'http://scweb.cwb.gov.tw/Page.aspx?ItemId=20&loc=tw&adv=1'
	driver = webdriver.PhantomJS('../phantomjs.exe')
	driver.get(url)
	today = datetime.datetime.now()
	current_max_id, last_time, base_year, base_month = get_sql_current_max_id_and_time(cursor)
	if base_month is None:
		# initial
		store_data(cursor, driver, current_max_id, last_time)
	else:
		# store by database time till now
		store_data(cursor, driver, current_max_id, last_time, base_year, base_month)

def store_data(cursor, driver, current_max_id, last_time, base_year = 1995, base_month = 1):
	today = datetime.datetime.now()
	# keep old data from 1995/1 till now 
	# using selenium select item, click next page in ajax item
	if base_year == 1995 and base_month == 1:
		for s_year in range(base_year,(today.year)):
			for s_month in range(base_month, 13):
				changing_pages_on_fetch_site(driver, s_year, s_month)
				current_max_id = initial_store_data(cursor, driver.find_element_by_id('ctl03_gvEarthquake').find_elements_by_tag_name('tr'), current_max_id, s_year, s_month)
		s_year = today.year
		for s_month in range(1,(today.month+1)):
			changing_pages_on_fetch_site(driver, s_year, s_month)
			current_max_id = initial_store_data(cursor, driver.find_element_by_id('ctl03_gvEarthquake').find_elements_by_tag_name('tr'), current_max_id, s_year, s_month)
	elif base_year != today.year:
		changing_pages_on_fetch_site(driver, base_year, base_month)
		current_max_id = normal_store_data(cursor, driver.find_element_by_id('ctl03_gvEarthquake').find_elements_by_tag_name('tr'), current_max_id, last_time, base_year, base_month)
		if (base_month+1) != 13:
			for s_month in range((base_month+1), 13):
				changing_pages_on_fetch_site(driver, base_year, s_month)
				current_max_id = initial_store_data(cursor, driver.find_element_by_id('ctl03_gvEarthquake').find_elements_by_tag_name('tr'), current_max_id, base_year, s_month)
			for s_year in range((base_year+1),(today.year)):
				for s_month in range(base_month, 13):
					changing_pages_on_fetch_site(driver, s_year, s_month)
					current_max_id = initial_store_data(cursor, driver.find_element_by_id('ctl03_gvEarthquake').find_elements_by_tag_name('tr'), current_max_id, s_year, s_month)
			s_year = today.year
			for s_month in range(1,(today.month+1)):
				changing_pages_on_fetch_site(driver, s_year, s_month)
				current_max_id = initial_store_data(cursor, driver.find_element_by_id('ctl03_gvEarthquake').find_elements_by_tag_name('tr'), current_max_id, s_year, s_month)	
		elif (base_year+1) <= (today.year-1):
			for s_year in range((base_year+1),(today.year)):
				for s_month in range(base_month, 13):
					changing_pages_on_fetch_site(driver, s_year, s_month)
					current_max_id = initial_store_data(cursor, driver.find_element_by_id('ctl03_gvEarthquake').find_elements_by_tag_name('tr'), current_max_id, s_year, s_month)
			s_year = today.year
			for s_month in range(1,(today.month+1)):
				changing_pages_on_fetch_site(driver, s_year, s_month)
				current_max_id = initial_store_data(cursor, driver.find_element_by_id('ctl03_gvEarthquake').find_elements_by_tag_name('tr'), current_max_id, s_year, s_month)		
		else:
			s_year = today.year
			for s_month in range(1,(today.month+1)):
				changing_pages_on_fetch_site(driver, s_year, s_month)
				current_max_id = initial_store_data(cursor, driver.find_element_by_id('ctl03_gvEarthquake').find_elements_by_tag_name('tr'), current_max_id, s_year, s_month)
	else:
		s_year = today.year
		if base_month == today.month:
			current_max_id = normal_store_data(cursor, driver.find_element_by_id('ctl03_gvEarthquake').find_elements_by_tag_name('tr'), current_max_id, last_time, s_year, base_month)
		else:
			changing_pages_on_fetch_site(driver, s_year, base_month)
			current_max_id = normal_store_data(cursor, driver.find_element_by_id('ctl03_gvEarthquake').find_elements_by_tag_name('tr'), current_max_id, last_time, s_year, base_month) 
			for s_month in range((base_month+1),(today.month+1)):
				changing_pages_on_fetch_site(driver, s_year, s_month)
				current_max_id = initial_store_data(cursor, driver.find_element_by_id('ctl03_gvEarthquake').find_elements_by_tag_name('tr'), current_max_id, s_year, s_month) 
	driver.close()
	driver.quit()

def initial_store_data(cursor, dataset, current_max_id, s_year, s_month):
	data = list()
	fetch_data = list()
	float_data = list()
	tmp_list = list()
	for index in range(1,len(dataset)):
		if "(" in dataset[index].text:
			current_max_id += 1
			fetch_data = dataset[index].text.split()[:-4]
			fetch_data, float_data = fetch_data[:-4], [float(i) for i in fetch_data[-4:]]
			tmp_list.extend([int(current_max_id),int(s_year),int(s_month)])
			tmp_list.extend(fetch_data)
			tmp_list.extend(float_data)
			tmp_list.append("".join(dataset[index].text.split()[-4:]))
			data.append(tuple(tmp_list))
			tmp_list = list()
		else:
			current_max_id += 1
			fetch_data = dataset[index].text.split()[:-3]
			fetch_data, float_data = fetch_data[:-3], [float(i) for i in fetch_data[-3:]]
			tmp_list.extend([int(current_max_id),int(s_year),int(s_month)])
			tmp_list.extend(fetch_data)
			tmp_list.extend(float_data)
			tmp_list.append("".join(dataset[index].text.split()[-3:]))
			data.append(tuple(tmp_list))
			tmp_list = list()
	cursor.executemany('INSERT INTO ear_info VALUES (?,?,?,?,?,?,?,?,?,?)',data)

	return current_max_id

def normal_store_data(cursor, dataset, current_max_id, last_time, s_year, s_month):
	data = list()
	fetch_data = list()
	float_data = list()
	tmp_list = list()
	for fetch_data_index in range((len(dataset)-1),1,-1 ):
		webdata= dataset[fetch_data_index].text.split()[1]
		if last_time == webdata:
			if fetch_data_index == (len(dataset)-1):
				pass
			else:
				for store_index in range((fetch_data_index+1),len(dataset)):
					if "(" in dataset[store_index].text:
						current_max_id += 1
						fetch_data = dataset[index].text.split()[:-4]
						fetch_data, float_data = fetch_data[:-4], [float(i) for i in fetch_data[-4:]]
						tmp_list.extend([int(current_max_id),int(s_year),int(s_month)])
						tmp_list.extend(fetch_data)
						tmp_list.extend(float_data)
						tmp_list.append("".join(dataset[index].text.split()[-4:]))
						data.append(tuple(tmp_list))
						tmp_list = list()
					else:
						current_max_id += 1
						fetch_data = dataset[index].text.split()[:-3]
						fetch_data, float_data = fetch_data[:-3], [float(i) for i in fetch_data[-3:]]
						tmp_list.extend([int(current_max_id),int(s_year),int(s_month)])
						tmp_list.extend(fetch_data)
						tmp_list.extend(float_data)
						tmp_list.append("".join(dataset[index].text.split()[-3:]))
						data.append(tuple(tmp_list))
						tmp_list = list()
				cursor.executemany('INSERT INTO ear_info VALUES (?,?,?,?,?,?,?,?,?,?)',data)
				return current_max_id
		else:
			pass
	return current_max_id	

def changing_pages_on_fetch_site(driver, s_year, s_month):
	# waiting for site loading
	try:
	    element = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, "ctl03_btnSearch")))
	finally:
		select_year = Select(driver.find_element_by_name('ctl03$ddlYear'))
		select_year.select_by_value(str(s_year))
		select_month = Select(driver.find_element_by_name('ctl03$ddlMonth'))
		select_month.select_by_visible_text(str(s_month))
		driver.find_element_by_name('ctl03$btnSearch').click()

def finish_filling_data(conn):
	conn.commit()
	conn.close()

def job():
	conn, cursor = turn_on_sql()
	store_data_from_earthquake_website(cursor)
	finish_filling_data(conn)

if __name__ == '__main__':
	job()