import traceback
import pandas as pd
import datetime
from time import sleep
from parsel import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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
from selenium.webdriver.remote.command import Command
import pdb
# from geopy.geocoders import Nominatim

# ***************  For developer use only  **************
# chrome_options = Options()
# # chrome_options.add_argument("--headless")
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument("--window-size=1920,1080")
# chrome_options.add_argument("--start-maximised")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--disable-extensions")
#
# mysql_user = 'av'
# mysql_pass = 'azad'
# mysql_db = 'test'
# mysql_host = 'localhost'

# ***************   for developer use ends   ***************

# ***************  For server use only  **************

chrome_options = Options()
chrome_options.add_argument("--headless")
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument("--window-size=1920,1080")
# chrome_options.add_argument("--start-maximised")
#
mysql_user = 'av'
mysql_pass = 'codegaragetech'
mysql_db = 'google_map'
mysql_host = 'localhost'
# ***************   for server use ends   ***************

mydb = mysql.connector.connect(
    host= mysql_host ,
    user=mysql_user,
    password=mysql_pass,
    database=mysql_db
)
cursor = mydb.cursor()
print("DB Connection Pass ")
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


def scrape_data():
    page_data=[]
    global scraping_zip,div_count,page_number,div_number,elementClick,input_state,driver,div_exception,wait
    wait = WebDriverWait(driver, 5)
    wait_elem = WebDriverWait(driver,4)
    print('Page No.',page_number)
    div_count=0
    sleep(3)
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH,'//span[contains(@class, "n7lv7yjyC35__left")]')))
    except Exception as e:
        print(f"ZIP Code {scraping_zip}, State -> {input_state} , Exception in Span Class of Page No. count")
        skip_log = open('skip_log.log', 'a')
        skip_log.write(f'\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n'
                       f'ZIP Code {scraping_zip}, State -> {input_state} , Exception in Span Class of Page No. count Skipping Zip  , {e}')
        skip_log.close()
        return "scrap_data_exception"

    div_count = driver.find_element_by_xpath('//span[contains(@class, "n7lv7yjyC35__left")]').text.replace(
             'Showing results', '').replace('-', ',').split(',')
    div_count = int(div_count[1]) - int(div_count[0]) + 2

    for listing in range(1,div_count):
        div_number = listing
        try:
            if listing == 1:
                sleep(2)
            wait_elem.until(EC.element_to_be_clickable((By.XPATH,f'//{elementClick}[contains(@data-result-index, "{listing}")]')))
            click_fun('''//{}[contains(@data-result-index, "{}")]'''.format(elementClick,listing),0)
        except :
            temp=''
            if 'a' in elementClick :
                temp='div'
            elif 'div' in elementClick:
                temp = 'a'
            try:
                wait_elem.until(EC.element_to_be_clickable(
                    (By.XPATH, f'//{temp}[contains(@data-result-index, "{listing}")]')))
                click_fun('''//{}[contains(@data-result-index, "{}")]'''.format(temp, listing), 0)
                elementClick = temp
            except Exception as e:
                print(f'\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n'
                          f'ZIP Code {scraping_zip}, State -> {input_state} , Exception Of listing loop Record Skipped , ')
                skip_log = open('skip_log.log', 'a')
                skip_log.write(f'\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n'
                          f'ZIP Code {scraping_zip}, State -> {input_state} , Exception Of listing loop Record Skipped , page no : {page_number}  {e}')
                skip_log.close()
                status = get_status()
                if status is 'Dead':
                    continue
                else:
                    div_exception = True
                    break

        try:
            check = waitAndExecute("Selector(text=driver.page_source).xpath('//h1/span/text()')[0]",0)
            if check == 'Selector_exception':
                wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Back to results"]')))
                driver.find_element_by_xpath('//span[text()="Back to results"]').click()
                raise TimeoutError
            sel = Selector(text=driver.page_source)
        except Exception as e:
            print(f'\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n'
                          f'ZIP Code {scraping_zip}, State -> {input_state} , Exception of Selector Modeule Skipping Record ')
            skip_log = open('skip_log.log', 'a')
            skip_log.write(f'\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n'
                          f'ZIP Code {scraping_zip}, State -> {input_state} , Exception of Selector Modeule Skipping Record  , page no : {page_number}  {e}')
            skip_log.close()
            continue
        ################ AGENCY NAME #################
        try:
            agency_name=Selector(text=driver.page_source).xpath('//h1/span/text()').extract_first()
            if agency_name is None:
                wait.until(EC.element_to_be_clickable((By.XPATH,'//span[text()="Back to results"]')))
                driver.find_element_by_xpath('//span[text()="Back to results"]').click()
                continue
            else:
                agency_name=agency_name.strip()
            print('\tSaving data for ' + agency_name)
            ################ GOOGLE REFERENCE  #################
            reference = driver.current_url
            print("Reference : ", reference)
            latitude = reference.split('@')[1].split(',')[0]
            longitude = reference.split('@')[1].split(',')[1]
            print(f'latitude :{latitude} and longitude :{longitude}')

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
                print("Empty Url")
            else:
                url = url.replace('Website: ', '').strip()
                print(url , "this is url ")

            ################ EMAIL #################
            email = ''
            ################ Facebook link #################
            facebook_link=''
            ################ LinkedIn Link #################
            linkdin_link=''
            ################ ADDRESS #################

            address = sel.xpath('//button[@data-item-id="address"]/@aria-label').extract_first()
            if address is not None:
                address = address.replace('Address: ', '').replace(', United States','')
                print("if condition --> ",address)
                if len(address.split(",")) == 1:
                    address_street = ''
                    address_city = ''
                    address_state = address.split(',')[0].strip().split()[0].strip()
                    address_zip = address.split(',')[0].strip().split()[1].strip()
                    address_zip_code = int(address_zip)
                    address_country = "United States"
                elif len(address.split(',')) == 2:
                    address_street = ''
                    address_city = address.split(',')[0].strip()
                    address_state = address.split(',')[1].strip().split()[0].strip()
                    address_zip = address.split(',')[1].strip().split()[1].strip()
                    address_zip_code = int(address_zip)
                    address_country = "United States"
                elif len(address.split(',')) == 4:
                    address_street = address.split(',')[0]+address.split(',')[1].strip()
                    address_city = address.split(',')[2].strip()
                    address_state = address.split(',')[3].strip().split()[0].strip()
                    address_zip = address.split(',')[3].strip().split()[1].strip()
                    address_zip_code = int(address_zip)
                    address_country = "United States"
                elif len(address.split(',')) == 3:
                    address_street = address.split(',')[0].strip()
                    address_city = address.split(',')[1].strip()
                    address_state = address.split(',')[2].strip().split()[0].strip()
                    address_zip = address.split(',')[2].strip().split()[1].strip()
                    address_zip_code = int(address_zip)
                    address_country = "United States"
                elif len(address.split(',')) == 5:
                    address_street = address.split(',')[0] + address.split(',')[1] + address.split(',')[2]
                    address_city = address.split(',')[3].strip()
                    address_state = address.split(',')[4].strip().split()[0].strip()
                    address_zip = address.split(',')[4].strip().split()[1].strip()
                    address_zip_code = int(address_zip)
                    address_country = "United States"
                else:
                    driver.find_element_by_xpath('//span[text()="Back to results"]').click()
                    print("Address Not match conditions ")
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
           ################## geopy   ######
            # geolocator = Nominatim(user_agent="Google_map")
            # location = geolocator.geocode(address+', United States')
            # if location is None:
            #     latitude =''
            #     longitude = ''
            # else:
            #     latitude = location.latitude
            #     longitude = location.longitude
            #
            # print(f'latitude :{latitude} and longitude :{longitude}')
            ################ LOGO #################

            logo = sel.xpath('//button[@jsaction="pane.heroHeaderImage.click"]/img/@src').extract_first()

            if logo is None:
                logo=''
            else:
                if logo.startswith('//'):
                    logo = 'https:' + logo.strip()

            print('logo url',logo)

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
                          logo,facebook_link,linkdin_link,address_zip_code,address_street.strip(),address_city,address_state,address_country,
                          latitude,longitude,str(datetime.datetime.now()),str(datetime.datetime.now())]
                # mon.strip(),tue.strip(),wed.strip(),
                #                       thu.strip(),fri.strip(),sat.strip(),sun.strip()
                page_data.append(zipdata)
            driver.find_element_by_xpath('//span[text()="Back to results"]').click()
        except Exception as e:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Back to results"]')))
            driver.find_element_by_xpath('//span[text()="Back to results"]').click()
            print(f'\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n'
                      f' ZIP Code {scraping_zip}, State -> {input_state} , Exception While Scraping Record Skipped  ')
            skip_log = open('skip_log.log', 'a')
            skip_log.write(f'\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n'
                      f' ZIP Code {scraping_zip}, State -> {input_state} , Exception While Scraping Record Skipped  , Page No. {page_number}, url -> {reference} {e}')
            skip_log.close()
            continue
    sleep(2)
    return page_data

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
            print("Exception of waitandexecte :",e)
            return 'Selector_exception'
        else:
            return waitAndExecute(execString,waitingCount+1)

def insert_into_db(data):
    global scraping_zip,page_number,input_state
    count = 0
    if len(data) > 0:
        try:
            for i in data:
                count = count + 1
                query="INSERT INTO googles (name,phone_number,email,business_category,maps_reference, review_score," \
                      "number_of_reviews,url,logo,facebook_page,linkedin_page,zip_code,street,city,state,country,latitude," \
                      "longitude,created_at,updated_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                cursor.execute(query,tuple(i))
                mydb.commit()
        except Exception as e:
            skip_log = open('skip_log.log', 'a')
            skip_log.write(f'\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n'
                           f'ZIP Code {scraping_zip} , State -> {input_state} , Error while record saving in db Google Page Ref : {i[4]} ,{e}')
            skip_log.close()
            del data[:count]
            insert_into_db(data)


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


def get_status():
    global driver
    try:
        driver.execute(Command.STATUS)
        return "Alive"
    except :
        return "Dead"

def scraper():
    global page_number,data,div_count,driver,div_exception,scraping_zip,input_state,wait,div_exception_count
    while True:
        if div_exception == True :
            if div_exception_count < 5:
                driver.quit()
                driver = webdriver.Chrome(chromedriver, options=chrome_options)
                driver.get('https://www.google.com/maps/?hl=en')
                sleep(1)
                wait = WebDriverWait(driver, 5)
                search()
                div_exception = False
                page_number = 1
                div_exception_count =div_exception_count + 1
                temp_data = scrape_data()
                if temp_data == "scrap_data_exception":
                    break
                else:
                    data = data + temp_data
            else:
                div_exception = False
                break
        elif page_number == 0:
            page_number +=1
            temp_data = scrape_data()
            if temp_data == "scrap_data_exception":
                break
            else:
                data = data + temp_data
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
            temp_data = scrape_data()
            if temp_data == "scrap_data_exception":
                break
            else:
                data = data + temp_data
        else:
            break
def chromedriver_fun():
    global chromedriver_count,driver,wait
    print(chromedriver_count)
    if chromedriver_count > 10:
        driver.quit()
        driver = webdriver.Chrome(chromedriver, options=chrome_options)
        driver.get('https://www.google.com/maps/?hl=en')
        sleep(2)
        chromedriver_count = 1
        wait = WebDriverWait(driver, 5)
    else:
        chromedriver_count = chromedriver_count +1

def search():
    global scraping_zip,input_state,driver,wait
    search_input = driver.find_element_by_xpath('//*[@id="searchboxinput"]')
    print('\n')
    print('Scraping insurance agency near ' + scraping_zip)
    search_input.clear()
    search_input.send_keys('insurance agency near ' + scraping_zip + ' ' + input_state + ' USA')
    search_input.send_keys(Keys.ENTER)
    wait.until(EC.url_contains(input_state.replace(' ','+')))

############### Update your ChromeDriver Location #############
chromedriver = '/usr/bin/chromedriver' # For local
driver = webdriver.Chrome(chromedriver, options=chrome_options)
driver.get('https://www.google.com/maps/?hl=en')
wait = WebDriverWait(driver,5)
data = []
page_number = 0
div_count = 0
scraping_zip = ''
div_number = 0
error = ''
elementClick = 'div'
chromedriver_count = 1
div_exception = False
try:
    line = checkErrorLogs()
    make_new_log("Error_Check.log")
################# Update InPut CSV Here ######################
    df=pd.read_csv('Master_Csv_Virginia_to_Wisconsin+Florida.csv',sep=',')
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
        input_state = row[0]
        scraping_zip = row[1].replace('ZIP Code ','')
        input_city = row[2].strip()
        input_type = row[4]
        page_number = 0
        if 'P.O. Box' in input_type:
            print('Skipping ' + scraping_zip + ' P.0. Box')
        else:
            chromedriver_fun()
            search()
            div_exception_count = 0
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
                scraper()
            div_count=0
            insert_into_db(data)
            data =[]
            done_zip = open('done_zip.log', 'a')
            done_zip.write(f'{scraping_zip} \n')
            done_zip.close()

    msg ='Scraping script has been completed'
############# Update mail address Here ##################
    send_mail('msingh@anviam.com', 'Google Map Scraper Daily: Success', msg)
    print('All done!')
    driver.quit()
except Exception as e:
    insert_into_db(data)
    error =traceback.format_exc()
    log = open('Error_Check.log', 'a')
    log.write(f"Zipecode , {scraping_zip} , Page-No. , {page_number} ,Div-count., {div_count} ,Div-No. ,{div_number}  \n Error :  {error} ")
    log.close()
    msg = 'Please rerun the script to continue scraping.'
############# Update mail address Here ##################
    send_mail('msingh@anviam.com', 'Google Map Scraper Custom: Error', msg)
    print("Final Exception>>> ", e)
    driver.quit()
