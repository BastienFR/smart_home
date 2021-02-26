##########
####
##    Morning Sun
####
##########

## The function turn on slowly a smart light through MQTT and keep the light on for
## a certain ammount of time.  The goal of the function is to help me wake up in the morning

## It is run with a crontab job on my rpi
## cron line of code:
###  crontab -e
###    40 5 * * * python /home/smart_home/morning_sun.py

 
###  Modules needed
import time
import paho.mqtt.client as paho
import datetime

###  Parameters to adjust
broker="192.168.1.66"  # MQTT broker address
sun_rise_duration = int(20) # time wanted to go from 0 to 100% intensity in minutes
day_length = 3600 # in seconds
day_off = ["2021-04-02","2021-04-05","2021-05-24","2021-06-24",
           "2021-07-01","2021-09-06","2021-10-11", "2021-12-24",
           "2021-12-27", "2021-12-28", "2021-12-31"]  # the week days you don't want to sun to rise

### Calculation needed

## what is the day today
today = datetime.datetime.date(datetime.datetime.now()).strftime("%Y-%m-%d")
print(today)

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
            print(x)
            time.sleep(wait_time)

        time.sleep(day_length)  ## time to keep the sun up
        client.publish("home/master/globe_bulb_2/cmnd/POWER","off")

        ## disconnect the service
        client.disconnect() #disconnect
        client.loop_stop() #stop loop


        

        
