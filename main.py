#!/usr/bin/python3.8
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
import os
import re

import nltk
from nltk.stem.snowball import FrenchStemmer, EnglishStemmer
from nltk.stem import WordNetLemmatizer
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

from pickle import Unpickler as Upck
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression, Perceptron
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

lemmatizer = WordNetLemmatizer()
stemmer = EnglishStemmer()
tokenizer = nltk.RegexpTokenizer(r'\w+')

def tokensLem(text):
    '''tokenize les documents puis les lemmatize'''
    tokens = tokenizer.tokenize(text)
    for j, word in enumerate(tokens):
        tokens[j] = lemmatizer.lemmatize(word)
    return tokens

with open("dataAPI", 'rb') as file:
    Upickler = Upck(file)
    tfidf = Upickler.load()
    cls_lr = Upickler.load()
    label = Upickler.load()

SECRET_KEY = os.urandom(32)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

def textRg(text):

    # en minuscule
    question = text.lower()  

    # suprime tout ce qui n'est pas du texte
    question = re.sub(r'[^a-z ]', ' ', question)  

    # Supprime les mots de 1 ou 2 lettre ou > 30 lettres
    question = re.sub(r'(( \w{1,2})* \w{1,2}$)|(^\w{1,2} (\w{1,2} )*)|( \w{1,2} (\w{1,2} )*)', ' ', question)
    question = re.sub(r'\w{30,}', ' ', question)

    # contenant des liens type href
    question = re.sub(r'www|http|https|com|org|fr', ' ', question)
    question = tokensLem(question)
    question = " ".join(question)
    
    # Tranformation text
    X = tfidf.transform([question])
    
    # Prediction un prends en compte les 3 classes
    # ayant les plus fortes probabilité
    pred = cls_lr.predict_proba(X.toarray())[0]
    tag = Tag[pred.argsort()][:-4:-1]
    tag = " ".join(tag.tolist())
    return tag

class GreetUserForm(FlaskForm):
    username = StringField(label=('Enter question:'))
    submit = SubmitField(label=('Submit'))

@app.route('/', methods=('GET', 'POST'))
def index():
    form = GreetUserForm()
    if form.validate_on_submit():
        form.username.data = textRg(form.username.data)
        return f'''<h1> suggested Tag : {form.username.data} </h1>'''
    return render_template('index.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)
