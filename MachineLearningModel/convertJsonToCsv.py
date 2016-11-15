import json
import csv

inputJsonPathOpen =   "datathon/surrey_api/data/requests_20160101_20161112_OPEN.json"
inputJsonPathClosed = "datathon/surrey_api/data/requests_20160101_20161112_CLOSED.json"


outputCsvPathOpen =   "request_20160101_20161112_OPEN.csv"
outputCsvPathClosed = "request_20160101_20161112_CLOSED.csv"

def convertJsonToCsv(inputJsonPath, outputCsvPath):
    with open (inputJsonPath, "r") as myfile:
        x=str(myfile.read().replace('\n', ''))
    x = json.loads(x)

    f = csv.writer(open(outputCsvPath, "wb+"))


    f.writerow(["description", "agency_responsible"])

    for x in x:
        f.writerow([x["description"],
                    x["agency_responsible"]])
