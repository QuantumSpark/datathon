import pandas as pd;

df = pd.read_csv('DataCSVFiles/CrimesData/nevercrime2015.csv')

df = df[df["INCIDENT_TYPE"] == "Fatal/Injury Collision"]
df.to_csv("DataCSVFiles/FilteredCrimeData/filtered2016.csv", sep='\t', encoding='utf-8')
