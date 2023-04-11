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
        data2 = {"username":username,"password":password,"Location":Location,"years":1,"charged":0.0,"total_cars":25}
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
        data = db.collection('owner').document(session['username']).get().to_dict()
        location = data["Location"]
        data2 = db.collection("property").document(location).get().to_dict()
        if data2 :
            if data2["type"]=='Highway':
                result=[location,data2["Cam_count"],data2["Cam_count"],data["years"],50*data2['total_cars'],data2['total_cars']]
            if data2["type"]=='Campus':
                result=[location,data2["Cam_count"],data2["Cam_count"],data["years"],0,data2['total_cars']]
            if data2["type"]=='Parking':
                result=[location,data2["Cam_count"],data2["Cam_count"],data["years"],data2['Charge'],data2['total_cars']]
        else:
            result = [location,2,2,3,0,0]
        return render_template('owner_home_page.html',result=result)
        
    else:
        return "User not logged in"

@app.route('/cars_list', methods=['GET'])
def cars_list():
    # Render a success page
    if 'username' in session:

        dict1 = db.collection('owner').document(session['username']).get().to_dict()
        location = dict1["Location"]
        res = db.collection("property").document(location).collection("Cars").document("nplate").get().to_dict()
        result=[]
        i1=1
        cost_param = db.collection("property").document(location).get().to_dict()["type"]

        print(cost_param)
        for i in res['nplate']:
            res1 = db.collection("property").document(location).collection("Cars").document(i).collection("timestamps").get()
            for doc in res1:
                dict2 = doc.to_dict()
                count = str(i1)
                l = [count,dict2['n_plate'],dict2['Entry_camera'],dict2['Entry_Timestamp']]
                if "Exit_Timestamp" in dict2:
                    l.append(dict2['Exit_camera'])
                    l.append(dict2['Exit_Timestamp'])
                    
                else:
                    l.append("-")
                    l.append("-")
                result.append(l)
                i1=i1+1
        
        if result == []:
            result = ['-','-',"-","-","-","-"]
        
        
        return render_template('cars_list.html',result=result)
    else:
        return "User not logged in"
    

@app.route('/owner_analytics', methods=['GET'])
def owner_analytics():
    if 'username' in session:
        result=[]
        return render_template('owner_analytics.html',result=result)
    else:
        return "User not logged in"

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)

