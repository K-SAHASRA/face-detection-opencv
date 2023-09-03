import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://attendance-tracker-80294-default-rtdb.firebaseio.com/"
})

ref = db.reference('students')

data = {
    "009":
        {
            "name":"k.sahasra",
            "role": "cse cc",
            "joining-date": "21-25",
            "total_attendance":6,
            "standing":"G",
            "Year":3,
            "last_attendance_time": "2023-08-15 00:35:34"
        },
    "035":
        {
            "name":"likhitha",
            "role": "cse cc",
            "joining-date": "21-25",
            "total_attendance":4,
            "standing":"G",
            "Year":3,
            "last_attendance_time": "2023-08-15 00:35:34"
        },
    "077":
        {
            "name":"akshay",
            "role": "cse core",
            "joining-date": "21-25",
            "total_attendance":9,
            "standing":"G",
            "Year":3,
            "last_attendance_time": "2023-08-15 00:35:34"
        }


}

for key,value in data.items():
    ref.child(key).set(value)