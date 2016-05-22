__author__ = 'prashantravi'
import numpy as np
from sklearn.svm import SVC
from sklearn import cross_validation
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.externals import joblib
from sklearn.preprocessing import LabelEncoder
from itertools import chain
from preprocess import transformTweetData
from readData import getSumVectors
from readData import DataModel
from readData import getFeatures
from postprocess import author_constraints
import pandas as pd


def learn(currentDataset, topic):
        le = LabelEncoder()
        mapping = {"+1": +1, "-1": -1}
        le.fit([mapping[model.stance] for model in currentDataset])

        data = list(map(transformTweetData, currentDataset))
        classes = le.transform([mapping[model.stance] for model in currentDataset])
        #print set(classes)

        feature_array = np.asarray(getFeatures(data))

        class_array = np.asarray(classes)

        #print feature_array.shape, class_array.shape
        #print le.classes_

        skf = cross_validation.KFold(len(currentDataset), n_folds=5, shuffle=False,
                               random_state=None)
        idx = 0
        average_accuracy = np.zeros(5)
        average_f1 = np.zeros(5)

        for train, test in skf:
            clf = SVC(kernel="linear",gamma= 3.0, C= 0.56, shrinking= True, probability=True,class_weight='auto')

            X_train = feature_array[np.array(train)]
            Y_train = class_array[np.array(train)]

            X_test = feature_array[np.array(test)]
            Y_test = class_array[np.array(test)]

            clf.fit(X_train, Y_train)
            #predict = clf.predict(X_test)
            predict = author_constraints(clf, X_test,test, currentDataset, topic);

            print "Fold /", idx + 1, ", Training Set /", Y_train.shape, " ", np.sum(Y_train), ", Test Set /", Y_test.shape, " ", np.sum(Y_test)
            #print predict;

            y_actu = pd.Series(Y_test, name='Actual')
            y_pred = pd.Series(predict, name='Predicted')
            df_confusion = pd.crosstab(y_actu, y_pred)

            print df_confusion
            print metrics.accuracy_score(Y_test, predict), metrics.f1_score(Y_test, predict)

            average_accuracy[idx] = metrics.accuracy_score(Y_test, predict)
            average_f1[idx] = metrics.f1_score(Y_test, predict)
            idx += 1


        print "Average Accuracy =", np.mean(average_accuracy)
        print "Average F-1 =", np.mean(average_f1)
        target_short = topic
        joblib.dump(le, "SavedModels/Part1_VectorSumLabelEncoder_Target_" + target_short + ".pkl")
        joblib.dump(clf,"SavedModels/Part1_VectorSum_Target_" + target_short + ".pkl")
        joblib.dump(X_test, "SavedModels/" + target_short + "X_test.pkl");
        joblib.dump(Y_test, "SavedModels/" + target_short + "Y_test.pkl");
        joblib.dump(train,"SavedModels/" + target_short + "trainRange.pkl");
        joblib.dump(test, "SavedModels/" + target_short + "testRange.pkl");
        joblib.dump(X_test, "SavedModels/" + target_short + "X_test.pkl");
        joblib.dump(currentDataset, "SavedModels/" + target_short + "CurrDataSet.pkl");


def predict(sentence, topic):
    currentDataset = [];
    currentDataset.append(DataModel(None, None, None,None, None, None, sentence));
    data = list(map(transformTweetData, currentDataset))
    feature_array = np.asarray([getSumVectors(d) for d in data])
    clf = joblib.load("SavedModels/Part1_VectorSum_Target_" + topic + ".pkl");
    le = joblib.load("SavedModels/Part1_VectorSumLabelEncoder_Target_" + topic + ".pkl")
    print le.classes_
    X_test = feature_array;
    predict = clf.predict(X_test)
    print clf.predict_proba(X_test);
    print predict;
    print 'done';
