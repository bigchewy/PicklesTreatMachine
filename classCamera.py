#!/usr/bin/env python

# import the necessary packages
from pyimagesearch.tempimage import TempImage
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import warnings
import datetime
import imutils
import json
import time
import cv2
from time import sleep, strftime

conf = json.load(open('conf.json'))
		
class Camera:

	def __init__(self, name):
		self.name = name
		self.frame = []
		self.text = 'No Pickles'

		# initialize the camera and grab a reference to the raw camera capture
		self.camera = PiCamera()
		self.camera.resolution = tuple(conf["camera"]["resolution"])
		self.camera.framerate = conf["camera"]["fps"]
		self.rawCapture = PiRGBArray(self.camera, size=tuple(conf["camera"]["resolution"]))
		self.fourcc = cv2.VideoWriter_fourcc(*'MJPG')
#		self.video = cv2.VideoWriter(conf["recordings"]["videoName"], self.fourcc, conf["camera"]["fps"], tuple(conf["camera"]["resolution"]), True)

		# allow the camera time to warmup
		#print "warming up camera..."
		time.sleep(conf["camera"]["cameraWarmupTime"])

	##########################################
	#Clear the stream and prepare it for the next frame
	##########################################

	def clearStream(self):
		# clear the stream in preparation for the next frame
		self.rawCapture.truncate(0)

	##########################################
	#take a photo and store it
	##########################################

	def takeAndStorePhoto(self):

		# write the image to file
		cv2.imwrite(conf["recordings"]["imageName"], self.frame)
			
	##########################################
	#Check to see if any motion is detected by the camera
	##########################################
						
	def isMotionDetected(self):

		isMotionDetected = False
		isMotionVerified = False
		motionCounter = 0
		avg = None
		numFrames = 0
		
		# capture frames from the camera
		for f in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
			# grab the raw NumPy array representing the image and initialize
			# the timestamp and occupied/unoccupied text
			self.frame = f.array
			numFrames = numFrames + 1
			
			# resize the frame, convert it to grayscale, and blur it
			self.frame = imutils.resize(self.frame, width=500)
			gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
			gray = cv2.GaussianBlur(gray, (21, 21), 0)

			# if the average frame is None, initialize it
			if avg is None:
				print "starting motion detection process..."
				avg = gray.copy().astype("float")
				self.rawCapture.truncate(0)
				continue

			# accumulate the weighted average between the current frame and
			# previous frames, then compute the difference between the current
			# frame and running average
			cv2.accumulateWeighted(gray, avg, 0.5)
			frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

			# threshold the delta image, dilate the thresholded image to fill
			# in holes, then find contours on thresholded image
			thresh = cv2.threshold(frameDelta, conf["camera"]["deltaThresh"], 255,
				cv2.THRESH_BINARY)[1]
			thresh = cv2.dilate(thresh, None, iterations=2)
			(_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
				cv2.CHAIN_APPROX_SIMPLE)

			# loop over the contours. 
			for c in cnts:
				# if the contour is too small, ignore it
				if cv2.contourArea(c) < conf["camera"]["minArea"]:
					continue

				# compute the bounding box for the contour, draw it on the frame,
				# and update the text
				(x, y, w, h) = cv2.boundingRect(c)
				cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
				isMotionDetected = True

			if isMotionDetected:
				motionCounter += 1
				print "motion detected " + str(motionCounter) 
				# check to see if the number of frames with consistent motion is high enough
				if motionCounter >= conf["camera"]["minMotionFrames"]:
					isMotionVerified = True
					self.text = conf["camera"]["foundTextToDisplay"]

			self.clearStream()
			isMotionDetected = False

			if numFrames > conf["camera"]["fps"]*conf["camera"]["numSecondsToDetectMotion"]:
				# cleanup
				print "no motion detected"
				return False 

			if isMotionVerified:
				print "motion verified"
				return True
				
	##########################################
	#This method takes video for a certain number of seconds, set above
	##########################################
	def takeVideo(self):

		numFrames = 0
		isFilmingComplete = False
		self.video = cv2.VideoWriter(conf["recordings"]["videoName"], self.fourcc, conf["camera"]["fps"], tuple(conf["camera"]["resolution"]), True)
		
		# capture frames from the camera
		for f in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
			# grab the raw NumPy array representing the image and initialize
			# the timestamp and occupied/unoccupied text
			self.frame = f.array

			# if the first frame, indicate that we are starting the video capture process
			if numFrames == 0:
				print conf["camera"]["filmingTextToDisplay"]
				self.takeAndStorePhoto()

			# write to the video file
			self.video.write(self.frame)

			#Increment the counter for video length
			numFrames += 1
			
			#self.displayVideoOnScreen()
			self.clearStream()

			if numFrames > conf["camera"]["fps"]*conf["camera"]["videoLengthInSeconds"]:
			#if isFilmingComplete:
				# cleanup
				self.video.release()
				print "Recording Complete" 
				self.frame = f.array
				return True	
