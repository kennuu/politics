import json
import pandas as pd

candidatefile = '../data/candidateanswers.json'


with open(candidatefile) as file:
    candidates = json.load(file)

vihreat = set()
with open('../data/vihreat') as target:
    for line in target:
        vihreat.add(line.rstrip())

indata = set()
for candidate in candidates:
    if candidate['lastName'] + ' ' + candidate['firstName'] in vihreat:
        print(candidate['lastName'], candidate['firstName'], candidate['answers'][9])
        indata.add(candidate['lastName'] + ' ' + candidate['firstName'])

print(vihreat.difference(indata))