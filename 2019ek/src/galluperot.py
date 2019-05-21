import numpy as np

gallup = [18.7, 17.1, 16.9, 12.8, 12.7, 8.3]
parties = np.array(['PS', 'KOK', 'SDP', 'VIHR', 'KESK', 'VAS'])

vm = 2.8
orders = set()
for p1 in np.arange(gallup[0] - vm, gallup[0] + vm, vm):
    for p2 in np.arange(gallup[1] - vm, gallup[1] + vm, vm):
        for p3 in np.arange(gallup[2] - vm, gallup[2] + vm, vm):
            for p4 in np.arange(gallup[3] - vm, gallup[3] + vm, vm):
                for p5 in np.arange(gallup[4] - vm, gallup[4] + vm, vm):
                    for p6 in np.arange(gallup[5] - vm, gallup[5] + vm, vm):
                        order = np.argsort([p1, p2, p3, p4, p5, p6])[::-1]
                        orders.add(' '.join(parties[order]))

print(len(orders))
for order in orders:
    print(order)
