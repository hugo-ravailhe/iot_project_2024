import paho.mqtt.client as mqtt

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
    "ac_trigger": 'efrei/liu_ravailhe/clim/ac/trigger', # Set trigger value for AC
    "heater_trigger": 'efrei/liu_ravailhe/clim/heater/trigger', # Set trigger value for heater
    "temperature": 'efrei/liu_ravailhe/clim/temperature' # Display temperature
}

topic_garage = {
    "distanceA": 'efrei/liu_ravailhe/garage/distanceA', # Set distance A to open the door automatically
    "distanceB": 'efrei/liu_ravailhe/garage/distanceB', # Set a smaller distance B to close the door
    "status": 'efrei/liu_ravailhe/garage/status' # Show car parking status (distance < B)
}


####### Set up Broker #######

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


####### Application #######

#### Variables ####

alarm_status = None
clim_temperature = None
garage_status = None
verbose = False

#### Methods ####

# Alarms
def alarm_enable():
    client.publish(topic_alarm["enable"])

def alarm_disable():
    client.publish(topic_alarm["disable"])

def alarm_get_status():
    if alarm_status:
        print("Alarm status: Enable")
    else:
        print("Alarm status: Disable")

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
    print(clim_temperature)

# Garage
def garage_distanceA(distance):
    client.publish(topic_garage["distanceA"], distance)

def garage_distanceB(distance):
    client.publish(topic_garage["distanceB"], distance)

def garage_get_status():
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
       global clim_temperature
       clim_temperature = payload
       if verbose:
            print(f"Temperature: {clim_temperature}")
    
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

try:
    while True:
        choice = input("Choose a service (1: Alarm, 2: Light, 3: Climatization, 4: Garage), or 'Q' to quit: ")

        if choice == "q" or choice == "Q":
            break

        # Alarm
        if choice == "1":
            while True:
                alarm_action = input("Select an action (1: Enable alarm, 2: Disable alarm, 3: get alarm status), or 'Q' to quit: ")
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
        
        # Light
        elif choice == "2":
            while True:
                light_action = input("Select an action (1: Enable light, 2: Disable light), or 'Q' to quit: ")
                if light_action == "1":
                    light_room = input("Select a room ('0' to select all rooms), or 'Q' to quit: ")

                    if light_room == "q" or light_room == "Q":
                        print()
                        print()
                        break
                
                    # Verify room exists
                    light_enable(light_room)

                elif light_action == "2":
                    light_room = input("Select a room ('0' to select all rooms), or 'Q' to quit: ")

                    if light_room == "q" or light_room == "Q":
                        print()
                        print()
                        break
                
                    # Verify room exists
                    light_disable(light_room)

                elif light_action == "q" or light_action == "Q":
                    print()
                    print()
                    break

                else:
                    print("Invalid value, try again")

        # Climatization
        elif choice == "3":
            while True:
                clim_action = input("Select an action (1: Set AC trigger, 2: Set Heater trigger, 3: Display temperature), or 'Q' to quit: ")
                if clim_action == "1":
                    trigger = input("Select a AC trigger ('none' to disable), or 'Q' to quit: ")

                    if trigger == "q" or trigger == "Q":
                        print()
                        print()
                        break
                
                    # Verify room exists
                    clim_ac_trigger(trigger)

                elif clim_action == "2":
                    trigger = input("Select a Heater trigger ('none' to disable), or 'Q' to quit: ")

                    if trigger == "q" or trigger == "Q":
                        print()
                        print()
                        break
                
                    # Verify room exists
                    clim_heater_trigger(trigger)
                
                elif clim_action == "3":
                    clim_get_temperature()

                elif clim_action == "q" or clim_action == "Q":
                    print()
                    print()
                    break

                else:
                    print("Invalid value, try again")
        
        # Garage
        elif choice == "4":
            while True:
                garage_action = input("Select an action (1: Set distance A, 2: Set distance B, 3: Get garage status), or 'Q' to quit: ")
                if garage_action == "1":
                    distance = input("Select a distance, or 'Q' to quit: ")

                    if distance == "q" or distance == "Q":
                        print()
                        print()
                        break
                
                    # Verify room exists
                    clim_ac_trigger(distance)

                elif garage_action == "2":
                    distance = input("Select a trigger, or 'Q' to quit: ")

                    if distance == "q" or distance == "Q":
                        print()
                        print()
                        break
                
                    # Verify room exists
                    clim_heater_trigger(distance)

                elif garage_action == "3":
                    garage_get_status()

                elif garage_action == "q" or garage_action == "Q":
                    print()
                    print()
                    break

                else:
                    print("Invalid value, try again")

        elif choice == "t" or choice == "T":
            # Request temperature reading
            client.subscribe(f"efrei/liu_ravailhe/temperature")

        else:
            print("Invalid choice, try again")

    
except KeyboardInterrupt:
    pass

finally:
    client.disconnect()
    print("Disconnected from the broker.")