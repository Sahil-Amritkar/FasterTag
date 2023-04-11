from flask import Flask, render_template, request, redirect, url_for,session
import pyrebase
from flask import *

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


app = Flask(__name__)
app.secret_key = '1234567eaf'

users = {
    "user1": "password1",
    "user2": "password2",
    "user3": "password3"
}

app.template_folder = 'templates'

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('owner_home_page'))
    return render_template('toll_owner_login.html')

@app.route('/signup',methods=['POST'])
def signup():
    username = request.form.get("username")
    password = request.form.get("password")
    Location = request.form.get("Location")
    result = db.collection('owner').document(username).get()    
    if result.exists:
        return render_template('toll_owner_login.html',us = "User already existed")
    else: 
        # signin = auth.create_user_with_email_and_password(username, password)
        data2 = {"username":username,"password":password,"Location":Location,"years":1,"charged":0.0,"total_cars":25}
        # card_details = {"Card Type":"Visa","Card Number":"12345678","Card Holder Name":"JOHAN","EXPIRY":"27-01-2003","CVV":"377","Amount":300}
        db.collection('owner').document(data2['username']).set(data2)
        session['username'] = username
        return redirect(url_for('owner_home_page'))

@app.route('/login', methods=['POST'])
def login():
    # Get the form data
    username = request.form.get("username")
    password = request.form.get("password")
    # print("Username = ", type(username))
    if username == "":
        return render_template('toll_owner_signin.html',us = "User Doesn't Exist, Sign Up")
    else:    
        result = db.collection('owner').document(username).get()
        if result.exists:
            dicti = result.to_dict()
            if dicti['password']==password:
                session['username'] = username
                return redirect(url_for('owner_home_page'))
            else:
                return render_template('toll_owner_login.html',us = "Invalid login password")

        else:
            return render_template('toll_owner_signin.html',us = "User Doesn't Exist, Sign Up")


@app.route('/owner_home_page')
def owner_home_page():
    # Render a success page
    if 'username' in session:
        # result=['Marina Mall','3','3','2','250.00','25']
        data = db.collection('owner').document(session['username']).get().to_dict()
        # print(data)
        result=[data['Location'],'3','3',data['years'],data['charged'],data['total_cars']]
        return render_template('owner_home_page.html',result=result)
        
    else:
        return "User not logged in"
    # return 'successful login'

@app.route('/cars_list', methods=['GET'])
def cars_list():
    # Render a success page
    if 'username' in session:

        dict1 = db.collection('owner').document(session['username']).get().to_dict()
        location = "VITC"
        res = db.collection("property").document(location).get().to_dict()
        print(res)
        result=[['1','PB65AW6527','Front Gate','2022-05-19 08:10:35','-']]
        i=2
        for doc in res:
            # print(doc.to_dict())
            dict2 = doc.to_dict()
            if(dict2["Name"]==location):
                print(dict2)
                res1 = db.collection("property").document(location).collection("Cars")
                docs = res.stream()
                ids = []
                for coll in docs:
                    ids.append(coll.id)
                print(ids)
                # collnameref = db.collection("property")
                # docs = collnameref.stream()
                # for doc in docs:
                    # List subcollections in each doc
                    # for collection_ref in doc.reference.collections():
                    #     print(collection_ref.parent.path + collection_ref.id)
                # print(res1.to_dict())
                # count = str(i)
                # d = dict2['Date'] +" "+ dict2['Time']
                # l = [count,dict2['N_plate'],dict2['Location'],d]
                # if "Exit_Time" in dict2:
                #     l.append(dict2["Exit_Time"]+" "+dict2["Exit_Date"])
                # else:
                #     l.append("-")
                # result.append(l)
                # i=i+1


        
        return render_template('cars_list.html',result=result)
    else:
        return "User not logged in"

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
