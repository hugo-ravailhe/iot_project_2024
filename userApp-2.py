import paho.mqtt.client as mqtt
from gpiozero import LED

# Define the broker and topics
broker_address = "test.mosquitto.org"
broker_port = 1883
keep_alive_interval = 60

led_topic = "efrei/OUVIOT-PRJ/2324S9-01/led"

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(led_topic)

# Callback when a message is received from the broker
def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")

# Create an MQTT client instance
client = mqtt.Client()

# Set the callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(broker_address, broker_port, keepalive=keep_alive_interval)

# Start the MQTT client loop to handle messages
client.loop_start()

try:
    while True:
        user_input = input("Enter 0 to turn off the LED, 1 to turn on, or 'q' to quit: ")
        
        if user_input.lower() == 'q':
            break
        
        if user_input in ['0', '1']:
            client.publish(led_topic, user_input)
        else:
            print("Invalid input. Please enter 0 to turn off or 1 to turn on.")
            
except KeyboardInterrupt:
    # Disconnect the client upon keyboard interruption
    client.disconnect()
    print("Disconnected from the broker.")
