#!/usr/bin/python

#generic imports
import time
from time import sleep, strftime
import datetime
from datetime import timedelta
import json
from random import randint
import math
import logging

#class to operate the treat dispensers
#from classTreatDispenser import TreatDispenser
from classEmailServer import EmailServer 

#from Adafruit_IO import MQTTClient
from Adafruit_IO import Client

#key = None

conf = json.load(open('conf.json'))

##########################################
#Periodically proactively dispense treats
##########################################
def isTimeToProactivelyDispense():

	#Figure out how many hours the dog is likely to be alone
	numHoursToDispense = conf["proactive"]["randomDispenseEndHour"] - conf["proactive"]["randomDispenseStartHour"]

	#add a fudge factor for likely dog walker, etc. Need to increase the frequency of dispensing because sometimes it will dispense mid day while dog is gone
	numHoursToDispense = numHoursToDispense*1.25

	#Method is run every time the main program loops so calculate the number of times the program runs each hour 
	#then use that to calculate how often the randomizer comes back True
	numTimesRunPerHour = 60*60/conf["email"]["programpause"]
	maxRandomNumber = numHoursToDispense*numTimesRunPerHour/conf["proactive"]["avgRandomTreatsPerDay"]
	intRandom = randint(0,int(math.ceil(maxRandomNumber)))

	print "Random number is " + str(intRandom) + "out of max " + str(maxRandomNumber)

	now = datetime.datetime.now()
	todayStart = now.replace(hour=conf["proactive"]["randomDispenseStartHour"], minute=0, second=0, microsecond=0)
	todayEnd = now.replace(hour=conf["proactive"]["randomDispenseEndHour"], minute=0, second=0, microsecond=0)
		
	if now < todayStart:
		print "too early"
	elif now > todayEnd:
		print "too late"
			
	if intRandom == 0 and now > todayStart and now < todayEnd:
		return True
	else:
		return False


try:

	##########################################
	#MAIN BODY SETUP
	##########################################
	emailServer = EmailServer('emailServer')
	aio = Client(conf["adafruit"]["ADAFRUIT_IO_KEY"])
	logging.basicConfig(filename=conf["log"]["logListenTriggers"],level=logging.DEBUG)

	##########################################
	#MAIN BODY. SEARCHES FOR UNREAD EMAILS OR OTHER TRIGGERS FOR THE TREAT MACHINE
	##########################################
	
	nextTimeEmailChecked = datetime.datetime.now()

	print "Starting the while loop"

	while True:

		if emailServer.generateUnreadEmailList(): 
			#if emails have come through triggering the treat machine, send notification via MQQT
			aio.send(conf["adafruit"]["FEED_ID"], emailServer.getEmail())  
			print "sent notification via MQTT" + emailServer.getEmail() + ": " + str(datetime.datetime.now())
			logging.info("sent notification via MQTT" + emailServer.getEmail() + ": " + str(datetime.datetime.now()))
		elif isTimeToProactivelyDispense(): 
			#if it's time to proactively dispens, send notification via MQQT
			aio.send(conf["adafruit"]["FEED_ID"], conf["proactive"]["proactiveTrigger"])
			print "proactive dispensing triggered" + str(datetime.datetime.now())
			logging.info("proactive dispensing triggered" + str(datetime.datetime.now()))

		#only check for emails periodically
		lastTimeEmailChecked = nextTimeEmailChecked
		nextTimeEmailChecked = nextTimeEmailChecked + datetime.timedelta(seconds = conf["email"]["programpause"])
		print "program will check email again at " + str(nextTimeEmailChecked)
		logging.info("program will check email again at " + str(nextTimeEmailChecked))
		sleep(conf["email"]["programpause"])


except KeyboardInterrupt:
	pass
	
except Exception, e:
	logging.error('Exception raise', exc_info=True)
	
finally:
	logging.info('Program terminated at ' + str(datetime.datetime.now()))

