import pandas as pd
import numpy as np
import sys
import pickle

from sklearn.externals import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
from sklearn.datasets import load_files
from sklearn.cross_validation import train_test_split
from sklearn import metrics


surrey = pd.read_csv("requestsClosed2016.csv")

surrey["agency_responsible_num"] = surrey["agency_responsible"].map(
     {'ROADS':0, 'LITTER/DUMPING':1, "SPECIMEN TREES":2, "TRAFFIC":3,  "GARBAGE":4, "NATURAL AREAS": 5, "STRUCTURES":6,
            "SECTORS": 7, "DRAINAGE": 8, "LANDSCAPE": 9 , "WATER":10, "TRANSPORTATION":11, "DESIGN&CONSTRUCTION":12, "SEWER":13,
            "LAND DEVELOPMENT": 14, "METERS":15 , "STLIGHTS":16, "UTILITIES":17, "ATHLETIC FIELDS":18, "GRAFFITI":19,  "PARKING":20,
                 "CROSSCUT":21, "TRSIGNAL":22, "BUILDING":23})
 

surrey = surrey[~np.isnan(surrey["agency_responsible_num"])]
x = surrey["description"]
y = surrey["agency_responsible_num"]

# split the dataset in training and test set:
docs_train, docs_test, y_train, y_test = train_test_split(
    x, y,   test_size=0.25, random_state=None)

# TASK: Build a vectorizer / classifier pipeline that filters out tokens
# that are too rare or too frequent
pipeline = Pipeline([
    ('vect', TfidfVectorizer(min_df=3, max_df=0.95)),
    ('clf', LinearSVC(C=1000)),
])

# TASK: Build a grid search to find out whether unigrams or bigrams are
# more useful.
# Fit the pipeline on the training set using grid search for the parameters
parameters = {
    'vect__ngram_range': [(1, 1), (1, 2)],
}
grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1)
grid_search.fit(docs_train, y_train)

# TASK: print the cross-validated scores for the each parameters set
# explored by the grid search
print(grid_search.grid_scores_)

# TASK: Predict the outcome on the testing set and store it in a variable
# named y_predicted
y_predicted = grid_search.predict(docs_test)

# Print the classification report
print(metrics.classification_report(y_test, y_predicted))

# Print and plot the confusion matrix
#cm = metrics.confusion_matrix(y_test, y_predicted)
#print(cm)

#import matplotlib.pyplot as plt
#plt.matshow(cm)
#plt.show()

saved_classifier = pickle.dumps(grid_search)
joblib.dump(grid_search, 'mysentiment-classifier.pkl')

# Predict the result on some short new sentences:
sentences = [
     u'Notification of Missed Pick-Up',
     u'Notification of Sidewalk, Curb or Letdown Problem',
     u'Notification of Roadside Dumping',
     u'Parks Other Issue',
]

#pickle.loads(saved_classifier)
restored_classifier = joblib.load('classifier.pkl')

predicted = restored_classifier.predict(sentences)
print (predicted)

# for s, p in zip(sentences, predicted):
#     print(u'The sentiment of "%s" is "%s"' % (s, dataset.target_names[p]))

 



