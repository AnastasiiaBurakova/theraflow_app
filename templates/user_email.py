import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import mail
import secrets
from data import get_user_by_username, reset_data_password
import random
import string
from werkzeug.security import generate_password_hash

def send_message(username, subject, body):

    user = get_user_by_username('therapist')
    name = user['Name']
    email = user['Email']

    message = Mail(
        from_email='burakova.anastasiia@gmail.com',
        to_emails=email,
        subject="Hello %s" % name,
        html_content=body)
    try:
        sg = SendGridAPIClient(secrets.sendgrid_api_key)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def reset_password(username):
    new_password = get_random_string(20)
    password_hash = generate_password_hash(new_password)
    reset_data_password(username, password_hash)
    send_message(username, 'Theraflow password reset', 'Your new password is %s' % new_password)       



