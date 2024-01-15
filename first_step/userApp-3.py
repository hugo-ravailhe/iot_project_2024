import paho.mqtt.client as mqtt

broker_address = "127.0.0.1"
broker_port = 1883
keep_alive_interval = 60

# Initialize MQTT client for UserApp
client = mqtt.Client("UserApp")

# Callback when a message is received from the broker
def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")

client.on_message = on_message

# Connect to the broker
client.connect(broker_address, broker_port, keepalive=keep_alive_interval)

# Start the MQTT client loop to handle messages
client.loop_start()

try:
    while True:
        choice = input("Choose an action (L for LED control, T for temperature reading), or 'Q' to quit: ")

        if choice == "q" or choice == "Q":
            break

        if choice == "l" or choice == "L":
            while True:
                led_action = input("Enter 0 to turn off the LED, 1 to turn on, or 'Q' to quit: ")
                if led_action == "0" or led_action == "1":
                    client.publish(f"efrei/liu_ravailhe/led", led_action)
                elif led_action == "q" or led_action == "Q":
                    break
                else:
                    print("Invalid value")

        elif choice == "t" or choice == "T":
            # Request temperature reading
            client.subscribe(f"efrei/liu_ravailhe/temperature")

        else:
            print("Invalid choice")

except:
    client.disconnect()
    print("Disconnected from the broker.")