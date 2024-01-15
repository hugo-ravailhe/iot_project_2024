# iot_project_2024

# Set up env
## Install Python library
```bash
sudo pip install paho-mqtt
```

## Install and run mosquitto
```bash
sudo apt-get install mosquitto mosquitto-clients
```
```bash
sudo /etc/init.d/mosquitto start
```

```py
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("$SYS/#")

def on_message(client, userdata, msg):
    try:
        print(msg.topic+" "+str(msg.payload))
    except UnicodeDecodeError:
        pass
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
# Using the broker hosted at localhost
client.connect("127.0.0.1", 1883, 60)
client.loop_forever()
```