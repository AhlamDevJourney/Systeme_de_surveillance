import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
#biblio pour la création de database reférence
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://securitysystem-35548-default-rtdb.firebaseio.com/",
    'storageBucket':"securitysystem-35548.appspot.com"

})


#Importing people images into a list
folderPath='images'
PathList=os.listdir(folderPath)
print(PathList)
imgList= []
PeopleIDs=[]
for path in PathList:
    imgList.append(cv2.imread(os.path.join(folderPath,path)))
    PeopleIDs.append(os.path.splitext(path)[0])

    fileName= f'{folderPath}/{path}'
    bucket=storage.bucket()
    blob= bucket.blob(fileName)
    blob.upload_from_filename(fileName)


    #print(path)
    #print(os.path.splitext(path)[0])

print(PeopleIDs)

def findEncodings(imagesList):
    encodeList=[]
    for img in imagesList:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList
print("Encoding started ....")
encodeListKnown= findEncodings(imgList)
encodeListKnownWithIds=[encodeListKnown,PeopleIDs]
print("Encoding complete")
# Il faut sauvgarder ces images avec IDs dans un fichier afin de les importer
file=open("EncodeFile.p",'wb')
pickle.dump(encodeListKnownWithIds,file)
file.close()
print("File saved")
