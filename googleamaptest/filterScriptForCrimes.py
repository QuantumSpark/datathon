import pandas as pd;

df = pd.read_csv('/Users/QuantumSpark/Developer/timagesopendataarchivescsvmonthlycrime2016.csv')

df = df[df["INCIDENT_TYPE"] == "Fatal/Injury Collision"]
df.to_csv("/Users/QuantumSpark/Developer/filtered2016.csv", sep='\t', encoding='utf-8')
