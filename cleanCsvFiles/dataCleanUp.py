import pandas as pd
import time

collisionAllYears = []


def read_concatenate_csv():
    for i in range(1, 7):
        df = pd.read_csv("originalCsvFiles/collisionCsvFiles/collision201" + str(i) + ".csv")
        collisionDataFrame = pd.DataFrame(df[df.INCIDENT_TYPE == "Fatal/Injury Collision"])
        collisionAllYears.append(collisionDataFrame)


read_concatenate_csv()
dataFrameAllYears = pd.concat(collisionAllYears)
dataFrameAllYears.to_csv("crimeAllYears.csv", encoding='utf-8', index=False)