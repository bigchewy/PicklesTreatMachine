#!/usr/bin/python

#generic imports
import time
import os
import subprocess
from time import sleep, strftime
from subprocess import *
from subprocess import call
from datetime import datetime
import json


#imports for email
import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.parser import HeaderParser
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.Utils import COMMASPACE, formatdate
from email import Encoders
from random import randint

conf = json.load(open('conf.json'))

temp_list = []

imap_server = imaplib.IMAP4_SSL(conf["email"]["IMAP_ADDRESS"],conf["email"]["IMAP_PORT"])

class EmailServer:
	
	
	def __init__(self, name):
		self.name = name
		self.subjectText = conf["email"]["subjectText"]
		self.bodyText = ''
		self.attachment1 = conf["recordings"]["videoName"]
		self.attachment2 = conf["recordings"]["imageName"]
		self.attachment3 = conf["recordings"]["imageTreatMachine"]
		self.newEmailsArePresent = False
		self.mail_list = []

	##########################################
	#FUNCTION TO SEND THANK-YOU EMAILS
	##########################################

	def sendThankYou(self):
		print "Sending thank you emails"
		for item in self.mail_list:
			files = []
			files.append(self.attachment1)
			files.append(self.attachment2)
			files.append(self.attachment3)
			assert type(files)==list
			msg = MIMEMultipart()
			msg['Subject'] = self.subjectText
			msg['From'] = conf["email"]["emailUserName"]
			msg['To'] = item
			msg.attach ( MIMEText(self.bodyText) )  
			for file in files:
				part = MIMEBase('application', "octet-stream")
				part.set_payload( open(file,"rb").read() )
				Encoders.encode_base64(part)
				part.add_header('Content-Disposition', 'attachment; filename="%s"'
				   % os.path.basename(file))
				msg.attach(part)
			server = smtplib.SMTP(conf["email"]["SMTP_ADDRESS"])
			server.ehlo_or_helo_if_needed()
			server.starttls()
			server.ehlo_or_helo_if_needed()
			server.login(conf["email"]["emailUserName"],conf["email"]["emailPassword"])
			server.sendmail(conf["email"]["emailUserName"], item, msg.as_string() )
			server.quit()
			print('Email sent to ' + item + '!')

	##########################################
	#method to send email to author with any error message
	##########################################

	def sendErrorMessage(self, exception):
		print "Attempting to send error message"
		
		for item in self.mail_list:
			msg = MIMEMultipart()
			subject = 'There has been a catastrophic error with ' + conf["log"]["dogMaster"] + 's machine'
			msg['Subject'] = subject
			msg['From'] = conf["email"]["emailUserName"]
			msg['To'] = item
			msg.attach ( MIMEText(exception) )  
			server = smtplib.SMTP(conf["email"]["SMTP_ADDRESS"])
			server.ehlo_or_helo_if_needed()
			server.starttls()
			server.ehlo_or_helo_if_needed()
			server.login(conf["email"]["emailUserName"],conf["email"]["emailPassword"])
			server.sendmail(conf["email"]["emailUserName"], item, msg.as_string() )
			server.quit()
			print('Email sent to ' + item + '!')

		print "Error message sent"

			
	###########################################
	#Function to set variables for Pickles not at home e.g. randomly pull different text for the body of the email sent when Pickles is not at home
	###########################################
	def setTreatNotReceived(self):

		self.subjectText = 'Thank you so much but I am not home right now'

		#Set body text
		intRandom = randint(0,4)
		switcher = {
				0: "oh my gosh I'm so sorry that I'm not home to enjoy the treat you gave me. Maybe when I get home a treat will be waiting for me",
				1: "oh boy oh boy oh boy! I'm not home right now but I'm hoping to get home soon so I can enjoy my treat!",
				2: "words can not describe how much I am looking forward to the treat when I get home",
				3: "You have just given me yet another thing to look forward to when I get home - a treat from you!",
				4: "I love you so much. Unfortunately I'm not at home right now. When I get back, I am sooooo going to enjoy the treat you gave me",
		}

		self.bodyText = switcher.get(intRandom, "This will be amazingly awesome when I get home!")
        
		self.attachment1 = conf["recordings"]["imageIsAway"]
		self.attachment2 = conf["recordings"]["videoIsAway"]

		
	###########################################
	#Function to set variables for when Pickles is home e.g. randomly pull different text for the body of the email sent when Pickles is not at home
	###########################################
	def setTreatReceived(self):

		self.subjectText = 'Thank you so much for the treat!'

		#Set body text

		intRandom = randint(0,9)
		switcher = {
			0: "oh my gosh that was so delicious. I love you today, tomorrow and forever", 
			1: "oh boy oh boy oh boy that was good!", 
			2: "words can not describe how much I appreciate what you are doing for me. But if I had to, I would say you are the best friend a dog could ever ask for", 
			3: "Thanks to you, this may be the greatest day of my life", 
			4: "I love you so much. Any chance you want to give me some more? Did I tell you that I love you?", 
			5: "I already love you infinity. Because you gave me the treat, I love you infinity + 1",
			6: "You know, I was just thinking that I could use a treat and then you come along and give me one. You are amazing!",
			7: "Treats! Treats! Treats! I love treats!",
			8: "Wow, an amzing day just got even better",
			9: "Today was already awesome and it just got even better!"
		}
		  
		self.bodyText = switcher.get(intRandom, "Wow, that was amazingly awesome!")

		self.attachment1 = conf["recordings"]["videoName"]
		self.attachment2 = conf["recordings"]["imageName"]

				
	###########################################
	#Function to randomly pull different text for the body of the Thank You - Treat Delivered email
	###########################################
	def setProactivelyDelivered(self):

		print('in set proactively delivered')

		self.subjectText = 'Did you forget about me?'

		#Set body text

		intRandom = randint(0,0)
		switcher = {
			0: "You must be busy so I went ahead and gave myself the treat that I know you wanted me to have. Thank you so much", 
			1: "oh boy oh boy oh boy that was good! What, you didn't trigger the treat machine? hmmmm... maybe I figured out a way to do it myself?!?!", 
			2: "I know you haven't forgotten about me but, because I haven't seen a treat recently, I got a little worried and got some for myself", 
			3: "Remember, it's not who delivers the treat that matters. It's the fact that I got to enjoy them. So I gave some to myself",
		}
 
		self.bodyText = switcher.get(intRandom, "Remembember, it's not who delivers the treat that matters. It's the fact that I got to enjoy them. So, yes, I did dispense these myself")

		self.attachment1 = conf["recordings"]["imageName"]
		self.attachment2 = conf["recordings"]["videoName"]

#		self.mail_list = []
#		self.mail_list.append(conf["proactive"]["proactiveEmailRecipient"])
#		print('List of email senders: ', self.mail_list)

	###########################################
	#Set triggered by AdafruitIO
	###########################################
	def setMailList(self, emailAddress):
		self.mail_list = []
		self.mail_list.append(emailAddress)
#		self.mail_list.append(conf["proactiveEmailRecipient"])
		
	###########################################
	#Method to login to the email server and generate the list of unread emails
	###########################################
	def generateUnreadEmailList(self):
		imap_server = imaplib.IMAP4_SSL(conf["email"]["IMAP_ADDRESS"],conf["email"]["IMAP_PORT"])
		imap_server.login(conf["email"]["emailUserName"], conf["email"]["emailPassword"])
		imap_server.select('INBOX')
		
		# Search inbox for unread emails 
		status, email_ids = imap_server.search(None, '(UNSEEN)')    #The SEARCH command searches the mailbox for messages that match the given searching criteria.  Searching criteria consist of one or more search keys. The untagged SEARCH response from the server contains a listing of message sequence numbers corresponding to those messages that match the searching criteria. Status is result of the search command: OK - search completed, NO - search error: can't search that charset or criteria, BAD - command unknown or arguments invalid. Criteria we are using here is looking for unread emails
		if email_ids == ['']:
			print('No Unread Emails')
			self.mail_list = []
		else:
			for e_id in email_ids[0].split():              #Loops IDs of a new emails created from email_ids = imap_server.search(None, '(UNSEEN)')
				resp, data = imap_server.fetch(e_id, '(RFC822)')   #FETCH command retrieves data associated with a message in the mailbox.  The data items to be fetched can be either a single atom or a parenthesized list. Returned data are tuples of message part envelope and data.
				perf = HeaderParser().parsestr(data[0][1])     #parsing the headers of message
				self.mail_list.append(perf['From'])          #Looks through the data parsed in "perf", extracts the "From" field 
			print('List of email senders: ', self.mail_list)         #FYI when calling the get_senders function, the email is marked as 'read'
			print len(self.mail_list),
			print("New emails!")

		imap_server.close()
				
		if self.mail_list:
				return True
		else:
				return False
						
	###########################################
	#get individual email address 
	###########################################
	def getEmail(self):
		shortEmail = ''
		for i in self.mail_list:
			if i > 0:
				shortEmail = shortEmail + ";"
			begin = i.find("<")
			begin = begin + 1
			end = i.find(">")
			shortEmail = i[begin:end]
			print shortEmail 
		return shortEmail 
