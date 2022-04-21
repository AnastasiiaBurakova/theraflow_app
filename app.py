from flask import Flask, render_template
from data import form

app = Flask(__name__)

@app.route('/')
def register():
    return render_template('register.html')

@app.route('/starter')
def starter():
    return render_template('starter.html', form=form)    

@app.route('/startclient')
def starter_client():
    return render_template('startet-client.html')       