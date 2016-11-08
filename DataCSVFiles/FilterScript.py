import pandas as pd;

df = pd.read_csv('CrimesData/monthlycrime2016.csv')

df = df[df["INCIDENT_TYPE"] == "Fatal/Injury Collision"]
df.to_csv("FilteredCrimeData/filtered2016.csv", sep='\t', encoding='utf-8')