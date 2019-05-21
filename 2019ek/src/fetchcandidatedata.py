import urllib.request, json, os

print(os.getcwd())


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

for (ind, candidate) in enumerate(candidates):
    candidate['partyName'] = parties[candidate['partyId']]['name']
    id = candidate['id']
    description = ', '.join(
    [candidate['firstName'], candidate['lastName'], parties[candidate['partyId']]['officialName'].lower()])
    print(ind, '( /', len(candidates), ')', id, description)
    with urllib.request.urlopen(base_url + candidate_answer_dir + '/' + str(id)) as url:
        answers = json.loads(url.read().decode())['candidateAnswers']
    candidates[ind]['answers'] = answers

with open('../data/candidateanswers.json', 'w') as out:
    json.dump(candidates, out)