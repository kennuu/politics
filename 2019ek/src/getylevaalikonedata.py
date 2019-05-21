from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import re, time
import numpy as np
import urllib.request, json
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

def initialise_machine(base_url):
    driver = webdriver.Safari()
    driver.get(base_url)
    time.sleep(0.2)
    return driver

def try_action_click(driver, xpath):
    # action = ActionChains(driver)
    maxtries = 10
    tries = 0
    success = False
    while not success and tries < maxtries:
        try:
            # action.move_to_element(driver.find_element_by_xpath(xpath)).perform()
            driver.find_element_by_xpath(xpath).click()
            success = True
        except Exception as e:
            if tries > 3:
                print("Server too slow, waiting")
            tries += 1
            time.sleep(0.2)
    # if tries >= maxtries:
    #     print("Failing to get data with XPATH", xpath, ". Returning error code")
    return success

def try_action_text(driver, xpath, maxtries = 10):
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
        return ''

def try_action_text_scroll(driver, xpath, maxtries = 10):
    currpos = 0
    success = False
    text = 'na'
    while not success:
        try:
            text = driver.find_element_by_xpath(xpath).text
            success = True
        except Exception as e:
            currpos += 200
            script = "window.scrollTo(0, " + str(currpos) + ");"
            driver.execute_script(script)
            time.sleep(0.2)
    return text

base_url = 'https://vaalikone.yle.fi/eduskuntavaali2019/ehdokkaat?lang=fi-FI'
xpath_candidate_link_beg = "/html/body/div[@id='root']/main/div[@class='constituencyroute__MainWrapper-sc-1cmvtcm-0 bBopNv']\
                        /div[@class='candidatespage__Container-lc4j1t-1 gbJZop']/div[3]/div[1]\
                        /div[@class='ReactVirtualized__Grid ReactVirtualized__List']/div\
                        [@class='ReactVirtualized__Grid__innerScrollContainer']/div"
xpath_candidate_link_end = "/section[@class='ResultCard-b3imyv-4 dWctTj card__Card-jgylk6-1 kZXFax']\
                        /div[@class='ResultCard__InfoRow-b3imyv-1 gXVvhG']\
                        /div[@class='ResultCard__InfoColumn-b3imyv-3 buutWZ']/a[2]"
xpath_name = "/html/body/div[@id='root']/main/div[@class='constituencyroute__MainWrapper-sc-1cmvtcm-0 bBopNv']\
              /div[@class='candidatepage__Container-tjvm5y-10 kvZixK']/section[@class='card__Card-jgylk6-1 kZXFax']\
              /div[@class='candidatepage__InfoRow-tjvm5y-4 hqqHCT'][1]/div[@class='candidatepage__InfoColumn-tjvm5y-3 MiRea'][1]/h1"
# xpath_answer_text = "/html/body/div[@id='root']/main/div[@class='constituencyroute__MainWrapper-sc-1cmvtcm-0 bBopNv']\
#                      /div[@class='candidatepage__Container-tjvm5y-10 kvZixK']\
#                      /article[@class='candidatepage__Category-tjvm5y-9 dwycKX'][1]\
#                      /section[@class='AnswersCard__AnswerCard-sc-1gm55j5-9 cavSFX card__Card-jgylk6-1 kmYdWT']\
#                      /div[@class='AnswersCard__CardContent-sc-1gm55j5-8 iCFovP']/div[@class='AnswersCard__Explabox-sc-1gm55j5-1 bsFLmK']"
xpath_answer_text = "/html/body/div[@id='root']/main/div[@class='constituencyroute__MainWrapper-sc-1cmvtcm-0 bBopNv']\
                    /div[@class='candidatepage__Container-tjvm5y-10 kvZixK']/article[@class='candidatepage__Category-tjvm5y-9 dwycKX']\
                    [1]/section[@class='AnswersCard__AnswerCard-sc-1gm55j5-9 cavSFX card__Card-jgylk6-1 kmYdWT']\
                    /div[@class='AnswersCard__CardContent-sc-1gm55j5-8 iCFovP']\
                    /div[@class='AnswersCard__Explabox-sc-1gm55j5-1 hXgmpT']"
xpath_party = "/html/body/div[@id='root']/main/div[@class='constituencyroute__MainWrapper-sc-1cmvtcm-0 bBopNv']\
                /div[@class='candidatepage__Container-tjvm5y-10 kvZixK']/section[@class='card__Card-jgylk6-1 kZXFax']\
                /div[@class='candidatepage__InfoRow-tjvm5y-4 hqqHCT'][1]\
                /div[@class='candidatepage__InfoColumn-tjvm5y-3 MiRea'][1]\
                /a[@class='PartyPill-sc-4kyu6g-1 ssTZD PartyPill__Pill-sc-4kyu6g-0 lnFpFR']"

# load meps
party_shorts = {'Suomen Sosialidemokraattinen Puolue': 'SDP',
                'Perussuomalaiset': 'PS',
                'Kansallinen Kokoomus': 'KOK',
                'Suomen Keskusta': 'KESK',
                'Vihreä liitto': 'VIHR',
                'Vasemmistoliitto': 'VAS',
                'Suomen ruotsalainen kansanpuolue': 'RKP',
                'Suomen Kristillisdemokraatit (KD)': 'KD'
                }

meps = pd.read_csv('../data/valitut.csv', index_col=0)
meps = meps[meps.party !='Muut ryhmät']
meps.party = [party_shorts[x.party] for x in meps.itertuples() if 'Muut ryhmät' not in x.party]
meps['name and party'] = meps.name + ' ' + meps.party

driver = webdriver.Safari()

candidate_numbers = list(range(70, 3000))
found_candidates = []
candidate_answers = []
candidates_found = 0
meps_found = 0
for section in range(1, 20):
    for cand in found_candidates:
        candidate_numbers.pop(cand)
    found_candidates = []
    for ind, id in enumerate(candidate_numbers):
        print(section, id, end = ' ')
        try:
            driver.get('https://vaalikone.yle.fi/eduskuntavaali2019/' + str(section) + '/ehdokkaat/' + str(id) + '?lang=fi-FI')
            time.sleep(0.2)
            name = try_action_text(driver, xpath_name, 1)
            party = try_action_text(driver, xpath_party, 1).upper().replace('.', '')
            if name != '':
                if name == 'Juhana Vartiainen':
                    print('tähän')
                names = name.split()
                name = names[-1] + ', ' + ' '.join(names[:-1])
                name_and_party = name + ' ' + party
                found_candidates += [ind]
                candidates_found += 1
                print('(', candidates_found, ', ', meps_found, ') ', end=' ')
                if  name_and_party in list(meps['name and party']):
                    meps_found += 1
                    answer_text = try_action_text(driver, xpath_answer_text, 1)
                    print(name, party, answer_text)
                    candidate_answers.append({'party': party, 'name': name, 'answer 1': answer_text})
                else:
                    print(name_and_party, 'ei valittu kansanedustajaksi')
            else:
                print()
        except:
            print('no data found')
            pass

with open('../data/candidate_text_answer.json', 'w') as out:
    json.dump(candidate_answers, out)