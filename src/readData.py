import os;
import sys;
import numpy as np
from sentiWord import get_scores
punctuation = ".,:;!?\""
gloveText = '/Users/prashantravi/Desktop/StanceClassification/glove.840B.300d.txt'
class DataModel(object):

    def __init__(self, topic, author, fieldId, parentId, stance, rebuttal, sentence):
        self.topic = topic;
        self.author = author;
        self.fieldId = fieldId;
        self.parentId = parentId;
        self.stance = stance;
        self.rebuttal = rebuttal;
        self.sentence = sentence;

    def printModel(self):
        print(" DataModel |topic:" + self.topic + " |author:" + self.author + " |fieldId:" + self.fieldId + " |parentId:" + self.parentId + " |stance:" + self.stance + " |rebuttal:" + self.rebuttal + " |sentence:" + self.sentence);

def readData(pathToTopic, pathToAuthors, topic):
    counter =0;
    dataset = {}
    for filename in os.listdir(pathToTopic):
        if(counter == 0 or counter% 2 ==0 ):
            f = open(pathToTopic + '/' + filename, 'r');
            dataModel = DataModel(None, None, None,None, None, None, f.read().lower());
        else:
            f = open(pathToTopic + '/' + filename, 'r');
            dataModel.author = filename[0];
            key = filename.rsplit('.', 1)[0]
            metadata = f.read();
            for info in metadata.split('\n'):
                metasplit = info.split('=')
                if(metasplit[0] == 'ID'):
                    dataModel.fieldId = metasplit[1];
                elif(metasplit[0] == 'PID'):
                    dataModel.parentId = metasplit[1];
                elif(metasplit[0] == 'Stance'):
                    if(metasplit[1] == ''):
                        print ' unlabeled Stance in ' + topic + ' ' + filename;
                        sys.exit(-1);
                    dataModel.stance = metasplit[1];
                elif(metasplit[0] == 'rebuttal'):
                    dataModel.rebuttal = metasplit[1];
                elif(metasplit[0] == ''):
                    None;
                else:
                    print ' unparseable meta data ' + metadata;
            dataModel.topic = topic;
            dataset[key] = dataModel
        counter = counter +1;
    return dataset;

def readGloveData(glove_word_vec_file):
    global word_vec_dict
    f = open(glove_word_vec_file, 'r')
    rawData = f.readlines()
    word_vec_dict = {}
    for line in rawData:
        line = line.strip().split()
        tag = line[0]
        vec = line[1:]
        word_vec_dict[tag] = np.array(vec, dtype=float)

    return word_vec_dict

def getWordVector(word):
    global word_vec_dict
    if remove_punctuation(word) in word_vec_dict:
        return word_vec_dict[remove_punctuation(word)]
    return np.zeros_like(word_vec_dict['hi'])

word_vec_dict = None;


def readLexicon(filename):
    f = open(filename,'r');
    wordList = []
    words = f.read();
    for word in words.split('\n'):
        if(word.startswith(';') is False and word):
            wordList.append(unicode(word, errors='ignore'));
    return wordList;

def getFeatures(tweets):
    X = []
    i =0;
    for tweet in tweets:


        X.append(getSumVectors(tweet))

        numPos = 0;
        numNeg = 0;
        #for j in xrange(len(tweet)):

         #   word = remove_punctuation(tweet[j]);
          #  scores = get_scores(word)
            #print str(i) + " " +  word + " length of tweet " + str(len(tweet)) ;
            #scores.printModel();
          #  if scores.pos > scores.neg:
           #     numPos += 1	;
           # else:
           #     numNeg += 1;
        #X[i] = X[i].tolist()
        #if(len(tweet) == 0 or numPos ==0 or numNeg == 0):
         #   X[i].append(0.0);
         #   X[i].append(0.0);
       # else:
        #    X[i].append(numPos/len(tweet))
        #    X[i].append(numNeg/len(tweet))
        #i+=1;
        # print tweet

    return X


def prepare_dictionary():
    global word_vec_dict
    word_vec_dict = readGloveData(gloveText)

def getSumVectors(tweetData):
    global word_vec_dict
    numNonZero = 0
    vector = np.zeros_like(word_vec_dict['hi'])

    for word in tweetData:
        vec = getWordVector(word)
        vector = vector + vec
        if vec.sum() != 0:
            numNonZero += 1

    if numNonZero:
        vector = vector / numNonZero

    return vector

def reorder(data, pathToFold):
    reordered = []
    print pathToFold;
    for filename in os.listdir(pathToFold):
        f = open(pathToFold+ '/' + filename, 'r');
        lines = f.readlines();
        for line in lines:
            reordered.append(data.get(line.strip()));
    return reordered;



def remove_punctuation(input_string):
    for item in punctuation:
        input_string = input_string.replace(item, '')
    #print input_string
    return input_string