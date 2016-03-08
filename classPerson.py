#!/usr/bin/env python
  
##################################
# Absolutely terrible code that needs to be updated.
#General purpose is to determine the email address of the person who triggered the treat machine,
#if it was triggered via some method other than email.
#This could be updated to remove the switchers, perhaps putting them in a json file
#It could also be used if/when the results of the treat machine are sent back via SMS vs email
##################################


#generic imports
from email.utils import parseaddr
import json

conf = json.load(open('conf.json'))
	
class Person:

	def __init__(self, name):

		self.name = name
		self.key = None
		self.email = None
		self.cellPhoneNumber = None		

	def setKey (self, payload):
		
		if payload == conf["proactive"]["proactiveTrigger"]:  # payload is the proactive triggering 
			self.email = conf["proactive"]["proactiveEmailRecipient"]

		elif self.isPayloadEmail(payload):
			self.email = payload 
			print 'Payload is email' 
			
		else: #payloadIsKey():
			self.key = payload
			print 'payload is key' 
			
			print 'setting email and cell based on key value'
			switcher = {
				'JanisPage' : 'janispage7@gmail.com',
				'EmilyHannon' : 'ekate.hannon8@gmail.com',
				'AliHannon' : 'amhannon10@gmail.com',
				'LeahHannon' : 'lhannon11@gmail.com',
				'ShirinOreizy' : 'soreizy@gmail.com',
				'EricPage' : 'eric.w.page@gmail.com',
				'JenHannon' : 'jen.hannon5@gmail.com'
			}
			
			self.email = switcher.get(self.key, 'nothing')

			print 'class person.email: ' + self.email 
			
			switcher = {
				'JanisPage' : '5084239583',
				'EmilyHannon' : '9787329678',
				'AliHannon' : '9788683872',
				'LeahHannon' : '9788555404',
				'ShirinOreizy' : '4159941681',
				'EricPage' : '2064911065',
				'JenniferHannon' : '9784337997'
			}
			
			self.cellPhoneNumber = switcher.get(self.key, 'nothing')			

		
	def getEmail(self):
		return self.email
		
	def getCell(self):
		return self.cellPhoneNumber
		
	def isPayloadEmail(self, payload):
		if '@' in payload:
			return True
		else: 
			return False
		
		
