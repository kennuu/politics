import pandas as pd

chosen = []
parties = []

def extractfields(line):
    fields = [s.strip() for s in line.split(' ') if s]
    anchor = fields.index('vaalipiiri')
    district = ' '.join(fields[anchor-1:anchor+1])
    name = ' '.join(fields[:anchor-1])
    votes = fields[anchor + 2]
    return [name, district, votes]

with open('../data/valitut.txt', encoding='latin-1') as file:
    line = ''
    while 'Vaalipiireittäin' not in line:
        line = file.readline()

    while line != "\n":
        line = file.readline()
        # print(line)
        if ']' in line:
            parties.append(line.rstrip().split(']')[1])

    while parties:
        print('finding next party')
        while parties[0] not in line:
            line = file.readline()
        party = parties.pop(0)
        print("########## " + party + " ###########")
        print('finding the beginning of the list for this party')
        while not 'Vertausluku' in line:
            line = file.readline()
        for line in file:
            print(line)
            if 'Varalla' in line:
                print('found all the chosen ones for this party')
                break
            try:
                fields = extractfields(line)
            except:
                # print('some error')
                # print(line)
                pass
            chosen.append([party] + fields)

chosen = pd.DataFrame(chosen, columns=['party', 'name', 'district', 'votes'])

chosen.to_csv('../data/valitut.csv')