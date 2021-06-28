from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
import os
from app.function import *

SECRET_KEY = os.urandom(32)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

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
