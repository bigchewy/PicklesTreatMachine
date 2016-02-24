#!/usr/bin/env python
  
#generic imports
import time
#import os
#import subprocess
from time import sleep, strftime
import datetime
#from subprocess import *
#from subprocess import call
import json

#imports for OpenCV motion detection system
from classCamera import Camera

#imports for audio player
import pygame
	
#arduino connector stuff
#import serial

#control the stepper motor
import RPi.GPIO as GPIO

#holds all the variables
conf = json.load(open('conf.json'))

#ser = serial.Serial(conf["arduino"]["ARDUINO_PORT"], conf["arduino"]["ARDUINO_BAUD"])
 
#GPIO pins for the stepper motor 
enable_pin = 18
coil_A_1_pin = 4
coil_A_2_pin = 17
coil_B_1_pin = 23
coil_B_2_pin = 24


delay = 5 #delay betweeen steps in the motor. in milliseconds
steps = 512 #steps each time the motor is turned on. Represents 1 full revolution

class TreatDispenser:

	def __init__(self, name):
		self.name = name

		print 'setting up camera'
		self.camera = Camera('camera')

		#setup the stepper motor
		GPIO.cleanup()
		print 'setting up GPIO pins for stepper motor'
		GPIO.setmode(GPIO.BCM)		 
#		GPIO.setup(enable_pin, GPIO.OUT)
		GPIO.setup(coil_A_1_pin, GPIO.OUT)
		GPIO.setup(coil_A_2_pin, GPIO.OUT)
		GPIO.setup(coil_B_1_pin, GPIO.OUT)
		GPIO.setup(coil_B_2_pin, GPIO.OUT)

		GPIO.output(coil_A_1_pin, False)
		GPIO.output(coil_A_2_pin, False)
		GPIO.output(coil_B_1_pin, False)
		GPIO.output(coil_B_2_pin, False)

		#only use when using the L293D  
		#GPIO.output(enable_pin, 1)

		print 'GPIO pins established'

#	def __enter__(self):
#		self.name = 'dispenser'
#		self.camera = Camera('camera')
#		return self.name

#	def __exit__(self, type, value, traceback):
#		print "Exit treat dispenser object"
#		return False
#		return isInstance(value, TypeError)

	def cleanupTreatDispenser(self):
		print 'cleaning up treat dispenser instance'
		GPIO.cleanup()
		

	##########################################
	#Start camera
	##########################################
#	def startCamera(self):
#		self.camera.startCamera()

	##########################################
	#Stop camera
	##########################################
#	def stopCamera(self):
#		self.camera.stopCamera()
				
	##########################################
	#DETECT SIGNIFICANT MOTION IN THE FIELD OF VISION
	##########################################
	def isMotionDetected(self):
		print 'in motion detection'
		return self.camera.isMotionDetected()
	
	##########################################
	#TAKE VIDEO
	##########################################
	def takeVideo(self):
		print 'taking video now'
		self.camera.takeVideo()
		
	##########################################
	#Upload video to Dropbox
	##########################################
	def uploadToDropbox(self):
		format = "%a%b%d:%H:%M"
		dropboxVideoName = "Videos/Pickles" + time.strftime(format) + ".avi"
		#dropboxVideoName25 = "Videos/Pickles25:" + time.strftime(format) + ".mp4"
		#dropboxVideoName30 = "Videos/Pickles30:" + time.strftime(format) + ".mp4"

		print "uploading " + dropboxVideoName
		uploadtoDropboxShellCommand = "/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload /home/pi/Pickles.avi " + dropboxVideoName 
		call([uploadtoDropboxShellCommand], shell=True)

		print 'Video Uploaded to Dropbox'
		
	##########################################
	#Track until no motion
	##########################################	
	def trackUntilNoMotion(self):
		print "continue tracking until no more motion is not implemented yet"


	##########################################
	#Make noise so Pickles knows the treats are coming
	##########################################	
	def makeNoise(self):
		print "let Pickles know a treat is coming"
		pygame.mixer.init()
		pygame.mixer.music.load("makeNoise.wav")
		pygame.mixer.music.play()
		while pygame.mixer.music.get_busy() == True:
			continue
		
		
	##########################################
	#Dispense the treats by letting the Arduino know it's time for dispensing
	#########################################
	def dispenseTreats(self):
		print "Dispense the treat!"

		#rotate 1/2 way so that that dispenser is open and dispensing treats
		for i in range(0, int(steps/2)):

			self.setStep(1, 0, 0, 0)
			time.sleep(int(delay)/1000.0)
			self.setStep(0, 1, 0, 0)
			time.sleep(int(delay)/1000.0)
			self.setStep(0, 0, 1, 0)
			time.sleep(int(delay)/1000.0)
			self.setStep(0, 0, 0, 1)
			time.sleep(int(delay)/1000.0)

		#pause for a bit with the opening at the bottom to allow all treats to drop
		time.sleep(2)


		#rotate 1/2 way so that that dispenser is back up to the top
		for i in range(0, int(steps/2)):

			self.setStep(1, 0, 0, 0)
			time.sleep(int(delay)/1000.0)
			self.setStep(0, 1, 0, 0)
			time.sleep(int(delay)/1000.0)
			self.setStep(0, 0, 1, 0)
			time.sleep(int(delay)/1000.0)
			self.setStep(0, 0, 0, 1)
			time.sleep(int(delay)/1000.0)

#old code to rotate the dispenser. may be more accurate, better torque, something. not really sure but didn't want to delete in case the code above isn't working
			#print "step " + str(i) 
			#print "delay " + str(int(delay)/1000.0)
#			self.setStep(1, 0, 1, 0)
#			time.sleep(int(delay)/1000.0)
#			self.setStep(0, 1, 1, 0)
#			time.sleep(int(delay)/1000.0)
#			self.setStep(0, 1, 0, 1)
#			time.sleep(int(delay)/1000.0)
#			self.setStep(1, 0, 0, 1)
#			time.sleep(int(delay)/1000.0)

		print "treat dispensed with " + str(steps) + " steps" 

	def setStep(self, w1, w2, w3, w4):

		GPIO.output(coil_A_1_pin, w1)
		GPIO.output(coil_A_2_pin, w2)
		GPIO.output(coil_B_1_pin, w3)
		GPIO.output(coil_B_2_pin, w4)
