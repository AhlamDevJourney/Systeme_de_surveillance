import os
import pickle
import cv2
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import datetime
########### Get hight unkown face counter########
def get_highest_unknown_face_counter():
    folderPathUnknown = 'images_inconnues'
    PathListUnknown = os.listdir(folderPathUnknown)
    max_unknown_face_counter = 0

    for pathUnknown in PathListUnknown:
        # Extraire l'unknown_face_counter du nom de fichier
        filename_parts = os.path.splitext(os.path.basename(pathUnknown))[0].split("_")
        image_id = int(filename_parts[0])

        if image_id > max_unknown_face_counter:
            max_unknown_face_counter = image_id

    return max_unknown_face_counter

###########

#### SQLITE DATABASE######
import sqlite3

# Établir une connexion à la base de données
conn = sqlite3.connect('visages_connus.db')
cursor = conn.cursor()
# Établir une connexion à la base de données visages inconnus
conn1 = sqlite3.connect('visages_inconnus.db')
cursor1 = conn1.cursor()

# Créer une table 'people' si elle n'existe pas déjà
cursor.execute('''
    CREATE TABLE IF NOT EXISTS people (
        counter INTEGER PRIMARY KEY,
        id INTEGER ,
        timestamp TEXT,
        image BLOB
    )
''')

# Créer une table 'unknown_people' si elle n'existe pas déjà
cursor1.execute('''
    CREATE TABLE IF NOT EXISTS unknown_people (
        counter INTEGER PRIMARY KEY,
        id INTEGER ,
        timestamp TEXT,
        image BLOB
    )
''')

def update_unknown_encodings():
    folderPathUnknown = 'images_inconnues'
    PathListUnknown = os.listdir(folderPathUnknown)
    imgListUnknown = []
    UnknownPeopleIDs = []

    for pathUnknown in PathListUnknown:
        imgListUnknown.append(cv2.imread(os.path.join(folderPathUnknown, pathUnknown)))
        # Extraire l'ID, la date et l'heure à partir du nom du fichier
        filename_parts = os.path.splitext(os.path.basename(pathUnknown))[0].split("_")
        image_id = filename_parts[0]

        image_date = filename_parts[1]
        # print(image_date)
        image_time = filename_parts[2]
        # print(image_time)

        # Ajouter l'ID à la liste des ID inconnus
        UnknownPeopleIDs.append(image_id)
        """
        print("Image:", pathUnknown)
        print("ID:", image_id)
        print("Date:", image_date)
        print("Heure:", image_time)
"""
    # Maintenant, imgListUnknown contient les images et UnknownPeopleIDs contient les IDs correspondants


    #print(UnknownPeopleIDs)

    def findEncodings(imagesList):
        encodeList = []
        for img in imagesList:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # Détecter les visages dans l'image
            face_locations = face_recognition.face_locations(img)

            if face_locations:
                # Si au moins un visage est détecté, obtenir ses encodages
                encode = face_recognition.face_encodings(img, face_locations)[0]
                encodeList.append(encode)

            else:
                # Aucun visage détecté dans cette image
                print("Aucun visage n'a été détecté dans cette image.")

        return encodeList

    encodeListUnKnown = findEncodings(imgListUnknown)
    encodeListUnKnownWithIds = [encodeListUnKnown, UnknownPeopleIDs]

    existing_encode_file = "UnknownEncodeFile.p"
    with open(existing_encode_file, 'wb') as f:
        pickle.dump(encodeListUnKnownWithIds, f)

#update_unknown_encodings()
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://securitysystem-35548-default-rtdb.firebaseio.com/",
    'storageBucket':"securitysystem-35548.appspot.com"

})
bucket=storage.bucket()


cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
imgBackground= cv2.imread('Resources/Backgrounde.png')

#Importing the mode images into a list
folderModePath='Resources/Modes'
modePathList=os.listdir(folderModePath)
imgModeList= []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))
#print(len(imgModeList))


# Load the encoding File
print("Loading Encode File.....")
file= open('EncodeFile.p','rb')
encodeListKnownWithIds=pickle.load(file)
file.close()
encodeListKnown,PeopleIDs= encodeListKnownWithIds
#print(PeopleIDs)
print("Encode File loaded")

# Load the encoding File for Unknown Person
print("Loading Encode File for Unknown Person.....")
file= open('UnknownEncodeFile.p','rb')
encodeListUnKnownWithIds=pickle.load(file)
file.close()
encodeListUnKnown,UnknownPeopleIDs= encodeListUnKnownWithIds
#print(UnknownPeopleIDs)
print("Encode File loaded for Unknown Person")

modeType=1
counter=0
id=-1
id_inconnu=-1
out_mode=0
visage_connu=0
imgPeople=[]
last_index = None
last_detection_time = None

last_detection_time_inconnu = None
last_index_inconnu = None
unknown_face_counter=4
detected=0
active_cam=1


while True:
    update_unknown_encodings()
    success, img=cap.read()
    imgS=cv2.resize(img,(0,0),None,0.25,0.25)
    detected = 0
    counter = 0
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame=face_recognition.face_locations(imgS)
    encodeCurFrame=face_recognition.face_encodings(imgS,faceCurFrame)

    imgBackground[162:162+480,55:55+640]=img
    if active_cam==1:
        imgBackground[44:44+ 633, 808:808 + 414] = imgModeList[1]
        active_cam += 1


    for encodeFace , faceLoc in zip(encodeCurFrame,faceCurFrame):
        matches=face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis=face_recognition.face_distance(encodeListKnown,encodeFace)
        #print("matches",matches)
        #print("Face distance", faceDis)


        matchIndex=np.argmin(faceDis)
        print("MatchIndex =",matchIndex)

        if matches[matchIndex]:
            visage_connu=1
            print("Kown face detected")



            # print(PeopleIDs[matchIndex])
            #bbox est obtenu à partir de la localisation du visage
            y1,x2,y2,x1=faceLoc
            #On multiplie par 4 car avant on a résuit la taille de l'image par 4
            y1, x2, y2, x1 = y1 * 4,x2 * 4,y2 * 4,x1 * 4
            #Attention on travaille sur imageBackground ce n'est pas l'image du visage , on ajoute des valeurs d'ofset pour la correction
            bbox=55+x1,162+y1,x2-x1,y2-y1
            imgBackground=cvzone.cornerRect(imgBackground,bbox,rt=0)
            id=PeopleIDs[matchIndex]
            print(id)
            #Gestion du date et heure pour les visages connus
            if last_index != id or (last_detection_time is not None and (
                    datetime.datetime.now() - last_detection_time).total_seconds() >= 10 ):
                current_time = datetime.datetime.now()
                print("Date and Time:", current_time)
                last_detection_time = current_time
                last_index = id
                # Enregistrement de l'image du visage inconnu avec un numéro d'ID

                timestamp = current_time .strftime("%Y-%m-%d %H:%M:%S")

                # Enregistrement de l'image comme un tableau d'octets (BLOB)
                _, image_encoded = cv2.imencode('.png', img)
                image_blob = image_encoded.tobytes()

                # Insérer les données dans la base de données
                cursor.execute('''
                            INSERT INTO people (id,timestamp, image)
                            VALUES (?, ?,?)
                        ''', (last_index,timestamp, image_blob))
                conn.commit()
                print("Image enregistrée dans la base de données")



            if counter==0:
                counter=1
                #modeType=1 # le premier modeType

    if visage_connu==1:
        if counter!=0:

            if counter==1:
                #Importer les infos = get data

                PeopleInfo = db.reference(f'People/{id}').get()
                if PeopleInfo is not None:
                    print("Person Information:", PeopleInfo)
                else:
                    print(f"No information found for person with ID {id}")
                # Get the images from the storage
                blob=bucket.get_blob(f'images/{id}.png')
                array=np.frombuffer(blob.download_as_string(),np.uint8)
                imgPeople=cv2.imdecode(array,cv2.COLOR_BGRA2BGR)
                # Up date data for last visite time
                ref=db.reference(f'People/{id}')
                ref.child('last_visit_time').set(timestamp)

            #if counter>=7 and out_mode == 1:
                #modeType = 3
                #imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
            if counter>=1 :
                modeType=2
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
                if counter==10:
                    out_mode = 1

                cv2.putText(imgBackground, str(id), (1006, 493),cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255),1)
                cv2.putText(imgBackground,str(PeopleInfo['Occupation']),(1006, 550),cv2.FONT_HERSHEY_COMPLEX,0.5,(255, 255, 255), 1)
                cv2.putText(imgBackground, str(PeopleInfo['last_visit_time']), (910, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6,
                            (100, 100, 100), 1)
                    # Centrer le nom lors de l'affichage:

                    # Récupérer la taille du texte pour calculer l'offset
                (w, h), _ = cv2.getTextSize(PeopleInfo['name'],cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                offset = int((414 - w) / 2)

                    # Convertir les coordonnées en entiers avant de les passer à cv2.putText
                cv2.putText(imgBackground, str(PeopleInfo['name']), (808 + offset, 445), cv2.FONT_HERSHEY_COMPLEX, 1,
                            (50, 50, 50), 1)
                imgBackground[175:175+216,909:909+216]=imgPeople
            counter += 1

    if visage_connu==0:
        modeType = 4
        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
        print("unknown face")
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            # Le visage n'est pas connu, vérifions s'il est déjà dans les visages inconnus
            threshold = 0.6  # Ajustez le seuil selon vos besoins
            matches_unknown = face_recognition.compare_faces(encodeListUnKnown, encodeFace, threshold)
            if True in matches_unknown:
                detected = 1
                faceDis_unk = face_recognition.face_distance(encodeListUnKnown, encodeFace)

                matchIndex_unk = np.argmin(faceDis_unk)
                id_inconnu  =matchIndex_unk
                #print("MatchIndex_unk =", matchIndex_unk)

        if detected ==1:
            print(" Visage déja existant dans images_inconnu")
            print("MatchIndex_unk =", matchIndex_unk)
        else:
            # À l'endroit où vous souhaitez enregistrer une nouvelle image de visage inconnu :
            max_unknown_face_counter = get_highest_unknown_face_counter()
            unknown_face_counter = max_unknown_face_counter + 1
            matchIndex_unk = unknown_face_counter
            id_inconnu  = matchIndex_unk

            unknown_faces_directory = "images_inconnues/"
            # Enregistrement de l'image du visage inconnu avec un numéro d'ID
            now = datetime.datetime.now()
            timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
            image_filename = f"{unknown_faces_directory}{unknown_face_counter}_{timestamp}.png"
            cv2.imwrite(image_filename, img)
            # Incrémenter le compteur pour les visages inconnus
            unknown_face_counter += 1
         # Gestion du date et heure pour les visages connus
        if last_index_inconnu  != id_inconnu  or (last_detection_time_inconnu  is not None and (
                 datetime.datetime.now() - last_detection_time_inconnu ).total_seconds() >= 10):
            current_time = datetime.datetime.now()
            print("Date and Time for unknown:", current_time)
            last_detection_time_inconnu  = current_time
            last_index_inconnu  = id_inconnu
            # Enregistrement de l'image du visage inconnu avec un numéro d'ID

            timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

            # Enregistrement de l'image comme un tableau d'octets (BLOB)
            _, image_encoded_inconnu  = cv2.imencode('.png', img)
            image_blob_inconnu  = image_encoded_inconnu .tobytes()

            # Insérer les données dans la base de données
            cursor1.execute('''
                            INSERT INTO unknown_people (id,timestamp, image)
                            VALUES (?, ?,?)
                         ''', (last_index_inconnu , timestamp, image_blob_inconnu ))
            conn1.commit()
            print("Image enregistrée dans la base de données des visages inconnus")

    #cv2.imshow("webcam",img)
    cv2.imshow("Face Show", imgBackground)
    cv2.waitKey(1)
