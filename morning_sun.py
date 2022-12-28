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
###    40 5 * * * python /home/smart_home/morning_sun.py

 
###  Modules needed
import time
import paho.mqtt.client as paho
import datetime

###  Parameters to adjust
broker="192.168.1.66"  # MQTT broker address
sun_rise_duration = int(30) # time wanted to go from 0 to 100% intensity in minutes
day_length = 3600 # in seconds
day_off = ["2023-12-22","2023-12-23","2023-12-24","2023-12-25","2023-12-26","2023-12-27", "2022-12-28",
           "2022-12-29","2022-12-30","2022-12-31","2023-01-01","2023-01-02","2023-01-03","2023-01-04","2023-01-05",
           "2023-01-06","2023-01-07","2023-01-08",
           "2023-04-07","2023-04-10",
           "2023-05-22",
           "2023-06-24","2023-07-01",
           "2023-08-02","2023-08-03","2023-08-04","2023-08-05","2023-08-06",
	         "2023-08-09","2023-08-10","2023-08-11","2023-08-12","2023-08-13",
	         "2023-08-16","2023-08-17","2023-08-18","2023-08-19","2023-08-20",
           "2023-09-04","2023-10-09"]  # the week days you don't want to sun to rise

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


        

        
