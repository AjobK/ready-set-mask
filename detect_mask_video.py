# import the necessary packages
from handDetection import handDetector
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2
import os

class MaskDetector:
	def __init__(self):
		# load our serialized face detector model from disk
		self.prototxtPath = r"face_detector/deploy.prototxt"
		self.weightsPath = r"face_detector/res10_300x300_ssd_iter_140000.caffemodel"
		self.faceNet = cv2.dnn.readNet(self.prototxtPath, self.weightsPath)

		# load the face mask detector model from disk
		self.maskNet = load_model("mask_detector.model")

		self.handDetector = handDetector()
		self.medium = self.getMedium()

		# initialize the video stream
		print("[INFO] starting video stream...")
		self.vs = VideoStream(src=0).start()
    
	def getMedium(self):
		# Open Video
		cap = cv2.VideoCapture(0)

		# Randomly select 25 frames
		frameIds = cap.get(cv2.CAP_PROP_FRAME_COUNT) * np.random.uniform(size=25)

		# Store selected frames in an array
		frames = []
		for fid in frameIds:
			cap.set(cv2.CAP_PROP_POS_FRAMES, fid)
			ret, frame = cap.read()
			frames.append(frame)

		# Calculate the median along the time axis
		medianFrame = np.median(frames, axis=0).astype(dtype=np.uint8)    

		# Reset frame number to 0
		cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

		# Convert background to grayscale
		grayMedianFrame = cv2.cvtColor(medianFrame, cv2.COLOR_BGR2GRAY)
		
		return grayMedianFrame

	def detect_and_predict_mask(self, frame, faceNet, maskNet):
		# grab the dimensions of the frame and then construct a blob
		# from it
		(h, w) = frame.shape[:2]
		blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224),
			(104.0, 177.0, 123.0))

		# pass the blob through the network and obtain the face detections
		faceNet.setInput(blob)
		detections = faceNet.forward()

		# initialize our list of faces, their corresponding locations,
		# and the list of predictions from our face mask network
		faces = []
		locs = []
		preds = []

		# loop over the detections
		for i in range(0, detections.shape[2]):
			# extract the confidence (i.e., probability) associated with
			# the detection
			confidence = detections[0, 0, i, 2]

			# filter out weak detections by ensuring the confidence is
			# greater than the minimum confidence
			if confidence > 0.5:
				# compute the (x, y)-coordinates of the bounding box for
				# the object
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")

				# ensure the bounding boxes fall within the dimensions of
				# the frame
				(startX, startY) = (max(0, startX), max(0, startY))
				(endX, endY) = (min(w - 1, endX), min(h - 1, endY))

				# extract the face ROI, convert it from BGR to RGB channel
				# ordering, resize it to 224x224, and preprocess it
				face = frame[startY:endY, startX:endX]
				face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
				face = cv2.resize(face, (224, 224))
				face = img_to_array(face)
				face = preprocess_input(face)

				# add the face and bounding boxes to their respective
				# lists
				faces.append(face)
				locs.append((startX, startY, endX, endY))

		# only make a predictions if at least one face was detected
		if len(faces) > 0:
			# for faster inference we'll make batch predictions on *all*
			# faces at the same time rather than one-by-one predictions
			# in the above `for` loop
			faces = np.array(faces, dtype="float32")
			preds = maskNet.predict(faces, batch_size=32)

		# return a 2-tuple of the face locations and their corresponding
		# locations
		return (locs, preds)

	def is_gassing(self):
		frame = self.vs.read()

		(locs, preds) = self.detect_and_predict_mask(frame, self.faceNet, self.maskNet)

		for (box, pred) in zip(locs, preds):
			(startX, startY, endX, endY) = box
			(mask, withoutMask) = pred

			color = (0, 255, 0) if mask > withoutMask else (0, 0, 255)
			cv2.putText(frame, 'GASSING' if mask > withoutMask else 'REVERSE', (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
			cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
			
			return mask > withoutMask

	def detectHand(self):
		capture = self.vs
	
		frame_colorful = capture.read()

		# Convert current frame to grayscale
		frame = cv2.cvtColor(frame_colorful, cv2.COLOR_BGR2GRAY)
		# Calculate absolute difference of current frame and 
		# the median frame
		dframe = cv2.absdiff(frame, self.medium)
		# Treshold to binarize
		th, frame = cv2.threshold(dframe, 30, 255, cv2.THRESH_BINARY)
		# Display image
		status = "STRAIGHT"

		cv2.rectangle(frame_colorful, (self.handDetector.leftBox.startX, self.handDetector.leftBox.startY), (self.handDetector.leftBox.endX, self.handDetector.leftBox.endY), (0,255,0), 2)
		cv2.rectangle(frame_colorful, (self.handDetector.rightBox.startX, self.handDetector.rightBox.startY), (self.handDetector.rightBox.endX, self.handDetector.rightBox.endY), (0,255,0), 2)

		try:
			cv2.imshow("hands", cv2.flip(frame_colorful, 1))
		except:
			pass

		try:
			status = self.handDetector.startHandDetection(frame)
		except:
			pass

		return status