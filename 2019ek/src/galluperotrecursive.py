import numpy as np

vm = 2.8
gallup = [18.7, 17.1, 16.9, 12.8, 12.7, 8.3]
# gallup = [0, 10, 20, 30, 40, 50]
parties = np.array(['PS', 'KOK', 'SDP', 'VIHR', 'KESK', 'VAS'])

orders = set()

def addalternative(orders, parties, baselines, errormargin, result = []):
    try:
        baseline = baselines.pop(0)
    except:
        print('baselines should always have items')
        exit(-1)
    for support in np.arange(baseline - errormargin, baseline + errormargin, errormargin):
    # for support in range(baseline, baseline + 3):
        result.append(support)
        if len(result) == len(parties):
            # print(result)
            orders.add(' '.join(parties[np.argsort(result)[::-1]]))
            result.pop()
        else:
            addalternative(orders, parties, baselines, errormargin, result)
    # FIXME: when to append, and pop
    if result != []:
        baselines.insert(0, baseline)
        result.pop()

addalternative(orders, parties, gallup, vm)

orders2 = np.array([x for x in orders])

largest = {}
oldp = ''
oldi = -1
for i, order in enumerate(np.sort(orders2)):
    p = order.split()[0]
    if p != oldp:
        if oldp != '':
            largest[oldp] = i - oldi
        oldi = i
        oldp = p
    print(i, order)
largest[oldp] = i + 1 - oldi

print(len(orders))
print(largest)
