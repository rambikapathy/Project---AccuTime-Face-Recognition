"""
CMP3753M - REISIGANAN AMBIKAPATHY (AMB19705060)
FINAL PORTFOLIO (ACCUTIME ATTENDANCE SYSTEMS)
 
 
All of the code is implemented as one file, due to multiple ciruclation import errors that prevent the better use of the program, when code was segregated into individual files.
Upon feedback received from supervisor meetings, the task was to implement one code file that saw a working application.
 
For better comprehension of the code whilst marking, a code contents has been provided below, labeliing the main pillars of the code according to relevant line no.
To locate any functions or peices of code, control + F helped me to easily navigate through code without the need to scroll
 
Pip install commands, in any case of an execution error
 
pip install numpy
pip install pygame
pip install Pillow
pip install opencv-python
pip install cmake
pip install dlib
pip install face-recognition
pip3 install PySide6
pip install playsound
pip install pyttsx3
 
 
-----------------------CODE CONTENTS--------------------------
 
Task                                Line numbers
Quit/ Destroy windows               60-80
 
Progress/Verification Bar           98-117
 
Voice Assistance                    140-155
 
Insert Student data into database   210-260
 
Capture Student Image               280-350  
 
Convert Student Image into bytes    355-385
& store in database
 
Face encoding                       427-437
 
Log attendance of students in       444-457
csv file
 
Face recognition                    460-490
(Eucildean Algorithms)
 
Login Success window(MainMenu)      494-512
 
Database Initialization             560-579
 
Password Strength Scale             583-598
(for admin Register)
 
Adminstrator Register Form          604-654
 
Adminstrator Login Form             847-885
 
Main Window                         909-962
 
 
"""
 
 
#import neccessary libraries
#For GUI,Authentication system
from calendar import c
import tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import *
from tkinter import messagebox
from unicodedata import name
from PIL import ImageTk, Image, ImageDraw
import os
import pandas as pd
 
#For Database
import sqlite3
from sqlite3 import Error
 
#For real time clock
import time
from datetime import datetime
from tkinter import messagebox
 
#For camera (Open CV)
import cv2
import numpy as np
import face_recognition as fr
 
#For progressbar after succesfull user login
from tkinter import Label, Tk, Label
from time import sleep
 
#For OTP using twilio
#from twilio.rest import Client
 
#For voice assistance
import pyttsx3
 
#For Animated Gif
from PySide6.QtWidgets import QApplication, QWidget, QLabel
from PySide6.QtGui import QIcon, QMovie
 
 
#------------------Destroy root windows, once the next phase has been iniated
#Quit function  to exit application
def quit():
    root = Tk() #define the root window
    Button(root, text="Quit", command=quit).pack()
    root.mainloop()
 
# This function is designed to destroy the login form, once adminstrator inputs credentials to iniate Main Menu
def destroyLoginSuccess():
    cv2.destroyAllWindows()
 
# This function is designed to destroy the login form, once adminstrator inputs credentials to iniate Main Menu
def destroyregister():
    windowRegister.destroy()  
 
#Attempt at initiating Verification gif to improve user interaction using Qwidget
"""""
class VerifyGIF(QWidget):
    def __init__(self):
        super().__init__()
 
        self.setGeometry(200,200,750,500)
        self.setWindowTitle("Verifying")
 
        label = QLabel(self)
        global VerifyGIF
        VerifyGif = QMovie('verify.gif')
 
        label.setMovie(VerifyGif)
        VerifyGif.start()
 
"""
#------------------VerificationBar implementation
class VerificationBar:
    def __init__(self):
    #Define verification bar progress window
        self.root = Tk()
        self.root.config(bg="cadet blue")
        self.root.title("Verifying")
        self.root.geometry("750x500")
 
        #Iniaite verfication text through label
        Label(self.root, text = "Verifying.....",font=("Times New Roman", 20),
            bg="cadet blue", fg="black").place(x=325, y=160)
 
        #Load the progress block
        for i in range(16):
            Label(self.root, width=2, height=1).place(x=(i+10)*22, y=200)
 
        #Update root window upon animation
        self.root.update()
        self.loadAnime()
 
 
#Load the animation
    def loadAnime(self):
        for i in range(16):
            for j in range(16):
                #make block black
                Label(self.root, bg="black", width=2, height=1).place(x=(j+10)*22, y=200)              
                sleep(0.15)
                self.root.update_idletasks()
                #make block white:
                Label(self.root, bg="white",width=2, height=1).place(x=(j+10)*22, y=200)  
            return loginSuccess()
        self.root.mainloop()  
 
#------------------Voice Assistance implementation for visually impaired students
 
accuTimeVoice = pyttsx3.init() #Initialize text to spech converter library defined as accuTimeVoice
 
#Voice Assistance on Main  Menu
def voiceAssist():
    accuTimeVoice.say("Welcome to AccuTime")
    accuTimeVoice.say("The next phase will take you onto the student registration form")    
    accuTimeVoice.say("This consists of you inputting your full name, Student ID and course title")  
    accuTimeVoice.say("If you have already enrolled on to the system, please head over to Student Attendance Clock-in to log in your attendance")          
    accuTimeVoice.runAndWait()
    accuTimeVoice.stop()
 
#Voice Assistance on Student register window
def voiceAssist2():
    accuTimeVoice.say("Whilst training your image, please ensure the camera is well positoned and not affected by unfavourable lighting")
    accuTimeVoice.say("Inorder to capture and store your face to the image database, please ensure you enter the spacebar")  
    accuTimeVoice.say("Please ensure you key E to exit the registration form")                
    accuTimeVoice.runAndWait()
    accuTimeVoice.stop()    
 
#------------------Student Registration Form (located on Main menu)
def registerStudent():
    global windowRegisterStudent
    windowRegisterStudent = Toplevel(window) #iniate separate window for student registration
    windowRegisterStudent.title("Student Register")
    windowRegisterStudent.geometry("950x660")
 
    global StudentName
    global StudentSurname
    global courseName
    global studentID
    StudentName = StringVar()
    StudentSurname = StringVar()
    courseName = StringVar()
    studentID = StringVar()
 
    global StudentName_input #variable defined to store student's name
    global StudentSurname_input #variable defined to store student's surname
    global course_Input #variable defined to store student's course name
    global studentID_Input #variable defined to store student's ID
 
    Label(windowRegisterStudent,text = "Please register your details below (Students ONLY) ", fg = "Cornsilk",bg = "cadet blue", width = "100", height = "2", font = ("Times New Roman", 15)).pack()
    voiceAssist() #Activate first phase of voice recognition
    Label(windowRegisterStudent,text = "").pack()
 
    Label(windowRegisterStudent,text = "Student Name: ", width = 15, height = 1, font = ("Times New Roman", 12)).pack()
    StudentName_input = Entry(windowRegisterStudent,textvariable = StudentName)
    StudentName_input.pack()
 
    Label(windowRegisterStudent,text = "Student Surname: ", width = 15, height = 1, font = ("Times New Roman", 12)).pack()
    StudentSurname_input = Entry(windowRegisterStudent,textvariable = StudentSurname)
    StudentSurname_input.pack()
 
    Label(windowRegisterStudent,text = "Student ID No: ", width = 15, height = 1, font = ("Times New Roman", 12)).pack()
    studentID_Input = Entry(windowRegisterStudent,textvariable = studentID)
    studentID_Input.pack()
 
    Label(windowRegisterStudent,text = "Course Name ", width = 15, height = 1, font = ("Times New Roman", 12)).pack()
    course_Input = Entry(windowRegisterStudent,textvariable = courseName)
    course_Input.pack()
 
 #Instructions
    Label(windowRegisterStudent,text = "").pack()
    Label(windowRegisterStudent,text = "INSTRUCTIONS", fg = "black").pack()    
    Label(windowRegisterStudent,text = "Once 'Take Picture & Submit' button is pressed,face recording will be initiated", fg = "black").pack()
    Label(windowRegisterStudent,text = "Key ENTER to store as many images of your face to the database", fg = "black").pack()    
    Label(windowRegisterStudent,text = "Key E to exit the face recording, once registration is complete", fg = "black").pack()  
    Label(windowRegisterStudent,text = "").pack()
    #Button to capture student image
    Button(windowRegisterStudent,text = "Take Picture & Submit", command = takestudentpic, width = 25, height = 1,bg = "powder blue", font = ("Times New Roman", 12)).pack()
         
   
#------------------Inserting Student Registration Data into database (named Student)
def insertStudentData():
    global StudentName
    global StudentSurname
    global courseName
    global studentID
 
    global StudentName_input
    global StudentSurname_input
    global studentID_Input
    global course_Input
 
#Clone student's input from the registration entry box
    StudentName_Input = StudentName_input.get()
    StudentSurname_Input = StudentSurname_input.get()
    studentID_input = studentID_Input.get()
    course_input = course_Input.get()
 
#Once user keys submit, erase any data from the entry box
    StudentName_input.delete(0, END)
    StudentSurname_input.delete(0, END)
    studentID_Input.delete(0, END)
    course_Input.delete(0, END)
 
 #Open and Write user's input into the database
    data = open(StudentName_Input, "w")
    data.write(StudentSurname_Input)
    data.write(studentID_input)        
    data.write(course_input)
    data.close()
 
    Label (windowRegisterStudent,text = "Registration Successful", fg = "green", font = ("Times New Roman", 20)).pack()#output to student that their enrollment has been succesfull
    #define query to insert student entry from the Student Registration window into the database accordingly
    query = "INSERT INTO Student (studentName, studentLastName ,studentID , courseName ) VALUES (?, ?,?,?)" #VALUES are unknown(???), until user inputs into entry fields      
    cursor.execute(query, (StudentName_Input, StudentSurname_Input, studentID_input, course_input))
    conn.commit()
 
#Define directory of student image location
path = 'StudentImages'
images = []
classNames = []
ImageDir = os.listdir(path)
print(ImageDir)
for cl in ImageDir:
    #This section is relevant when user presses the Student Attendance Clock-in button that iniates face recogntion to log attendance.
    #By implenting the cv2.imread, it perfoms reading student's image file from the local database prior to the face identification process through matching images from the directory incontrast to the face detected in the camera
    cloneImage = cv2.imread(f'{path}/{cl}')#read student images prior to
    images.append(cloneImage)
    #os.path.splittext splits the pathname into the pair of root and ext
    classNames.append(os.path.splitext(cl)[0])
 
#------------------Capture, Train and store student's image in accordance with the provided data
def takestudentpic():
    #global variable declaration for the values student entered in the registration form
    global StudentName
    global StudentSurname
    global courseName
    global studentID
    global StudentName_input
    global StudentSurname_input
    global course_Input
    global studentID_Input
    global img_counter
 
    #Phase 2 of voice assitance giving the visually impaired student with concise instructions as to how to log attendance
    voiceAssist2()
    #Iniate the video camera from PC/laptop webcam to capture student facces
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Student Face Registration")
   
    #student face capture counter
    img_counter = 0
   
    while True:
        ret, frame = cam.read()
        if not ret: #If CV2 video camera cannot read, output error message
            print("failed to capture student image")
            break
        cv2.imshow("Student Face Registration", frame)
 
        k = cv2.waitKey(1)
 
        if k%256 == 32: #press spacebar to capture unlimited no of images
            global student
            student = "{},{},{}.png".format(StudentName_input.get(),studentID_Input.get(),img_counter)#Store the captured face of student in a particular format
            global writeImage
            writeImage = cv2.imwrite(student, frame)#write captured image to database/local drive
 
            #cv2.imwrite(student, frame)
            #location = 'StudentImages'
            #uploadImage = [os.path.join(location,store) for store in os.listdir(location)]
 
            print("{} image captured!Thankyou".format(student)) #Terminal output, not on application window
            img_counter += 1 #increase counter depending on the image take
        elif(cv2.waitKey(1)==ord('e')):#if student wishes to exit, key E
            break
 
    cam.release()#end face detection
    cv2.destroyAllWindows()#destroy cv2 window
 
#Clone student's input from the registration entry box
    StudentName_Input = StudentName_input.get()
    StudentSurname_Input = StudentSurname_input.get()
    studentID_input = studentID_Input.get()
    course_input = course_Input.get()
#Once user keys submit, erase any data from the entry box  
    StudentName_input.delete(0, END)
    StudentSurname_input.delete(0, END)
    studentID_Input.delete(0, END)
    course_Input.delete(0, END)
 
 #Write user's input into the database
    data = open(StudentName_Input, "w")
    data.write(StudentSurname_Input)
    data.write(studentID_input)        
    data.write(course_input)
    data.close()
 
    #image2BinaryASSERT()
    #Output enrollment success message to user whilst inserting the relevant student registration entry fields into database
    Label (windowRegisterStudent,text = "Enrollment Successful", fg = "green", font = ("Times New Roman", 20)).pack()
    query = "INSERT INTO Student (studentName, studentLastName ,studentID , courseName ) VALUES (?, ?,?,?)"      
    cursor.execute(query, (StudentName_Input, StudentSurname_Input, studentID_input, course_input))
    conn.commit()
'''
#------------------Convert captured student image into bytes then insert into database
#Image to be converted into binary (bytes) prior to its integration into student database
def image2BinaryREAD(filename):
    with open(filename, 'rb') as file:
        studentImage = file.read() #read student image prior to converting to binary
    return studentImage
 
def image2BinaryASSERT():#Once the image has been converted into bytes load into database
    AccuTimeDatabase = sqlite3.connect("Student.db")#connect with database (Student)
    data = AccuTimeDatabase.cursor()
   
    for image in student:
       insert_photo   = image2BinaryREAD(image)
       data.execute("INSERT INTO Image Values(:image)",#insert binary image
                 {'image': insert_photo })
 
    AccuTimeDatabase.commit()
    AccuTimeDatabase.close()#close
 
#Create database in database and table if it does not exist
''' 
def create_database():
    AccuTimeDatabase = sqlite3.connect("Student.db")
    data = AccuTimeDatabase.cursor()
 
    data.execute("CREATE TABLE IF NOT EXISTS Image(Image BLOB)")
 
    AccuTimeDatabase.commit()
    AccuTimeDatabase.close()
 
create_database()
 

    while True:
        ret, frame = video_capture.read()
        rgb_frame = frame[:, :, ::-1]
        face_locations = fr.face_locations(rgb_frame)
        face_encodings = fr.face_encodings(rgb_frame, face_locations)
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = fr.compare_faces(known_face_encondings, face_encoding)
            name = "Unknown"
            face_distances = fr.face_distance(known_face_encondings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
           
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom -35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        with open('attendanceReport.csv','r+') as FILE:
            allLines = FILE.readlines()
            attendanceList = []
            for line in allLines:
                entry = line.split(',')
                attendanceList.append(entry[0])
            if name not in attendanceList:
                now = datetime.now()
                dtString = now.strftime('%d/%b/%Y, %H:%M:%S')
                FILE.writelines(f'\n{name},{dtString}')              
           
 
        cv2.imshow('AccuTime FaceRecognition', frame)
       
 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
       
           
    video_capture.release()
    cv2.destroyAllWindows()  
"""
#------------------Face Encoding
# This function implements an algorithm in the form of Eucildean, to measure and contrast important features on faces
# This can be the contrast in colour or size, distances between both eyes, eyebrows and distance between mouth and nose
def training(images):
    encodeList = []
 
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = fr.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
 
#------------------Initiate csv file to log student attendance
def studentAttendance(name):
    with open('attendanceReport.csv','r+') as FILE:    
        allLines = FILE.readlines() #read all lines in file        
        #name = "Unknown"
        attendanceList = [] #declare list literal
        for line in allLines:
            entry = line.split(',') #split any string into array of substring
            attendanceList.append(entry[0])#apply to csv
        if name not in attendanceList:
            now = datetime.now()
            dtString = now.strftime('%d/%b/%Y, %H:%M:%S')
            FILE.write("Student Name, Date, Time")#write headers in csv files
            FILE.writelines(f'\n{name},{dtString}')  #write students who have attended to the csv file
 
#------------------Attendance marking through face recogniton (Eucildean Algorithms)
def attendanceClockIn():
    encodeListKnown = training(images) #if the algorithms identify student image through encoding, train the images
    cap = cv2.VideoCapture(0)
 
    while True:
        success, img = cap.read()#read student face from camera
        capturingImage = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        capturingImage = cv2.cvtColor(capturingImage, cv2.COLOR_BGR2RGB)#convert image to colour(RGB)
        studentFrame = fr.face_locations(capturingImage)
        Eframe = fr.face_encodings(capturingImage, studentFrame)
        for encodeFace, faceLoc in zip(Eframe, studentFrame):
#the effect of the (Eucildean Algorithms) is seen here, on the principle that the greatest common divisor of two values does not alter if the larger number is replaced by its difference with the smaller number
            compare = fr.compare_faces(encodeListKnown, encodeFace)
            faceDis = fr.face_distance(encodeListKnown, encodeFace)
            matchImage = np.argmin(faceDis)
            if compare[matchImage]:
                name = classNames[matchImage].upper()
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)#draws a rectangle if face is identified according to the size of student's face
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                studentAttendance(name)  
           
            cv2.imshow('AccuTime Recognition', img)
            if(cv2.waitKey(1)==ord('e')):#exit
                cv2.destroyAllWindows()
 
#------------------Login Success Window leading to Main Menu for Student to enrol or log their attendance              
def loginSuccess():
    global windowloginSuccess
    windowloginSuccess = Toplevel(window)
    Label(windowloginSuccess,text = " ", width = 15, height = 1, font = ("Times New Roman", 12)).pack()
    windowloginSuccess.title("Authentication Success")
    Label(windowloginSuccess,text = " ", width = 15, height = 1, font = ("Times New Roman", 12)).pack()
    windowloginSuccess.geometry("750x500")
    Label(windowloginSuccess,text = "Admin login successful", fg = "green", font = ("Times New Roman", 13)).pack()
    Label(windowloginSuccess,text = " ", width = 15, height = 1, font = ("Times New Roman", 12)).pack()
    Label(windowloginSuccess,text = "Main Menu", fg = "cadet blue", font = ("Times New Roman", 28)).pack()
    Label(windowloginSuccess,text = " ", width = 15, height = 1, font = ("Times New Roman", 12)).pack()
    Button(windowloginSuccess,text = "Register Student", command = registerStudent, width = 25, height = 1,bg = "powder blue", font = ("Times New Roman", 15)).pack()
    Label(windowloginSuccess,text = " ", width = 15, height = 1, font = ("Times New Roman", 12)).pack()
    Button(windowloginSuccess,text = "Student Attendance Clock-in", command = attendanceClockIn, width = 25, height = 1,bg = "powder blue", font = ("Times New Roman", 15)).pack()
    Label(windowloginSuccess,text = " ", width = 15, height = 1, font = ("Times New Roman", 12)).pack()
    #Button(windowloginSuccess,text = "Attendance Report", command = attendanceCSVviewer, width = 25, height = 1,bg = "powder blue", font = ("Times New Roman", 15)).pack()
    Label(windowloginSuccess,text = " ", width = 15, height = 1, font = ("Times New Roman", 12)).pack()
    video_capture = cv2.VideoCapture(0)
    Button(windowloginSuccess,text = "Exit", command = window.destroy, width = 25, height = 1,bg = "powder blue", font = ("Times New Roman", 15)).pack()
 
#------------------HaarCascade Implementation for face recognition using grey scale (was a backup method should Euclidean algorithm fail to identify students)
 
#    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#    cap = cv2.VideoCapture(0)
   
#    while(True):
        #Capture frame by frame in grey scale
#        cam, frame = cap.read()
#        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #GREY SCALE IMPLEMENTATION
#        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5 )
#        for (x,y,w,h) in faces:
#            print(x,y,w,h)
#            #roi(region of interest)
#            #pixel is taking y values and y+h values to
#            roi_gray = gray[y:y+h, x:x+w]
#            roi_colour = frame[y:y+h, x:x+w]
#            
        #recognize the faces whilst saving the student image
#           img_item = "student-image.png"
#            cv2.imwrite(img_item, roi_gray) # WRITE REGION OF INTEREST
   
#            colour = (255,0,0) #BGR 0-255 colour for rectangle
        #Rectangle thickness
#            thickness = 2
        #Rectangle coordinates
#            end_CordX = x+w
#            end_CordY = y+h
#            cv2.rectangle(frame, (x,y), (end_CordX,end_CordY), colour, thickness)    
   
        #Display resulting frame of captured student image in colour scale
       # cv2.imshow('frame', frame)
        #if cv2.waitKey(20) & 0xFF == ord('q'): #BREAK LOOP
         #   break
   
    #When student frame is captured, release the capture
   # cap.release()
 
#The next functions outline the label for notifying adminstrators if they had entered incorrect, unmatchable details
def incorrectPW():
    Label(windowLogin,text = "Passcode Incorrect", fg = "red", font = ("Times New Roman", 20)).pack()
 
def userUnfound():
    Label(windowLogin,text = "User not found", fg = "red", font = ("Times New Roman", 20)).pack()
 
#------------------Database initalization (Admins)
#This method establishes a connection within a database for Adminstrators
def create_AdminTable():
    query = "DROP TABLE IF EXISTS Admin"#DROP ANY EXISTING TABLES
    cursor.execute(query)
    #.commit - Reserves the changes that have been altered within
    conn.commit()
   
   #CREATE TABLE
    query = "CREATE TABLE Admin(firstName VARCHAR, lastName VARCHAR,username VARCHAR UNIQUE, passcode VARCHAR)"
    cursor.execute(query)
    conn.commit()
 
    query = "DROP TABLE IF EXISTS Student"
    cursor.execute(query)
    conn.commit()
   
    query = "CREATE TABLE Student(studentName VARCHAR, studentLastName VARCHAR,studentID VARCHAR UNIQUE, courseName VARCHAR)"
    cursor.execute(query)
    conn.commit()
 
#------------------Password Strength scale
def passcodeStrength(passcode):
   
    special_char = list('$%£&@*')
    num_char = any(char.isdigit() for char in passcode)
    upper_char = any(char.isupper() for char in passcode)
    specialUpper_char = any(char.isdigit() for char in passcode)
    lower_char = any(char.islower() for char in passcode)
 
    valid = all([num_char, upper_char,specialUpper_char,lower_char])#consider all arguments for strong password
    if len(passcode)<4: # if character for password is less than 4 output weak
        return "Weak Passcode"
    elif len(passcode)>=6 and valid: #if character is above 6, then output strong
        return "Strong Passcode"
    else:
        return "Average Passcode"#else average
 
#------------------Adminstrator register page
def adminstratorRegister():
    global username_input
    global passcode_input
    global confirmPasscode
    global firstName
    global lastName
    global firstName_input
    global lastName_input
    global confirmPasscode_input
 
    username_input = username.get()
    passcode_input = passcode.get()
    firstName_input = firstName.get()
    lastName_input = lastName.get()
    confirmPasscode_input = confirmPasscode.get()
 #Write user's input into the database
    data = open(username_input, "w")
    data.write(firstName_input)
    data.write(lastName_input)        
    data.write(username_input)
    data.write(passcode_input)
    data.close()
 
 #Password verifyer.
 #If password and confirm password is not the same,print error.
    if passcode.get() == confirmPasscode.get():
        print("")
    else:
        messagebox.showerror("Error", "Passcode does not match")
#If any of the values are missing , throw an error to complete all fields
    if passcode.get() == "" or confirmPasscode.get() == "" or firstName.get() == "" or lastName.get() == "" or username.get()== "":
        messagebox.showerror("Error", "Please complete all required fields")
        if passcode.get() == confirmPasscode.get():
            print("")
        else:
            messagebox.showerror("Error", "Passcode does not match")        
    else:
        #Removes any strings on Admin register page once submit button is entered
        username_Input.delete(0, END)
        passcode_Input.delete(0, END)
        firstName_Input.delete(0, END)
        lastName_Input.delete(0, END)
        confirmPasscode_Input.delete(0, END)
 
        strength = passcodeStrength(passcode_input)#outputs the strength of the password once user submits their credentials
        Label (windowRegister,text = "Passcode is {}".format(strength), fg = "Black", font = ("Times New Roman", 14)).pack()    
        Label (windowRegister,text = "Registration Successful", fg = "green", font = ("Times New Roman", 20)).pack()
        query = "INSERT INTO Admin (firstName, lastName, username, passcode) VALUES (?, ?,?,?)"    #Stores data as query into database  
        cursor.execute(query, (firstName_input, lastName_input, username_input, passcode_input))
        conn.commit()    
 
#------------------Adminstrator Login page
def adminstratorLogin():
    global username_authenticate
    global passcode_authenticate
    username_authenticate = username_validation.get()
    passcode_authenticate = passcode_validation.get()
 
    if username_validation.get() == "" or passcode_validation.get() == "":
        messagebox.showerror("Error", "Please complete all required fields")
    else:
        datalist = os.listdir()#look for all users in the datalist
        if username_authenticate in datalist:
            data1 = open(username_authenticate, "r")
            #Start to read the lines, if user is already registered in the database,.
            verify = data1.read().splitlines()
            if passcode_authenticate in username_authenticate:
                #If password matches according to the username, open verfication/progress bar
                if __name__=='__main__':
                    VerificationBar()
                    windowLogin.destroy()#destroy any other windows that are open
 
            else:
                incorrectPW()#else paswsword is incorrect
                #windowLogin.destroy()
        else:
            userUnfound()#else user not found
            #windowLogin.destroy()
 
#Reset buttons should user enter any wrong values into entry box
def adminstratorReset():
    username_validation.set("")
    passcode_validation.set("")
 
def adminstratorReset1():
    username.set("")
    passcode.set("")
    confirmPasscode.set("")
    firstName.set("")
    lastName.set("")
 
#Exit button
def adminstratorExit():
    exit = tkinter.messagebox.askyesno("Exit","Please confirm to exit?")
    if exit > 0:
        window.destroy()
    else:
        return
 
#Adminstrator Registration window
def AdminRegisterWindow():
    global windowRegister
    windowRegister = Toplevel(window)
    windowRegister.title("Register")
    windowRegister.geometry("950x660")  
 
    #Initialize the Global string variables for Username and Password
    global username
    global passcode
    global confirmPasscode
    global firstName
    global lastName
    global select_gender
    firstName = StringVar()
    lastName = StringVar()
    username = StringVar()
    passcode = StringVar()
    confirmPasscode = StringVar()
 
    global firstName_Input
    global lastName_Input
    global confirmPasscode_Input
 
    #Global string variables for user's input for username and password on register window
    global username_Input
    global passcode_Input
    Label(windowRegister,text = "Please register your details below (Adminstrator ONLY) ", fg = "Cornsilk",bg = "cadet blue", width = "100", height = "2", font = ("Times New Roman", 15)).pack()
    Label(windowRegister,text = "").pack()
 
    #Adminstrator to input first name
    Label(windowRegister,text = "First Name: ", width = 15, height = 1, font = ("Times New Roman", 12)).pack()
    firstName_Input = Entry(windowRegister,textvariable = firstName)
    firstName_Input.pack()
   
    #Adminstrator to input last name
    Label(windowRegister,text = "Last Name: ", width = 15, height = 1, font = ("Times New Roman", 12)).pack()
    lastName_Input = Entry(windowRegister,textvariable = lastName)
    lastName_Input.pack()
 
    #Adminstrator to input username
    Label(windowRegister,text = "Username: ", width = 15, height = 1, font = ("Times New Roman", 12)).pack()
    username_Input = Entry(windowRegister,textvariable = username)
    username_Input.pack()
 
    #Adminstrator to input password
    Label(windowRegister,text = "Passcode: ", width = 15, height = 1, font = ("Times New Roman", 12)).pack()
    Label(windowRegister,text = "Passcode must contain upper,lower case and special values for strong passcode", fg = "red").pack()    
    passcode_Input = Entry(windowRegister,textvariable = passcode, show = "*")
    passcode_Input.pack()
 
    #Adminstrator to confirm password
    Label(windowRegister,text = "Confirm Passcode: ", width = 15, height = 1, font = ("Times New Roman", 12)).pack()    
    confirmPasscode_Input = Entry(windowRegister,textvariable = confirmPasscode, show = "*")
    confirmPasscode_Input.pack()
    #passcodeStrength(passcode)
   
    #Terms & Conditions
    checkBox =Checkbutton(windowRegister, text="I Agree to all the Terms & Conditions!").pack()
 
 
    Label(windowRegister,text = "").pack()
    Button(windowRegister,text = "Register", width = 25, height = 1,bg = "powder blue", font = ("Times New Roman", 12), command = adminstratorRegister).pack()
    Label(windowRegister,text = "").pack()
    Button(windowRegister,text = "Login", width = 25, height = 1,bg = "powder blue", font = ("Times New Roman", 12), command = AdminLoginWindow).pack()
    Label(windowRegister,text = "").pack()
    Button(windowRegister,text = "Reset", width = 25, height = 1,bg = "powder blue", font = ("Times New Roman", 12), command = adminstratorReset1).pack()
    Label(windowRegister,text = "").pack()
    Button(windowRegister,text = "Exit", width = 25, height = 1,bg = "powder blue", font = ("Times New Roman", 12), command = adminstratorExit).pack()
 
 
#CLock on Adminstrator registration page
    def clock2():
        hour = time.strftime("%I")
        minute = time.strftime("%M")
        second = time.strftime("%S")
        day = time.strftime("%A")
        am_pm = time.strftime("%p")
        time_zone = time.strftime("%Z")
 
        register_label.config(text=hour + ":" + minute + ":" + second + " " + am_pm)
        register_label.after(1000, clock2)
 
    def update():
        register_label.config(text="New Text")
    register_label = Label(windowRegister, text="", font=("Times New Roman", 13), fg="cadet blue")
    register_label.pack(pady=20)
 
    clock2()    
 
 
#----------------Update database for users who have forgotten password
#def forgotPasscodeTable():
#    if username_Entry.get=='' and passcode_Entry.get=='' and passcode_Entry_Confirm.get=='':
#        messagebox.showerror('Please complete all fields')
#    else:
#        con= sqlite3.connect("Admin.db")
#        cur = con.cursor()
 
    #query = "INSERT INTO students (username, passcode) VALUES (?, ?)"      
    #cursor.execute(query, (username_input, passcode_input))
    #conn.commit()
 
#        cur.execute("UPDATE Admin SET passcode=%s WHERE username=%s",(passcode_Entry.get(),username_Entry.get()))  
#        con.commit()
#        con.close()
#        messagebox.showinfo("Passcode changed successfuly")
 
# Window for forgot passcode
#def forgotPasscode():
#    global forgetwindow
#    global username_Entry
#    global passcode_Entry
#    global passcode_Entry_Confirm
#    forgetwindow=Toplevel(window)
#    forgetwindow.title("Forget Password")
#    forgetwindow.geometry("750x500")
   
#    username_Entry = StringVar()
#    passcode_Entry = StringVar()
#    passcode_Entry_Confirm = StringVar()  
   
#    Label(forgetwindow,text = "").pack()
#    Label(forgetwindow, text="Username",font=("Times New Roman", 15)).pack()
#    usernameEntry = Entry(forgetwindow,textvariable = username_Entry)
   
#    usernameEntry.pack()
#    Label(forgetwindow,text = "").pack()    
#    Label(forgetwindow,text = "New Passcode: ", font = ("Times New Roman", 15)).pack()        
#    passcodeEntry = Entry(forgetwindow,textvariable = passcode_Entry,show = "*")
#    passcodeEntry.pack()
#    Label(forgetwindow,text = "").pack()
#    Label(forgetwindow,text = "Confirm New Passcode: ", font = ("Times New Roman", 15)).pack()    
#    passcodeEntry_Confirm = Entry(forgetwindow,textvariable = passcode_Entry_Confirm,show = "*")
#    passcodeEntry_Confirm.pack()
#    Label(forgetwindow,text = "").pack()
#    Button(forgetwindow,text = "Change Passcode",bd=5,activebackground= "light green", command = lambda:forgotPasscodeTable()).pack()
#    Label(forgetwindow,text = "").pack()
 
 
#Assigning the funcitonalites for buttons on login window
def AdminLoginWindow():
    #global variable for login window
    global windowLogin
    global username_validation
    global passcode_validation
    #global variable for user's entry on login window
    global username_validate
    global passcode_validate
    windowLogin = Toplevel(window)
 
    windowLogin.title("Login")
    windowLogin.geometry("950x660")
    Label(windowLogin,text = "Please login your details below (Adminstrator ONLY)", fg = "Cornsilk",bg = "cadet blue", width = "300", height = "5", font = ("Times New Roman", 15)).pack()
    Label(windowLogin,text = "").pack()
    username_validation = StringVar()
    passcode_validation = StringVar()  
 
    #Student to input username
    Label(windowLogin,text = "Username: ", font = ("Times New Roman", 15)).pack()
    username_validate = Entry(windowLogin, textvariable = username_validation)
    username_validate.pack()
    Label(windowLogin,text = "").pack()
 
    #Student to input password    
    Label(windowLogin,text = "Passcode: ", font = ("Times New Roman", 15)).pack()
    passcode_validate = Entry(windowLogin, textvariable = passcode_validation,show = "*")
    passcode_validate.pack()
    Label(windowLogin,text = "").pack()
    Button(windowLogin,text = "Login", width = 25, height = 2,bg = "powder blue", font = ("Times New Roman", 12), command = adminstratorLogin).pack()
    #Button(windowLogin,text = "forgot Password?", bd=0, width = 0, height = 2, font = ("Times New Roman", 9), command = forgotPasscode).pack()
 
    Button(windowLogin,text = "New User Register", width = 25, height = 2,bg = "powder blue", font = ("Times New Roman", 12), command = AdminRegisterWindow ).pack()  
    #newregister_btn = PhotoImage(file=r"E:\FRAS\Images GUI\register.png")
    #img_label = Label(image=newregister_btn)
    #Button(windowLogin,image=newregister_btn,width = "212", height = "70", command = AdminRegisterWindow).pack()
    #Label(text = "").pack()
 
    Button(windowLogin,text = "Reset", width = 25, height = 2,bg = "powder blue", font = ("Times New Roman", 12), command = adminstratorReset).pack()
    Button(windowLogin,text = "Exit", width = 25, height = 2,bg = "powder blue", font = ("Times New Roman", 12), command = adminstratorExit).pack()
 
 
#CLock on Adminstrator login page  
    def clock1():
        hour = time.strftime("%I")
        minute = time.strftime("%M")
        second = time.strftime("%S")
        day = time.strftime("%A")
        am_pm = time.strftime("%p")
        time_zone = time.strftime("%Z")
 
        login_label.config(text=hour + ":" + minute + ":" + second + " " + am_pm)
        login_label.after(1000, clock1)
 
    def update():
        login_label.config(text="New Text")
    login_label = Label(windowLogin, text="", font=("Times New Roman", 13), bg="cadet blue")
    login_label.pack(pady=20)
 
    clock1()
 
 
#Main Window
def main_window():
    #Globalise the window variable
    global window
    #initialize tkinter
    window = Tk()
   
    bg=ImageTk.PhotoImage(file=r"E:\FRAS\Images GUI\AccuTime.jpg")
    mw_bg=Label(window,image=bg)
    mw_bg.place(x=0,y=0, relwidth=1,relheight=1)
 
    #Set size of login window
    window.geometry("950x660")
    #Store notes
    window.title("Face Recognition Attendance System")
    #Set the font and size
    #bg refers to background colour of text
    Label(text = "Welcome to AccuTime Attendance Systems", fg = "Cornsilk",bg = "teal", width = "100", height = "5", font = ("Times New Roman", 25)).pack()
    #Create a blank label
    Label(text = "").pack()
   
    #Login Button for registered admins
    login_btn = PhotoImage(file=r"E:\FRAS\Images GUI\login.png")
    img_label = Label(image=login_btn)
    Button(image=login_btn,width = "200", height = "70", command = AdminLoginWindow).pack()
    Label(text = "").pack()    
 
    #Registration Button for new admins
    register_btn = PhotoImage(file=r"E:\FRAS\Images GUI\register.png")
    img_label = Label(image=register_btn)
    Button(image=register_btn,width = "212", height = "70", command = AdminRegisterWindow).pack()
    Label(text = "").pack()
   
    #Clock on Main menu
    def clock():
        hour = time.strftime("%I")
        minute = time.strftime("%M")
        second = time.strftime("%S")
        day = time.strftime("%A")
        am_pm = time.strftime("%p")
        time_zone = time.strftime("%Z")
 
        my_label.config(text=hour + ":" + minute + ":" + second + " " + am_pm)
        my_label.after(1000, clock)
 
    def update():
        my_label.config(text="New Text")
 
 
    my_label = Label(window, text="", font=("Times New Roman", 30), bg="teal",fg="Cornsilk")
    my_label.pack(pady=20)
 
    clock()
 
#Tells python to run the tkinter for login/register events in loops
#This is a method that acknowledges button clicks and blocks codes that come after closing the login/register window
 
    window.mainloop()
 
conn = sqlite3.connect("Student.db")
# SQLite3 cursor is a cursor method of the connection object. A cursor object is requried to be initiated to executes SQLite statements.
cursor = conn.cursor()  
create_AdminTable()  
 
main_window()
#otp_verfication()
 
cursor.close()
conn.close()
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 

