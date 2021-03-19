######
###
#   Run when kodi stop playback
###
#####

## Bastien Ferland-Raymond
## march 18 2021

## This script should be run when kodi stops playback.
## It will open the window blind
## It will turn off side light
## It will turn on the seeling light if it's night time


## load packages, they have to be export in a folder with this script as they are not available for kodi otherwise
import time
import datetime
import resources.paho.mqtt.client as paho
from resources.astral import LocationInfo
from resources.astral.sun import sun

## prepare time information:
#### Find dusk and dawn
loc = LocationInfo(name='QC', timezone='America/Toronto',
                   latitude= 46.829853, longitude=-71.254028)
s = sun(loc.observer, date=datetime.datetime.date(datetime.datetime.now()), tzinfo=loc.timezone)
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

### Open the blind
client.publish("home/boudoir/blind/0/set",0)

### Turn on the ceiling light (dimmed) (only at night)
if(not (s["dawn"].replace(tzinfo=None) < now < s["dusk"].replace(tzinfo=None))) 
    client.publish("home/boudoir/dimmer_MJ_1/cmnd/Dimmer",70)

### Turn off the side lamp 
client.publish("home/boudoir/globe_bulb_1/cmnd/Dimmer",0)

time.sleep(4)
client.disconnect() #disconnect
client.loop_stop() #stop loop
