__author__ = 'prashantravi'
from sklearn.preprocessing import LabelEncoder
from nltk.tokenize import TreebankWordTokenizer
from nltk.tag.stanford import StanfordPOSTagger
from nltk.corpus import stopwords
from readData import DataModel
from itertools import chain, imap
from sentiWord import get_scores
stopwords = stopwords.words("English")
stopwords.extend(['#', ',', '+', '.'])
punctuation = ".,:;!?\""

def transformTweetData(tweet):
    content = unicode(tweet.sentence.lower(), errors='ignore')
    words = content.strip().split()
    tokenizer = TreebankWordTokenizer()
    extra_features = []
    content = " ".join(words + extra_features)
    tokens = tokenizer.tokenize(content)
    tokens = [t for t in tokens if t not in stopwords]
    return tokens

def remove_punctuation(input_string):
    for item in punctuation:
        input_string = input_string.replace(item, '')
    #print input_string
    return input_string

def main():
    sentence = raw_input("What's your sentence? ");
    dataModel = DataModel(None, None, None,None, None, None, sentence.lower());
    for tweet in transformTweetData(dataModel):
         print tweet;

#main();