import datetime
from bs4 import BeautifulSoup
import requests
import mysql.connector
import re

mysql_user = 'av'
mysql_pass = 'azad'
mysql_db = 'google_map'

mydb = mysql.connector.connect(
    host="localhost",
    user=mysql_user,
    password=mysql_pass,
    database=mysql_db
)
cursor = mydb.cursor(buffered=True)

facebook_reg ='(?:(?:http|https):\/\/)?(?:www.)?facebook.com\/(?:(?:\w)*#!\/)?(?:pages\/)?(?:[?\w\-]*\/)?(?:profile.php\?id=(?=\d.*))?([\w\-]*)?'
linkedin_reg ='^https:\/\/[a-z]{2,3}\.linkedin\.com\/.*$'
query = f"select * from googles"
cursor.execute(query)
data = cursor.fetchall()
for record in data:
    print(record)
    record_id = record[0]
    name = record[1]
    phn = record[2]
    business_cat = record[4]
    maps_reference = record[5]
    review_score = record[6]
    number_of_reviews = record[7]
    url = record[8]
    logo = record[9]
    zip_code = record[12]
    street = record[13]
    city = record[14]
    country = record[15]
    state = record[16]
    latitude = record[17]
    longitude = record[18]
    facebook_url = ''
    linkedin_url = ''
    email = ''
    if len(url) > 0:
        print(f"Record Contain Url -> {url} ")
        agency_query = f"select id from agencies where url = %s limit 1 ;"
        agency_array = [url]
        cursor.execute(agency_query,tuple(agency_array))
        agency_result = cursor.fetchone()

        if agency_result is not None:
            print('Agency Already Present ')
            fetch_email_query = f"Select email from agency_locations where agency_id = {agency_result[0]} and email is not NULL and email != '' limit 1;"
            cursor.execute(fetch_email_query)
            email = cursor.fetchone()
            if email is None:
                email = ''
            else:
                email = email[0]
            location_check_query = f"Select id from agency_locations where agency_id = %s and phone = %s and email = %s and " \
                             f"street = %s and city = %s and state = %s and zipcode = %s and country = %s and agency_category = %s  limit 1;"
            loc_array = [agency_result[0],phn,email,street,city,state,zip_code,country,business_cat]
            cursor.execute(location_check_query,tuple(loc_array))
            loc_id = cursor.fetchone()
            if loc_id is None:
                new_location_query = f"INSERT INTO agency_locations(phone,email,street,city,state,zipcode,country,agency_category,lat,lng,gmap_reference," \
                                     f"gmaps_review_score,gmaps_reviews,created_at,updated_at,agency_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
                new_loc_array = [phn,email,street,city,state,zip_code,country,business_cat,latitude,longitude,maps_reference,review_score,number_of_reviews,
                                 str(datetime.datetime.now()),str(datetime.datetime.now()),agency_result[0]]
                cursor.execute(new_location_query,tuple(new_loc_array))
                mydb.commit()
            continue
        #------------------------ Hitting URL -------------------------------------#
        try:
            req = requests.get('http://'+url,timeout=20)
            doc =BeautifulSoup(req.content,'html.parser')
            req.close()
        except Exception as e:
            doc = ''
            print(f"Exception in BeautifulSoup --> {e}")

        #------------------ Checking FaceBook , LinkedIn , Email -----------------#
        if len(doc) > 0:
            links=[]
            for link in doc.find_all('a'):
                links.append(link.get('href'))
            links =list(filter(None, links))
            for facebook in links:
                check = re.match(facebook_reg,facebook)
                if check is not None:
                    facebook_url = check.string
                    break
            for linkedin in links:
                check = re.match(linkedin_reg,linkedin)
                if check is not None:
                    linkedin_url = check.string
                    break
            dom = doc.text.lower().split()
            for e in dom:
                check = re.match('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$',e)
                if check is not None:
                    email = check.string
                    break

        #------------- Creating New Agency and Location  --------------------#
        new_agency_query = f"INSERT INTO agencies(name,logo,url,facebook,linkedin,created_at,updated_at)" \
               f"VALUES (%s,%s,%s,%s,%s,%s,%s);"
        new_agency_array =[name,logo,url,facebook_url,linkedin_url,str(datetime.datetime.now()),str(datetime.datetime.now())]
        cursor.execute(new_agency_query,tuple(new_agency_array))
        new_agency_id = cursor.lastrowid
        mydb.commit()

        new_location_query = f"INSERT INTO agency_locations(phone,email,street,city,state,zipcode,country,agency_category,lat,lng,gmap_reference," \
                           f"gmaps_review_score,gmaps_reviews,created_at,updated_at,agency_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        new_loc_array = [phn,email,street,city,state,zip_code,country,business_cat,latitude,longitude,maps_reference,review_score,number_of_reviews,
                         str(datetime.datetime.now()),str(datetime.datetime.now()),new_agency_id]
        cursor.execute(new_location_query,tuple(new_loc_array))
        mydb.commit()

        #------------- Creating Categories ----------------#
        if len(doc) > 0:
            insurance = doc.text.lower()
            if 'car insurance' in insurance or 'auto insurance' in insurance:
                query = f"INSERT INTO agency_categories (status, created_at, updated_at,category_id,agency_id)" \
                        f"VALUES ('Active','{str(datetime.datetime.now())}','{str(datetime.datetime.now())}','1','{new_agency_id}');"
                cursor.execute(query)
                mydb.commit()
            if 'health insurance' in insurance:
                query = f"INSERT INTO agency_categories (status, created_at, updated_at,category_id,agency_id)" \
                        f"VALUES ('Active','{str(datetime.datetime.now())}','{str(datetime.datetime.now())}','2','{new_agency_id}');"
                cursor.execute(query)
                mydb.commit()
            if 'life insurance' in insurance:
                query = f"INSERT INTO agency_categories (status, created_at, updated_at,category_id,agency_id)" \
                        f"VALUES ('Active','{str(datetime.datetime.now())}','{str(datetime.datetime.now())}','3','{new_agency_id}');"
                cursor.execute(query)
                mydb.commit()
            if 'home insurance' in insurance:
                query = f"INSERT INTO agency_categories (status, created_at, updated_at,category_id,agency_id)" \
                        f"VALUES ('Active','{str(datetime.datetime.now())}','{str(datetime.datetime.now())}','4','{new_agency_id}');"
                cursor.execute(query)
                mydb.commit()
    else:
        print(" Record Not Contain Url ")
        agency_query = f"select id from agencies where name = %s and url = %s limit 1;"
        agency_array = [name,url]
        cursor.execute(agency_query,tuple(agency_array))
        agency_result = cursor.fetchone()
        if agency_result is not None:
            print(' Agency Already Present ')
            location_check_query = f"Select id from agency_locations where agency_id = %s and phone = %s and " \
                                   f"street = %s and city = %s and state = %s and zipcode = %s and country = %s and agency_category = %s limit 1;"
            loc_array = [agency_result[0],phn,street,city,state,zip_code,country,business_cat]
            cursor.execute(location_check_query,tuple(loc_array))
            loc_id = cursor.fetchone()
            if loc_id is None:
                new_location_query = f"INSERT INTO agency_locations(phone,email,street,city,state,zipcode,country,agency_category,lat,lng,gmap_reference," \
                                     f"gmaps_review_score,gmaps_reviews,created_at,updated_at,agency_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
                new_loc_array = [phn,email,street,city,state,zip_code,country,business_cat,latitude,longitude,maps_reference,review_score,number_of_reviews,
                                    str(datetime.datetime.now()),str(datetime.datetime.now()),agency_result[0]]
                cursor.execute(new_location_query,tuple(new_loc_array))
                mydb.commit()
            continue

        #-------------- New Agency and Location Create -----------------#
        new_agency_query = f"INSERT INTO agencies(name,logo,url,facebook,linkedin,created_at,updated_at)" \
                           f"VALUES (%s,%s,%s,%s,%s,%s,%s);"
        new_agency_array =[name,logo,url,facebook_url,linkedin_url,str(datetime.datetime.now()),str(datetime.datetime.now())]
        cursor.execute(new_agency_query,tuple(new_agency_array))
        new_agency_id = cursor.lastrowid
        mydb.commit()
        new_location_query = f"INSERT INTO agency_locations(phone,email,street,city,state,zipcode,country,agency_category,lat,lng,gmap_reference," \
                             f"gmaps_review_score,gmaps_reviews,created_at,updated_at,agency_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        new_loc_array = [phn,email,street,city,state,zip_code,country,business_cat,latitude,longitude,
                         maps_reference,review_score,number_of_reviews,str(datetime.datetime.now()),str(datetime.datetime.now()),new_agency_id]
        cursor.execute(new_location_query,tuple(new_loc_array))
        mydb.commit()