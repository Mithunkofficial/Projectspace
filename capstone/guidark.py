import os
import csv
import shutil
import cv2 as cv
import webbrowser
import tkinter as tk
import face_recognition as fr
import numpy as np

from pathlib import Path
from tkinter import filedialog
from datetime import datetime, date
from tkinter import Tk, Canvas,Button, PhotoImage

window = Tk()
window.geometry("987x577")
window.resizable(False, False)
window.configure(bg = "#000000")
window.title("Facial Recognition System")
ti = PhotoImage(file='assets\\title\log.png')
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


            #creating excel file
            with open('Attendance.csv', 'w') as file:
                csv_writer = csv.writer(file)


            #marking entry with name, time, date
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
        print("Attendance updated to -> "+d)
        
        
    except:
        window = Tk()
        window.geometry("987x577")
        window.configure(bg = '#000000')
        window.title("Facial Recognition System")
        
        w = tk.Label(window, text="You have uploaded non-face images.\n Please delete it.",
                     font=("Lato SemiBold", 32 * -1), bg='black', fg='white')
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
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

canvas = Canvas(
    window,
    bg = "#000000",
    height = 577,
    width = 987,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
canvas.place(x = 0, y = 0)


#Images
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    759.0,
    288.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    70.0,
    288.0,
    image=image_image_2
)


#Buttons
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    bg='black',
    highlightthickness=0,
    command=lambda: webbrowser.open('assets\\faces'),
    relief="flat"
)
button_1.place(
    x=133.0,
    y=422.0,
    width=361.0,
    height=89.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    bg='black',
    highlightthickness=0,
    command=lambda: webbrowser.open('Attendance'),
    relief="flat"
)
button_2.place(
    x=133.0,
    y=303.0,
    width=361.0,
    height=88.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    bg='black',
    highlightthickness=0,
    command=af,
    relief="flat"
)
button_3.place(
    x=133.0,
    y=183.00006103515625,
    width=361.0,
    height=89.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    bg='black',
    highlightthickness=0,
    command=mainprog,
    relief="flat"
)
button_4.place(
    x=133.0,
    y=65.0,
    width=361.0,
    height=88.0
)


window.mainloop()