IOT Project 2024
=

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

# Project Overview
We divide our projet in three services. The Broker, the Device App and the User App.

To run our project you have to open two terminals.
In the first one (device terminal) run those commands:
```
cd part_two
python deviceApp.py
```

In the second one (user terminal):
```
cd part_two
python userApp.py
```

Then follow the instruction on the user terminal and enjoy.

---------

Here is the output of the user interface.
```
    /\ 
   /  \ 
  /----\ 
 /      \
 |  .-.  |
 |  | |  |
 |__|_|__|

Smart Home Application is starting...


Connected with result code 0

Smart Home Application Menu
1. Alarm
2. Light
3. Climatization
4. Garage
Q. Quit

Choose an option: 
```

It's divide in four services:
- Alarm
- Light
- Climatization
- Garage

Each one have differents commands.

# Project Explanation

##  Smart Home sketch

### Overview :
![IMG_20240122_161606](https://github.com/hugo-ravailhe/iot_project_2024/assets/73168837/5485d20a-b274-46b1-b246-d842cbd73784)

### LED :
![IMG_20240122_161629](https://github.com/hugo-ravailhe/iot_project_2024/assets/73168837/e9acbb22-029d-4750-9561-c060cd0abfce)

### Buzzer :
![IMG_20240122_161634](https://github.com/hugo-ravailhe/iot_project_2024/assets/73168837/7ec73999-b5ac-4987-82dc-aeb61b74ffed)

### Sonar, temperature & movement detector :
![IMG_20240122_161656](https://github.com/hugo-ravailhe/iot_project_2024/assets/73168837/e1523407-7340-45aa-96d1-b16c17f92ae1)

### Cervo motor :
![IMG_20240122_161706](https://github.com/hugo-ravailhe/iot_project_2024/assets/73168837/7a69ec10-70e0-4304-b2af-cc0f1732ce37)

### GPIO Header :
![IMG_20240122_175200](https://github.com/hugo-ravailhe/iot_project_2024/assets/73168837/d31d793e-11c7-467f-b2a4-0b50ca50bd7e)
