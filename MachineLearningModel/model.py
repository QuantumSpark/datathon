import pandas as pd
import numpy
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics

pathForOpen = 'request_20160101_20161112_OPEN.csv'
pathForClosed = 'request_20160101_20161112_CLOSED.csv'

openMap  =  {'ROADS':0, 'LITTER/DUMPING':1, "SPECIMEN TREES":2, "TRAFFIC":3,  "GARBAGE":4, "NATURAL AREAS": 5, "STRUCTURES":6,
        "SECTORS": 7, "DRAINAGE": 8, "LANDSCAPE": 9 , "WATER":10, "TRANSPORTATION":11, "DESIGN&CONSTRUCTION":12, "SEWER":13,
        "LAND DEVELOPMENT": 14, "METERS":15 , "STLIGHTS":16, "UTILITIES":17, "ATHLETIC FIELDS":18, "GRAFFITI":19,  "PARKING":20  }
invOpenMap = {v: k for k, v in openMap.iteritems()}

closedMap = {'ROADS':0, 'LITTER/DUMPING':1, "SPECIMEN TREES":2, "TRAFFIC":3,  "GARBAGE":4, "NATURAL AREAS": 5, "STRUCTURES":6,
        "SECTORS": 7, "DRAINAGE": 8, "LANDSCAPE": 9 , "WATER":10, "TRANSPORTATION":11, "DESIGN&CONSTRUCTION":12, "SEWER":13,
        "LAND DEVELOPMENT": 14, "METERS":15 , "STLIGHTS":16, "UTILITIES":17, "ATHLETIC FIELDS":18, "GRAFFITI":19,  "PARKING":20,
             "CROSSCUT":21, "TRSIGNAL":22, "BUILDING":23}
invClosedMap = {v: k for k, v in closedMap.iteritems()}

def predictCategoryOpen(inputString):
    surrey = pd.read_csv(pathForOpen)
    print "Open has this many data: " + str(surrey["agency_responsible"].size)
    surrey = surrey[surrey["agency_responsible"] != "OTHER"]
    surrey["agency_responsible_num"] = surrey["agency_responsible"].map(openMap)

    X = surrey["description"]
    y = surrey["agency_responsible_num"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

    vect = CountVectorizer()

    # fit and transform X_train into X_train_dtm
    X_train_dtm = vect.fit_transform(X_train)

    # transform X_test into X_test_dtm
    X_test_dtm = vect.transform(X_test)

    nb = MultinomialNB()
    nb.fit(X_train_dtm, y_train)

    intputStringAsArray = [inputString]

    input_String_dtm = vect.transform(intputStringAsArray)

    predictedNum = nb.predict(input_String_dtm)

    # make class predictions for X_test_dtm
    y_pred_class = nb.predict(X_test_dtm)


    # calculate accuracy of class predictions
    print "Accuracy score for open Request: " + str(metrics.accuracy_score(y_test, y_pred_class))

    print "Weighted f1_score for open Request:  " + str(metrics.f1_score(list(y_test),y_pred_class ,average='weighted'))
    return invOpenMap.get(predictedNum[0])



def predictCategoryClosed (inputString):
    surrey = pd.read_csv(pathForClosed)
    print "Closed has this many data: " +  str(surrey["agency_responsible"].size)
    surrey["agency_responsible_num"] = surrey["agency_responsible"].map(closedMap)
    surrey = surrey[~numpy.isnan(surrey["agency_responsible_num"])]
    X = surrey["description"]
    y = surrey["agency_responsible_num"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

    vect = CountVectorizer()

    # fit and transform X_train into X_train_dtm

    X_train_dtm = vect.fit_transform(X_train)

    # transform X_test into X_test_dtm
    X_test_dtm = vect.transform(X_test)

    nb = MultinomialNB()
    nb.fit(X_train_dtm, y_train)

    intputStringAsArray = [inputString]

    input_String_dtm = vect.transform(intputStringAsArray)

    predictedNum = nb.predict(input_String_dtm)

    # make class predictions for X_test_dtm
    y_pred_class = nb.predict(X_test_dtm)


    # calculate accuracy of class predictions
    print "Accuracy score for Closed Request : " + str(metrics.accuracy_score(y_test, y_pred_class))

    print "Weighted f1_score for Closed Request : " + str(metrics.f1_score(list(y_test),y_pred_class ,average='weighted'))
    return invClosedMap.get(predictedNum[0])


print predictCategoryOpen("Notification of Missed Pick-Up")
print predictCategoryClosed("Notification of Missed Pick-Up")

