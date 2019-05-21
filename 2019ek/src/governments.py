import pandas as pd
import numpy as np
from itertools import combinations
import json

desired_width = 1000
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', None)

party_shorts = {'Suomen Sosialidemokraattinen Puolue': 'SDP',
                'Perussuomalaiset': 'PS',
                'Kansallinen Kokoomus': 'KOK',
                'Suomen Keskusta': 'KESK',
                'Vihreä liitto': 'VIHR',
                'Vasemmistoliitto': 'VAS',
                'Suomen ruotsalainen kansanpuolue': 'RKP',
                'Suomen Kristillisdemokraatit (KD)': 'KD'
                }

party_shorts2 = {'RKP':'RKP',
                  'SDP': 'SDP',
                  'Vihreät': 'VIHR',
                  'Keskusta': 'KESK', 'Perussuomalaiset': 'PS', 'Kristillisdemokraatit': 'KD',
                  'Vasemmistoliitto': 'VAS', 'Kokoomus':'KOK'}

meps = pd.read_csv('../data/valitut.csv', index_col = 0)

seats = meps.groupby('party')['party'].count().sort_values(ascending=False).drop('Muut ryhmät')

print(seats)

parties = seats.keys()
parties = [party_shorts[x] for x in parties]

possible_combs = []
for ingov in range(3, 7):
    combs = combinations(range(len(parties)), ingov)
    possible_combs += list(combs)

possible_governments = []
seat_limit = 110
for comb in possible_combs:
    total_seats = int(sum([seats[x] for x in comb]))
    if total_seats > seat_limit:
        ingov_parties = [parties[x] for x in comb]
        possible_governments.append({'parties': ingov_parties, 'seats': total_seats})

print(f'{len(possible_governments)} mahdollista enemmistöhallitusta')

# with open('../data/possible_governments.json', 'w') as out:
#     json.dump(possible_governments, out)

candidate_answers = pd.read_csv('../data/yle_2019_factored.csv', sep=';', decimal=',').iloc[:, [1, 2, -2, -1]]
candidate_answers.columns = [candidate_answers.columns[0]] + ['valitaan'] + list(candidate_answers.columns[2:])

candidate_answers = candidate_answers[candidate_answers['valitaan'] == 1]
candidate_answers = candidate_answers[candidate_answers['puolue'] != 'Sitoutumaton']
candidate_answers = candidate_answers[candidate_answers['puolue'] != 'Liike Nyt']

parties = candidate_answers['puolue']
parties = [party_shorts2[x] for x in parties]

candidate_answers['puolue'] = parties

PA1 = candidate_answers['PA1'].copy()
candidate_answers['PA1'] = candidate_answers['PA2']
candidate_answers['PA2'] = -PA1

# party means
party_means = candidate_answers.groupby(by='puolue').mean()
party_means['puolue'] = party_means.index

for gov in possible_governments:
    gov_members = candidate_answers[candidate_answers['puolue'].isin(gov['parties'])]
    gov['PA1_mean'] = gov_members.iloc[:, -2].mean()
    gov['PA2_mean'] = gov_members.iloc[:, -1].mean()
    gov['PA1_std'] = gov_members.iloc[:, -2].std()
    gov['PA2_std'] = gov_members.iloc[:, -1].std()
    gov['std_norm'] = np.linalg.norm(np.array(gov_members.iloc[:, -2:].std()))
    gov['disttoSDP'] = np.linalg.norm(np.array([gov['PA1_mean'], gov['PA2_mean']]) -
                                           np.array([party_means['PA1']['SDP'], party_means['PA2']['SDP']]))

    gov_c_members = party_means[party_means['puolue'].isin(gov['parties'])]
    gov['PA1_c_mean'] = gov_c_members.iloc[:, -3].mean()
    gov['PA2_c_mean'] = gov_c_members.iloc[:, -2].mean()
    gov['PA1_c_std'] = gov_c_members.iloc[:, -3].std()
    gov['PA2_c_std'] = gov_c_members.iloc[:, -2].std()
    gov['std_c_norm'] = np.linalg.norm(np.array(gov_c_members.iloc[:, -3:-2].std()))

possible_governments = pd.DataFrame(possible_governments).sort_values('std_norm')
print(possible_governments)
possible_governments['c_order'] = np.argsort(np.array(possible_governments['std_c_norm']))
print(possible_governments)

# print(possible_governments.head(50))

candidate_answers.to_csv('../data/yle_2019_mep_factors.csv')
possible_governments.to_csv('../data/yle_2019_governments.csv')