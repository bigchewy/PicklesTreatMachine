#!/usr/bin/python

#generic imports
from time import sleep #, strftime
import json

import random
import time
import datetime
import logging

#class to operate the treat dispensers
from classTreatDispenser import TreatDispenser
from classEmailServer import EmailServer
from classPerson import Person

# Import Adafruit IO MQTT client
from Adafruit_IO import MQTTClient
conf = json.load(open('conf.json'))
isFirstMQTTMessage = True

logging.basicConfig(filename=conf["log"]["logListenMQTT"],level=logging.DEBUG)

##########################################
#Adafruit related functions
##########################################

# Define callback functions which will be called when certain events happen.
def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    # This is a good place to subscribe to feed changes.  The client parameter
    # passed to this function is the Adafruit IO MQTT client so you can make
    # calls against it easily.
    print 'Connected to Adafruit IO!  Listening for {0} changes...'.format(conf["adafruit"]["FEED_ID"])
    # Subscribe to changes on a feed.
    client.subscribe(conf["adafruit"]["FEED_ID"])

def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print 'Disconnected from Adafruit IO!'
    sys.exit(1)

def message(client, feed_id, payload):
    # Message function will be called when a subscribed feed has a new value. The feed_id parameter identifies the feed, and the payload parameter has
    # the new value.

	global isFirstMQTTMessage

	logging.info('MQTT notification received at ' + str(datetime.datetime.now()) + ' with payload of ' + payload)
	
	if isFirstMQTTMessage == True:
		isFirstMQTTMessage = False
		print 'Do not dispense treat because service is just starting'
	else:
		tempEmail = None

		print 'payload is: ' + payload
		#Special use case for when we need some alone time and want the dog to eat treats instead of trying to be with us
		if payload == 'AloneTime':
			print 'AloneTime'
#			dispenser.startCamera() 
#			for i in range (0,10):
#				dispenser.makeNoise()
#				dispenser.dispenseTreats()
#				if dispenser.isMotionDetected():
#					dispenser.trackUntilNoMotion()
#				else:
#					sleep(7)
#					dispenser.makeNoise() 
#					sleep(25)
			
		#normal case of just dispensing treats
		else:
			person.setKey (payload)
			if person.getEmail() == 'nothing':	#no email corresponding to the  payload
				print 'No email corresponding to payload: ' + payload
			else:
				emailServer.setMailList(person.getEmail())
				dispenser.makeNoise()
				dispenser.dispenseTreats()
				if dispenser.isMotionDetected():
					dispenser.takeVideo()
					if payload == conf["proactive"]["proactiveTrigger"]:
						emailServer.setProactivelyDelivered() #set variables to indicate that Pickles dispensed his own treats
					else:
						emailServer.setTreatReceived() #set the email server variables to return a response to the server
					emailServer.sendThankYou()
				else:
					emailServer.setTreatNotReceived()
					emailServer.sendThankYou()
	
	print 'waiting for next triggering event...'

##########################################
#INSTANTIATE CLASSES
##########################################

print 'begin initialization process'
dispenser = TreatDispenser('dispenser')
print 'dispenser initialized'
emailServer = EmailServer('emailServer')
print 'email server initialized'
person = Person('person')
print 'person initialized'

# Create an MQTT client instance.
client = MQTTClient(conf["adafruit"]["ADAFRUIT_IO_USERNAME"], conf["adafruit"]["ADAFRUIT_IO_KEY"])

# Setup the callback functions defined above.
client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message

try:

	# Connect to the Adafruit IO server.
	client.connect()

	#Run a thread in the background so you can continue doing things in your program.
	client.loop_background()
#	client.loop_blocking()
	sleep(2)

	# Now send new values every X seconds. This is done simply to keep the connection alive
	print 'Publishing a new message periodically to keep the connection alive (press Ctrl-C to quit)...'
	while True:
		value = random.randint(0, 100)
		print 'Publishing {0} to outbound feed.'.format(value)
		client.publish(conf["adafruit"]["outboundFeed"], value)
		time.sleep(conf["adafruit"]["MQQTPublishingDelay"])

except KeyboardInterrupt:
	pass
	
except Exception, e:
	print e
	logging.error('Exception raise', exc_info=True)
	emailServer.setMailList(conf["log"]["developerEmail"])
	emailServer.sendErrorMessage(e)
	
finally:
	dispenser.cleanupTreatDispenser()
	logging.info('Program terminated at ' + str(datetime.datetime.now()))
