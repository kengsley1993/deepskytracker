# import matplotlib.pyplot as plt
import cv2
from math import degrees, atan, cos, sin, pi

# Draw the lines represented in the hough accumulator on the original image
def get_slopes(houghLines):
	slopes = []

	for line in houghLines:
		for rho,theta in line:
			a = cos(theta)
			b = sin(theta)
			x0 = a*rho
			y0 = b*rho
			x1 = int(x0 + 1000*(-b))
			y1 = int(y0 + 1000*(a))
			x2 = int(x0 - 5000*(-b))
			y2 = int(y0 - 5000*(a))
			slope = (y2 - y1) / (x2 - x1)
			slopes.append(slope)
			
	return slopes

def median(array):
	n = len(array)
	array.sort()
	
	if n % 2 == 0:
		median1 = array[n//2]
		median2 = array[n//2 - 1]
		return (median1 + median2)/2
	else:
		return array[n//2]

def get_angle(image, hemisphere, short, direction, orientation):
	image = cv2.imread(image) # load image in grayscale
	gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
	blurredImage = cv2.GaussianBlur(gray_image, (5, 5), 0)
	edgeImage = cv2.Canny(blurredImage, 120, 240)

	# Detect points that form a line
	dis_reso = 1 # Distance resolution in pixels of the Hough grid
	theta = pi /180 # Angular resolution in radians of the Hough grid
	threshold = 100 # minimum no of votes

	houghLines = cv2.HoughLines(edgeImage, dis_reso, theta, threshold)

	slopes = get_slopes(houghLines) # draw the lines on the empty image

	slope_mean = sum(slopes)/ len(slopes)

	m1 = []
	m2 = []
	for slope in slopes:
		if (slope < slope_mean):
			m2.append(slope)
		else:
			m1.append(slope)

	# print(str(len(m1))+" of slopes m1:")
	# print(str(len(m2))+" of slopes m2:")

	m1_median = median(m1)
	m2_median = median(m2)

	photo_angle = degrees(atan(abs((m1_median-m2_median)/(1+m1_median*m2_median))))

	angle_ratio = 1

	angle = photo_angle * angle_ratio

	status = ""
	total_rolls = 0
	total_teeths = 0
	each_teeth_angle = 0.327

	if (angle > each_teeth_angle*16*3.5):
		if (hemisphere == "N"):
			if (direction == "N"):
				if (short == "DOWN"):
					status = "overL"
				elif (short == "UP"):
					status = "overR"
			elif (direction == "S"):
				if (short == "DOWN"):
					status = "overR"
				elif (short == "UP"):
					status = "overL"
		elif (hemisphere == "S"):
			if (direction == "N"):
				if (short == "DOWN"):
					status = "overR"
				elif (short == "UP"):
					status = "overL"
			elif (direction == "S"):
				if (short == "DOWN"):
					status = "overL"
				elif (short == "UP"):
					status = "overR"
	elif (orientation == "landscape"):
		if (hemisphere == "N"):
			if (direction == "N"):
				if (short == "DOWN"):
					status = "L"
				elif (short == "UP"):
					status = "R"
			elif (direction == "S"):
				if (short == "DOWN"):
					status = "R"
				elif (short == "UP"):
					status = "L"
		elif (hemisphere == "S"):
			if (direction == "N"):
				if (short == "DOWN"):
					status = "R"
				elif (short == "UP"):
					status = "L"
			elif (direction == "S"):
				if (short == "DOWN"):
					status = "L"
				elif (short == "UP"):
					status = "R"
	elif (orientation == "portrait"):
		if (hemisphere == "N"):
			if (direction == "N"):
				if (short == "LEFT"):
					status = "D"
				elif (short == "RIGHT"):
					status = "U"
		elif (hemisphere == "S"):
			if (direction == "S"):
				if (short == "LEFT"):
					status = "D"
				elif (short == "RIGHT"):
					status = "U"

	total_teeths = angle/(0.327)
	if (total_teeths >= 7):
		total_rolls = total_teeths//7
		total_teeths = total_teeths%7
	
	if (status == "D" or status == "L"):
		angle = -angle

	return (status, angle, total_rolls, total_teeths)

def distanceL(cur_angle, target_angle):
	if (target_angle < cur_angle):
		return cur_angle-target_angle
	else:
		return 360-target_angle+cur_angle

def distanceR(cur_angle, target_angle):
	if (target_angle > cur_angle):
		return target_angle-cur_angle
	else:
		return 360-cur_angle+target_angle