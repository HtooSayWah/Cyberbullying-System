from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.metrics import accuracy_score
import random

#file declaration
def FileInitiation():
    with open("./bullywords.txt", encoding = "utf-8-sig") as f: w = f.readlines()
    wlist = [i.strip() for i in w]

    ccorpus =open("./stopword_removed_segmented_file.txt", encoding = "utf-8-sig")
    corpuslist = ccorpus.readlines()
    corpus = [i.strip() for i in corpuslist]
    return wlist,corpus


#building vocabulary
def BuildVocab(corpus):
    dictionary = []
    for c in corpus:
        cc = c.split()
        dictionary.extend(cc)
    dictionary = list(set(dictionary))
    vocab = {}
    for index,i in enumerate(dictionary):
        vocab[i] = index
    return vocab

#Expected Target
def ExpectedTarget(wlist,corpus):
    Yvalue = []
    for c in corpus:
        ctemp = c.split()
        ytemp = []
        for ct in ctemp:
            if ct in wlist:
                ytemp.append(1)
            else:
                ytemp.append(0)
        if sum(ytemp)>0:
            Yvalue.append(1)
        else: 
            Yvalue.append(0)
    return Yvalue

#Vectorization
def Vectorization(vocab):
    vectorizer = TfidfVectorizer(min_df=0.01,sublinear_tf=True,vocabulary = vocab)
    X = vectorizer.fit_transform(texttemp)
    return X

#Labeling
def Labeling(Yvalue):
    le = LabelEncoder()
    le.fit(Yvalue)
    Yvalue = le.transform(Yvalue)
    return Yvalue

#Classification
def Classification(X,Yvalue):
    classifier = GaussianNB()
    classifier.fit(X.toarray(), Yvalue)

def ExtractBullywords(text,blist):
    e1 = text.split()
    bwords = []
    for e  in e1:
        if e in blist:
            bwords.append(e)
    return bwords
    

def Classify(text):
    wlist,corpus = FileInitiation()
    vocab = BuildVocab(corpus)
    Yvalue = ExpectedTarget(wlist,corpus)
    txtArray = []
    txtArray.append(text)
    #vectorizer
    vectorizer = TfidfVectorizer(min_df=0.01,sublinear_tf=True,vocabulary = vocab)
    X = vectorizer.fit_transform(corpus)

    #Labeling
    LabelX = Labeling(Yvalue)
    #print(LabelX)

    #Classification
    classifier = GaussianNB()
    classifier.fit(X.toarray(), LabelX)

    Y = vectorizer.fit_transform(txtArray)
    predicted = classifier.predict(Y.toarray())
    temp = predicted[0]
    bullywords = []
    #print(temp)
    if temp == 1:
        bullywords = ExtractBullywords(text,wlist)
    e1 = text.split()
    bwords = []
    for e  in e1:
        if e in wlist:
            bullywords.append(e)

    return list(set(bullywords))


    
    
    
    
    
    
    
    




