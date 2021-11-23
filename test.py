import random

def transposta(lista):
    return list(map(list, zip(*lista))) 

m1 = 3
n1 = 4
m2 = 4
n2 = 2

n = 10

A = []

for i in range(m1):
    A.append([random.randint(0, n) for i in range(n1)])

B = []

for i in range(m2):
    B.append([random.randint(0, n) for i in range(n2)])

trans_B = transposta(B)
prod = []
for row in A:
    aux = []
    
    for rowt in trans_B:
        elem = sum([row[i]*rowt[i] for i in range(len(row))])
        aux.append(elem)
    prod.append(aux)

import numpy as np

prod = np.dot(A, B)