from parsel import Selector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from geopy.geocoders import Nominatim
import pgeocode


# import mysql.connector
# mysql_user = 'admin'
# mysql_pass = 'nRf6vmrNcinY'
# mysql_db = 'Policy_Pals_MainDb'
# mysql_host = 'ppfirstdb.c272dqo6slhc.us-east-2.rds.amazonaws.com'
#
#
# mydb = mysql.connector.connect(
#     host= mysql_host ,
#     user=mysql_user,
#     password=mysql_pass,
#     database=mysql_db
# )
# cursor = mydb.cursor()
# print("DB Connection Pass ")

# nomi = pgeocode.Nominatim('fr')
# nomi.query_postal_code("75013")
#
# geolocator = Nominatim(user_agent="specify_your_app_name_here")
# location = geolocator.geocode("")
# print(location.address)
# # Flatiron Building, 175, 5th Avenue, Flatiron, New York, NYC, New York, ...
# print((location.latitude, location.longitude))
# # (40.7410861, -73.9896297241625)
# print(location.raw)
# # {'place_id': '9167009604', 'type': 'attraction', ...}
#
driver = webdriver.Chrome('/usr/bin/chromedriver')
driver.get('https://www.google.co.in/maps/search/insurance+agency+near+82001+usa/@41.1574793,-104.8413916,13z/data=!3m1!4b1')
try:
    print('adf')
    asd='as'
except Exception as e:
    print(e)