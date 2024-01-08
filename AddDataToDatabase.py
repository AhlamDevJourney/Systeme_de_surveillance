import firebase_admin
from firebase_admin import credentials
#biblio pour la création de database reférence
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://securitysystem-35548-default-rtdb.firebaseio.com/"
})
# créer une réference pour le fichier qui va contenir data des personnes
ref = db.reference('People')
data= {
    "11":
        {
            "name": "Alaoui Ahlam",
            "Occupation": "Famille",
            "last_visit_time":"2023-07-27 00:45:20"
         },
    "12":
            {
                "name": "Emly Blunt",
                "Occupation": "Amie",
                "last_visit_time":"2023-06-02 10:00:00"
             },
    "13":
            {
                "name": "Elon Musk",
                "Occupation": "Ami",
                "last_visit_time":"2023-04-28 12:00:20"
             },
    "14":
            {
                "name": "Alaoui youssef",
                "Occupation": "Famille",
                "last_visit_time":"2023-07-15 12:30:00"
             }
    }
# sending values to real time data base
for key,value in data.items():
    ref.child(key).set(value)