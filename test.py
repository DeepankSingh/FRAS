import requests  # For making HTTP requests to fetch image data from the webcam URL
import cv2       # OpenCV library for image display and processing
import numpy as np  # For handling image arrays and numerical data

# URL of the camera stream or snapshot (IP webcam app on mobile usually serves frames here)
url = "http://192.168.0.6:8080/shot.jpg"

# Infinite loop to continuously fetch and display images from the camera
while True:
    # Send a GET request to the URL and retrieve the image content (JPEG)
    cam = requests.get(url)

    # Convert the binary image content to a NumPy array (1D array of bytes)
    imgNp = np.array(bytearray(cam.content), dtype=np.uint8)

    # Decode the NumPy array into an OpenCV image (cv2.imdecode converts raw bytes to image format)
    img = cv2.imdecode(imgNp, -1)  # -1 means keep the original image color format

    # Display the image in a window titled "cam"
    cv2.imshow("cam", img)

    # Wait for 1 millisecond for a key press; break loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break  # Exit the loop and close the window when 'q' is pressed
