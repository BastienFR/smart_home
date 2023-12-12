##########
####
##    Morning Sun
####
##########

## The function turn on slowly a smart light through MQTT and keep the light on for
## a certain ammount of time.  The goal of the function is to help me wake up in the morning

## It is run with a crontab job on my rpi (don't forget to set the time zone setting of the pi)
## cron line of code:
###  crontab -e
###    40 5 * * * TZ=America/Toronto python3 /home/smart_home/morning_sun.py

 
###  Modules needed
import time
import paho.mqtt.client as paho
import datetime
import holidays

## what is the day today
today = datetime.datetime.date(datetime.datetime.now())
print(today)

###  Parameters to adjust
broker="192.168.1.66"  # MQTT broker address
sun_rise_duration = int(30) # time wanted to go from 0 to 100% intensity in minutes
day_length = 3600 # in seconds

### Managing the day I don't want the light to turn on.

#### find the holidays for a bunch of coming years
holiday = []
for ptr in holidays.CA(years = [2023, 2024, 2025, 2026], prov="QC").items(): 
    holiday.append(ptr)

##### Adding good friday which I have but is not offical
h = holidays.CA(years=2022, prov="QC")
good_monday = h.get_named('Good Friday')[0] + datetime.timedelta(days=4)

#### Set my upcoming vacations
num_of_dates = 22
vacations_start = datetime.date(2024, 7, 26)
vacations_days = [vacations_start +  datetime.timedelta(days=x) for x in range(num_of_dates)]

#### join both
day_off = vacations_days
day_off.append(holiday)
day_off.append(good_monday)
print(today in day_off)

### Calculation needed


## what day of the week is it?
day_of_week = datetime.datetime.today().weekday()
print(day_of_week)  # 0 is monday, 6 is sunday

## if today is not a day off:
if today not in day_off:
    ## And it's a week day
    if day_of_week < 5:
        ## then:
        
        ## connect to the mqtt server:
        #define callback
        def on_message(client, userdata, message):
            time.sleep(1)
            print("received message =",str(message.payload.decode("utf-8")))

        client= paho.Client("client-001") #create client object client1.on_publish = on_publish #assign function to callback client1.connect(broker,port) #establish connection client1.publish("house/bulb1","on")
        ######Bind function to callback
        client.on_message=on_message
        #####
        print("connecting to broker ",broker)
        client.connect(broker)#connect
        client.loop_start() #start loop to process received messages
        print("publishing ")

        ## Turn on the light slowly
        wait_time = sun_rise_duration * 60 / 100 # calculated the time step between increament

        for x in range(101):
            client.publish("home/master/globe_bulb_2/cmnd/Dimmer",x)
            client.publish("home/master/globe_bulb_3/cmnd/Dimmer",x)
            print(x)
            time.sleep(wait_time)

        time.sleep(day_length)  ## time to keep the sun up
        client.publish("home/master/globe_bulb_2/cmnd/POWER","off")
        client.publish("home/master/globe_bulb_3/cmnd/POWER","off")

        ## disconnect the service
        client.disconnect() #disconnect
        client.loop_stop() #stop loop


        

        
