from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
import os
from app.function import *
import nltk
from nltk.stem.snowball import FrenchStemmer, EnglishStemmer
from nltk.stem import WordNetLemmatizer
import numpy as np
import re
from pickle import Unpickler as Upck
import nltk
from nltk.stem.snowball import FrenchStemmer, EnglishStemmer
from nltk.stem import WordNetLemmatizer

SECRET_KEY = os.urandom(32)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

def tokensLem(text):
    lemmatizer = WordNetLemmatizer()
    stemmer = EnglishStemmer()
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    for j, word in enumerate(tokens):
        tokens[j] = lemmatizer.lemmatize(word)
    return tokens

with open("dataCLSlabel", 'rb') as file:
    Upickler = Upck(file)
    cls_u = Upickler.load()
    cls_s = Upickler.load() 
    
with open("dataAPIlabel", 'rb') as file:
    Upickler = Upck(file)
    Tag = Upickler.load()

def textRg(text, Tag=Tag):
    
    # en minuscule
    question = text.lower()  

    # Supprime les mots de 1 ou 2 lettre ou > 30 lettres
    question = re.sub(r'[^a-z|c++|c#|node\.js|\.net|asp\.net|ruby\-on\-rails|sql\-server|objective\-c|android\-studio|visual\-studio]', ' ', question)
    #question = re.sub(r'\.', ' ', question)
    question = re.sub(r'(\-{2,})|( \-+ )|(\-+ )|( \-+)', ' ', question)
    question = re.sub(r'( \++$)|( \++)|( \++ )|(^\++)', ' ', question)
    question = re.sub(r'(^\.+)|( \.{2,})|( \.+ )|(\.+$)|(\.{2,})', ' ', question)
    question = re.sub(r'\w{30,}', ' ', question)
    
    # Prediction on prends en compte les 3 classes
    # ayant les plus fortes probabilité
    pred = cls_s.predict([question])[0]
    pred_p = cls_s.predict_proba([question])[0]
    pred = pred[pred_p.argsort()][::-1]
    Tag = Tag[pred_p.argsort()][::-1]
    i=0
    ans = []
    while pred[i] == 1:
        ans.append(Tag[i])
        i += 1 
    tag = " ".join(ans)
    return tag

############################################
# User interface
class GreetUserForm(FlaskForm):
    username = StringField(label=('Enter une question:'))
    submit = SubmitField(label=('Submit'))

@app.route('/', methods=('GET', 'POST'))
def index():
   
    form = GreetUserForm()
    if form.validate_on_submit():
        form.username.data = textRg(form.username.data)
        return f'''<h1> suggested Tag(s) : {form.username.data} </h1>'''
    return render_template('index.html', form=form)

#if __name__ == "__main__":
#    app.run(debug=True)
