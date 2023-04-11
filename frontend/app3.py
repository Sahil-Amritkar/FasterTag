from flask import Flask, render_template, request, redirect, url_for,session

import pyrebase
from flask import *

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import re

txt = "The rain in Spain"
x = re.search("^The.*Spain$", txt)
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# data1 = {"N_plate": "H982FKL", "Location": "Parking_Entry1","Time": "20:08:52","Date":"2023-04-04"}
# data2 = {"N_plate": "H982FKL", "Location": "Parking_Entry1","Time": "21:08:52","Date":"2023-04-03"}
# data3 = {"N_plate": "H982FKL", "Location": "Parking_Entry2","Time": "20:08:52","Date":"2023-04-03"}
# data4 = {"N_plate": "H982FKL", "Location": "Parking_Entry2","Time": "21:08:52","Date":"2023-04-03"}
# data5 = {"N_plate": "H982FKL", "Location": "NH1_START","Time": "20:08:52","Date":"2023-04-03"}
# data6 = {"N_plate": "H982FKL", "Location": "NH1_END","Time": "20:30:52","Date":"2023-04-03"}


# def park(txt):
#     park_search = re.search("^Parking", txt)
#     return park_search

# def highway(txt):
#     highway_search = re.search("^NH", txt)
#     return highway_search

N_plate =  "H982FKL"
Location = "Parking_Entry1"
Time = "20:08:52"
Date = "2023-04-04"
data = {"N_plate": N_plate, "Location": Location ,"Date":Date,"Time": Time}

result = db.collection('toll').document(data["N_plate"]).get()

print(result)
if result.exists:
    db.collection('toll').document(data["N_plate"]).set({"Exit_Time":Date,"Exit_Date":  Time},merge = True)
else:
    db.collection('toll').document(data["N_plate"]).set(data)

    

# db.collection('toll').document(data2["Location"]).set(data2)
# db.collection('toll').document(data3["Location"]).set(data3)
# db.collection('toll').document(data4["Location"]).set(data4)
# db.collection('toll').document(data5["Location"]).set(data5)
# db.collection('toll').document(data6["Location"]).set(data6)




