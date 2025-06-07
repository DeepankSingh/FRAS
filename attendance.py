# Import necessary modules
import tkinter as tk
from tkinter import ttk, messagebox
import os
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import pyttsx3

# Custom utility to center tkinter windows
from utils import center_window

# Custom modules for functionality
import show_attendance
import takeImage
import trainImage
import automaticAttendance

# ------------------------- Global Setup -------------------------

# Initialize Text-to-Speech engine
tts_engine = pyttsx3.init()

# Function to speak a given text using TTS
def text_to_speech(user_text):
    tts_engine.say(user_text)
    tts_engine.runAndWait()

# ------------------------- Directory & Path Setup -------------------------

# Paths for Haarcascade file and image directories
haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = "./TrainingImageLabel/Trainner.yml"
trainimage_path = "./TrainingImage"

# Create training image directory if it doesn't exist
if not os.path.exists(trainimage_path):
    os.makedirs(trainimage_path)

studentdetail_path = "./StudentDetails/studentdetails.csv"
attendance_path = "Attendance"

# ------------------------- Main Window Setup -------------------------

# Create the main application window
window = tk.Tk()
window.title("Face Recognizer")
window.attributes("-fullscreen", True)  # Fullscreen mode
window.configure(background="#4A90E2")  # Set background color

# Ask for confirmation before closing the app
def on_closing():
    if messagebox.askokcancel("Quit", "Are you sure want to close?"):
        window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)

# ------------------------- Utility Functions -------------------------

# Show an error popup if user input is missing
def err_screen():
    err_win = tk.Toplevel(window)
    err_win.title("Warning!!")
    err_win.geometry("400x110")
    center_window(err_win, 400, 110)
    err_win.configure(background="#4A90E2")
    err_win.resizable(False, False)
    tk.Label(err_win, text="Enrollment & Name required!!!", fg="yellow", bg="#4A90E2",
             font=("Verdana", 16, "bold")).pack(pady=10)
    tk.Button(err_win, text="OK", command=err_win.destroy, fg="yellow", bg="#FFFFFF",
              activebackground="red", font=("Verdana", 16, "bold")).pack()

# Input validation for Enrollment (only allow digits)
def validate_enroll(P):
    return P.isdigit() or P == ""

# Helper function to create styled buttons
def create_button(parent, text, command, x, y):
    btn = tk.Button(parent, text=text, command=command, bd=0,
                    font=("Verdana", 18, "bold"),
                    bg="#2980B9", fg="#FFFFFF",
                    activebackground="#2471A3",
                    activeforeground="#FFFFFF",
                    height=3, width=30, relief="flat", cursor="hand2")
    btn.place(x=x, y=y)
    return btn

# ------------------------- Header, Logos, and Title -------------------------

# Load and place institution logo
try:
    logo_img = Image.open("UI_Image/0001.png").resize((70, 47), Image.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(window, bg="#4A90E2", relief=tk.RIDGE, bd=0, font=("Verdana", 30, "bold"))
    logo_label.pack(fill=tk.X)
    logo1 = tk.Label(window, image=logo_photo, bg="#4A90E2")
    logo1.place(x=70, y=10)
except Exception as e:
    print(f"Error loading institution logo: {e}")

# Load and place partner/logo
try:
    logo2_img = Image.open("UI_Image/pheme_logo.png").resize((70, 47), Image.LANCZOS)
    logo2_photo = ImageTk.PhotoImage(logo2_img)
    logo2_label = tk.Label(window, image=logo2_photo, bg="#4A90E2")
    screen_width = window.winfo_screenwidth()
    logo2_label.place(x=screen_width - 100, y=10)
except Exception as e:
    print(f"Error loading partner logo: {e}")

# Main Title
title_label = tk.Label(window, text="University of Petroleum and Energy Studies", bg="#4A90E2",
                       fg="#FFFFFF", font=("Verdana", 27, "bold"))
title_label.place(relx=0.5, y=10, anchor='n')

# Welcome Message
welcome_label = tk.Label(window, text="Welcome to FRAS: Face Recognition Attendance System",
                         bg="#4A90E2", fg="#FFFFFF", bd=0, font=("Verdana", 35, "bold"))
welcome_label.pack(pady=20)

# Set ttk theme and entry font
style = ttk.Style()
style.theme_use("clam")
style.configure("TEntry", font=("Segoe UI", 18))

# ------------------------- Take Image UI -------------------------

# Function to open new window for capturing and training student images
def TakeImageUI():
    ImageUI = tk.Toplevel(window)
    ImageUI.title("Take Student Image..")
    ImageUI.attributes("-fullscreen", True)
    ImageUI.configure(background="#4A90E2")
    center_window(ImageUI, 780, 480)
    ImageUI.resizable(False, False)

    # Header & Instructions
    tk.Label(ImageUI, bg="#4A90E2", relief="flat", font=("Segoe UI", 40, "bold")).pack(fill=tk.X)
    tk.Label(ImageUI, text="Register Your Face", bg="#4A90E2", fg="#FFFFFF", font=("Segoe UI", 30, "bold")).place(relx=0.5, y=10, anchor='n')
    tk.Label(ImageUI, text="Enter the details", bg="#4A90E2", fg="#FFFFFF", font=("Segoe UI", 20, "bold")).place(relx=0.5, y=80, anchor='n')

    # Enrollment Input
    lbl_enroll = tk.Label(ImageUI, text="Enrollment No", bg="#4A90E2", fg="#FFFFFF", font=("Segoe UI", 30, "bold"))
    lbl_enroll.place(x=420, y=150)
    txt_enroll = ttk.Entry(ImageUI, width=30, font=("Segoe UI", 14))
    txt_enroll.place(x=710, y=165)
    reg = ImageUI.register(validate_enroll)
    txt_enroll.config(validate="key", validatecommand=(reg, '%P'))

    # Name Input
    lbl_name = tk.Label(ImageUI, text="Name", bg="#4A90E2", fg="#FFFFFF", font=("Segoe UI", 30, "bold"))
    lbl_name.place(x=420, y=210)
    txt_name = ttk.Entry(ImageUI, width=30, font=("Segoe UI", 14))
    txt_name.place(x=710, y=220)

    # Status Message Label
    message = tk.Label(ImageUI, text="", width=50, height=10, bg="#4A90E2", fg="#333333",
                       font=("Segoe UI", 12), anchor="w", padx=10, relief="sunken", bd=1)
    message.place(x=540, y=270)

    # Take image logic
    def take_image():
        enroll = txt_enroll.get()
        name = txt_name.get()
        if not enroll or not name:
            err_screen()
            return
        takeImage.TakeImage(enroll, name, haarcasecade_path, trainimage_path, message, err_screen, text_to_speech)
        txt_enroll.delete(0, tk.END)
        txt_name.delete(0, tk.END)

    # Button - Take Image
    create_button(ImageUI, "Take Image", take_image, x=130, y=500)

    # Button - Train Image
    def train_image():
        trainImage.TrainImage(haarcasecade_path, trainimage_path, trainimagelabel_path, message, text_to_speech)

    create_button(ImageUI, "Train Image", train_image, x=900, y=500)

    # Button - Back to Main Menu
    create_button(ImageUI, "Back", ImageUI.destroy, x=550, y=700)

# ------------------------- Main Menu Buttons -------------------------

# Button - Register a new student (takes image)
create_button(window, "Register a new student", TakeImageUI, x=500, y=250)

# Button - Take attendance using face recognition
def automatic_attendance():
    automaticAttendance.subjectChoose(text_to_speech)

create_button(window, "Take Attendance", automatic_attendance, x=500, y=400)

# Button - View attendance record
def view_attendance():
    show_attendance.subjectchoose(text_to_speech)

create_button(window, "View Attendance", view_attendance, x=500, y=550)

# Button - Exit the application
create_button(window, "Exit", window.destroy, x=500, y=700)

# Start the GUI main loop
window.mainloop()



