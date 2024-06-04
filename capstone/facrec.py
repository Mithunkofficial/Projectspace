import cv2 as cv
import face_recognition as fr
import os
import numpy as np
from datetime import datetime, date
import csv

class run:
    

    path = 'faces'


    images = []
    classNames = []
    mylist = os.listdir(path)

    for cl in mylist:
        curImg = cv.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
        

    def findEncodings(images):
        encodeList = []
        for img in images:
            img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            encoded_face = fr.face_encodings(img)[0]
            encodeList.append(encoded_face)
        return encodeList
    encoded_face_train = findEncodings(images)


    with open('Attendance.csv', 'w') as file:
        csv_writer = csv.writer(file)

    def markAttendance(name):
        
        with open('Attendance.csv','r+') as f:
            myDataList = f.readlines()
            nameList = []
            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])
                
            if name not in nameList:
                now = datetime.now()
                time = now.strftime('%I:%M:%S:%p')
                date = now.strftime('%d-%B-%Y')
                f.writelines(f'\n{name}, {time}, {date}')
                            
                
    # take pictures from webcam 
    cap  = cv.VideoCapture(0)
    while True:
        success, img = cap.read()
        imgS = cv.resize(img, (0,0), None, 0.25,0.25)
        imgS = cv.cvtColor(imgS, cv.COLOR_BGR2RGB)
        faces_in_frame = fr.face_locations(imgS)
        encoded_faces = fr.face_encodings(imgS, faces_in_frame)
        
        for encode_face, faceloc in zip(encoded_faces,faces_in_frame):
            
            matches = fr.compare_faces(encoded_face_train, encode_face)
            faceDist = fr.face_distance(encoded_face_train, encode_face)
            matchIndex = np.argmin(faceDist)
            print(matchIndex)
            
            if matches[matchIndex]:
                name = classNames[matchIndex].upper().lower()
                y1,x2,y2,x1 = faceloc
                # since we scaled down by 4 times
                y1, x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                cv.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv.rectangle(img, (x1,y2-35),(x2,y2), (0,255,0), cv.FILLED)
                cv.putText(img,name, (x1+6,y2-5), cv.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                markAttendance(name)
            
        cv.imshow('webcam', img)
        
        if cv.waitKey(1) & 0xFF == ord('x'):
            break
        
    exit


    try:
        c="Attendance/"
        
        today = date.today()
        d1 = today.strftime("%d-%m-%y/")
        f = str(d1)
        
        time = datetime.now()
        d2 = time.strftime("%H-%M-%S")
        cc = str(d2)

        cfn2 = c+f+cc
        cfn = str(cfn2)
    
        s='Attendance.csv'
        d= cfn+ '.csv'

        os.renames (s,d)

    except FileNotFoundError as e:
        print("File not Found in the system")
        

    print("Attendance updated to "+cfn+ ".csv")