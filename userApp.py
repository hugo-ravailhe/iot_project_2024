import paho.mqtt.client as mqtt

# Define the broker and topics
broker_address = "test.mosquitto.org"
broker_port = 1883
keep_alive_interval = 60

pressure_topic = "efrei/OUVIOT-PRJ/2324S9-01/pressure"
temperature_topic = "efrei/OUVIOT-PRJ/2324S9-01/temperature"
time_topic = "efrei/OUVIOT-PRJ/2324S9-01/timestamp"

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribe to topics upon successful connection
    client.subscribe(pressure_topic)
    client.subscribe(temperature_topic)
    client.subscribe(time_topic)

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

# Keep the application running
try:
    while True:
        pass
except KeyboardInterrupt:
    # Disconnect the client upon keyboard interruption
    client.disconnect()
    print("Disconnected from the broker.")
