import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

Cam_ID = "01"
Cam_type1 = "Entry"
Cam_type2 = "Exit"
nplate = "HR214312"
Charge_ph = 10
Charge_camp = 0
Charge_pk = 10
prop_type = "Campus"

if prop_type == "Campus":
        data_prop = {"Name": "VITC","type":prop_type,"Charge":Charge_camp}
        data_cam = {"Cam_type":Cam_type1,"Cam_name":Cam_ID}
        data_car1  ={"n_plate":nplate,"Cam_type":Cam_type1,"Timestamp":"ABCD"}
        data_car2  ={"n_plate":nplate,"Cam_type":Cam_type2,"Timestamp":"ABCE"}
        data_real = {"n_plate":nplate}

# db.collection('property').document(data_prop["Name"]).set(data_prop)
db.collection("property").document(data_prop["Name"]).collection("Camera").set(data_cam)






# db.collection('admin').add({"name" : "John","age" : 40,"toll_entry_location":"CAM_VITC_001","toll_exit_location":"CAM_VITC_001"})


# data = {"Name":'John Doe',"Car":'Toyota Camry',"N_plate":'H982FKL',"years":'2',"spent":250.00,"balance":'1500.00'}


# data2 = {"Name":"JOHAN","Car":"Mercedes Benz","N_plate":"H982FKL","years":3,"spent":250.00,"balance":1500.00}
# card_details = {"Card Type":"Visa","Card Number":"12345678","Card Holder Name":"JOHAN","EXPIRY":"27-01-2003","CVV":"377","Amount":300}
# db.collection('users').document(data2['Name']).set(data2)
# db.collection("users").document(data2['Name']).collection('card').document(card_details["Card Number"]).set(card_details)


# result = db.collection('users').document('John Doe').get()

# if result.exists:
#         print(result.to_dict())

# docs = db.collection("users").get()

# docs = db.collection("users").document('JOHAN').collection('card').where("CVV","==","377").get()

# for doc in docs:
#         print(doc.to_dict())


