
import cv2
import face_recognition
import pickle
import os

# Importing people images into a list
folderPath = 'images_inconnues'
PathListUnknown = os.listdir(folderPath)
print(PathListUnknown)
imgListUnknown = []
UnknownPeopleIDs = []
for path in PathListUnknown:
    imgListUnknown.append(cv2.imread(os.path.join(folderPath, path)))
    UnknownPeopleIDs.append(os.path.splitext(path)[0])

print(UnknownPeopleIDs)


def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(img_rgb)

        if len(face_locations) > 0:
            encode = face_recognition.face_encodings(img_rgb, face_locations)[0]
            encodeList.append(encode)
            cv2.rectangle(img, (face_locations[0][3], face_locations[0][0]),
                          (face_locations[0][1], face_locations[0][2]), (0, 255, 0), 2)

    return encodeList


print("Encoding started ....")
encodeListUnKnown = findEncodings(imgListUnknown)
encodeListUnKnownWithIds = [encodeListUnKnown, UnknownPeopleIDs]
print("Encoding complete")

file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListUnKnownWithIds, file)
file.close()
print("File saved")
