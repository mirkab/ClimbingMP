
import requests
import json
import csv
import os.path

save_path = input('Output Location')
Northcomp = input('Northern Site Json')
Eastcomp = input('Eastern Site Json')
Southcomp = input('South Site Json')
Westcomp = input('West Site Json')
Centralcomp = input('Central Site Json')

headers = {'authorization': "Basic API Key Ommitted", 'accept': "application/json", 'accept': "text/csv"}

Ncomp = requests.get(Northcomp, headers=headers)
Ecomp = requests.get(Eastcomp, headers=headers)
Wcomp = requests.get(Southcomp, headers=headers)
Scomp = requests.get(Westcomp, headers=headers)
Ccomp = requests.get(Centralcomp, headers=headers)

# Write to .txt

NcompleteName = os.path.join(save_path, 'NorthSites.txt')
f = open(NcompleteName, 'a+')
f.write(Ncomp.text)
f.close()

print('North Sites complete')

EcompleteName = os.path.join(save_path, 'EasternSites.txt')
f = open(EcompleteName, 'a+')
f.write(Ecomp.text)
f.close()

print('Eastern Sites complete')

WcompleteName = os.path.join(save_path, 'WesternSites.txt')
f = open(WcompleteName, 'a+')
f.write(Wcomp.text)
f.close()

print('Western Sites complete')

ScompleteName = os.path.join(save_path, 'SouthernSites.txt')
f = open(ScompleteName, 'a+')
f.write(Scomp.text)
f.close()

print('Southern Sites complete')

CcompleteName = os.path.join(save_path, 'CentralSites.txt')
f = open(CcompleteName, 'a+')
f.write(Ccomp.text)
f.close()

print('Central Sites complete')

filenames = [NcompleteName, EcompleteName, WcompleteName, ScompleteName, CcompleteName]
mergeName = os.path.join(save_path, 'AllSite.txt')
with open(mergeName, 'w') as outfile:
    for names in filenames:
        with open(names) as infile:
            outfile.write(infile.read())
        outfile.write("\n")


print('Done')