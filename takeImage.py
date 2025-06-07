import csv
import os, cv2

# Function to take image of a student and save for facial recognition
def TakeImage(l1, l2, haarcasecade_path, trainimage_path, message, err_screen, text_to_speech):
    # Check if both enrollment number and name are empty
    if (l1 == "") and (l2 == ""):
        t = 'Please Enter your Enrollment Number and Name.'
        text_to_speech(t)
    # Check if only enrollment number is missing
    elif l1 == '':
        t = 'Please Enter your Enrollment Number.'
        text_to_speech(t)
    # Check if only name is missing
    elif l2 == "":
        t = 'Please Enter your Name.'
        text_to_speech(t)
    else:
        try:
            # Initialize the camera
            cam = cv2.VideoCapture(0)

            # Load the Haar cascade classifier for face detection
            detector = cv2.CascadeClassifier(haarcasecade_path)

            Enrollment = l1  # Student's enrollment number
            Name = l2        # Student's name
            sampleNum = 0    # Counter for number of face samples

            # Create a unique directory for the student using enrollment and name
            directory = Enrollment + "_" + Name
            path = os.path.join(trainimage_path, directory)
            os.mkdir(path)  # Create directory to save face images

            # Start capturing frames from the camera
            while True:
                ret, img = cam.read()  # Capture frame
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

                # Detect faces in the grayscale image
                faces = detector.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    # Draw rectangle around detected face
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

                    # Increment the face image count
                    sampleNum += 1

                    # Save the cropped face image to the student directory
                    face_img_path = os.path.join(path, f"{Name}_{Enrollment}_{sampleNum}.jpg")
                    cv2.imwrite(face_img_path, gray[y:y + h, x:x + w])

                    # Show the live frame with rectangle
                    cv2.imshow("Frame", img)

                # Break if 'q' key is pressed
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
                # Or after collecting 50 samples
                elif sampleNum > 50:
                    break

            # Release the camera and close the window
            cam.release()
            cv2.destroyAllWindows()

            # Save student enrollment and name into CSV file
            row = [Enrollment, Name]
            with open("StudentDetails/studentdetails.csv", "a+") as csvFile:
                writer = csv.writer(csvFile, delimiter=",")
                writer.writerow(row)
                csvFile.close()

            # Notify success
            res = "Images Saved for ER No: " + Enrollment + " Name: " + Name
            message.configure(text=res)
            text_to_speech(res)

        # Handle the case where directory already exists (i.e., student already registered)
        except FileExistsError as F:
            F = "Student Data already exists"
            text_to_speech(F)
