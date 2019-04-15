from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier

def fileToArray(filename, sentiment):
    arr = []
    with open(filename) as fp:
        line = fp.readline()
        while line:
            arr.append(tuple((line.replace("\n", ""), sentiment)))
            line = fp.readline()
    return arr

filename = "romance_sentences.txt"
sentiment = "rom"
train = fileToArray(filename, sentiment)
filename = "horror_sentences.txt"
sentiment = "horror"
train += fileToArray(filename, sentiment)
print(train)
# print(type(t))
# bobo = TextBlob(t)
# bobo.tags

cl = NaiveBayesClassifier(train)
blob = TextBlob("He grabbed the axe and began swinging at me. He pulled me close and told me he loved me.", classifier=cl)
for s in blob.sentences:
    print("hi")
    prob_dist = 0
    prob_dist = cl.prob_classify(s)
    print(prob_dist.prob("rom"))
    print(s)
    print(s.classify())
