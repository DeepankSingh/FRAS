# Import necessary libraries
import pandas as pd
from glob import glob
import os
import tkinter as tk
from tkinter import *
from tkinter import ttk
import csv
from utils import center_window

def subjectchoose(text_to_speech):

    def calculate_attendance():
        Subject = tx.get().strip()

        if Subject == "":
            text_to_speech('Please enter the subject name.')
            return

        # Get all attendance CSVs
        filenames = glob(f"Attendance\\{Subject}\\{Subject}*.csv")
        if not filenames:
            text_to_speech(f"No attendance files found for subject '{Subject}'. Please check the name or files.")
            return  # Prevent IndexError by returning early

        # Read all files into DataFrames
        df_list = [pd.read_csv(f) for f in filenames]

        newdf = df_list[0]
        for i in range(1, len(df_list)):
            newdf = newdf.merge(df_list[i], how="outer")

        newdf.fillna(0, inplace=True)

        # Initialize "Attendance" column as string to avoid dtype conflict
        newdf["Attendance"] = ""

        # Calculate attendance percentage using safe .loc[] assignment
        for i in range(len(newdf)):
            avg = newdf.iloc[i, 2:-1].mean()
            percentage = str(int(round(avg * 100))) + '%'
            newdf.loc[i, "Attendance"] = percentage  # Use loc instead of chained iloc

        # Save updated attendance to a file
        output_path = f"Attendance\\{Subject}\\attendance.csv"
        newdf.to_csv(output_path, index=False)

        # Display the attendance in a new window
        root = tk.Tk()
        root.title(f"Attendance of {Subject}")
        root.configure(background="black")

        with open(output_path) as file:
            reader = csv.reader(file)
            for r, row in enumerate(reader):
                for c, cell in enumerate(row):
                    label = tk.Label(
                        root,
                        width=10,
                        height=2,
                        fg="black",
                        font=("times", 15, "bold"),
                        bg="#FFFFFF",
                        text=cell,
                        relief=tk.RIDGE,
                    )
                    label.grid(row=r, column=c)

        root.mainloop()
        print(newdf)  # Optional: for debugging

    # GUI Setup for subject input
    subject = Tk()
    subject.title("Subject...")
    subject.attributes("-fullscreen", True)
    subject.resizable(0, 0)
    subject.configure(background="#4A90E2")
    center_window(subject, 580, 320)

    # Entry styling
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TEntry", font=("Segoe UI", 18))
    style.map("TEntry", fieldbackground=[("active", "#F0F0F0")])

    # Title label
    tk.Label(subject, bg="#4A90E2", relief=RIDGE, bd=0, font=("arial", 30)).pack(fill=X)
    tk.Label(
        subject,
        text="Which Subject of Attendance?",
        bg="#4A90E2",
        fg="#FFFFFF",
        font=("arial", 25),
    ).place(x=570, y=10)

    # Open folder function
    def Attf():
        sub = tx.get().strip()
        if sub == "":
            text_to_speech("Please enter the subject name!!!")
        else:
            os.startfile(f"Attendance\\{sub}")

    # Check Sheets Button
    tk.Button(
        subject,
        text="Check Sheets",
        command=Attf,
        bd=0,
        font=("Verdana", 18, "bold"),
        bg="#2980B9",
        fg="#FFFFFF",
        activebackground="#2471A3",
        activeforeground="#FFFFFF",
        height=3,
        width=30,
        relief="flat",
        cursor="hand2"
    ).place(x=900, y=350)

    # Subject Entry Prompt
    tk.Label(
        subject,
        text="Enter Subject",
        bg="#4A90E2",
        fg="#FFFFFF",
        font=("Segoe UI", 30, "bold")
    ).place(x=420, y=150)

    # Subject Entry Field
    tx = ttk.Entry(subject, width=30, font=("Segoe UI", 14))
    tx.place(x=710, y=165)

    # View Attendance Button
    tk.Button(
        subject,
        text="View Attendance",
        command=calculate_attendance,
        bd=0,
        font=("Verdana", 18, "bold"),
        bg="#2980B9",
        fg="#FFFFFF",
        activebackground="#2471A3",
        activeforeground="#FFFFFF",
        height=3,
        width=30,
        relief="flat",
        cursor="hand2"
    ).place(x=130, y=350)

    # Back Button
    tk.Button(
        subject,
        text="Back",
        command=subject.destroy,
        bd=0,
        font=("Verdana", 18, "bold"),
        bg="#2980B9",
        fg="#FFFFFF",
        activebackground="#2471A3",
        activeforeground="#FFFFFF",
        height=3,
        width=30,
        relief="flat",
        cursor="hand2"
    ).place(x=500, y=700)

    subject.mainloop()







# # Import necessary libraries
# import pandas as pd  # For handling CSV and dataframes
# from glob import glob  # To match file patterns
# import os  # For opening directories
# import tkinter  # GUI package
# import csv  # For reading CSV files
# import tkinter as tk  # Alias for tkinter for convenience
# from tkinter import *  # Import all tkinter widgets
# from utils import center_window
# from tkinter import ttk

# # Function that asks the user to enter a subject and calculates & displays attendance
# def subjectchoose(text_to_speech):
    
#     # Function to calculate attendance from all session CSVs of a subject
#     def calculate_attendance():
#         Subject = tx.get()  # Get subject name from entry box

#         # If no subject is entered, speak a prompt
#         if Subject == "":
#             t = 'Please enter the subject name.'
#             text_to_speech(t)
#             return
        
#         # Get all attendance CSV files for the subject
#         filenames = glob(f"Attendance\\{Subject}\\{Subject}*.csv")
#         if not filenames:
#             t = f"No attendance files found for subject '{Subject}'. Please check the subject name or ensure files exist."
#             text_to_speech(t)
        
        
#         # Read all CSVs into a list of DataFrames
#         df = [pd.read_csv(f) for f in filenames]

#         # Merge all DataFrames into one using outer join
#         newdf = df[0]
#         for i in range(1, len(df)):
#             newdf = newdf.merge(df[i], how="outer")

#         # Replace any missing values with 0 (absent)
#         newdf.fillna(0, inplace=True)

#         # Initialize an "Attendance" column
#         newdf["Attendance"] = 0

#         # Calculate attendance percentage for each student and update the column
#         for i in range(len(newdf)):
#             # Average of attendance across sessions (ignoring first 2 columns and the last)
#             avg = newdf.iloc[i, 2:-1].mean()
#             newdf["Attendance"].iloc[i] = str(int(round(avg * 100))) + '%'

#         # Save final attendance to a new CSV
#         newdf.to_csv(f"Attendance\\{Subject}\\attendance.csv", index=False)

#         # Create a new window to display attendance table
#         root = tkinter.Tk()
#         root.title("Attendance of " + Subject)
#         root.configure(background="black")
        
#         # Read and display the attendance CSV file in GUI as a table
#         cs = f"Attendance\\{Subject}\\attendance.csv"
#         with open(cs) as file:
#             reader = csv.reader(file)
#             r = 0  # Row index

#             # Create labels in a grid for each row and column
#             for col in reader:
#                 c = 0  # Column index
#                 for row in col:
#                     label = tkinter.Label(
#                         root,
#                         width=10,
#                         height=2,
#                         fg="black",
#                         font=("times", 15, " bold "),
#                         bg="#FFFFFF",
#                         text=row,
#                         relief=tkinter.RIDGE,
#                     )
#                     label.grid(row=r, column=c)
#                     c += 1
#                 r += 1

#         root.mainloop()  # Display the GUI window
#         print(newdf)  # Optional: print the final DataFrame to console

#     # Main GUI window to ask for subject
#     subject = Tk()
#     subject.title("Subject...")
#     subject.attributes("-fullscreen",True)
#     subject.resizable(0, 0)
#     subject.configure(background="#4A90E2")
#     center_window(subject, 580, 320)

#     # Define styles once 
#     style = ttk.Style()
#     style.theme_use("clam")
#     style.configure("TEntry", font=("Segoe UI", 18))
#     style.map("TEntry", fieldbackground=[("active", "#F0F0F0")])

#     # Title label
#     titl = tk.Label(subject, bg="#4A90E2", relief=RIDGE, bd=0, font=("arial", 30))
#     titl.pack(fill=X)
#     titl = tk.Label(
#         subject,
#         text="Which Subject of Attendance?",
#         bg="#4A90E2",
#         fg="#FFFFFF",
#         font=("arial", 25),
#     )
#     titl.place(x=570, y=10)

#     # Function to open the folder containing subject attendance files
#     def Attf():
#         sub = tx.get()
#         if sub == "":
#             t = "Please enter the subject name!!!"
#             text_to_speech(t)
#         else:
#             os.startfile(f"Attendance\\{sub}")

#     # Button to open attendance folder
#     attf = tk.Button(
#         subject,
#         text="Check Sheets",
#         command=Attf,
#         bd=0,
#         font=("Verdana", 18, "bold"),
#         bg="#2980B9",      # button background color (blue)
#         fg="#FFFFFF",      # text color (white)
#         activebackground="#2471A3",  # hover background color (darker blue)
#         activeforeground="#FFFFFF",
#         height=3,
#         width=30,
#         relief="flat",
#         cursor="hand2"
#     )
#     attf.place(x=900, y=350)

#     # Label prompting user to enter subject name
#     sub = tk.Label(
#         subject,
#         text="Enter Subject",
#         bg="#4A90E2", 
#         fg="#FFFFFF", 
#         font=("Segoe UI", 30, "bold")
#     )
#     sub.place(x=420, y=150)

#     # Entry box for subject name input
#     tx = ttk.Entry(
#         subject,
#          width=30, font=("Segoe UI", 14)
#     )
#     tx.place(x=710, y=165)

#     # Button to trigger attendance calculation and display
#     fill_a = tk.Button(
#         subject,
#         text="View Attendance",
#         command=calculate_attendance,
#         bd=0,
#         font=("Verdana", 18, "bold"),
#         bg="#2980B9",      # button background color (blue)
#         fg="#FFFFFF",      # text color (white)
#         activebackground="#2471A3",  # hover background color (darker blue)
#         activeforeground="#FFFFFF",
#         height=3,
#         width=30,
#         relief="flat",
#         cursor="hand2"
#     )
#     fill_a.place(x=130, y=350)

#     # Exit button
#     r = tk.Button(
#         subject,
#         text="Back",
#         command=subject.destroy,
#         bd=0,
#         font=("Verdana", 18, "bold"),
#         bg="#2980B9",      # button background color (blue)
#         fg="#FFFFFF",      # text color (white)
#         activebackground="#2471A3",  # hover background color (darker blue)
#         activeforeground="#FFFFFF",
#         height=3,
#         width=30,
#         relief="flat",
#         cursor="hand2"
#     )
#     r.place(x=500, y=700)

#     subject.mainloop()  # Launch the GUI window
