from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, REGISTRY
from datetime import datetime
import time
import board
import busio
import adafruit_sgp30

i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
# Create library object on our I2C port
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
sgp30.iaq_init()
eCO2, TVOC = sgp30.iaq_measure()
elapsed_sec = 0

class sgp30Collector(object):
    def collect(self):
        eCO2, TVOC = sgp30.iaq_measure()
        H2, Ethanol = sgp30.raw_measure()
        sensor = GaugeMetricFamily('air_quality', 'sgp30_|_kitchen', labels=['CO2', 'VOC', 'H2', 'Ethanol'])
    #    c = CounterMetricFamily(
    #        'my_counter_total', 'Help text', labels=['foo'])
        sensor.add_metric(['CO2'], sgp30.eCO2)
        sensor.add_metric(['VOC'], sgp30.TVOC)
        sensor.add_metric(['H2'], sgp30.H2)
        sensor.add_metric(['Ethanol'], sgp30.Ethanol)
        yield sensor


if __name__ == "__main__":
    start_http_server(9000)
    REGISTRY.register(sgp30Collector())
    while True:
        time.sleep(5)

