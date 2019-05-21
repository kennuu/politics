from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import re, time
import pandas as pd

base_url = 'https://www.vaalikone.fi/eduskunta2019/'
driver = webdriver.PhantomJS(service_args=['--load-images=no'])
driver.get(base_url)


while(True):
    try:
        driver.find_element_by_css_selector("div.btn[ng-click^='more']").click()
        time.sleep(1)
        print('getting more people')
    except:
        print('everybody visible')
        break

soup = BeautifulSoup(driver.page_source, 'html.parser')
all_links = soup.findAll('a', attrs = {'href': re.compile("^/fi/ihmiset/[a-zA-Z\-åäöÅÄÖ]+/")})

for link in all_links:
    links.append(link.get('href'))
    names.append(link.find('h3').contents[0])

    print(names[-1], links[-1])

# with open('../data/names.csv', 'w') as file:
    # for (name, link) in zip(names, links):
    #     file.write('"' + name + '"')

pd.DataFrame({'names':names, 'links':links}).to_csv('../data/names.csv')
