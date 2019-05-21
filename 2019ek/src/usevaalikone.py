from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import re, time
import numpy as np
import urllib.request, json

def initialise_machine():
    driver.get(base_url)
    time.sleep(0.2)
    driver.find_element_by_xpath(select_city_xpath).click()
    time.sleep(0.1)
    driver.find_element_by_xpath(start_xpath).click()
    time.sleep(0.2)


def try_action_click(driver, xpath):
    maxtries = 10
    tries = 0
    success = False
    while not success and tries < maxtries:
        try:
            driver.find_element_by_xpath(xpath).click()
            success = True
        except Exception as e:
            if tries > 3:
                print("Server too slow, waiting")
            tries += 1
            time.sleep(0.2)
    if tries >= maxtries:
        print("Failing to get data with XPATH", xpath, ". Exiting")
        exit(-1)

def try_action_text(driver, xpath):
    maxtries = 10
    tries = 0
    success = False
    while not success and tries < maxtries:
        try:
            text = driver.find_element_by_xpath(xpath).text
            success = True
        except Exception as e:
            if tries > 3:
                print("Server too slow, waiting")
            tries += 1
            time.sleep(0.2)
    if tries < maxtries:
        return text
    else:
        print("Failing to get data with XPATH", xpath, ". Exiting")
        exit(-1)

base_url = 'https://www.vaalikone.fi/eduskunta2019'
candidate_answer_dir = '/api/candidates'
party_dir = '/api/parties'

# fetch candidates
with urllib.request.urlopen(base_url + candidate_answer_dir) as url:
    candidates = json.loads(url.read().decode())

# fetch parties
with urllib.request.urlopen(base_url + party_dir) as url:
    parties = json.loads(url.read().decode())
parties = {party['id']:party for party in parties}

# initialise answering
# driver = webdriver.PhantomJS(service_args=['--load-images=no'])
driver = webdriver.Safari()
driver.get(base_url)



# print(driver.find_element_by_css_selector("div.preDefinedDistrictsWrapper__2Kl36"))
#
# print(driver.find_element_by_xpath("//preDefinedDistrictsWrapper__2Kl36//input[@type="button" and @data-district-id='49']"))
#
# driver.find_element_by_css_selector("districtButton__3mlrh".[datadistrict-id='49']")

# Select Espoo
select_city_xpath = "/html[@class=' no-touchevents']/body/div[@id='app']/div/div[@class='wrapper__14ojg hs']\
/main[@class='content__259k1']/div[@class='someWrapper__oxPfx']/div[@class='content__3UVlg']/div[@class='card__1IEXc']\
/div[@class='districtSelectForm__3YZdk']/form[@class='form__3P9uY']/div[@class='preDefinedDistrictsWrapper__2Kl36']\
/span[2]/button[@class='districtButton__3mlrh'][1]"
# Start the machine
start_xpath = "/html[@class=' no-touchevents']/body/div[@id='app']/div/div[@class='wrapper__14ojg hs']\
/main[@class='content__259k1']/div[@class='someWrapper__oxPfx']/div[@class='content__3UVlg']/div[@class='card__1IEXc']\
/div[@class='districtSelectForm__3YZdk']/form[@class='form__3P9uY']/div[@class='submitWrapper__1_DJu']\
/button[@class='big__1_aAh button__38IWe']/span"
# choose an answer
choice_xpath = "/html[@class=' no-touchevents']/body/div[@id='app']/div/div[@class='wrapper__14ojg hs']\
/main[@class='content__259k1']/div[@class='someWrapper__oxPfx']/div[@class='content__3UVlg']/div[@class='card__1IEXc']\
/div/div[1]/div[@class='answerSelectorContainer__3N92g']/div[@class='answerSelector__3GCJn']/button[@class='option__38vU9']"
# go to the next question (obsolete as choosing already goes to the next)
next_xpath = "/html[@class=' no-touchevents']/body/div[@id='app']/div/div[@class='wrapper__14ojg hs']\
/main[@class='content__259k1']/div[@class='someWrapper__oxPfx']/div[@class='content__3UVlg']/div[@class='card__1IEXc']\
/div/div[@class='navigation__3ozAB']/div[@class='buttonWrapper__2-lO0'][2]/button[@class='navi__DyQiA']/span"
# show the results
show_results_xpath = "/html[@class=' no-touchevents']/body/div[@id='app']/div/div[@class='wrapper__14ojg hs']\
/main[@class='content__259k1']/div[@class='someWrapper__oxPfx']/div[@class='content__3UVlg']/div[@class='card__1IEXc']\
/div[@class='buttonContainer__35HWF']/button[@class='big__1_aAh button__38IWe']/span"
# get the text that gives the best matching party
results_xpath = "/html[@class=' no-touchevents']/body/div[@id='app']/div/div[@class='wrapper__14ojg hs']\
/main[@class='content__259k1']/div[@class='footerNavWrapper__1VMEQ']/div[@class='content__1dQMM']/div[1]\
/div[@class='card__1IEXc']/h1[@class='title__ALq8l partyTitle__yQNfb']"
party_match_xpath = "/html[@class=' no-touchevents']/body/div[@id='app']/div/div[@class='wrapper__14ojg hs']\
/main[@class='content__259k1']/div[@class='footerNavWrapper__1VMEQ']/div[@class='content__1dQMM']\
/div[@class='card__1IEXc separate__1gwLc']/div/div[@class='wrapper__bn44K']/div[@class='recommendedParties__3NmiJ']"
party_match_party_xpath = "/span[@class='partyName__2810z']"
party_match_percentage_xpath = "/span[@class='partyResult__zoXJC']"

candidates_with_party_matches = []

for (ind, candidate) in enumerate(candidates):
    if candidate['districtId'] == 49:
        candidate['partyName'] = parties[candidate['partyId']]['name']
        id = candidate['id']
        description = ', '.join([candidate['firstName'], candidate['lastName'], parties[candidate['partyId']]['officialName'].lower()])
        print(ind, '( /', len(candidates), ')', id, description, end='')
        with urllib.request.urlopen(base_url + candidate_answer_dir + '/' + str(id)) as url:
            answers = json.loads(url.read().decode())['candidateAnswers']
            answers = {answer['questionId']: answer for answer in answers}
            initialise_machine()
            for question in range(1, 31):
                try_action_click(driver, choice_xpath + '[' + str(answers[question]["answer"]) + "]")
            try_action_click(driver, show_results_xpath)
            result = try_action_text(driver, results_xpath).split('sopivin puolue on ')[1]
            if result == parties[candidate['partyId']]['officialName'].lower():
                match = "(SAMA)"
            else:
                match = ""
            print(': koneen paras osuma', result, match)
            for party in range(1, 22):
                party_match = try_action_text(driver,  party_match_xpath + '[' + str(party) + ']'
                                              + party_match_party_xpath)
                party_match_percentage = try_action_text(driver, party_match_xpath + '[' + str(party) + ']'
                                                         + party_match_percentage_xpath)
                # print(party_match, int(party_match_percentage.split('%')[0]))
                candidate[party_match] = int(party_match_percentage.split('%')[0])
            candidates_with_party_matches += [candidate]

with open('../data/candidates.json', 'w') as candidates:
    json.dump(candidates_with_party_matches, candidates)


