import paho.mqtt.client as mqtt
import time
import Adafruit_DHT
import RPi.GPIO as GPIO

print("Device APP 3 is running")

SENSOR  = 22
PIN     = 27
LED     = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, GPIO.HIGH)


# MQTT Broker settings
broker_address = "127.0.0.1"
broker_port = 1883
broker_timeout = 60

# Initialize MQTT client for DeviceApp
device_client = mqtt.Client("DeviceApp")

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("efrei/liu_ravailhe/led")

device_client.on_connect = on_connect

# Callback function for when the LED topic message is received
def led_callback(client, userdata, message):
    payload = message.payload.decode("utf-8")
    print("led message")
    if payload == "0":
        # Turn off the LED
        print("Turning off LED")
        GPIO.output(LED, GPIO.LOW)

    elif payload == "1":
        # Turn on the LED
        print("Turning on LED")
        GPIO.output(LED, GPIO.HIGH)

# Set the LED topic callback function
device_client.message_callback_add(f"efrei/liu_ravailhe/led", led_callback)

# Connect to the MQTT broker
device_client.connect(broker_address, broker_port, broker_timeout)

# Start the MQTT loop
device_client.loop_start()


def read_temp():
    humidity, temperature = Adafruit_DHT.read_retry(SENSOR, PIN)
    print('Temp={0:0.1f}°  '.format(temperature))
    return temperature

try:
    while True:
        # Simulate temperature reading
        temperature = read_temp()
        device_client.publish(f"efrei/liu_ravailhe/temperature", f"{temperature}")
        time.sleep(5)

except KeyboardInterrupt:
    GPIO.cleanup()
