from src import readData

__author__ = 'prashantravi'

import os;
from learn import learn
from learn import predict
from readData import reorder
from readData import prepare_dictionary
pathVars = []

pathToAbortion =os.getcwd() +'/data/abortion'
pathToObama = os.getcwd() + '/data/obama'
pathToMarijuana = os.getcwd() + '/data/marijuana'
pathToGayRights = os.getcwd() + '/data/gayRights'
pathToAuthors = os.getcwd() + '/data/authors'

pathVars.append(pathToAbortion);
pathVars.append(pathToObama);
pathVars.append(pathToMarijuana);
pathVars.append(pathToGayRights);

pathTopics = ['abortion', 'obama', 'marijuana','gayRights']


pathToAuthors = os.getcwd() +'/data/authors'

def main():
    choice='TP'
    prepare_dictionary();
    if(choice == 'TP'):
        global pathVars;
        global pathToAuthors;
        global gloveText;
        for i, item in enumerate(pathVars):
                pathToFold = os.getcwd() + "/data/folds"+ "/" + pathTopics[i]+ "_folds";
                reorderedData = reorder(readData.readData(pathVars[i], pathToAuthors, pathTopics[i]), pathToFold);
                learn(reorderedData, pathTopics[i]);
    elif(choice == 'E'):
        sentence = raw_input("Enter your sentence..");
        topic = raw_input(' What is the topic? ');
        predict(sentence.lower(), topic);
    #print(readData.getSumVectors('hello my name is bernie sander'));
main();