from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

def query(query_text, *param):
    conn = sqlite3.connect("theraflow.db")
    cur = conn.cursor()
    cur.execute(query_text, param)

    column_names = []
    for column in cur.description:
        column_names.append(column[0])

    rows = cur.fetchall()
    dicts = []

    for row in rows:
        d = dict(zip(column_names, row))
        dicts.append(d)

    conn.close()
    return dicts        

def get_users():
    return query('SELECT * FROM Users')

def get_user_by_username(username):
    try: 
        return query('SELECT * FROM Users WHERE Username=?', username)[0]
    except IndexError: 
        print ('not a valid username')
        return None 

def get_all_usernames():
    usernames = query("SELECT Username FROM Users")
    results = []
    for dictionary in usernames:
        results.append(dictionary["Username"])
    return results 

test_user = {
        "Name": "Anastasia Burakova",
        "Age": 27,
        "Email": "burakova.anastasiia@gmail.com",
        "Field": "Behavior therapy",
        "About": "Hello there",
        "Username": "therapist",
        "Password": generate_password_hash("therapist"),
        "Picture": "therapist_pic.png"
}        


users = {
    "therapist": test_user
}    