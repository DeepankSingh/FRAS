# FRAS - Face Recognition Attendance System

**FRAS** is a desktop-based attendance system that leverages face recognition technology to automate the attendance process. It is designed for educational institutions to reduce manual work, eliminate proxy attendance, and ensure reliable and fast attendance marking.

This project is built using **Python**, **OpenCV**, **Tkinter**, and **NumPy**, offering an intuitive user interface and accurate facial recognition using Haar Cascade classifiers.

---

## 🔧 Features

- 👤 **Student Registration**  
  Capture and store face images of students with their IDs and names.

- 🎯 **Real-time Face Recognition**  
  Recognizes registered faces and marks attendance automatically.

- 🗂️ **Attendance Log**  
  Generates a CSV file storing student name, ID, date, and time of attendance.

- 🧭 **User-Friendly Interface**  
  GUI designed using Tkinter for ease of use by faculty or admin staff.

---

## 🧪 Technologies Used

- **Python**
- **OpenCV** (for face detection and recognition)
- **Tkinter** (for GUI)
- **NumPy**, **Pandas** (for data handling)
- **CSV** (for attendance records)
- **Haar Cascade Classifier** (for face detection)

---

## 🖥️ Project Structure

```
FRAS/
│
├── __pycache__/                  # Python cache files
├── Attendance/                   # Stores attendance CSVs
├── StudentDetails/               # CSV files and student info
├── TrainingImage/                # Captured images of students
├── TrainingImageLabel/           # Label data for training
├── UI_Image/                     # GUI-related images
├── attendance/                   # Scripts for marking attendance
├── automaticAttendance/          # Auto attendance logic
├── show_attendance/              # View past attendance records
├── takelmage/                    # Scripts to capture images
├── takemanually/                 # Manual attendance options
├── test/                         # Test scripts or samples
├── trainImage/                   # Training logic and data
├── utils/                        # Helper functions
├── haarcascade_frontalface_alt.xml       # Haar Cascade XML for face detection
├── haarcascade_frontalface_default.xml   # Haar Cascade XML for face detection
```

---

## 🚀 How to Run the Project

### 1. Clone the repository
```bash
git clone https://github.com/DeepankSingh/FRAS.git
cd FRAS
```

### 2. Install dependencies
Make sure you have Python 3.x installed. Then run:
```bash
pip install -r requirements.txt
```

### 3. Run the application
```bash
python main.py
```

---

## 📷 How It Works

1. **Register Student** – Capture multiple images of a student's face using a webcam.
2. **Train Model** – The captured faces are used to train a simple recognizer using OpenCV's LBPH algorithm.
3. **Mark Attendance** – On running attendance, the system detects and recognizes faces in real time and logs attendance with a timestamp.

---

## 🛠️ Requirements

- Python 3.x
- OpenCV
- Tkinter
- NumPy
- Pandas

---

## 📌 Future Improvements

- Integration with cloud storage or database (e.g., Firebase, MySQL)
- Admin authentication/login system
- Export attendance as PDF/Excel
- Email or SMS alerts for absentee students

---

## 👨‍💻 Author

**Deepank Singh**  
[MCA Final Year | AI/ML | Developer | OpenCV Enthusiast]  
Connect with me on [LinkedIn](https://www.linkedin.com/in/deepank-singh/)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
