import tkinter as tk
import pandas as pd
import datetime
import time
from utils import center_window

# Capture current date and time
ts = time.time()
Date = datetime.datetime.fromtimestamp(ts).strftime("%Y_%m_%d")
timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
Time = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
Hour, Minute, Second = timeStamp.split(":")

# Dictionary to store attendance data
d = {}
index = 0

# GUI function to manually fill attendance
def manually_fill():
    global sb
    sb = tk.Tk()
    sb.iconbitmap("AMS.ico")
    sb.title("Enter subject name...")
    sb.geometry("580x320")
    center_window(sb, 580, 320)
    sb.configure(background="snow")
    

    # Error window if subject name is not entered
    def err_screen_for_subject():
        def ec_delete():
            ec.destroy()

        global ec
        ec = tk.Tk()
        ec.geometry("300x100")
        ec.iconbitmap("AMS.ico")
        ec.title("Warning!!")
        ec.configure(background="snow")
        tk.Label(
            ec, text="Please enter subject name!!!", fg="red", bg="white", font=("times", 16, " bold ")
        ).pack()
        tk.Button(
            ec, text="OK", command=ec_delete, fg="black", bg="lawn green",
            width=9, height=1, activebackground="Red", font=("times", 15, " bold ")
        ).place(x=90, y=50)

    # Function to proceed with filling attendance after subject name is entered
    def fill_attendance():
        global subb
        subb = SUB_ENTRY.get()

        # If subject name is empty, show error
        if subb == "":
            err_screen_for_subject()
        else:
            sb.destroy()

            # Create new window for filling attendance manually
            MFW = tk.Tk()
            MFW.iconbitmap("AMS.ico")
            MFW.title("Manually attendance of " + str(subb))
            MFW.attributes("-fullscreen",True)
            MFW.configure(background="snow")

            # Show error if enrollment or name is not entered
            def err_screen1():
                def del_errsc2():
                    errsc2.destroy()

                global errsc2
                errsc2 = tk.Tk()
                errsc2.geometry("330x100")
                errsc2.iconbitmap("AMS.ico")
                errsc2.title("Warning!!")
                errsc2.configure(background="snow")
                tk.Label(
                    errsc2,
                    text="Please enter Student & Enrollment!!!",
                    fg="red", bg="white",
                    font=("times", 16, " bold ")
                ).pack()
                tk.Button(
                    errsc2, text="OK", command=del_errsc2,
                    fg="black", bg="lawn green",
                    width=9, height=1,
                    activebackground="Red", font=("times", 15, " bold ")
                ).place(x=90, y=50)

            # Validation function to allow only digits in enrollment field
            def testVal(inStr, acttyp):
                if acttyp == "1":  # insert
                    return inStr.isdigit()
                return True

            # Labels for enrollment and student name
            ENR = tk.Label(MFW, text="Enter Enrollment", width=15, height=2, fg="white",
                           bg="blue2", font=("times", 15, " bold "))
            ENR.place(x=30, y=100)

            STU_NAME = tk.Label(MFW, text="Enter Student name", width=15, height=2, fg="white",
                                bg="blue2", font=("times", 15, " bold "))
            STU_NAME.place(x=30, y=200)

            # Entry for enrollment number
            global ENR_ENTRY
            ENR_ENTRY = tk.Entry(MFW, width=20, validate="key", bg="yel low",
                                 fg="red", font=("times", 23, " bold "))
            ENR_ENTRY["validatecommand"] = (ENR_ENTRY.register(testVal), "%P", "%d")
            ENR_ENTRY.place(x=290, y=105)

            # Entry for student name
            STUDENT_ENTRY = tk.Entry(MFW, width=20, bg="yellow", fg="red", font=("times", 23, " bold "))
            STUDENT_ENTRY.place(x=290, y=205)

            # Clear buttons
            def remove_enr():
                ENR_ENTRY.delete(first=0, last=22)

            def remove_student():
                STUDENT_ENTRY.delete(first=0, last=22)

            # Store data in dictionary
            def enter_data_DB():
                global index, d
                ENROLLMENT = ENR_ENTRY.get()
                STUDENT = STUDENT_ENTRY.get()
                if ENROLLMENT == "" or STUDENT == "":
                    err_screen1()
                else:
                    d[index] = {"Enrollment": ENROLLMENT, "Name": STUDENT, Date: 1}
                    index += 1
                    ENR_ENTRY.delete(0, "end")
                    STUDENT_ENTRY.delete(0, "end")
                    print(d)  # Debug print

            # Convert dictionary data to CSV
            def create_csv():
                df = pd.DataFrame.from_dict(d, orient='index')
                csv_name = f"Attendance(Manually)/{subb}_{Date}_{Hour}-{Minute}-{Second}.csv"
                df.to_csv(csv_name)
                Notifi.configure(
                    text="CSV created Successfully",
                    bg="Green", fg="white", width=33,
                    font=("times", 19, "bold")
                )
                Notifi.place(x=180, y=380)

            # Success notification label (initially hidden)
            Notifi = tk.Label(MFW, text="CSV created Successfully", bg="Green",
                              fg="white", width=33, height=2, font=("times", 19, "bold"))

            # Buttons to clear inputs
            c1ear_enroll = tk.Button(MFW, text="Clear", command=remove_enr, fg="black",
                                     bg="deep pink", width=10, height=1,
                                     activebackground="Red", font=("times", 15, " bold "))
            c1ear_enroll.place(x=690, y=100)

            c1ear_student = tk.Button(MFW, text="Clear", command=remove_student, fg="black",
                                      bg="deep pink", width=10, height=1,
                                      activebackground="Red", font=("times", 15, " bold "))
            c1ear_student.place(x=690, y=200)

            # Button to submit data
            DATA_SUB = tk.Button(MFW, text="Enter Data", command=enter_data_DB, fg="black",
                                 bg="lime green", width=20, height=2,
                                 activebackground="Red", font=("times", 15, " bold "))
            DATA_SUB.place(x=170, y=300)

            # Button to create CSV
            MAKE_CSV = tk.Button(MFW, text="Convert to CSV", command=create_csv, fg="black",
                                 bg="red", width=20, height=2,
                                 activebackground="Red", font=("times", 15, " bold "))
            MAKE_CSV.place(x=570, y=300)

            # Button to open Attendance folder
            def attf():
                import subprocess
                subprocess.Popen(
                    r'explorer /select,"C:/Users/patel/OneDrive/Documents/E/FBAS/Attendance(Manually)"'
                )

            attf = tk.Button(MFW, text="Check Sheets", command=attf, fg="black",
                             bg="lawn green", width=12, height=1,
                             activebackground="Red", font=("times", 14, " bold "))
            attf.place(x=730, y=410)

            MFW.mainloop()

    # Subject input section in main window
    SUB = tk.Label(sb, text="Enter Subject", width=15, height=2, fg="white",
                   bg="blue2", font=("times", 15, " bold "))
    SUB.place(x=30, y=100)

    global SUB_ENTRY
    SUB_ENTRY = tk.Entry(sb, width=20, bg="yellow", fg="red", font=("times", 23, " bold "))
    SUB_ENTRY.place(x=250, y=105)

    # Button to fill attendance
    fill_manual_attendance = tk.Button(
        sb, text="Fill Attendance", command=fill_attendance, fg="white",
        bg="deep pink", width=20, height=2,
        activebackground="Red", font=("times", 15, " bold "))
    fill_manual_attendance.place(x=250, y=160)

    sb.mainloop()
