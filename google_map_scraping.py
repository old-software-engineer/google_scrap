import traceback
import pandas as pd
import os,datetime
from time import sleep
from parsel import Selector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import mysql.connector
mysql_user = 'av'
mysql_pass = 'azad'
mysql_db = 'test'

mydb = mysql.connector.connect(
    host="localhost",
    user=mysql_user,
    password=mysql_pass,
    database=mysql_db
)
cursor = mydb.cursor()

def send_mail(_mail, currentSubject,currentMsg):
    try:
        msg = MIMEMultipart()
        message = currentMsg
        username = "msingh@anviam.com"
        password = "codegaragetech@123"
        smtphost = "smtp.gmail.com:587"
        msg["From"] = "msingh@anviam.com"
        msg["To"] = _mail
        msg["Subject"] = currentSubject
        msg.attach(MIMEText(message, 'html'))


        # -------------INCLUDE THIS FOR ATTACHMENT------------------
        # open the file to be sent
        filename = "Error_Check.log"
        attachment = open("Error_Check.log", "rb")

        # instance of MIMEBase and named as p
        p = MIMEBase('application', 'octet-stream')

        # To change the payload into encoded form
        p.set_payload((attachment).read())

        # encode into base64
        encoders.encode_base64(p)

        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        # attach the instance 'p' to instance 'msg'
        msg.attach(p)

        # -------------INCLUDE THIS FOR ATTACHMENT ENDS------------------

        server = smtplib.SMTP(smtphost)
        server.ehlo()
        server.starttls()
        server.login(user=username,password=password)
        server.sendmail(msg['From'], [msg['To']], msg.as_string())
        print('Sent mail successfully')
    except:
        print('Unable to send mail')
    finally:
        server.quit()


def scrape_data(driver):
    page_data=[]
    unknown_pin = open('unknown.log', 'a')
    global scraping_zip,div_count,page_number,div_number
    wait = WebDriverWait(driver,10)
    print('Page No.',page_number)
    div_count=0
    sleep(3)
    wait.until(EC.visibility_of_element_located((By.XPATH,'//span[contains(@class, "n7lv7yjyC35__left")]')))
    div_count = driver.find_element_by_xpath('//span[contains(@class, "n7lv7yjyC35__left")]').text.replace(
             'Showing results', '').replace('-', ',').split(',')
    div_count = int(div_count[1]) - int(div_count[0]) + 2

    for listing in range(1,div_count):
        div_number = listing
        wait.until(EC.element_to_be_clickable((By.XPATH,f'//a[contains(@data-result-index, "{listing}")]')))
        click_fun('''//a[contains(@data-result-index, "{}")]'''.format(listing),0)
        print("this is try")

        waitAndExecute("Selector(text=driver.page_source).xpath('//h1/span/text()')[0]",0)
        sel = Selector(text=driver.page_source)

        ################ AGENCY NAME #################

        agency_name=Selector(text=driver.page_source).xpath('//h1/span/text()').extract_first()
        if agency_name is None:
            wait.until(EC.element_to_be_clickable((By.XPATH,'//span[text()="Back to results"]')))
            driver.find_element_by_xpath('//span[text()="Back to results"]').click()
            continue
        else:
            agency_name=agency_name.strip()
        print('\tSaving data for ' + agency_name)
        ################ Phone NUMBER #################

        phone_number = sel.xpath('//button[@data-tooltip="Copy phone number"]/@aria-label').extract_first()

        if phone_number is None:
            phone_number=''
        else:
            phone_number = phone_number.replace('Phone: ', '').strip()

        print("Phone No.",phone_number)

        ################ URL  #################

        url = sel.xpath('//*[@data-tooltip="Open website"]/@aria-label').extract_first()
        if url is None:
            url=''
        else:
            url = url.replace('Website: ', '').strip()
            print(url , "this is url ")

        ################ EMAIL #################

        email = ''
        print('empty email',email )

        ################ Facebook link #################

        facebook_link=''
        print('FaceBook Link:',facebook_link)

        ################ LinkedIn Link #################

        linkdin_link=''
        print('LinkedIn Link : ',linkdin_link)

        ################ GOOGLE REFERENCE  #################

        reference = driver.current_url
        print("Reference : ", reference)
        latitude = reference.split('@')[1].split(',')[0]
        longitude = reference.split('@')[1].split(',')[1]
        print(f'latitude :{latitude} and longitude :{longitude}')

        ################ ADDRESS #################

        address = sel.xpath('//button[@data-item-id="address"]/@aria-label').extract_first()

        if address:
            address = address.replace('Address: ', '')
            if len(address.split(",")) == 2:
                address_street = ''
                address_city = ''
                address_state = address.split(',')[0].strip().split()[0].strip()
                address_zip = address.split(',')[0].strip().split()[1].strip()
                address_zip_code = int(address_zip)
                address_country = address.split(',')[1].strip()
            elif len(address.split(',')) == 3:
                address_street = ''
                address_city = address.split(',')[0].strip()
                address_state = address.split(',')[1].strip().split()[0].strip()
                address_zip = address.split(',')[1].strip().split()[1].strip()
                address_zip_code = int(address_zip)
                address_country = address.split(',')[2].strip()
            elif len(address.split(',')) == 5:
                address_street = address.split(',')[0]+address.split(',')[1].strip()
                address_city = address.split(',')[2].strip()
                address_state = address.split(',')[3].strip().split()[0].strip()
                address_zip = address.split(',')[3].strip().split()[1].strip()
                address_zip_code = int(address_zip)
                address_country = address.split(',')[4].strip()
            elif len(address.split(',')) == 4:
                address_street = address.split(',')[0].strip()
                address_city = address.split(',')[1].strip()
                address_state = address.split(',')[2].strip().split()[0].strip()
                address_zip = address.split(',')[2].strip().split()[1].strip()
                address_zip_code = int(address_zip)
                address_country = address.split(',')[3].strip()
            else:
                driver.find_element_by_xpath('//span[text()="Back to results"]').click()
                continue
        else:
            address = ''
            address_street = ''
            address_city = ''
            address_state = ''
            address_zip_code = 0
            address_country = ''

        print(address)
        print('street adr: ',address_street )
        print('city:',address_city)
        print('state:',address_state)
        print('zip_code',address_zip_code)
        print('Country :',address_country)

        ################ LOGO #################

        logo = sel.xpath('//button[@jsaction="pane.heroHeaderImage.click"]/img/@src').extract_first()

        if logo is None:
            logo=''
        else:
            if logo.startswith('//'):
                logo = 'https:' + logo.strip()

        print('logo url',logo)

        #################### Working days #########
        # days=sel.xpath("//div[contains(@class,'section-open-hours-container')]//@aria-label").extract_first()
        # mon = tue = wed = thu = fri = sat = sun = ''
        # if days is not None:
        #     list_of_days = days.lower().replace('hide open hours for the week','').replace('.','').split(';')
        #     for i in list_of_days:
        #         if 'monday' in i :
        #             mon = week_check(i)
        #         elif 'tuesday' in i:
        #             tue=week_check(i)
        #         elif 'wednesday' in i :
        #             wed=week_check(i)
        #         elif 'thursday' in i:
        #             thu=week_check(i)
        #         elif 'friday' in i :
        #             fri=week_check(i)
        #         elif 'saturday' in i:
        #             sat=week_check(i)
        #         elif 'sunday' in i:
        #             sun=week_check(i)
        #
        # print(f'Monday : {mon} , Tuesday : {tue} , wednesday : {wed} , thursday : {thu} , friday : {fri} , saturday : {sat} , sunday : {sun} ' )
        ################ CATEGORY  #################
        category = sel.xpath('''//div[contains(@class,'gm2-body-2')][2]//text()''').extract_first()

        if category is None:
            category = ''
        else:
            category = category.strip()
        print("Category : ",category)

        ################ REVIEW SCORE #################

        review_score = sel.xpath('//ol[contains(@aria-label, " stars")]/@aria-label').extract_first()

        if review_score is None:
            review_score=0
        else:
            review_score = review_score.replace('stars','').strip()

        print("Review :",review_score)

        ################ NUMBER OF REVIEWS  #################

        number_of_reviews = sel.xpath('//button[contains(@aria-label, " review")]/@aria-label').extract_first()

        if number_of_reviews is None:
            number_of_reviews=0
        else:
            if 'Write a review' in number_of_reviews:
                number_of_reviews= ''
            if 'Manage this location?' in number_of_reviews:
                number_of_reviews = ''
            if 'Search reviews' in number_of_reviews:
                number_of_reviews = ''
            number_of_reviews = number_of_reviews.replace(',','').replace('review','').replace('s','').strip()
            if len(number_of_reviews) == 0:
                number_of_reviews = 0

        print("Number Of Reviews : ",number_of_reviews)
        input_zip = scraping_zip
        if address_zip_code == int(input_zip):
            zipdata =[agency_name,phone_number,email,category,reference,float(review_score),int(number_of_reviews),url,
                      logo,facebook_link,linkdin_link,address_zip_code,address_street,address_city,address_state,address_country,
                      latitude,longitude,str(datetime.datetime.now()),str(datetime.datetime.now())]
            # mon.strip(),tue.strip(),wed.strip(),
            #                       thu.strip(),fri.strip(),sat.strip(),sun.strip()
            page_data.append(zipdata)
        else:
            unknown_pin.write(f'{address_zip_code} ,')

        driver.find_element_by_xpath('//span[text()="Back to results"]').click()
    unknown_pin.close()
    sleep(2)
    return page_data

def week_check(string):
    split_day_text = string.split(',')[0].strip().split(' ')
    if len(split_day_text) > 1:
        reason =''
        if 'closed' in string:
            for i in range(1,len(split_day_text)):
                reason=reason+split_day_text[i]
            return string.split(',')[1]+' '+reason.strip()
        else:
            return string.split(',')[1].strip()
    else:
        return string.split(',')[1].strip()

def click_fun(execString,waitingCount):
    try:
        driver.find_element_by_xpath(execString).click()
        # print("waitingCount click",waitingCount)
        return True
    except Exception as click_fun_exception:
        sleep(.25)
        if waitingCount > 40:
            print(f"Click_fun Error : {click_fun_exception}")
            return False
        else:
            click_fun(execString,waitingCount+1)

def waitAndExecute(execString,waitingCount):
    try:
        exec(execString)
        return True
    except Exception as e:
        sleep(0.25)
        if waitingCount > 40:
            print('waiting count of waitandexecute',waitingCount)
            print("Exception of waitandexecte :",e)
            return False
        else:
            return waitAndExecute(execString,waitingCount+1)

def insert_into_db(data):
    if len(data) > 0:
        for i in data:
            query="INSERT INTO googles (name,phone_number,email,business_category,maps_reference, review_score," \
                  "number_of_reviews,url,logo,facebook_page,linkedin_page,zip_code,street,city,state,country,latitude," \
                  "longitude,created_at,updated_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
            cursor.execute(query,tuple(i))
            mydb.commit()
# ,monday,tuesday,wednesday,thursday,friday,saturday,sunday    ,%s,%s,%s,%s,%s,%s,%s

def make_new_log(filename):
    new = open(filename, "w")
    new.close()

def checkErrorLogs():
    try:
        check = open("Error_Check.log", "r")
    except:
        return 'normal'
    lines = check.readlines()
    if len(lines) > 1:
        line = lines[0]
        check.close()
        return line
    else:
        check.close()
        return 'normal'



def scraper(driver):
    global page_number,data,div_count
    wait = WebDriverWait(driver, 10)
    while True:
        if page_number == 0:
            page_number +=1
            temp_data = scrape_data(driver)
            data = data+ temp_data
        elif page_number == 3:
            break
        elif div_count == 21:
            try:
                ### --  this check is for no next page present ----
                driver.find_element_by_xpath("//button[@aria-label=' Next page ' and @disabled='true']")
                break
            except:
                pass
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label,'Next page')]")))
            driver.find_element_by_xpath("//button[contains(@aria-label,'Next page')]").click()
            page_number += 1
            temp_data = scrape_data(driver)
            data = data+temp_data
        else:
            break

############### Update your ChromeDriver Location #############
driver = webdriver.Chrome('/usr/bin/chromedriver')
driver.get('https://www.google.com/maps/?hl=en')
done_zip =open('done_zip.log','a')
wait = WebDriverWait(driver, 10)
data = []
page_number = 0
div_count = 0
scraping_zip = ''
div_number = 0
error = ''
try:
    line = checkErrorLogs()
    make_new_log("Error_Check.log")
    log = open('Error_Check.log', 'a')
################# Update InPut CSV Here ######################
    df=pd.read_csv('/home/code/input.csv',sep=',')
    if line != 'normal':
        start_line = line.split(',')
        starting_zip = start_line[1].strip()
        starting_page = int(start_line[3].strip())
        df=df.loc[(df['ZIP Code'] == 'ZIP Code ' +starting_zip).idxmax():]
    else:
        starting_zip=''
        starting_page =0
    reader=df.values
    for row in reader:
        scraping_zip = row[0].replace('ZIP Code ','')
        input_city = row[1].strip()
        ########################################## Enter state manually ###############
        input_state = "Alabama"
        input_type = row[3]
        page_number = 0
        if 'P.O. Box' in input_type:
            print('Skipping ' + scraping_zip + ' P.0. Box')
        else:
            search_input =driver.find_element_by_xpath('//*[@id="searchboxinput"]')
            print('\n')
            print('Scraping insurance agency near ' + scraping_zip)
            search_input.clear()
            search_input.send_keys('insurance agency near ' +scraping_zip+' '+input_state+' USA')
            search_input.send_keys(Keys.ENTER)
            wait.until(EC.url_contains(input_state))
            if line != 'normal':
                line = 'normal'
                if starting_page == 2:
                    page_number = 1
                    div_count= 21
                elif starting_page > 2:
                    div_count = 21
                    click_count = starting_page - 2
                    page_number = 1
                    for x in range(0,click_count):
                        sleep(2)
                        try:
                            wait.until(EC.presence_of_element_located((By.XPATH,"//button[contains(@aria-label,'Next page')]")))
                        except:
                            continue

                        wait.until(
                            EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label,'Next page')]"))).click()
                        page_number=page_number+1
                        sleep(3)
###### If No records on searched Zip Code ########
            try:
                driver.find_element_by_class_name('section-partial-interpretation')
                continue
            except:
                scraper(driver)
            div_count=0
            insert_into_db(data)
            data =[]
            done_zip.write(f'{scraping_zip} \n')
    log.close()
    done_zip.close()
    msg ='Scraping script has been completed'
############# Update mail address Here ##################
    send_mail('msingh@anviam.com', 'Google Map Scraper Daily: Success', msg)
    print('All done!')
    driver.quit()
except Exception as e:
    insert_into_db(data)
    error =traceback.format_exc()
    log.write(f"Zipecode , {scraping_zip} , Page-No. , {page_number} ,Div-count., {div_count} ,Div-No. ,{div_number}  \n Error :  {error} ")
    log.close()
    msg = 'Please rerun the script to continue scraping.'
############# Update mail address Here ##################
    send_mail('msingh@anviam.com', 'Google Map Scraper Custom: Error', msg)
    print("Final Exception>>> ", e)
    driver.quit()
