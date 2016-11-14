import json
import csv

with open ("datathon/surrey_api/data/requests_20160101_20161112_OPEN.json", "r") as myfile:
    x=str(myfile.read().replace('\n', ''))
x = json.loads(x)
print(x)
f = csv.writer(open("requets_20160101_20161112_OPEN.csv", "wb+"))


f.writerow(["description", "agency_responsible"])

for x in x:
    f.writerow([x["description"],
                x["agency_responsible"]])
