# Importing the necessary packages
import numpy as np
import cv2 

# Reading the frames from webcam
cap = cv2.VideoCapture(0)
cnt = 0
bg = 0

# Capturing the background in the range of 60
for i in range(60):
    ret, bg = cap.read()
# Flipping the frame
bg = np.flip(bg, axis = 1)  

# Reading every frame from the webcam, till the camera is open(infinite loop is formed)
while (cap.isOpened()):
    ret, img = cap.read()
    if not ret:
        break
    cnt += 1
    img = np.flip(img, axis = 1)

    # Converting the color space from BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Generating masks to detect RED color

    # Setting the lower and upper range for mask1
    lower_red = np.array([0 ,120, 70])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    # Setting the lower and upper range for mask2
    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)
    mask1 = mask1 + mask2
    # Opening and Dilating the mask image
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3,3), np.uint8), iterations = 2)
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3,3), np.uint8), iterations = 1)

    # Bitwise not is used to create an inverted mask, thereby segmenting out the red colour from the frame
    mask2 = cv2.bitwise_not(mask1)

    # Bitwise and is used to segment out the red colour part from the frame from mask2
    res1 = cv2.bitwise_and(img, img, mask = mask2)
    # Creating image showing static background frame pixels only for the masked region
    res2 = cv2.bitwise_and(bg, bg, mask = mask1)

    #Generating the final output 
    finalOutput = cv2.addWeighted(res1, 1, res2, 1, 0)
    cv2.imshow('Original', img)
    cv2.imshow('Invisible Cloak', finalOutput)

    k = cv2.waitKey(5) & 0xFF                                   
    if k == 27:                                                 
        break    

cap.release()
cv2.destroyAllWindows()
    



    
