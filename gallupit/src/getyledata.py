from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import re, time
import numpy as np
import urllib.request, json

base_url = 'https://yle.fi/uutiset/3-10509309'

xpath_title = "/html[@class=' js no-touch fontface svg']/body/div[@id='app']/div[@class='yle__app']\
                /div/div[@id='yle__section--article']/div[@class='yle__layout']/div[@id='yle__contentAnchor']\
                /article[@id='yle__article--testCaseB']/div[@class='yle__article__header']/div[1]\
                /h1[@class='yle__article__heading yle__article__heading--h1']"

xpath_first = "/html[@class=' js no-touch fontface svg']/body/div[@id='app']/div[@class='yle__app']\
                /div/div[@id='yle__section--article']/div[@class='yle__layout']/div[@id='yle__contentAnchor']\
                /article[@id='yle__article--testCaseB']/div[@class='yle__article__content']\
                /div[@class='yle__article__externalContent']/div[@class='yle__article__externalContent__html']\
                /figure[@class='plus-app plus-app-2018-11-puoluekannatus wide']/div[@class='content']\
                /div[@class='navigation_container']/div[@class='navigation_wrapper']/div[@class='present']"

xpath_section_title = "/html[@class=' js no-touch fontface svg']/body/div[@id='app']/div[@class='yle__app']\
                /div/div[@id='yle__section--article']/div[@class='yle__layout']/div[@id='yle__contentAnchor']\
                /article[@id='yle__article--testCaseB']/div[@class='yle__article__content']\
                /div[@class='yle__article__externalContent']/div[@class='yle__article__externalContent__html']\
                /figure[@class='plus-app plus-app-2018-11-puoluekannatus wide']/div[@class='content']\
                /div[@class='container']/div[@class='content_wrapper'][5]/h3[@class='large_header']"

xpath_surrounding_texts = "/html[@class=' js no-touch fontface svg']/body/div[@id='app']/div[@class='yle__app']\
                /div/div[@id='yle__section--article']/div[@class='yle__layout']/div[@id='yle__contentAnchor']\
                /article[@id='yle__article--testCaseB']/div[@class='yle__article__content']\
                /div[@class='yle__article__externalContent']/div[@class='yle__article__externalContent__html']\
                /figure[@class='plus-app plus-app-2018-11-puoluekannatus wide']/div[@class='content']\
                /div[@class='container']/div[@class='content_wrapper'][5]/div[@class='chart_container']"

xpath_container = "/html[@class=' js no-touch fontface svg']/body/div[@id='app']/div[@class='yle__app']\
                /div/div[@id='yle__section--article']/div[@class='yle__layout']/div[@id='yle__contentAnchor']\
                /article[@id='yle__article--testCaseB']/div[@class='yle__article__content']\
                /div[@class='yle__article__externalContent']/div[@class='yle__article__externalContent__html']\
                /figure[@class='plus-app plus-app-2018-11-puoluekannatus wide']/div[@class='content']"

xpath_results = "/html[@class=' js no-touch fontface svg']/body/div[@id='app']/div[@class='yle__app'] \
                /div/div[@id='yle__section--article']/div[@class='yle__layout']/div[@id='yle__contentAnchor'] \
                /article[@id='yle__article--testCaseB']/div[@class='yle__article__content'] \
                /div[@class='yle__article__externalContent']/div[@class='yle__article__externalContent__html'] \
                /figure[@class='plus-app plus-app-2018-11-puoluekannatus wide']/div[@class='content']\
                /div[@class='container']/div[@class='content_wrapper']/div[@class='chart_container']\
                /div[@class='long_chart_container']/div[@id='highcharts-2irw9la-610']\
                /svg[@class='[object SVGAnimatedString]']/rect[@class='[object SVGAnimatedString]']"

xpath_timeinterval = "/html[@class=' js no-touch fontface svg']/body/div[@id='app']/div[@class='yle__app']\
                /div/div[@id='yle__section--article']/div[@class='yle__layout']/div[@id='yle__contentAnchor']\
                /article[@id='yle__article--testCaseB']/div[@class='yle__article__content']\
                /div[@class='yle__article__externalContent']/div[@class='yle__article__externalContent__html']\
                /figure[@class='plus-app plus-app-2018-11-puoluekannatus wide']/div[@class='content']\
                /div[@class='container']/div[@class='content_wrapper'][5]/div[@class='chart_container']\
                /div[@class='time_selection content_container']/a[@class='time_select time_select_3 active']"

xpath_interval_select = "/html[@class=' js no-touch fontface svg']/body/div[@id='app']/div[@class='yle__app']/div/div[@id='yle__section--article']/div[@class='yle__layout']/div[@id='yle__contentAnchor']/article[@id='yle__article--testCaseB']/div[@class='yle__article__content']/div[@class='yle__article__externalContent']/div[@class='yle__article__externalContent__html']/figure[@class='plus-app plus-app-2018-11-puoluekannatus wide']/div[@class='content']/div[@class='container']/div[@class='content_wrapper'][5]/div[@class='chart_container']/h3[@class='content_container'][2]"
xpath_end = "/html[@class=' js no-touch fontface svg']/body/div[@id='app']/div[@class='yle__app']/div/div[@id='yle__section--article']/div[@class='yle__layout']/div[@id='yle__contentAnchor']/article[@id='yle__article--testCaseB']/div[@class='yle__article__content']/div[@class='yle__article__externalContent']/div[@class='yle__article__externalContent__html']/figure[@class='plus-app plus-app-2018-11-puoluekannatus wide']/div[@class='container']/div[@class='content_wrapper'][1]/div[@class='content_container']/p[3]"

driver = webdriver.Safari()
driver.get(base_url)
# driver.set_window_size(1200, 1400)

e = 'start'
currpos = 0
while e != '':
    currpos += 200
    script = "window.scrollTo(0, " + str(currpos) + ");"
    driver.execute_script(script)
    time.sleep(0.2)
    try:
        element = driver.find_element_by_xpath(xpath_section_title)
        print(element)
        e = ''
    except Exception as ex:
        e = str(type(ex))

currpos += 500
script = "window.scrollTo(0, " + str(currpos) + ");"
driver.execute_script(script)

print(element)