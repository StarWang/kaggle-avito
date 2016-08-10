import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.cross_validation import KFold
from sklearn.metrics import roc_auc_score
from sklearn.svm import LinearSVC
from sklearn.externals import joblib

def saveModel(filename, clf):
    filename = 'model/' + filename
    joblib.dump(clf, filename)
    print ('output:', filename)

def loadModel(filename):
    filename = 'model/' + filename
    clf = joblib.load(filename)
    return clf


def crossValidate(X, y, n_estimators=20, max_depth=5):
    X, y = np.array(X), np.array(y)
    clf = RandomForestClassifier(n_estimators=n_estimators, n_jobs=-1, max_depth=max_depth, min_samples_split=1)
    kf = KFold(len(X), 5, shuffle=True, random_state=32)
    for train_index, test_index in kf:
        X_train = X[train_index]
        y_train = y[train_index]
        X_test = X[test_index]
        y_test = y[test_index]
        clf = clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        y_prob = clf.predict_proba(X_test)[:, 1]
        cm = confusion_matrix(y_test, y_pred)
        print ('accuracy:', (cm[0][0] + cm[1][1])/len(y_test))
        print ('auc:', roc_auc_score(y_test, y_prob))
        print ('confusion matrix:')
        print (cm)
    return clf.fit(X, y)

def predict(X, clf):
    X = np.array(X)
    return clf.predict_proba(X)[:, 1]
