import cv2
import face_recognition
import os
import pickle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://attendance-tracker-80294-default-rtdb.firebaseio.com/",
    'storageBucket': "attendance-tracker-80294.appspot.com"
})




# importing the student images
folderPath = 'images'
PathList = os.listdir(folderPath)
print(PathList)
imglist = []
studentIds = []
for path in PathList:
    imglist.append(cv2.imread(os.path.join(folderPath,path)))
    # print(path)
    # print(os.path.splitext(path)[0])
    studentIds.append(os.path.splitext(path)[0])

    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

# print(studentIds)


def findEncodings(imageslist):
    encodelist = []
    for img in imageslist:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    return encodelist

print("encoding started")
encodelistknown = findEncodings(imglist)
encodelistknownIds = [encodelistknown,studentIds]
print("encoding completed")


file = open("encodeFile.p",'wb')
pickle.dump(encodelistknownIds,file)
file.close()
print("file saved")