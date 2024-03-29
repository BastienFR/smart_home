######
###
#   Run when kodi starts playback
###
#####

## Bastien Ferland-Raymond
## march 18 2021

## This script should be run when kodi starts playback.
## It will close the window blind
## It will dim the side light if it's night time
## It will turn off the seeling light 


## load packages, they have to be export in a folder with this script as they are not available for kodi otherwise
import time
import datetime
import math
import resources.pytz as pytz
import resources.paho.mqtt.client as paho
from sys import version_info
if version_info[0] < 3:
    import os
    dirname = os.path.dirname(os.path.abspath(__file__))
    file_fc_sun = os.path.join(dirname, 'resources/evaluate_sunset_sunrise.py')
    execfile(file_fc_sun)  # python 2?
else:
    exec(open("resources/evaluate_sunset_sunrise.py").read())  # Python 3?

## prepare time information:
#### Find sunset and sunrise
latitude_deg = 46.829853
longitude_deg = -71.254028
timezone = datetime.datetime.now(pytz.timezone('America/Toronto')).strftime('%z')
timezone = int(timezone) / 100
sunrise, sunset = calculate_rise_set(latitude_deg, longitude_deg, timezone)
offset = 45  # number of minutes after sunrise or before sunset to consider it's light out
now = datetime.datetime.now()

## Set and connect to the MQTT broker 
broker="192.168.1.66"

### define callback
def on_message(client, userdata, message):
    time.sleep(1)
    print("received message =",str(message.payload.decode("utf-8")))

client= paho.Client("client-001") 
######Bind function to callback
client.on_message=on_message
#####
print("connecting to broker ",broker)
client.connect(broker)#connect
client.loop_start() #start loop to process received messages


## Do the required task

### Close the blind
client.publish("home/boudoir/blind/0/set",100)

### Turn off the ceiling light
### but only if not between 16 and 18, has it's when my kids watch tv and I want them to have light

#### preparing function
def in_between(now, start, end):
    if start <= end:
        return start <= now < end
    else: # over midnight e.g., 23:30-04:15
        return start <= now or now < end
      
if in_between(now.time(), datetime.time(16), datetime.time(18)):
    client.publish("home/boudoir/dimmer_MJ_1/cmnd/Dimmer",50)
else:
    client.publish("home/boudoir/dimmer_MJ_1/cmnd/Dimmer",0)

### Dim the side lamp (only at night)
dawn = sunrise + datetime.timedelta(minutes = offset)
dust = sunset - datetime.timedelta(minutes = offset)

daylight = (dawn.replace(tzinfo=None) < now < dust.replace(tzinfo=None))

if not daylight:
    client.publish("home/boudoir/globe_bulb_1/cmnd/Dimmer",33)

time.sleep(4)
client.disconnect() #disconnect
client.loop_stop() #stop loop
