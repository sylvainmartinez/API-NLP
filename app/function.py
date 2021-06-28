import nltk
from nltk.stem.snowball import FrenchStemmer, EnglishStemmer
from nltk.stem import WordNetLemmatizer
import re
import numpy as np
from pickle import Unpickler as Upck

# Récupération du modèle
with open("dataCLSlabel2", 'rb') as file:
    Upickler = Upck(file)
    cls = Upickler.load() 

# Récupération des Tags
with open("dataAPIlabel2", 'rb') as file:
    Upickler = Upck(file)
    Tag = Upickler.load()


def tokensLem(text):
    lemmatizer = WordNetLemmatizer()
    stemmer = EnglishStemmer()
    tokenizer = nltk.RegexpTokenizer(r'\s', gaps=True)
    tokens = tokenizer.tokenize(text)
    for j, word in enumerate(tokens):
        tokens[j] = lemmatizer.lemmatize(word)
    tokens = " ".join(tokens)
    return tokens

    
def textRg(text):
    '''Réponse a la question
    proposition de Tag(s)'''
    # en minuscule
    question = text.lower()  

    # Application de regex
    question = re.sub(r'[^a-z\+\#\.\-]', ' ', question)
    question = re.sub(r'([^c]\+{2,})| \++|\w+\++\w+', ' ', question)
    question = re.sub(r'[^a-z]\-{1,}|\-{1,}[^a-z]', ' ', question)
    question = re.sub(r'[^a-z+]\.{1,}|\.{1,}[^a-z]', ' ', question)
    question = re.sub(r'([^c]\#{1,})', ' ', question)
    question = re.sub(r'\w{30,}', ' ', question)
    question = re.sub(r'www|http|https|com |org ', ' ', question)
    
    # Pretraitement
    question = tokensLem(question)
    print('n', question)
    # Prediction on prends en compte les 3 classes
    # ayant les plus fortes probabilité
    pred = cls.predict([question])[0]
    pred_p = cls.predict_proba([question])[0]
    pred = pred[pred_p.argsort()][::-1]
    tag = Tag[pred_p.argsort()][::-1]
    
    if cls.predict([question])[0].sum() == 0:
        return tag[0]
    else:
        i=0
        ans = []
        while pred[i] == 1:
            ans.append(tag[i])
            i += 1 
        tag = " ".join(ans)
        return tag
