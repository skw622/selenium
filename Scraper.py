import os
import threading
from symbol import parameters

from selenium import webdriver
import json
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import csv
import tkinter


window = tkinter.Tk()
window.title("GUI")

# creating 2 text labels and input labels

tkinter.Label(window, text="Username").grid(row=0)  # this is placed in 0 0
# 'Entry' is used to display the input-field
tkinter.Entry(window).grid(row=0, column=1)  # this is placed in 0 1

tkinter.Label(window, text="Password").grid(row=1)  # this is placed in 1 0
tkinter.Entry(window, show='*').grid(row=1, column=1)  # this is placed in 1 1

# 'Checkbutton' is used to create the check buttons
tkinter.Checkbutton(window, text="Keep Me Logged In").grid(columnspan=2)
window.mainloop()
exit()

print('account3')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 2})
chrome_options.add_argument("log-level=3")

driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
print('open site')
url = "https://www.linkedin.com"
driver.get(url)


company = 'Applied Materials'
country = 'United States'
userinfomation = 'director application development'

# User infomation for creating csv file
number = 0


def login(arg):

    name = arg["username"]
    pwd = arg["password"]
    wait = WebDriverWait(driver, 20)
    username = wait.until(
        ec.visibility_of_element_located((By.NAME, "session_key")))
    username.send_keys(name)
    time.sleep(0.5)

    password = driver.find_element_by_name('session_password')
    password.send_keys(pwd)
    time.sleep(0.5)

    sign_in_button = driver.find_element_by_class_name(
        'sign-in-form__submit-btn')
    sign_in_button.click()
    print('logged in')
    time.sleep(1)

    searchUsers()


def searchUsers():
    time.sleep(1)
    search_box = driver.find_element_by_class_name(
        'search-global-typeahead__input')
    search_box.send_keys(company)
    time.sleep(0.5)
    search_box.send_keys(Keys.ENTER)
    time.sleep(2)

    wait = WebDriverWait(driver, 10)
    AllFilter = wait.until(
        ec.visibility_of_element_located(
            (By.CLASS_NAME, 'search-filters-bar__all-filters'))
    )
    AllFilter.click()
    time.sleep(1)

    wait = WebDriverWait(driver, 10)
    Locations = wait.until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, "#locations-facet-values ol li div div input")))
    time.sleep(0.5)
    Locations.send_keys(country)
    time.sleep(1.5)

    Locations.send_keys(Keys.DOWN)
    time.sleep(0.5)
    Locations.send_keys(Keys.ENTER)

    CurrentCompany = driver.find_element_by_css_selector(
        '#current-companies-facet-values ol li div div input')
    time.sleep(0.5)
    CurrentCompany.send_keys(company)
    time.sleep(1.5)
    CurrentCompany.send_keys(Keys.DOWN)
    time.sleep(0.5)
    CurrentCompany.send_keys(Keys.ENTER)

    ApplyBtn = driver.find_element_by_class_name(
        'search-advanced-facets__button--apply')
    ApplyBtn.click()
    time.sleep(1)

    search_box.clear()
    time.sleep(0.5)
    search_box.send_keys(userinfomation)
    time.sleep(0.5)
    search_box.send_keys(Keys.ENTER)
    time.sleep(3)
    search_box.send_keys(Keys.ENTER)

    currentUrl = driver.current_url
    for val in range(1, 101):
        page_number = str(val)
        driver.get(currentUrl + '&page=' + page_number)
        time.sleep(1)

        SCROLL_PAUSE_TIME = 0.5
        # Get scroll height
        last_height = driver.execute_script(
            "return document.body.scrollHeight")
        new_height = 0

        while True:
            # Scroll down to bottom
            heightto = new_height + 300
            driver.execute_script(
                "window.scrollTo(" + str(new_height) + ", " + str(heightto) + ");")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = new_height + 900
            if new_height > last_height:
                break

        users = driver.find_elements_by_class_name(
            'search-result__result-link')
        userlink = []
        for index in range(1, len(users), 2):
            if len(users[index].get_attribute('href')) < 100:
                userlink.append(users[index].get_attribute('href'))
                time.sleep(0.5)

        for index, user in enumerate(userlink):
            gotoUser(index, user, page_number)


def gotoUser(index, user, page):
    print(page + ' page')
    global number
    number += 1
    driver.get(user)

    fullname = driver.find_element_by_css_selector(
        '.pv-top-card-v3--list .inline').text
    degree = driver.find_element_by_css_selector('.flex-1 h2').text
    Location = driver.find_element_by_css_selector(
        '.pv-top-card-v3--list.pv-top-card-v3--list-bullet .t-16.inline-block').text

    selector = driver.find_elements_by_css_selector('a div h4 span')[0].text

    if selector == 'Dates Employed':
        ex_degree = driver.find_elements_by_css_selector(
            '.pv-entity__summary-info h3')[0].text
        ex_company = driver.find_elements_by_css_selector(
            '.pv-entity__summary-info .pv-entity__secondary-title')[0].text
        date_employed = driver.find_elements_by_css_selector(
            '.pv-entity__summary-info h4 span')[1].text
        employment_duration = driver.find_elements_by_css_selector(
            '.pv-entity__summary-info h4 span')[3].text
        employment_term = date_employed + ' (' + employment_duration + ')'
        try:
            ex_location = driver.find_elements_by_css_selector(
                '.pv-entity__location span')[1].text
        except:
            ex_location = ''
        total_duration = ''
    if selector == 'Total Duration':
        ex_company = driver.find_elements_by_css_selector(
            '.pv-entity__company-summary-info h3 span')[1].text
        total_duration = driver.find_elements_by_css_selector(
            '.pv-entity__company-summary-info h4 span')[1].text
        ex_degree = driver.find_elements_by_css_selector(
            '.pv-entity__summary-info-v2 h3 span')[1].text
        date_employed = driver.find_elements_by_css_selector(
            '.pv-entity__summary-info-v2 h4 span')[1].text
        employment_duration = driver.find_elements_by_css_selector(
            '.pv-entity__summary-info-v2 h4 span')[3].text
        employment_term = date_employed + ' (' + employment_duration + ')'
        try:
            ex_location = driver.find_elements_by_css_selector(
                '.pv-entity__location span')[1].text
        except:
            ex_location = ''
    row = [number, fullname, degree, Location, ex_company,
           ex_degree, total_duration, employment_term, ex_location]
    createcsv(row)


def createcsv(row):
    with open('output.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)
    csvFile.close()


def start():
    csvData = [['No', 'Full Name', 'Current Degree',
                'Current Location', 'Experienced Company', 'Experienced Degree', 'Total Duration', 'Employment Duration', 'Experienced Location'], ]
    with open('output.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData)
    csvFile.close()
    userinfo = {"username": "bhuvnesh.agarwal88@gmail.com",
                "password": "KCI@lifeisallover88"}
    login(userinfo)


start()
