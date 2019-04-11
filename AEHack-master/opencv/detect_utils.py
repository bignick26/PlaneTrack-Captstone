
from sklearn.cluster import KMeans
import numpy as np
from matplotlib import pyplot as plt
import utils, sys, math, argparse, cv2


def localize_video(fn, window_size):
	vidcap = cv2.VideoCapture(fn)
	success, img = vidcap.read()
	count = 0
	offsets = []
	while success:
		final, centroid, target, offset = localize_object(img)
		success, img = vidcap.read()
		count += 1


		offsets.append(offset)
		if (len(offsets) > window_size):
			del offsets[0]

		trueOffset = slideAvg(offsets)
		print "SLEW TO OFFSET: ", trueOffset

		cv2.line(final, (centroid[0], centroid[1]), (centroid[0] + trueOffset[0], centroid[1] + trueOffset[1]), (255,0,255), 4)

		cv2.imwrite("images/vid/plane_fixed" + str(count) + ".png", final);


# Returns image (debug), target coords of object, offset of object
def localize_object(img):

	img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
	h, w = img.shape[:2]
	img = img[0:int((0.25 * w)), int(0.25 * w):int(0.75 * w)]

	h, w = img.shape[:2]



	# global thresholding
	cv2.rectangle(img, (0,0),(w,h),(255,0,0), 2)
	ret1,th1 = cv2.threshold(img,170,255,cv2.THRESH_BINARY)

	# cv2.imwrite("images/plane_test" + str(count) + ".png", img)

	contours, hierarchy = cv2.findContours(th1,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
	# plot all the images and their histograms
	image = [img, 0, th1, contours, hierarchy]

	final = cv2.cvtColor(image[2], cv2.COLOR_GRAY2RGB)

	maxArea = 0
	for cnt in contours:
		area = cv2.contourArea(cnt)
		if (area > maxArea):
			maxArea = area

	centroid = ((w / 2), (h / 2))
	cv2.line(final, (centroid[0], (centroid[1] - 5)), (centroid[0], (centroid[1] + 5)),(0,0,0), 2)
	cv2.line(final, (centroid[0] - 5, centroid[1]), (centroid[0] + 5, centroid[1]),(0,0,0), 2)

	minDist = sys.maxint
	target = (0, 0)
	offset = (0, 0)

	for cnt in contours:
		area = cv2.contourArea(cnt)

		x,y,w,h = cv2.boundingRect(cnt)
		cv2.rectangle(final,(x,y),(x+w + 5,y+h + 5),(0,255,0),2)

		if ((area > 30 or area < 2) and area < maxArea):
			cv2.rectangle(final,(x,y),(x+w + 6,y+h+6),(255,255,255), -1)
		elif (area < maxArea):
			m = cv2.moments(cnt)
			try:
				cx = int(m['m10']/m['m00'])
				cy = int(m['m01']/m['m00'])

				dist = math.sqrt((cx - centroid[0])**2 + (cy - centroid[1])**2)
				if (dist < minDist):
					minDist = dist
					target = (cx, cy)
					offset = (cx - centroid[0], cy - centroid[1])
			except:
				print "div by 0, skipping"



	cv2.line(final, (centroid[0], centroid[1]), (target[0], target[1]), (255,0,0), 4)

	return final, centroid, target, offset

# Will calculate an average in window size defined
def slideAvg(offsets):
	sumX = 0
	sumY = 0
	count = 0
	print offsets
	for o in offsets:
		sumX += o[0]
		sumY += o[1]
		count += 1

	return (sumX / count, sumY / count)
