import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from w1thermsensor import W1ThermSensor
import prometheus_client
from prometheus_client import start_http_server
start_http_server(8000)

#prometheus_express.start_http_server(8000)
#for one wired sensor
sensor = W1ThermSensor()
#temprature = sensor.get_temperature()
# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan3 = AnalogIn(mcp, MCP.P3)
chan1 = AnalogIn(mcp, MCP.P1)
# Turbidity values are typically in NTU (Nephelometric Turbidity Units)
# Use the following conversion formula to convert the voltage to a turbidity value
# This formula is specific to the LGZD sensor and may need to be adjusted for other sensors
#turbidity = -0.065 * chan0.voltage + 0.50
#turbidity = -1120.4*pow(chan.voltage, 2)+5742.3*chan.voltage-4352.9

#ph = -(-5.70 * chan3.voltage +12.9)


# Create a Gauge metric to represent the temperature
temperature_gauge = prometheus_client.Gauge('temperature', 'Temperature in degrees Celsius')

# Create a Gauge metric to represent the pH
ph_gauge = prometheus_client.Gauge('ph', 'pH value')

# Create a Gauge metric to represent the turbidity
turbidity_gauge = prometheus_client.Gauge('turbidity', 'Turbidity in NTUs')

while True:
	#read_temprature_sensor
	temperature = sensor.get_temperature()
	temperature_gauge.set(temperature)
	#read_ph_sensor 
	ph = -(-5.70 * chan3.voltage +12.9)
	ph_gauge.set(ph)
	#read_turbidity_sensor
	turbidity = -1120.4*pow(chan1.voltage, 2)+5742.3*chan1.voltage-4352.9
	turbidity_gauge.set(turbidity)
	print('ok')
	time.sleep(1)


