# Import PuLP modeler functions
from pulp import *
from sklearn.externals import joblib
from sklearn import metrics
import pandas as pd
import numpy as np

pathToAuthors = "/Users/prashantravi/Desktop/StanceClassification/data/authors"

def author_constraints(clf, X_test,test, currentDataSet,topic):

    #load author map
    pathToFile = pathToAuthors + '/' + topic;
    authorMap = {}
    for filename in os.listdir(pathToFile):
        f = open(pathToFile + '/' + filename, 'r');
        metadata = f.read();
        for info in metadata.split('\n'):
            meta = info.split(None, 1);
            if(len(meta)==2):
                authorMap[meta[0]] = meta[1];
    #print authorMap
    #print authorMap;
    # create the LP object, set up as a maximization problem
    prob = pulp.LpProblem('AuthorConstraints', pulp.LpMaximize)
    # set up the decision varaible for each of the training sets
    x = [None] * len(X_test);
    for i in range(len(X_test)):
        x[i] = pulp.LpVariable('(x'+ str(i)+ ')', lowBound=0,upBound=1, cat='Integer')

    sumOverX = 0;
    for i in range(len(X_test)):
        tmp = clf.predict_proba(X_test[i])[0][1];
        sumOverX = sumOverX + x[i]*tmp  + (1-tmp)*(1-x[i]);

    prob += sumOverX

    done = {}
    for i in range(len(X_test)):
        author = authorMap[currentDataSet[test[i]].author+ str(currentDataSet[test[i]].fieldId)];
        if(author not in done or not done[author]):
            for b in range(len(X_test)):
                authorMatch = authorMap[currentDataSet[test[b]].author+ str(currentDataSet[test[b]].fieldId)];
                if (author == authorMatch and i !=b ):
                    prob += (x[i] - x[b]) == 0;
            done[author] = 'True';

    #print(prob)

    optimization_result = prob.solve()

    # make sure we got an optimal solution
    assert optimization_result == pulp.LpStatusOptimal
    # display the results
    resultList = []
    for i in range(len(X_test)):
        resultList.append(int(x[i].value()));

    return resultList;

    #print resultList;
    # Now add the constraints


def main():
    clf = joblib.load("/Users/prashantravi/Desktop/StanceClassification/SavedModels/Part1_VectorSum_Target_abortion" + ".pkl");
    X_test = joblib.load("/Users/prashantravi/Desktop/StanceClassification/SavedModels/abortionX_test.pkl");
    Y_test = joblib.load("/Users/prashantravi/Desktop/StanceClassification/SavedModels/abortionY_test.pkl");
    currentDataset = joblib.load("/Users/prashantravi/Desktop/StanceClassification/SavedModels/abortionCurrDataSet.pkl");
    test = joblib.load("/Users/prashantravi/Desktop/StanceClassification/SavedModels/abortiontestRange.pkl");
    predict = author_constraints(clf, X_test,test, currentDataset, "abortion");


    #predict = clf.predict(X_test)
    y_actu = pd.Series(Y_test, name='Actual')
    y_pred = pd.Series(predict, name='Predicted')
    df_confusion = pd.crosstab(y_actu, y_pred)

    print df_confusion
    print metrics.accuracy_score(Y_test, predict), metrics.f1_score(Y_test, predict)


#main();
