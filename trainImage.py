import os, cv2  # OpenCV for image processing and os for file system operations
import numpy as np  # For numerical operations, especially for handling images
from PIL import Image  # PIL (Pillow) for image processing, Tkinter integration for displaying images

# Function to train the face recognition model with images from the training directory
def TrainImage(haarcasecade_path, trainimage_path, trainimagelabel_path, message, text_to_speech):
    # Create a face recognizer using LBPH (Local Binary Pattern Histogram) method
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Load the pre-trained Haar Cascade classifier for face detection
    detector = cv2.CascadeClassifier(haarcasecade_path)

    # Fetch the images and their corresponding labels using the helper function
    faces, Id = getImagesAndLables(trainimage_path)

    # Train the recognizer with the faces and their respective IDs
    recognizer.train(faces, np.array(Id))

    # Save the trained model to the specified path
    recognizer.save(trainimagelabel_path)

    # Provide feedback to the user that training was successful
    res = "Image Trained successfully"
    message.configure(text=res)  # Update the GUI message label
    text_to_speech(res)  # Speak out the success message

# Helper function to collect all images and their labels from the training directory
def getImagesAndLables(path):
    # Get a list of all directories in the training path
    newdir = [os.path.join(path, d) for d in os.listdir(path)]
    
    # Collect all image file paths from each directory
    imagePath = [
        os.path.join(newdir[i], f)
        for i in range(len(newdir))
        for f in os.listdir(newdir[i])
    ]
    
    faces = []  # List to store face images
    Ids = []  # List to store corresponding IDs (enrollment numbers or student IDs)
    
    # Loop through each image path to process the images
    for imagePath in imagePath:
        pilImage = Image.open(imagePath).convert("L")  # Convert the image to grayscale (necessary for recognition)
        imageNp = np.array(pilImage, "uint8")  # Convert the image to a NumPy array
        Id = int(os.path.split(imagePath)[-1].split("_")[1])  # Extract the ID from the image file name (e.g., Enrollment number)
        
        # Append the processed face image and its ID to the respective lists
        faces.append(imageNp)
        Ids.append(Id)
    
    # Return the list of face images and their corresponding labels (IDs)
    return faces, Ids
