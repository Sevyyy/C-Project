# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import pandas as pd
from sklearn import ensemble
from sklearn import cross_validation
from sklearn.naive_bayes import GaussianNB
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn import grid_search
from nltk.stem import WordNetLemmatizer
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report
import sklearn.metrics
from sklearn.feature_extraction.text import TfidfVectorizer
import xgboost as xgb
import re

train = pd.read_json('train.json')
train['ingredients_string'] = [' '.join([WordNetLemmatizer().lemmatize(re.sub('[^A-Za-z]', ' ', line)) for line in lists]).strip() for lists in train['ingredients']]
test = pd.read_json('test.json')
test['ingredients_string'] = [' '.join([WordNetLemmatizer().lemmatize(re.sub('[^A-Za-z]', ' ', line)) for line in lists]).strip() for lists in test['ingredients']]

traincorpus = train['ingredients_string']
vectorizertr = TfidfVectorizer(stop_words='english',
                             ngram_range = ( 1 , 1 ),analyzer="word", 
                             max_df = .57 , binary=False , token_pattern=r'\w+' , sublinear_tf=False)
tfidftr = vectorizertr.fit_transform(traincorpus)
testcorpus = test['ingredients_string']
vectorrizerts = TfidfVectorizer(stop_words='english')
tfidfts = vectorizertr.transform(testcorpus)
predictors_tr = tfidftr
targets_tr = train['cuisine']
predictors_ts = tfidfts
print 'Begin predict'

####################################
##                                ##
## grid_search+logisticregression ##
##                                ##
####################################
parameters = {'C':[1, 20]}
clf = LogisticRegression()
classifier = grid_search.GridSearchCV(clf, parameters)
print 'Fitting'
classifier=classifier.fit(predictors_tr,targets_tr)
print 'predicting'
predictions=classifier.predict(predictors_ts)
testdf['cuisine'] = predictions

testdf[['id' , 'cuisine' ]].to_csv("submission.csv")

###################################
##                               ##
##  adaboost+logisticregression  ##
##                               ##
###################################

clf_lr = LogisticRegression(solver = 'lbfgs')
clf_ab = AdaBoostClassifier(clf_lr, learning_rate = 0.6)

print 'Fitting'
clf_ab = clf_ab.fit(predictors_tr.toarray(), targets_tr)

print 'Predictting'
predictions = clf_ab.predict(predictors_ts.toarray())
test['cuisine'] = predictions
test[['id','cuisine']].to_csv('ans.csv', index = False)

###################################
##                               ##
##             svm               ##
##                               ##
###################################
classifier = svm.SVC(kernel = 'rbf', C = 100)

print 'Fitting'
classifier=classifier.fit(predictors_tr,targets_tr)
print 'predicting'
predictions=classifier.predict(predictors_ts)
testdf['cuisine'] = predictions

testdf[['id' , 'cuisine' ]].to_csv("submission.csv")

###################################
##                               ##
##          naive_bayes          ##
##                               ##
###################################
print 'Fitting'
clf = GaussianNB()
clf = clf.fit(predictors_tr.toarray(), targets_tr)
print 'predicting'
predictions = clf.predict(predictors_ts.toarray())
test['cuisine'] = predictions
test[['id','cuisine']].to_csv('ans_by.csv', index = False)

###################################
##                               ##
##         GradientBoost         ##
##                               ##
###################################
print 'Fitting'
clf = ensemble.GradientBoostingClassifier()
clf = clf.fit(predictors_tr.toarray(), targets_tr)
print 'predicting'
predictions = clf.predict(predictors_ts.toarray())
test['cuisine'] = predictions
test[['id','cuisine']].to_csv('ans.csv', index = False)

###################################
##                               ##
##         random forest         ##
##                               ##
###################################
print 'Fitting'
clf = RandomForestClassifier(n_estimators = 100)
clf = clf.fit(predictors_tr.toarray(), targets_tr)
print 'Predictting'
predictions = clf.predict(predictors_ts.toarray())
test['cuisine'] = predictions
test[['id','cuisine']].to_csv('ans.csv', index = False)

###################################
##                               ##
##            xgboost            ##
##                               ##
###################################
print 'Fitting'
clf = xgb.XGBClassifier()
print 'Predictting'
clf.fit(predictors_tr,targets_tr)
test['cuisine'] = clf.predict(predictors_ts)
test[['id','cuisine' ]].to_csv("ansxgb.csv")

###################################
##                               ##
##         decision tree         ##
##                               ##
###################################
print 'Fitting'
clf = DecisionTreeClassifier()
clf = clf.fit(predictors_tr.toarray(), targets_tr)
print 'predicting'
predictions = clf.predict(predictors_ts.toarray())
test['cuisine'] = predictions
test[['id','cuisine']].to_csv('ans_by.csv', index = False)