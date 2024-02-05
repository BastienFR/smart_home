######
###
#   Run when kodi pause playback
###
#####

## Bastien Ferland-Raymond
## march 18 2021

## This script should be run when kodi pause playback.
## It will simply dim the ceiling light if it's night
## leaving everything else asis


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

### Turn on the ceiling light (dimmed) (only at night)
dawn = sunrise + datetime.timedelta(minutes = offset)
dust = sunset - datetime.timedelta(minutes = offset)

daylight = (dawn.replace(tzinfo=None) < now < dust.replace(tzinfo=None))

if not daylight:
    client.publish("home/boudoir/dimmer_MJ_1/cmnd/Dimmer",60)

time.sleep(4)
client.disconnect() #disconnect
client.loop_stop() #stop loop
