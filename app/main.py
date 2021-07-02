from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
import os
from app.function import *

SECRET_KEY = os.urandom(32)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

class GreetUserForm(FlaskForm):
    question = StringField(label=('Entrer une question:'))
    submit = SubmitField(label=('Submit'))
    reponse = StringField(label=('Tags suggéré(s)'))

@app.route('/', methods=('GET', 'POST'))
def index():
   
    form = GreetUserForm()
    if form.validate_on_submit():
        form.reponse.data = textRg(form.question.data)
    return render_template('index.html', form=form)
