__author__ = 'prashantravi'
import sys
import os

class Sent(object):

    def __init__(self,pos, neg, neu):
        self.pos = pos;
        self.neg = neg;
        self.neu = neu;

    def printModel(self):
        print("Sentiment |positive:" + str(self.pos) + " |negative:" + str(self.neg) );

def split_line(line):
    cols = line.split("\t")
    return cols

def get_words(cols):
    words_ids = cols[4].split(" ")
    words = [w.split("#")[0] for w in words_ids]
    return words

def get_positive(cols):
    return cols[2]

def get_negative(cols):
    return cols[3]

def get_objective(cols):
    return 1 - (float(cols[2]) + float(cols[3]))

def get_gloss(cols):
    return cols[5]


filepath = '/Users/prashantravi/Desktop/StanceClassification/data/SentiWord/sentinet.txt';
f = open(filepath)

def get_scores(word):

    filepath = '/Users/prashantravi/Desktop/StanceClassification/data/SentiWord/sentinet.txt';
    f = open(filepath)
    avg_pos = 0;
    avg_neg = 0;
    avg_neu = 0;
    counter =0;

    sent = Sent(avg_pos, avg_neg, avg_neu);
    for line in f:
        if not line.startswith("#"):
            cols = split_line(line)
            words = get_words(cols)

            if word in words:
                counter +=1;
                #print("For given word {0} - {1}".format(word, get_gloss(cols)))
                #print("P Score: {0}".format(get_positive(cols)))
                #print("N Score: {0}".format(get_negative(cols)))
                #print("O Score: {0}\n".format(get_objective(cols)))
                try:
                    avg_neg = avg_neg + float(get_negative(cols));

                except ValueError:
                    None
                    #print "Oops!  That was no valid number.  Try again..." + get_negative(cols)
                try:
                    avg_pos = avg_pos + float(get_positive(cols));
                except ValueError:
                    None
                    #print "Oops!  That was no valid number.  Try again..." + get_positive(cols)
                try:
                    avg_neu = avg_neu + float(get_objective(cols));
                except ValueError:
                    None
                    #print "Oops!  That was no valid number.  Try again..." + get_objective(cols)
    if(counter >=1):
        sent = Sent(avg_pos/counter, avg_neg/counter, avg_neu/counter);
    return sent;


def main():
    word = raw_input("Enter a word: ")
    print word;
    get_scores(word.lower()).printModel()

#main();