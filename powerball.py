# Author: Matthew Gray
# Copyright (C) 2018 Matthew Gray
# Last Modified: 12/27/2018
# powerball.py - Scrapes all Powerball drawing numbers since the program began on 09/22/1992 from powerball.net (Requires Selenium Chrome driver)

import csv
import datetime
import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_driver = r""    # Put path to Selenium chrome driver here
chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)

script_path = os.path.dirname(os.path.realpath(__file__))
output_csv = os.path.join(script_path, "powerball_drawings.csv")

file = open(output_csv, 'w')

wr = csv.writer(file, dialect='excel', lineterminator='\n')

headers = ["Date", "Num1", "Num2", "Num3", "Num4", "Num5", "Powerball"]
wr.writerow(headers)

base_url = r"https://www.powerball.net/numbers/"
start_date = "1992-04-22"

driver.get(base_url + start_date)

url_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")

while url_date <= datetime.datetime.today():

    date = [(driver.current_url).split(r"/")[-1]]
    balls = [x.text for x in driver.find_elements_by_class_name("ball")]
    powerball = [driver.find_element_by_class_name("powerball").text]

    powerball_draw = date + balls + powerball

    print(powerball_draw)
    wr.writerow(powerball_draw)

    day_of_week = url_date.weekday()
    if day_of_week == 2:
        url_date = url_date + datetime.timedelta(days=3)
    elif day_of_week == 5:
        url_date = url_date + datetime.timedelta(days=4)

    url_date_formatted = url_date.strftime("%Y-%m-%d")
    driver.get(base_url + url_date_formatted)
    time.sleep(1)

file.close()
driver.quit()
