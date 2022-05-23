import RPi.GPIO as GPIO
import time
from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import ASYNCHRONOUS

token = <"TOKEN">
org = "squawk"
bucket = "IoT_Sensors"

client = InfluxDBClient(url=<"DB_URL">, token=token, org=org)
write_api = client.write_api(write_options=ASYNCHRONOUS)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(26, GPIO.IN, pull_up_down= GPIO.PUD_UP)

GPIO.add_event_detect(26, GPIO.FALLING)

while True:
	time.sleep(0.1)
	if GPIO.event_detected(26):
		write_api.write(bucket,org, Point("ir_beam_sm").tag("Location","desk").field("open",1).time(time=datetime.utcnow()))
		print("detect")
