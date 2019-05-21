import numpy as np
import urllib.request, json
import pandas as pd

matchfile = '../data/candidates.json'
base_url = 'https://www.vaalikone.fi/eduskunta2019'
party_dir = '/api/parties'

with open(matchfile) as file:
    candidates = json.load(file)

# fetch parties
with urllib.request.urlopen(base_url + party_dir) as url:
    parties = json.loads(url.read().decode())
parties = [party['name'] for party in parties]


with open('../data/partymatches.csv', 'w') as file:
    file.write(';'.join(['id', 'nimi', 'puolue'] + parties + ['oma_puolue']) + "\n")
    for (row, candidate) in enumerate(candidates):
        party_matches = [str(candidate[party]) if party in candidate else 'NaN' for party in parties]
        file.write(';'.join([str(candidate['id']), ' '.join([candidate['firstName'], candidate['lastName']]),
                             candidate['partyName']] + party_matches + [str(candidate[candidate['partyName']])]) + "\n")

