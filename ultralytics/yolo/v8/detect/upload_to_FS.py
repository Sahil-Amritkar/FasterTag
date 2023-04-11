import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def upload_car(nplate, prop_name, Cam_ID, Cam_type, timestamp):
    #Ideally get property type and charge from database, but to save time, declaring it here 
    prop_type="Campus"
    if prop_type == "Campus":
        Charge=0
    if prop_type == "Highway":
        Charge=0
    if prop_type == "Parking":
        Charge=0

    if not firebase_admin._apps:
        cred = credentials.Certificate("/Users/sahilamritkar/Sahil Codes/VIT Projects/Automatic_Number_Plate_Detection_Recognition_YOLOv8/ultralytics/yolo/v8/detect/serviceAccountKey.json")
        firebase_admin.initialize_app(cred)

    db = firestore.client()

    data_prop = {"Name": prop_name,"type":prop_type,"Charge":Charge,"Cam_count":2,"total_charge":0}
    data_cam = {"Cam_type":Cam_type,"Cam_name":Cam_ID}
    db.collection("property").document(data_prop["Name"]).collection("Camera").document(data_cam["Cam_name"]).set(data_cam)
    db.collection('property').document(data_prop["Name"]).set(data_prop,merge=True)

    if Cam_type == "Entry":
        # db.collection("property").document(data_prop["Name"]).collection("Real_time").document(nplate).set({nplate:"in"})
        timestamp1 = db.collection("property").document(data_prop["Name"]).collection("Real_time").document(nplate).get()
        print(timestamp1)
        if timestamp1.to_dict() is None:
            data_car1  ={"n_plate":nplate,"Entry_camera":Cam_ID,"Entry_Timestamp":timestamp}
            db.collection("property").document(data_prop["Name"]).collection("Real_time").document(nplate).set({nplate:timestamp})
            db.collection("property").document(data_prop["Name"]).collection("Cars").document("nplate").update({"nplate":firestore.ArrayUnion([nplate])})
            db.collection("property").document(data_prop["Name"]).collection("Cars").document(data_car1["n_plate"]).collection("timestamps").document(timestamp).set(data_car1, merge=True)

    elif Cam_type == "Exit":
        timestamp1 = db.collection("property").document(data_prop["Name"]).collection("Real_time").document(nplate).get()
        print(timestamp1)
        if timestamp1.to_dict() is not None:
            data_car1  ={"n_plate":nplate,"Exit_camera":Cam_ID,"Exit_Timestamp":timestamp}
            time = timestamp1.to_dict()[nplate]
            db.collection("property").document(data_prop["Name"]).collection("Real_time").document(nplate).delete()
            db.collection("property").document(data_prop["Name"]).update({"total_cars":firestore.Increment(1)})
            db.collection("property").document(data_prop["Name"]).collection("Cars").document(data_car1["n_plate"]).collection("timestamps").document(time).set(data_car1, merge=True)
        
        if(prop_type == "Highway"):
            charged = 50
            time = timestamp1.to_dict()[nplate]
            db.collection("property").document(prop_name).collection("Cars").document(nplate).collection("timestamps").document(time).set({'charged':charged},merge = True)
            db.collection("property").document(prop_name).update({"Charge":firestore.Increment(charged)})

        

#upload_car('DL1ZA9759', 'VITC', 'Parking_Entry1', '2023-04-04', '08:40:03.199361')

# DL1ZA9759 CAM_VITC_001 2023-04-04 08:40:03.199361
# UP16BT5797 CAM_VITC_001 2023-04-04 08:40:14.074240s