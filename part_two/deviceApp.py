####### Import #######
import paho.mqtt.client as mqtt
import time
import Adafruit_DHT
import RPi.GPIO as GPIO
import threading

print("""
    .----.
   /      \\
  |  0  0  |
  |    >   |
  |  ____  |
   \______/
""")

print("Device App is running...\n\n")

####### Set up GPIO #######
# This part desciptes the GPIO pins used by the device app

GPIO.setmode(GPIO.BCM)

# Temperature Sensor
TEMP_SENSOR  = 22
TEMP_PIN     = 4


# Motion Sensor
PIR_MOTION = 25

GPIO.setup(PIR_MOTION, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# Ultrasonic Sensor
SONAR_TRIG = 23
SONAR_ECHO = 24

GPIO.setup(SONAR_TRIG,GPIO.OUT)
GPIO.setup(SONAR_ECHO,GPIO.IN)

GPIO.output(SONAR_TRIG, False)


# Servo Motor
MOTOR = 18

GPIO.setup(MOTOR, GPIO.OUT)
p = GPIO.PWM(MOTOR, 50)
p.start(2.5)


# Buzzer
BUZZER = 17

GPIO.setup(BUZZER,GPIO.OUT)

GPIO.output(BUZZER, GPIO.LOW)


# LED 
LED_WHITE = 26
LED_GREEN = 12
LED_YELLOW = 6
LED_RED = 5
LED_BLUE = 13

GPIO.setup(LED_WHITE, GPIO.OUT)
GPIO.setup(LED_GREEN, GPIO.OUT)
GPIO.setup(LED_YELLOW, GPIO.OUT)
GPIO.setup(LED_RED, GPIO.OUT)
GPIO.setup(LED_BLUE, GPIO.OUT)

GPIO.output(LED_WHITE, False)
GPIO.output(LED_GREEN, False)
GPIO.output(LED_YELLOW, False)
GPIO.output(LED_RED, False)
GPIO.output(LED_BLUE, False)

room_light = {
    '1': LED_WHITE,
    '2': LED_GREEN,
    '3': LED_YELLOW
}


####### Set up Topics #######
# This part describes the topics used by the device app

topic_alarm = {
    "enable": 'efrei/liu_ravailhe/alarm/enable', # Enable alarm
    "disable": 'efrei/liu_ravailhe/alarm/disable', # Disable alarm
    "status": 'efrei/liu_ravailhe/alarm/status', # Get alarm statuss
    }

topic_light = {
    "enable": 'efrei/liu_ravailhe/light/enable', # Enbale light for room x, below 0 for all light
    "disable": 'efrei/liu_ravailhe/light/disable' # Disable light for room x, below 0 for all light
}

topic_clim = {
    "ac_trigger": 'efrei/liu_ravailhe/clim/ac', # Set trigger value for AC
    "heater_trigger": 'efrei/liu_ravailhe/clim/heater', # Set trigger value for heater
    "temperature": 'efrei/liu_ravailhe/clim/temperature' # Display temperature
}

topic_garage = {
    "distanceA": 'efrei/liu_ravailhe/garage/distanceA', # Set distance A to open the door automatically
    "distanceB": 'efrei/liu_ravailhe/garage/distanceB', # Set a smaller distance B to close the door
    "status": 'efrei/liu_ravailhe/garage/status' # Show car parking status (distance < B)
}


####### Set up Broker #######
# This part describes the MQTT broker used by the device app and the methods to connect to it

# MQTT Broker settings
broker_address = "127.0.0.1"
broker_port = 1883
broker_timeout = 60

# Initialize MQTT client for DeviceApp
device_client = mqtt.Client("DeviceApp")

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("efrei/liu_ravailhe/alarm/+")
    client.subscribe("efrei/liu_ravailhe/light/+")
    client.subscribe("efrei/liu_ravailhe/clim/+")
    client.subscribe("efrei/liu_ravailhe/garage/+")

device_client.on_connect = on_connect

# Connect to the MQTT broker
device_client.connect(broker_address, broker_port, broker_timeout)


####### Application #######
# This part describes global variables and methods used by the device app

#### Variables ####

# Alarm
alarm_status = None

# Light


# Climatization
clim_ac_trigger = None
clim_heater_trigger = None
clim_temperature = None

# Garage
trigger_distanceA = None
trigger_distanceB = None
garage_distance = None
garage_door_status = False
parking_status = False


#### Methods ####

def data_to_send():
    while True:
        device_client.publish(topic_alarm["status"], alarm_status)
        device_client.publish(topic_clim["temperature"], clim_temperature)
        device_client.publish(topic_garage["status"], garage_get_status())
        time.sleep(2.5)

# Alarm
def alarm_system():
    print("Alarm System launched")
    while True:
        global alarm_status
        if alarm_status and GPIO.input(PIR_MOTION):
            GPIO.output(BUZZER, GPIO.HIGH)
        else:
            GPIO.output(BUZZER, GPIO.LOW)
        
        time.sleep(0.2)

# Read and trigger temperature
def read_temperature():
    print("Temperature System launched")
    while True:
        global clim_temperature
        global clim_ac_trigger
        global clim_heater_trigger
        humidity, clim_temperature = Adafruit_DHT.read_retry(TEMP_SENSOR, TEMP_PIN)
        print("Temperature: {0:0.1f}°C".format(clim_temperature))
        temp_light()

        time.sleep(3)
        
def temp_light():
        global clim_temperature
        global clim_ac_trigger
        global clim_heater_trigger
        print("Temperature: {0:0.1f}°C".format(clim_temperature))
        if clim_ac_trigger is not None:
            print("Ac trigger: {0:0.1f}°C".format(clim_ac_trigger))
        else:
            GPIO.output(LED_BLUE, GPIO.LOW)
        if clim_heater_trigger is not None:
            print("Heater trigger: {0:0.1f}°C".format(clim_heater_trigger))
        else:
            GPIO.output(LED_RED, GPIO.LOW)

        if clim_temperature is not None and clim_ac_trigger is not None and clim_temperature > clim_ac_trigger:
            GPIO.output(LED_BLUE, GPIO.HIGH)
        else:
            GPIO.output(LED_BLUE, GPIO.LOW)

        if clim_temperature is not None and clim_heater_trigger is not None and clim_temperature < clim_heater_trigger:
            GPIO.output(LED_RED, GPIO.HIGH)
        else:
            GPIO.output(LED_RED, GPIO.LOW)

# Garage
def get_distance():
    GPIO.output(SONAR_TRIG, True)
    time.sleep(0.00001)
    GPIO.output(SONAR_TRIG, False)
    pulse_start = 0
    pulse_end = 0
    while GPIO.input(SONAR_ECHO)==0:
        pulse_start = time.time()
        
    while GPIO.input(SONAR_ECHO)==1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance

def set_angle(angle):
    duty_cycle = 2.5 + (angle / 18.0)
    p.ChangeDutyCycle(duty_cycle)
    time.sleep(1)

def rotate_motor(open: bool = True):
    global garage_door_status
    if open:
        garage_door_status = True
        set_angle(180)
    else:
        garage_door_status = False
        set_angle(0)

def garage_trigger():
    print("Garage System launched")
    while True:
        global garage_distance
        global garage_door_status
        global parking_status
        garage_distance = get_distance()
        print("Distance: {0:0.1f}cm".format(garage_distance))

        if garage_distance is not None and trigger_distanceB is not None and trigger_distanceA is not None:
            if garage_distance < trigger_distanceA and garage_distance > trigger_distanceB:
                rotate_motor(open=True)
                time.sleep(3)
            elif garage_distance < trigger_distanceB and garage_door_status:
                rotate_motor(open=False)
                parking_status = True
                device_client.publish(topic_garage["status"], garage_get_status())
                
            elif garage_distance > trigger_distanceA and garage_door_status:
                rotate_motor(open=False)
                parking_status = False
                device_client.publish(topic_garage["status"], garage_get_status())
        
        time.sleep(1)

def garage_get_status():
    global parking_status
    return parking_status
  

####### Callback ######
# This part describes the callback methods used by the device app
    
## Alarm
def alarm_enable(client, userdata, message):
    print("Enable alarm")
    global alarm_status
    alarm_status = True
    device_client.publish(topic_alarm["status"], alarm_status)

def alarm_disable(client, userdata, message):
    print("Disable alarm")
    global alarm_status
    alarm_status = False
    device_client.publish(topic_alarm["status"], alarm_status)

## Light
def light_enable(client, userdata, message):
    payload = message.payload.decode("utf-8")
    print("Enable light")
    if payload == '0':
        for light in room_light:
            GPIO.output(room_light[light], GPIO.HIGH)
    elif payload in room_light:
        GPIO.output(room_light[payload], GPIO.HIGH)
    else:
        print(f"Invalid input: {payload}")

def light_disable(client, userdata, message):
    payload = message.payload.decode("utf-8")
    print("Disable light")
    if payload == '0':
        for light in room_light:
            GPIO.output(room_light[light], GPIO.LOW)
    elif payload in room_light:
        GPIO.output(room_light[payload], GPIO.LOW)
    else:
        print(f"Invalid input: {payload}")

## Climatization
# Methods to set the AC trigger
def clim_set_ac_trigger(client, userdata, message):
    payload = message.payload.decode("utf-8")
    print("Set AC trigger")
    try:
        global clim_ac_trigger
        if payload == 'none':
            clim_ac_trigger = None
            
        else:
            clim_ac_trigger = float(payload)
        print(f"AC Trigger: {clim_ac_trigger}")
        temp_light()
    except:
        print("Invalid input\n")

# Methods to set the heater trigger
def clim_set_heater_trigger(client, userdata, message):
    payload = message.payload.decode("utf-8")
    print("Set Heater trigger")
    try:
        global clim_heater_trigger
        if payload == 'none':
            clim_heater_trigger = None
        else:
            clim_heater_trigger = float(payload)
        print(f"Heater Trigger: {clim_heater_trigger}")
        temp_light()
    except:
        print("Invalid input\n")

## Garage
# Methods to set the distance A
def garage_set_trigger_distanceA(client, userdata, message):
    payload = message.payload.decode("utf-8")
    print("Set Distance A")
    try:
        global trigger_distanceA
        if payload == 'none':
            trigger_distanceA = None
        else:
            trigger_distanceA = float(payload)
        print(f"Distance A: {trigger_distanceA}")
    except:
        print("Invalid input\n")

# Methods to set the distance B
def garage_set_trigger_distanceB(client, userdata, message):
    payload = message.payload.decode("utf-8")
    print("Set Distance B")
    try:
        global trigger_distanceB
        if payload == 'none':
            trigger_distanceB = None
        else:
            trigger_distanceB = float(payload)
        print(f"Distance B: {trigger_distanceB}")
    except:
        print("Invalid input\n")


####### Set up Broker #######

device_client.message_callback_add(topic_alarm["enable"], alarm_enable)
device_client.message_callback_add(topic_alarm["disable"], alarm_disable)
device_client.message_callback_add(topic_light["enable"], light_enable)
device_client.message_callback_add(topic_light["disable"], light_disable)
device_client.message_callback_add(topic_clim["ac_trigger"], clim_set_ac_trigger)
device_client.message_callback_add(topic_clim["heater_trigger"], clim_set_heater_trigger)
device_client.message_callback_add(topic_garage["distanceA"], garage_set_trigger_distanceA)
device_client.message_callback_add(topic_garage["distanceB"], garage_set_trigger_distanceB)

# Start the MQTT loop
device_client.loop_start()

try:
    # Start the threads
    # 1. Read temperature
    thread_temperature = threading.Thread(target=read_temperature)
    thread_temperature.start()
    # 2. Alarm system
    thread_alarm = threading.Thread(target=alarm_system)
    thread_alarm.start()
    # 3. Garage system
    thread_garage = threading.Thread(target=garage_trigger)
    thread_garage.start()
    
    # 4. Send data to broker
    while True:
        data_to_send()
        time.sleep(10)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
    device_client.disconnect()
    print("Disconnected from the broker.")