from gpiozero import MotionSensor
from gpiozero import LED
import time
from email.message import EmailMessage
import ssl
import smtplib
import p
import os
from picamera2 import Picamera2, Preview


pir = MotionSensor (4)
red_led = LED(21)
red_led.off()

def email():
	email_sender = 'your email address'
#'p' is python file in the same folder as this program where the password needed to use gmail api is stored. 
	email_password = p.password
	email_receiver = 'receiver email address'

	subject = 'Alarm, motion detected in your house'
	body = 'motion detected'

	em = EmailMessage()
	em['From'] = email_sender
	em['To'] = email_receiver
	em['Subject'] = subject
	em.set_content(body)

	image_path =  'your photo path (same as the program by default)'
#this will attach photo to email 	
	with open(image_path, 'rb') as image_file:
		image_data = image_file.read()
		em.add_attachment(image_data, maintype='image', subtype=os.path.splitext(image_path)[1][1:], filename=os.path.basename(image_path))	
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
		smtp.login(email_sender, email_password)
		smtp.sendmail(email_sender, email_receiver, em.as_string())


def capture_photo():
	picam2 = Picamera2()
	camera_config = picam2.create_preview_configuration()
	picam2.configure(camera_config)
	picam2.start()
	picam2.capture_file('captured.jpg')


def counting_down(t):
	for i in range(t, 0, -1):
		print(f"time remaining: {i:2}", end ='\r')
		time.sleep(1)


time_to_active_alarm = input('How much time you need to leave the house(in seconds)')
counting_down(int(time_to_active_alarm))
print('Alarm actived')
pir.wait_for_motion()
print("motion detected")
red_led.on()
capture_photo()
time.sleep(2)
email()
