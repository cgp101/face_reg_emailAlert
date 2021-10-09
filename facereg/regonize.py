
#Face Rec libraries
import cv2
import numpy as np
import os

#Email libraries
import time
from datetime import datetime
import picamera
from smtplib import SMTP
from smtplib import SMTPException
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
   
    

    

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('facetrain/trainer.yml')
cascadePath = '/home/pi/Desktop/facereg/harrdata/haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascadePath);
font = cv2.FONT_HERSHEY_SIMPLEX
#iniciate id counter
id = 0
# names related to ids: example ==> Marcelo: id=1,  etc
names = ['t', 'Charit'] 
# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height
# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)
while True:
    ret, img =cam.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )
    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        # Check if confidence is less them 100 ==> "0" is perfect match 
        if (confidence < 100):
            id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
           

        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
            ret, unimg=cam.read()
            #unimg=cv2.imread('photo.jpg',cv2.IMREAD_ANYCOLOR)
            img_save = cv2.imwrite(filename='photo.jpg',img=unimg)
            
        
            print("Image saved and will be email");
            f_time = datetime.now().strftime('%a %d %b @ %H:%M')
            toaddr = 'charitgp1011@gmail.com'    # redacted
            me = 'rasip0321@gmail.com' # redacted
            subject = 'Photo_Alert ' + f_time
            msg = MIMEMultipart()
            msg['Subject'] = "Check home. Unknown person is in premise"
            msg['From'] = 'rasip0321@gmail.com'
            msg['To'] = 'charitgp1011@gmail.com'
            msg.preamble = "Photo @ " + f_time
            fp = open('/home/pi/Desktop/facereg/photo.jpg', 'rb')
            img = MIMEImage(fp.read(), _subtype=False)
            fp.close()
            msg.attach(img)
            try:
               s = smtplib.SMTP('smtp.gmail.com',587)
               s.ehlo()
               s.starttls()
               s.ehlo()
               s.login(user = 'rasip0321@gmail.com',password = 'qwerty@1011')
               #s.send_message(msg)
               s.sendmail(me, toaddr, msg.as_string())
               s.quit()
               print("Email Sent")
            #except:
            #   print ("Error: unable to send email")
            except SMTPException as error:
                  print ("Error: unable to send email")
            exit(0)
  
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)
    cv2.imshow('camera',img) 
    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()