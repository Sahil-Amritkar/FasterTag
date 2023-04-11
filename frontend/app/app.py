from flask import Flask, render_template, request, redirect, url_for,session

import pyrebase
from flask import *
config = {
    "apiKey": "AIzaSyDD5mB3u1qvVWpNU7tCyTPZj2U6lTE9eDE",
    "authDomain": "my-project1-ebe10.firebaseapp.com",
    "databaseURL": "https://my-project1-ebe10-default-rtdb.firebaseio.com",
    "projectId": "my-project1-ebe10",
    "storageBucket": "my-project1-ebe10.appspot.com",
    "messagingSenderId": "27480654527",
    "appId": "1:27480654527:web:efd9eb3d571bcaf562bc0a",
    "measurementId": "G-XVHQGNCJL1"
}


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


app = Flask(__name__)
app.secret_key = '1234567eaf'

# response.headers['Cache-Control'] = 'no-cache'


# Dummy user database
users = {
    "user1": "password1",
    "user2": "password2",
    "user3": "password3"
}

app.template_folder = 'templates'

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home_page'))
    return render_template('user_signin.html')

"""
def signup():
    email = input("Enter email : ")
    password = input("Enter password : ")
    try: 
        user = auth.create_user_with_email_and_password(email, password)
    except:
        print("Email already exists")
"""

@app.route('/signup',methods=['POST'])
def signup():
    username = request.form.get("username")
    password = request.form.get("password")
    try : 
        signin = auth.create_user_with_email_and_password(username, password)
        session['username'] = username
        return redirect(url_for('home_page'))
    except:
        return render_template('user_login.html',us = "User already existed")

@app.route('/login', methods=['POST'])
def login():
    # Get the form data
    username = request.form.get("username")
    password = request.form.get("password")
    # print(username,password)
    # Check if the username and password match a user in the database
    try : 
        login = auth.sign_in_with_email_and_password(username, password)
        # If authentication is successful, redirect to a new page
        # If authentication fails, show an error message
        session['username'] = username
        return redirect(url_for('home_page'))
    except:
        return "Invalid login credentials"


@app.route('/home_page')
def home_page():
    # Render a success page
    if 'username' in session:
        print(session['username'])
        result=['John Doe','Toyota Camry','H982FKL','2','250.00','1500.00']
        return render_template('user_home_page.html',result=result)
    else:
        return "User not logged in"
    # return 'successful login'

@app.route('/spent_analytics', methods=['GET'])
def spent_analytics():
    # Render a success page
    if 'username' in session:
        result=[['1','Mumbai-Pune Expressway','NH 20','94','150'],
                ['2','NH 44','Electronic City','38','75'],
                ['3','Poovarani','NH 48','72','100'],
                ['4','Madapam','Raipur','20','50'],
                ['5','Hoshiarpur','Batala','120','200']]
        return render_template('user_spent_analytics.html',result=result)
    else:
        return "User not logged in"
    

@app.route('/add_money', methods=['GET'])
def add_money():
    # Render a success page
    if 'username' in session:
        return render_template('user_add_money.html')
    else:
        return "User not logged in"

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)