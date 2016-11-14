import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

path = 'requets_20160101_20161112_OPEN.csv'

surrey = pd.read_csv(path)

surrey = surrey[surrey["agency_responsible"] != "OTHER"]
surrey["agency_responsible_num"] = surrey["agency_responsible"].map(
    {'ROADS':0, 'LITTER/DUMPING':1, "SPECIMEN TREES":2, "TRAFFIC":3,  "GARBAGE":4, "NATURAL AREAS": 5, "STRUCTURES":6,
     "SECTORS": 7, "DRAINAGE": 8, "LANDSCAPE": 9 , "WATER":10, "TRANSPORTATION":11, "DESIGN&CONSTRUCTION":12, "SEWER":13,
     "LAND DEVELOPMENT": 14, "METERS":15 , "STLIGHTS":16, "UTILITIES":17, "ATHLETIC FIELDS":18, "GRAFFITI":19,  "PARKING":20  })

X = surrey["description"]
y = surrey["agency_responsible_num"]

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=2)

vect = CountVectorizer()

# fit and transform X_train into X_train_dtm
X_train_dtm = vect.fit_transform(X_train)

# transform X_test into X_test_dtm
X_test_dtm = vect.transform(X_test)

nb = MultinomialNB()
nb.fit(X_train_dtm, y_train)

intputtest = ["Playground Issue"]

simple_test_dtm = vect.transform(intputtest)

y_pred_class = nb.predict(simple_test_dtm)
print y_pred_class

