# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

""" Example for using the SGP30 with CircuitPython and the Adafruit library"""
from datetime import datetime
import time
import board
import busio
import adafruit_sgp30
from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import ASYNCHRONOUS

token = <"ACCESS TOKEN">
org = "squawk"
bucket = "IoT_Sensors"

client = InfluxDBClient(url=<"DB_URL">, token=token, org=org)
write_api = client.write_api(write_options=ASYNCHRONOUS)
i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)

# Create library object on our I2C port
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)

print("SGP30 serial #", [hex(i) for i in sgp30.serial])

sgp30.iaq_init()
#sgp30.set_iaq_baseline(0x8973, 0x8AAE)

while True:
    eCO2, TVOC = sgp30.iaq_measure()
    H2, Ethanol = sgp30.raw_measure()
    print("eCO2 = %d ppm \t TVOC = %d ppb" % (eCO2, TVOC))
    print(H2, Ethanol)
    write_api.write(bucket,org, Point("sgp30").tag("Location","kitchen").field("eCO2",eCO2).time(time=datetime.utcnow()))
    time.sleep(0.1)
    write_api.write(bucket,org, Point("sgp30").tag("Location","kitchen").field("TVOC",TVOC).time(time=datetime.utcnow()))
    time.sleep(0.1)
    write_api.write(bucket,org, Point("sgp30").tag("Location","kitchen").field("H2",H2).time(time=datetime.utcnow()))
    time.sleep(0.1)
    write_api.write(bucket,org, Point("sgp30").tag("Location","kitchen").field("Ethanol",Ethanol).time(time=datetime.utcnow()))
    time.sleep(5)

