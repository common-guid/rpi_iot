import RPi.GPIO as GPIO
import time
import paho.mqtt.publish as pub

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
stime = time.time()
GPIO.setup(21, GPIO.IN, GPIO.PUD_UP)
GPIO.add_event_detect(21, GPIO.FALLING)
val = 0
while True:
	if GPIO.event_detected(21):
		while GPIO.input == 1:
			etime = time.time()
			val = etime - stime
		pub.single("fridge/door", '{"fridge_door":'+str(int(val))+'}', hostname="192.168.2.114", auth={'username':<"UNAME">,'password':<"PW">})
		time.sleep(1)
