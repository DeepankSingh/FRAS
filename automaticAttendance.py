# Import necessary modules for GUI, file handling, image processing, etc.
import tkinter as tk
from tkinter import *
import os, cv2
import pandas as pd
import datetime
import time
from utils import create_button

# Define file paths
haarcasecade_path = "haarcascade_frontalface_default.xml"  # Path for face detection model
trainimagelabel_path = "TrainingImageLabel\\Trainner.yml"  # Path to the trained recognizer model
trainimage_path = "TrainingImage"  # Path where training images are stored
studentdetail_path = "StudentDetails\\studentdetails.csv"  # Path of CSV containing student details
attendance_path = "Attendance"  # Folder to store attendance records

# Function to choose subject and fill attendance
def subjectChoose(text_to_speech):

    # Inner function to perform face recognition and mark attendance
    def FillAttendance():
        sub = tx.get()
        now = time.time()
        future = now + 20

        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            try:
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                try:
                    recognizer.read(trainimagelabel_path)
                except:
                    e = "Model not found, please train model"
                    Notifica.configure(
                        text=e,
                        bg="black",
                        fg="yellow",
                        width=33,
                        font=("times", 15, "bold"),
                    )
                    Notifica.place(x=20, y=250)
                    text_to_speech(e)
                    return

                facecasCade = cv2.CascadeClassifier(haarcasecade_path)
                df = pd.read_csv(studentdetail_path)

                cam = cv2.VideoCapture(0)
                font = cv2.FONT_HERSHEY_SIMPLEX

                col_names = ["Enrollment", "Name"]
                attendance = pd.DataFrame(columns=col_names)
                face_found = False  # New flag

                while True:
                    ___, im = cam.read()
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = facecasCade.detectMultiScale(gray, 1.2, 5)

                    for (x, y, w, h) in faces:
                        Id, conf = recognizer.predict(gray[y:y+h, x:x+w])

                        if conf < 70:
                            face_found = True
                            Subject = tx.get()
                            ts = time.time()
                            date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")

                            aa = df.loc[df["Enrollment"] == Id]["Name"].values
                            tt = str(Id) + "-" + str(aa)

                            attendance.loc[len(attendance)] = [Id, aa]

                            cv2.rectangle(im, (x, y), (x+w, y+h), (0, 260, 0), 4)
                            cv2.putText(im, str(tt), (x+h, y), font, 1, (255, 255, 0), 4)
                        else:
                            Id = "Unknown"
                            tt = str(Id)
                            cv2.rectangle(im, (x, y), (x+w, y+h), (0, 25, 255), 7)
                            cv2.putText(im, str(tt), (x+h, y), font, 1, (0, 25, 255), 4)

                    if time.time() > future:
                        break

                    attendance = attendance.drop_duplicates(["Enrollment"], keep="first")
                    cv2.imshow("Filling Attendance...", im)
                    key = cv2.waitKey(30) & 0xFF
                    if key == 27:
                        break

                cam.release()
                cv2.destroyAllWindows()

                # If no face found, exit early
                if not face_found or attendance.empty:
                    msg = "No face found for attendance."
                    Notifica.configure(
                        text=msg,
                        bg="black",
                        fg="yellow",
                        width=33,
                        font=("times", 15, "bold"),
                    )
                    Notifica.place(x=620, y=250)
                    text_to_speech(msg)
                    return

                ts = time.time()
                attendance[date] = 1
                date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                Hour, Minute, Second = timeStamp.split(":")

                path = os.path.join(attendance_path, Subject)
                if not os.path.exists(path):
                    os.makedirs(path)

                fileName = (
                    f"{path}/"
                    + Subject
                    + "_"
                    + date
                    + "_"
                    + Hour
                    + "-"
                    + Minute
                    + "-"
                    + Second
                    + ".csv"
                )

                attendance = attendance.drop_duplicates(["Enrollment"], keep="first")
                attendance.to_csv(fileName, index=False)

                m = "Attendance Filled Successfully of " + Subject
                Notifica.configure(
                    text=m,
                    bg="#4A90E2",
                    fg="#FFFFFF",
                    width=33,
                    relief=RIDGE,
                    bd=0,
                    font=("times", 15, "bold"),
                )
                text_to_speech(m)
                Notifica.place(x=620, y=250)

            # Show attendance in a popup only if there is valid data
                import csv
                import tkinter

                root = tkinter.Tk()
                root.title("Attendance of " + Subject)
                root.configure(background="black")

                cs = os.path.join(path, fileName)

                with open(cs, newline="") as file:
                    reader = csv.reader(file)
                    r = 0
                    for col in reader:
                        c = 0
                        for row in col:
                            label = tkinter.Label(
                                root,
                                width=10,
                            height=1,
                            fg="yellow",
                            font=("times", 15, " bold "),
                            bg="black",
                            text=row,
                            relief=tkinter.RIDGE,
                            )
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()

            except Exception as e:
                print("Error:", e)
                text_to_speech("Something went wrong. Please try again.")
                cv2.destroyAllWindows()

    # GUI window to enter subject name
    subject = Tk()
    subject.title("Subject...")
    subject.attributes("-fullscreen", True)
    subject.configure(background="#4A90E2")

    # Header label
    titl = tk.Label(subject, bg="#4A90E2", relief=RIDGE, bd=0, font=("arial", 30))
    titl.pack(fill=X)

    # Instruction label
    titl = tk.Label(
        subject,
        text="Enter the Subject Name",
        bg="#4A90E2",
        fg="#FFFFFF",
        font=("arial", 25),
    )
    titl.place(x=570, y=10)

    # Notification label (hidden by default)
    Notifica = tk.Label(
        subject,
        text="Attendance filled Successfully",
        bg="#4A90E2",
        fg="#FFFFFF",
        width=33,
        height=2,
        font=("Segoe UI", 15, "bold"),
    )

    # # Function to open attendance folder for entered subject
    # def Attf():
    #     sub = tx.get()
    #     if sub == "":
    #         t = "Please enter the subject name!!!"
    #         text_to_speech(t)
    #     else:
    #         os.startfile(f"Attendance\\{sub}")

    

    # Subject entry label (updated)
    sub = tk.Label(
        subject,
        text="Enter Subject",
        bg="#4A90E2",
        fg="#FFFFFF",
        font=("Segoe UI", 20, "bold"),
        width=13,
        height=2
    )
    sub.place(x=510, y=150)

    # Entry field to input subject name
    tx = tk.Entry(
        subject,
        width=15,
        bd=0,
        bg="#FFFFFF",
        fg="black",
        relief=RIDGE,
        font=("times", 30, "bold"),
    )
    tx.place(x=710, y=165)

    # Button to start attendance process

    create_button(subject,"Fill Attendance", FillAttendance, x=500, y=500)

    # fill_a = tk.Button(
    #     subject,
    #     text="Fill Attendance",
    #     command=FillAttendance,
    #     bd=7,
    #     font=("times new roman", 15),
    #     bg="black",
    #     fg="yellow",
    #     height=2,
    #     width=12,
    #     relief=RIDGE,
    # )
    # fill_a.place(x=195, y=170)

    # Button - Exit the application
    create_button(subject, "Back", subject.destroy, x=500, y=700)


    subject.mainloop()  # Start the GUI loop



