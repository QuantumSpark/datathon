import pickle

from sklearn.externals import joblib

closedMap = {'ROADS':0, 'LITTER/DUMPING':1, "SPECIMEN TREES":2, "TRAFFIC":3,  "GARBAGE":4, "NATURAL AREAS": 5, "STRUCTURES":6,
       "SECTORS": 7, "DRAINAGE": 8, "LANDSCAPE": 9 , "WATER":10, "TRANSPORTATION":11, "DESIGN&CONSTRUCTION":12, "SEWER":13,
       "LAND DEVELOPMENT": 14, "METERS":15 , "STLIGHTS":16, "UTILITIES":17, "ATHLETIC FIELDS":18, "GRAFFITI":19,  "PARKING":20,
            "CROSSCUT":21, "TRSIGNAL":22, "BUILDING":23}
invClosedMap = {v: k for k, v in closedMap.items()}
def predict(input):
    restored_classifier = joblib.load('classifierClosed.pkl')
    input_array = []
    input_array.append(input)
    predicted = restored_classifier.predict(input_array)
    return invClosedMap.get(predicted[0])


