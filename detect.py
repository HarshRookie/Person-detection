from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np 
import argparse
import cv2
import imutils

ap = argparse.ArgumentParser()
ap.add_argument("-i","--images",required=True,help="path to images directory")
args=vars(ap.parse_args())

#initialize person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

for imagePath in paths.list_images(args["images"]):
	img = cv2.imread(imagePath)
	img = imutils.resize(img, width=min(400, img.shape[1]))
	orig = img.copy()

	(rects,weigths) = hog.detectMultiScale(img, winStride=(4,4), padding=(8,8), scale=1.05)

	for (x,y,w,h) in rects:
		cv2.rectangle(orig, (x,y), (x+w,y+h), (0,0,255), 2)

	rects = np.array([[x,y,x+w,y+h] for (x,y,w,h) in rects])
	pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

	#draw the final bounding boxes
	for (xA, yA, xB, yB) in pick:
		cv2.rectangle(img, (xA, yA), (xB, yB), (0, 255, 0), 2)

	filename = imagePath[imagePath.rfind("/") + 1:]
	print("[INFO] {}: {} original boxes, {} after suppression".format(filename, len(rects), len(pick)))

	cv2.imshow("Before NMS", orig)
	cv2.imshow("After NMS", img)

	if cv2.waitKey(0) & 0xFF == ord('q'):
		break


