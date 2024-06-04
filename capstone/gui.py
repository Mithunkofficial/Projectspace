import os
import csv
import shutil
import cv2 as cv
import webbrowser
import numpy as np
import tkinter as tk
import face_recognition as fr

from pathlib import Path
from tkinter import filedialog
from datetime import datetime, date
from tkinter import Tk, Canvas,Button,Label, PhotoImage

window = Tk()
window.geometry("940x452")
window.configure(bg = '#f2f2f2')
window.title("Facial Recognition System")
ti = PhotoImage(file='assets\\title\logo.png')
window.iconphoto(False, ti)



#Facial recognition Attendance system
def mainprog():
       
    path = 'assets\\faces'
    images = []
    classNames = []
    mylist = os.listdir(path)

    for cl in mylist:
        curImg = cv.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
        
    class frs():
        
        try:
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
                    
                cv.imshow('Press "X" and the close', img)
                
                if cv.waitKey(1) & 0xFF == ord('x'):
                    break
        except Exception as e:
            print("Folder contains Non-face images.")            
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
        
        
    except:
        window = Tk()
        window.geometry("940x452")
        window.configure(bg = '#f2f2f2')
        window.title("Facial Recognition System")
        w = tk.Label(window, text="You have uploaded non-face images.\n Please delete it.",
                     font=("Lato SemiBold", 32 * -1))
        w.pack()



#Adding Faces to recognize
def af():
    
    try:
        filename =filedialog.askopenfilename(
            filetypes=(("jpg files","*.jpg"),("jpeg files","*.jpeg"))
            )
        filepath=os.path.abspath(filename)
        srcpath=str(filepath)
        shutil.copy(srcpath,'assets\\faces')
    except:
        print("No image selected")
exit

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

canvas = Canvas(
    window,
    bg = '#f2f2f2',
    height = 452,
    width = 940,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
canvas.place(x = 0, y = 0)

#images 
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    235.0,
    226.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    470.0,
    229.0,
    image=image_image_2
)


#Buttons 
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=mainprog,
    relief="flat"
)
button_1.place(
    x=541.0,
    y=154.0,
    width=358.2591247558594,
    height=63.677249908447266
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=af,
    relief="flat"
)
button_2.place(
    x=541.0,
    y=257.0,
    width=358.2591247558594,
    height=63.677249908447266
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: webbrowser.open('Attendance'),
    relief="flat"
)
button_3.place(
    x=541.0,
    y=361.0,
    width=358.2591247558594,
    height=63.677249908447266
)


canvas.create_text(
    534.0,
    30.0,
    anchor="nw",
    text="FACIAL RECOGNITION\n            SYSTEM",
    fill="#000000",
    font=("Lato SemiBold", 32 * -1)
)

window.resizable(False, False)
window.mainloop()
