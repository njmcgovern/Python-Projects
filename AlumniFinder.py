import regex as re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from math import ceil
from os import environ
# NUM_MINUTES = 3
# SLEEP = 60*NUM_MINUTES
TIMEOUT = 30

class AlumniAttributes:
    
    def __init__(self, 
                first=None, 
                last=None, 
                status=None, 
                initiated_chapter=None, 
                initiated_university=None, 
                associated_chapter=None, 
                associated_university=None, 
                initiation_year=None, 
                email=None):
        self.first = first
        self.last = last
        self.status = status
        self.initiated_chapter = initiated_chapter
        self.initiated_university = initiated_university
        self.associated_chapter = associated_chapter
        self.associated_university = associated_university
        self.initiation_year = initiation_year
        self.email = email


def create_table(alumni_list):

    df = pd.DataFrame(data={'Legal First Name': [x.first for x in alumni_list],
                            'Legal Last Name': [x.last for x in alumni_list],
                            'Status': [x.status for x in alumni_list],
                            'Initiated Chapter': [x.initiated_chapter for x in alumni_list],
                            'Initiated University': [x.initiated_university for x in alumni_list],
                            'Associated Chapter': [x.associated_chapter for x in alumni_list],
                            'Associated University': [x.associated_university for x in alumni_list],
                            'Initiation Year': [x.initiation_year for x in alumni_list],
                            'Email': [x.email for x in alumni_list]
                            }
                      )

    df.index = pd.RangeIndex(start=1, stop=len(alumni_list)+1, step=1)
    df.to_csv(environ['USERPROFILE'] + '\Desktop\Alumni_List.csv')

    print('\n', df)
    return df
def main():

    user_email = input("What is your mySigTau email? ")
    user_password = input("What is your mySigTau password? ")
    print(user_email, user_password)
    alumni_list = []
    num_elems = 6

    option = webdriver.ChromeOptions()
    option.add_argument("--incognito")
    option.add_argument('--headless')
    option.add_argument('--log-level=2')
    browser = webdriver.Chrome(
        executable_path=environ['USERPROFILE'] +
        r'\\Desktop\\chromedriver_win32\\chromedriver.exe',
        chrome_options=option)    

    browser.get('https://login.omegafi.com/cas/login?apikey=54bbbdb89d1446feae4383c331ee2853&oauth=0&eventid=&login_apikey=54bbbdb89d1446feae4383c331ee2853&org=stg&third_party=0&service=https%3A%2F%2Fmy.omegafi.com%2Fapps%2Fmyomegafi%2Flogin%2Flogin_post.php%3FUserName%3D%2A%2A%2A%26Password%3D%2A%2A%2A%26apikey%3D54bbbdb89d1446feae4383c331ee2853%26oauth%3D0%26eventid%3D%26login_apikey%3D54bbbdb89d1446feae4383c331ee2853%26org%3Dstg%26third_party%3D0&ra=1')

    try:
        WebDriverWait(browser, TIMEOUT).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "div.container-fluid")))

    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()
        exit()

    try:
        email = browser.find_element_by_xpath(
            "// input[@placeholder='email']")
        password = browser.find_element_by_xpath("// input[@placeholder='password']")
        email.send_keys(user_email)
        password.send_keys(user_password)
        browser.find_element_by_name("commit").submit()
        print("Logged in!")

    except:
        print("Error on login")
        browser.quit()
        exit()

    browser.get(
        'https://my.omegafi.com/apps/myomegafi/index.php#!national/membersearch')

    try:
        WebDriverWait(browser, TIMEOUT).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "div.form-group")))

    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()
        exit()
    
    alpha_chi = r"Alpha Chi"

    print("finding chapter")
    chapter = browser.find_elements_by_xpath(
        "// input[@value='Select Some Options']")
    chapter[0].click()
    chapter[0].send_keys(alpha_chi)
    chapter[0].click()
    chapter[0].send_keys(Keys.ENTER)
    chapter[0].click()

    browser.find_element_by_xpath("// input[@name='Submit']").submit()

    try:
        WebDriverWait(browser, TIMEOUT).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "div.table-responsive")))

    except TimeoutException:
        print("Timed out waiting for alumni to load")
        browser.quit()
        exit()

    alumni_page_info = browser.find_element_by_css_selector('div.dataTables_info').text.split()
    num_alumni = int(alumni_page_info[-2])
    num_alumni_per_page = int(alumni_page_info[-4])
    num_pages = ceil(num_alumni/num_alumni_per_page)

    print("Acquiring Alumni information ... ")
    for x in range(0,num_pages):
        try:
            WebDriverWait(browser, TIMEOUT).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "div.table-responsive")))

        except TimeoutException:
            print("Timed out waiting for alumni to load")
            browser.quit()
            exit()
        lastNamesHTML = browser.find_elements_by_xpath(
            "// td[@title='Legal Last Name']")
        assocChapterHTML = browser.find_elements_by_xpath(
            "// td[@title='Associated Chapter']")
        assocUniversityHTML = browser.find_elements_by_xpath(
            "// td[@title='Associated University']")
        brother_info = browser.find_elements_by_xpath(
            "// td[@class='excel pdf word screen print']")

        last_names = [x.text for x in lastNamesHTML]
        assoc_chapter = [x.text for x in assocChapterHTML]
        assoc_university = [x.text for x in assocUniversityHTML]
        bro = [x.text for x in brother_info]

        for info in range(0,len(last_names)):
            alumnus = AlumniAttributes(
                first=bro[info*num_elems],
                last=last_names[info],
                status=bro[info*num_elems+1],
                initiated_chapter=bro[info*num_elems+2],
                initiated_university=bro[info*num_elems+3],
                associated_chapter=assoc_chapter[info],
                associated_university=assoc_university[info],
                initiation_year=bro[info*num_elems+4],
                email=bro[info*num_elems+5]
            )
            alumni_list.append(alumnus)

        print("Page {:d} complete".format(x+1))
        browser.find_element_by_css_selector('span#memberresults_next').click()

    df = create_table(alumni_list)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram has been interrupted by user")
        print("Thank you for using this service!")
        print("\nExiting now ... \n")
        exit()
