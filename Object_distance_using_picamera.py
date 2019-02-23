from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import math

distance = 0.0
font = cv2.FONT_HERSHEY_SIMPLEX

camera = PiCamera()
camera.resolution =(1280,720)
camera.framerate =32
rawCapture = PiRGBArray(camera, size=(1280,720))

time.sleep(0.1)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

for frame in camera.capture_continuous(rawCapture,format="bgr",use_video_port=True):
    image = frame.array
    #cv2.imshow("Frame",image)
    #key= cv2.waitKey(1) & 0xFF
    # Caputure a single frame
    huge_frame = image
    frame = cv2.resize(huge_frame, (0,0), fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)
# Create the greyscale and detect faces
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    # Add squeres for each face
    for (x, y, w, h) in faces:
        distancei = (2*3.14 * 180)/(w+h*360)*1000 + 3
        print (distancei)
#        distance = distancei *2.54
        distance = math.floor(distancei)
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    rawCapture.truncate(0)
    cv2.putText(frame,'Distance = ' + str(distance) + ' Inch', (5,100),font,1,(255,255,255),2)
    cv2.imshow('face detection', frame)
    if cv2.waitKey(1) == ord('q'):
        break
