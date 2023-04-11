from flask import Flask, render_template, request, redirect, url_for,session
from flask import *

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


app = Flask(__name__)
app.secret_key = '1234567eaf'

app.template_folder = 'templates'

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home_page'))
    return render_template('user_login.html')

@app.route('/signup',methods=['POST'])
def signup():
    username = request.form.get("username")
    password = request.form.get("password")
    Car = request.form.get("Car")
    N_plate = request.form.get("N_plate")
    result = db.collection('users').document(username).get()
    if result.exists:
        return render_template('user_login.html',us = "User already existed")
    else: 
        data2 = {"username":username,"password":password,"Car":Car,"N_plate":N_plate,"years":1,'spent':0.00,"balance":100.00,"Card Type":"Visa","Card Number":"12345678","Card Holder Name":username,"EXPIRY":"27-01-2003","CVV":"377"}

        db.collection('users').document(data2['username']).set(data2)
        session['username'] = username
        return redirect(url_for('home_page'))

@app.route('/login', methods=['POST'])
def login():
    # Get the form data
    username = request.form.get("username")
    password = request.form.get("password")
    if username == "":
        return render_template('user_signin.html')
    else:    
        result = db.collection('users').document(username).get()
        if result.exists:
            dicti = result.to_dict()
            if dicti['password']==password:
                session['username'] = username
                return redirect(url_for('home_page'))
            else:
                return render_template('user_login.html',us = "Invalid login password")

        else:
            return render_template('user_signin.html',us = "User Doesn't Exist, Sign Up")


@app.route('/home_page')
def home_page():
    # Render a success page
    if 'username' in session:
        charge = 0
        data = db.collection('users').document(session['username']).get().to_dict()
        N_plate = data["N_plate"]
        Balance = data["balance"]
        spent = data['spent']
        data2 =  db.collection("property").get()
        for d in data2:
            dict1 = d.to_dict()
            print(dict1)
            if dict1 !={}:
                print(dict1['Name'])
                data3 =  db.collection("property").document(dict1['Name']).collection("Cars").document("nplate").get().to_dict()["nplate"]
                for d1 in data3:
                    if d1 == N_plate:
                        data4 = db.collection("property").document(dict1['Name']).collection("Cars").document(d1).collection("timestamps").get()
                        for d2 in data4:
                            dict2 = d2.to_dict()
                            if 'Exit_Timestamp' in dict2:
                                print(dict2)
                                charge = charge + 50
        db.collection('users').document(session['username']).set({'spent':charge},merge = True)
        if(charge>spent):
            db.collection('users').document(session['username']).set({'balance':Balance-charge},merge=True)
        result=[data['username'],data['Car'],data['N_plate'],data['years'],data['balance'],data['spent']]
        return render_template('user_home_page.html',result=result)
    else:
        return "User not logged in"
    # return 'successful login'

@app.route('/spent_analytics', methods=['GET'])
def spent_analytics():
    # Render a success page
    if 'username' in session:
        i1=1
        result = []
        data = db.collection('users').document(session['username']).get().to_dict()
        N_plate = data["N_plate"]
        data2 =  db.collection("property").get()
        for d in data2:
            dict1 = d.to_dict()
            # print(dict1)
            if dict1 !={}:
                name = dict1['Name']
                data3 =  db.collection("property").document(name).collection("Cars").document("nplate").get().to_dict()["nplate"]
                for d1 in data3:
                    if d1 == N_plate:
                        data4 = db.collection("property").document(dict1['Name']).collection("Cars").document(d1).collection("timestamps").get()
                        for d2 in data4:
                            dict2 = d2.to_dict()
                            count = str(i1)
                            if 'Exit_Timestamp' in dict2:
                                l =[count,name +" "+ dict2["Entry_camera"],name + dict2["Exit_camera"],'50',dict2["charged"],dict2["Entry_Timestamp"],dict2["Exit_Timestamp"]]
                                print(dict2)
                            else:
                                l =[count,name + " "+dict2["Entry_camera"],'-','50',dict2["charged"],dict2["Entry_Timestamp"],'-']
                                print(dict2)
                            i1=i1+1
                            result.append(l)
        
        if result == []:
            result = ['-','-',"-","-","-","-"]        

        return render_template('user_spent_analytics.html',result=result)
    else:
        return "User not logged in"
    

@app.route('/add_money', methods=['GET',"POST"])
def add_money():
    # Render a success page
    if 'username' in session:
        data = db.collection('users').document(session['username']).get().to_dict()
        print(data)
        Balance = data["balance"]
        amount  = request.form.get('amount')
        card_type  = request.form.get('card-type')
        card_number  = request.form.get('card-number')
        card_holder_name  = request.form.get('card-holder-name')
        expiry_date  = request.form.get('expiry-date')
        cvv  = request.form.get('cvv')
        print(type(amount),card_type,card_number,expiry_date,cvv,card_holder_name)
        if ((card_type == data["Card Type"] and (card_holder_name == data["Card Holder Name"])and (card_number == data["Card Number"])and (expiry_date == data["EXPIRY"])and (cvv == data["CVV"]))):
            print("yes")
            db.collection('users').document(session['username']).update({'balance':firestore.Increment(float(amount))})
            return render_template('user_add_money.html',us = " Succesfull")
        else:
            return render_template('user_add_money.html',us = "Wrong credentials")
    else:
        return "User not logged in"

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)