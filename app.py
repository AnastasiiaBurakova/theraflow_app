#import flask
from flask import Flask, render_template, request, abort, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField
from data import get_users, get_user_by_username, get_all_usernames, create_user
# from flask_httpauth import HTTPBasicAuth 
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse, urljoin
import user_email 

app = Flask(__name__)
# auth = HTTPBasicAuth()

login_manager = LoginManager()

login_manager.init_app(app)

users = {
    "therapist": generate_password_hash("therapist")
}

app.secret_key = b'fhfnefnernvienvgvfei;'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

class User():
    def __init__(self, username):
        self.__dict__ = get_user_by_username(username)
        self.username = username

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    @classmethod
    def get(cls,username):
        return User(username)                        

# @auth.verify_password
# def verify_password(username, password):
#    if username in get_all_usernames() and \
#            check_password_hash(get_user_by_username(username).get("Password"), password):
#        return username

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Submit')

class ResetPasswordForm(FlaskForm):
    username = StringField('Username')
    submit = SubmitField('Submit')    

class SignUpForm(FlaskForm):
    username = StringField('Username')
    name = StringField('Name')
    about = TextAreaField('About')
    age = IntegerField('Age')
    password = PasswordField('Password')
    email = StringField('Email')
    submit = SubmitField('Submit')
    

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
            ref_url.netloc == test_url.netloc 

@app.route("/reset-password", methods = ['POST'])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        username = form.username.data
        user_email.reset_password(username)
        return 'password successfully reset, check your email'   
    else:
        return 'failed to reset password, try again'             

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    reset_password_form = ResetPasswordForm()
    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        user = get_user_by_username(username)

        if username in get_all_usernames() and \
           check_password_hash(get_user_by_username(username).get("Password"), password):

            user = User(username)
            

            login_user(user)

            flash('Logged in successfully.')

            next = request.args.get('next')

            if not is_safe_url(next):
                return abort(400)

            return redirect(next or url_for('my_profile'))
    return render_template('login.html', form=form, reset_password_form=reset_password_form)

@app.route('/test')
def test():
    return render_template('test.html')       

@app.route('/')
def welcome():
    return render_template('welcome.html')     

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/starter', methods=['GET', 'POST'])
def starter():
    form = SignUpForm()
    if form.validate_on_submit():
        username = form.username.data
        password_hash = generate_password_hash(form.password.data)
        name = form.name.data
        about = form.about.data
        age = form.age.data
        email = form.email.data

        create_user(username, name, about, age, password_hash, email, 1)

        user = User(username)
        login_user(user)
        flash('Logged in successfully.')
        next = request.args.get('next')
        if not is_safe_url(next):
            return abort(400)
        return redirect(next or url_for('my_profile'))    
    return render_template('starter.html', form=form)    

@app.route('/startclient', methods=['GET', 'POST'])
def starter_client():
    form = SignUpForm()
    if form.validate_on_submit():
        username = form.username.data
        password_hash = generate_password_hash(form.password.data)
        name = form.name.data
        about = None 
        age = form.age.data
        email = form.email.data

        create_user(username, name, about, age, password_hash, email, 2)


        user = User(username)
        login_user(user)
        flash('Logged in successfully.')
        next = request.args.get('next')
        if not is_safe_url(next):
            return abort(400)
        return redirect(next or url_for('my_profile'))    
    return render_template('startet-client.html', form=form)    

@app.route("/my-profile")   
@login_required
def my_profile():
    return render_template('profile.html', user=current_user) 

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('/'))      

@app.route("/create", methods = ['POST'])
@login_required
def create():     
    return request.form['about-content']

@app.route("/request")   
@login_required
def request_session():
    return render_template('request.html', user=get_user_by_username(auth.current_user())) 

@app.route("/request_form")   
@login_required
def request_form():
    return render_template('request_form.html', user=get_user_by_username(auth.current_user())) 

@app.route("/processing")   
@login_required
def processing():
    return render_template('processing.html', user=get_user_by_username(auth.current_user()))     

    

