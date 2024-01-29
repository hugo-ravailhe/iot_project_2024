import paho.mqtt.client as mqtt
import time

print("""
    /\\ 
   /  \\ 
  /----\\ 
 /      \\
 |  .-.  |
 |  | |  |
 |__|_|__|
""")

print("Smart Home Application is starting...\n\n")

####### Set up Topics #######
# This part describes the topics used by the application to communicate with the broker

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
# This part describes the broker settings and the connection to the broker

# MQTT Broker settings
broker_address = "127.0.0.1"
broker_port = 1883
keep_alive_interval = 60

# Initialize MQTT client for UserApp
client = mqtt.Client("UserApp")

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("efrei/liu_ravailhe/alarm/+")
    client.subscribe("efrei/liu_ravailhe/light/+")
    client.subscribe("efrei/liu_ravailhe/clim/+")
    client.subscribe("efrei/liu_ravailhe/garage/+")

client.on_connect = on_connect

# Connect to the broker
client.connect(broker_address, broker_port, keepalive=keep_alive_interval)


#### Variables ####
# This part describes the variables used by the application

alarm_status = None
clim_temperature = None
garage_status = None
verbose = False

#### Methods ####
# This part describes the methods used by the application

# Alarms
def alarm_enable():
    client.publish(topic_alarm["enable"])

def alarm_disable():
    client.publish(topic_alarm["disable"])

def alarm_get_status():
    global alarm_status
    print(alarm_status)
    if alarm_status is None:
        print("Alarm status: Unknown")
    else:
        print(f"Alarm status: {alarm_status}")

# Light
def light_enable(room):
    client.publish(topic_light["enable"], room)

def light_disable(room):
    client.publish(topic_light["disable"], room)

# Clim
def clim_ac_trigger(trigger):
    client.publish(topic_clim["ac_trigger"], trigger)

def clim_heater_trigger(trigger):
    client.publish(topic_clim["heater_trigger"], trigger)

def clim_get_temperature():
    print("Temperature: {0:0.1f}°C".format(clim_temperature))

# Garage
def garage_distanceA(distance):
    client.publish(topic_garage["distanceA"], distance)

def garage_distanceB(distance):
    client.publish(topic_garage["distanceB"], distance)

def garage_get_status():
    global garage_status
    print(garage_status)

# Callback when a message is received from the broker
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()

    # Alarm
    if topic == topic_alarm["enable"] :
        if verbose:
            print("Alarm enable")

    elif topic == topic_alarm["disable"]:
        if verbose:
            print("Alarm disable")

    elif topic == topic_alarm["status"]:
        global alarm_status
        alarm_status = payload
        if verbose:
            print(f"Alarm status: {payload}")

    # Light
    elif topic == topic_light["enable"]:
        if verbose:
            print("Light enable")
    
    elif topic == topic_light["disable"]:
        if verbose:
            print("Light disable")
    
    # Climatization
    elif topic == topic_clim["ac_trigger"]:
        if verbose:
            print("AC trigger")
        
    elif topic == topic_clim["heater_trigger"]:
        if verbose:
            print("Heater trigger")
        
    elif topic == topic_clim["temperature"]:
        try:
            temp = float(payload)
            global clim_temperature
            clim_temperature = temp
        except:
            print("Invalid temperature value")
        if verbose:
                print("Temperature: {0:0.1f}°C".format(clim_temperature))
    
    # Garage
    elif topic == topic_garage["distanceA"]:
        if verbose:
            print("Distance A")

    elif topic == topic_garage["distanceB"]:
        if verbose:
            print("Distance A")

    elif topic == topic_garage["status"]:
        global garage_status
        garage_status = payload
        if verbose:
            print(f"Temperature: {garage_status}")

    # Default
    else:
        print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")

client.on_message = on_message

client.loop_start()

####### Main #######

### Interface ###

def display_main_menu():
    print("\nSmart Home Application Menu")
    print("1. Alarm")
    print("2. Light")
    print("3. Climatization")
    print("4. Garage")
    print("Q. Quit\n")

def handle_alarm():
    while True:
        alarm_action = input("\nAlarm menu:\n1. Enable alarm\n2. Disable alarm\n3. get alarm status\nQ. Quit\nSelect an action: ")
        if alarm_action == "1":
            alarm_enable()
        elif alarm_action == "2":
            alarm_disable()
        elif alarm_action == "3":
            alarm_get_status()
        elif alarm_action == "q" or alarm_action == "Q":
            print()
            print()
            break
        else:
            print("Invalid value, try again")

def handle_light():
    while True:
        light_action = input("\nLight menu:\n1. Enable light\n2. Disable light\nQ. Quit\nSelect an action: ")
        if light_action == "1":
            light_room = input("Select a room ('0' to select all rooms), or 'Q' to quit: ")

            if light_room == "q" or light_room == "Q":
                print()
                print()
                break
        
            light_enable(light_room)

        elif light_action == "2":
            light_room = input("Select a room ('0' to select all rooms), or 'Q' to quit: ")

            if light_room == "q" or light_room == "Q":
                print()
                print()
                break
        
            light_disable(light_room)

        elif light_action == "q" or light_action == "Q":
            print()
            print()
            break

        else:
            print("Invalid value, try again")

def handle_climatization():
    while True:
        clim_action = input("\nClimatization menu\n1. Set AC trigger\n2. Set Heater trigger\n3. Display temperature\nQ. Quit\nSelect an action: ")
        if clim_action == "1":
            trigger = input("Select a AC trigger ('none' to disable), or 'Q' to quit: ")

            if trigger == "q" or trigger == "Q":
                print()
                print()
                break
        
            clim_ac_trigger(trigger)

        elif clim_action == "2":
            trigger = input("Select a Heater trigger ('none' to disable), or 'Q' to quit: ")
            
            if trigger == "q" or trigger == "Q":
                print()
                print()
                break
        
            clim_heater_trigger(trigger)
        
        elif clim_action == "3":
            clim_get_temperature()

        elif clim_action == "q" or clim_action == "Q":
            print()
            print()
            break

        else:
            print("Invalid value, try again")

def handle_garage():
    while True:
        garage_action = input("\nGarage menu\n1. Set distance A\n2. Set distance B\n3. Get parking status\nQ. Quit\nSelect an action: ")
        if garage_action == "1":
            distance = input("Select a distance (cm), or 'Q' to quit: ")

            if distance == "q" or distance == "Q":
                print()
                print()
                break
        
            garage_distanceA(distance)

        elif garage_action == "2":
            distance = input("Select a distance (cm), or 'Q' to quit: ")

            if distance == "q" or distance == "Q":
                print()
                print()
                break
        
            garage_distanceB(distance)

        elif garage_action == "3":
            garage_get_status()

        elif garage_action == "q" or garage_action == "Q":
            print()
            print()
            break

        else:
            print("Invalid value, try again")


### Main ###

try:
    time.sleep(0.5)
    while True:
        display_main_menu()
        choice = input("Choose an option: ").strip().lower()

        if choice == "q":
            break
        elif choice == "1":
            handle_alarm()
        elif choice == "2":
            handle_light()
        elif choice == "3":
            handle_climatization()
        elif choice == "4":
            handle_garage()
        else:
            print("Invalid value, try again.")
    
except KeyboardInterrupt:
    pass

finally:
    client.disconnect()
    print("Disconnected from the broker.")