import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://attendance-tracker-80294-default-rtdb.firebaseio.com/",
    'storageBucket': "attendance-tracker-80294.appspot.com"
})


bucket = storage.bucket()


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
# fps = cap.get(cv2.CAP_PROP_FPS)
# print(fps)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)

imgBackground = cv2.imread('resources/background.png')

# importing the model images
folderModePath = 'resources/models'
modePathList = os.listdir(folderModePath)
imgmodelist = []
for path in modePathList:
    imgmodelist.append(cv2.imread(os.path.join(folderModePath,path)))

# print(len(imgmodelist))

# load the encoding file
file = open('encodeFile.p','rb')
encodelistknownIds = pickle.load(file)
file.close()
encodelistknown,studentIds = encodelistknownIds
# print(studentIds)
print("encode file loaded")

modeType = 0
counter = 0
id=-1
imgStudent = []

while True:
    success, img = cap.read()


    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)


    faceCurframe = face_recognition.face_locations(imgS)
    encodeCurframe = face_recognition.face_encodings(imgS, faceCurframe)

    imgBackground[162:162+480,55:55+640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgmodelist[modeType]


    if faceCurframe:



        for encodeface, faceloc in zip(encodeCurframe,faceCurframe):
            matches = face_recognition.compare_faces(encodelistknown,encodeface,tolerance=0.49)
            facedis = face_recognition.face_distance(encodelistknown,encodeface)
            print("matches",matches)
            print("faceid",facedis)

            matchindex = np.argmin(facedis)
            # print("match index", matchindex)
            if matches[matchindex]:

                # print("known face detected")
                # print(studentIds[matchindex])
                y1,x2,y2,x1 = faceloc
                y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                bbox = 55+x1,162+y1,x2-x1,y2-y1
                imgBackground = cvzone.cornerRect(imgBackground,bbox,rt=0)
                id= studentIds[matchindex]
                if counter==0:
                    cvzone.putTextRect(imgBackground,"Loading",(275,400))
                    cv2.imshow("face background", imgBackground)
                    cv2.waitKey(1)
                    counter=1
                    modeType=1
            else:
                y1, x2, y2, x1 = faceloc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                print("unknown face detected")
                imgBackground[44:44 + 633, 808:808 + 414] = imgmodelist[4]
                print(datetime.now())




        if counter!=0:
            if counter==1:
                # get data
                studentInfo = db.reference(f'students/{id}').get()
                print(studentInfo)
                # get from storage
                blob = bucket.get_blob(f'images/{id}.jpg')
                array= np.frombuffer(blob.download_as_string(),np.uint8)
                imgStudent = cv2.imdecode(array,cv2.COLOR_BGRA2BGR)

                # update data of attendance

                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'],"%Y-%m-%d %H:%M:%S")

                secondsElapsed = (datetime.now()-datetimeObject).total_seconds()
                print(secondsElapsed)
                # change this 30 to the time u want to attendance to be updated
                if secondsElapsed>30:


                    ref = db.reference(f'students/{id}')
                    studentInfo['total_attendance'] +=1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType =3
                    counter=0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgmodelist[modeType]



            if modeType!=3 :


                if 10<counter<20:
                    modeType =2

                imgBackground[44:44+ 633, 808:808+414] = imgmodelist[modeType]

                if counter<=10:


                    # print(studentInfo)
                    cv2.putText(imgBackground,str(studentInfo['total_attendance']),(861,125),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
                    cv2.putText(imgBackground, str(studentInfo['role']), (1006, 550), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                                (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(id), (1006, 493), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                                (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6,
                                (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['Year']), (1025, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6,
                                (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['joining-date']), (1125, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6,
                                (100, 100, 100), 1)

                    (w,h), _ = cv2.getTextSize(studentInfo['name'],cv2.FONT_HERSHEY_COMPLEX,1,1)
                    offset = (414-w)//2
                    cv2.putText(imgBackground, str(studentInfo['name']),(808+offset,445), cv2.FONT_HERSHEY_COMPLEX,1,(50,50,50),1)


                    imgBackground[175:175+216,909:909+216] = imgStudent



                counter+=1

                if counter>=20:
                    counter = 0
                    modeType = 0
                    studentInfo=[]
                    imgStudent = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgmodelist[modeType]
    else:
        modeType =0
        counter=0
    # cv2.imshow("web cam",img)
    cv2.imshow("face background", imgBackground)

    if cv2.waitKey(1) & 0xFF == ord('d'):
        break

