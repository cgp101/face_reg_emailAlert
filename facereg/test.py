import smtplib,ssl  
from picamera import PiCamera  
from time import sleep  
from email.mime.multipart import MIMEMultipart  
from email.mime.base import MIMEBase  
from email.mime.text import MIMEText  
from email.utils import formatdate  
from email import encoders

def send_email():
    toaddr = 'charitgp1011@gmail.com'      # To id 
    me = 'rasip0321@gmail.com'          # your id
    subject = "Hello Stranger!"              # Subject
  
    msg = MIMEMultipart()  
    msg['Subject'] = subject  
    msg['From'] = me  
    msg['To'] = toaddr  
    msg.preamble = "test "   
    part = MIMEBase('application', "octet-stream")  
    part.set_payload(open("imgt.jpg", "rb").read())  
    encoders.encode_base64(part)  
    part.add_header('Content-Disposition', 'attachment; filename="imgt.jpg"')   # File name and format name
    msg.attach(part)
    try:  
       s = smtplib.SMTP('smtp.gmail.com', 587)  # Protocol
       s.ehlo()  
       s.starttls()  
       s.ehlo()  
       s.login(user = 'rasip0321@gmail.com', password = 'qwerty@1011')
       s.sendmail(me, toaddr, msg.as_string())  
       s.quit()
    except SMTPException as error:  
          print ("Error")
