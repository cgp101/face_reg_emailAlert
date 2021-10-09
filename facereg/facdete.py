
import numpy as np
import cv2
hcass = cv2.CascadeClassifier('/home/pi/Desktop/facereg/harrdata/haarcascade_frontalface_default.xml')
cam= cv2.VideoCapture(0)
cam.set(3,640) # setting Width
cam.set(4,480)

# FACE 
while(True):
    ret ,img=cam.read()
    grayimg=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = hcass.detectMultiScale(
        grayimg,     
        scaleFactor=1.2,
        minNeighbors=5,     
        minSize=(20, 20)
    )
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = grayimg[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        
    cv2.imshow('video',img)
    k=cv2.waitKey(30)& 0xff
    if(k== 27):
        break#esc to exit
cam.release()
cv2.destroyAllWindows()