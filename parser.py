from geobr import read_municipality
import pandas as pd
import csv

# Read all municipalities in the country at a given year
#mun = read_municipality(code_muni="all", year=2018)
mun = pd.read_csv('mun.csv')
lista = mun.abbrev_state.unique()
print(mun.shape)
for i in lista:
    print(i)
    filtro = mun[mun.abbrev_state==i]
    filtro.to_csv(f'./geo/{i}.csv', index=False)
    print(filtro.shape)
#mun.to_csv('mun.csv', index=False)
# with open('eggs.csv', 'w', newline='') as csvfile:
#     spamwriter = csv.writer(csvfile,
#                             delimiter=' ',
#                             quotechar='|',
#                             quoting=csv.QUOTE_MINIMAL)
#     spamwriter.