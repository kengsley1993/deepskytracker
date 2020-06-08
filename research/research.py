# Necessary imports
import matplotlib.pyplot as plt
import numpy as np
# import cv2
# import math

# from numpy import cos, sin, median, pi
import cv2
from math import degrees, atan, cos, sin, pi

# Resource:
# https://stackoverflow.com/questions/46357099/calculating-the-angle-between-two-lines-in-an-image-in-python
# https://medium.com/@mrhwick/simple-lane-detection-with-opencv-bfeb6ae54ec0
# http://datahacker.rs/opencv-line-detection-using-hough-transform/#id2
# https://stackoverflow.com/questions/46565975/find-intersection-point-of-two-lines-drawn-using-houghlines-opencv/49590801

current_position = "N"
short = "down"
shot_pos = "top"

# Draw the lines represented in the hough accumulator on the original image
def drawhoughLinesOnImage(houghLines):
	slopes = []

	for line in houghLines:
		for rho,theta in line:
			# a = np.cos(theta)
			# b = np.sin(theta)
			a = cos(theta)
			b = sin(theta)
			x0 = a*rho
			y0 = b*rho
			# print("start point:")
			# print(x0, y0)
			x1 = int(x0 + 1000*(-b))
			y1 = int(y0 + 1000*(a))
			x2 = int(x0 - 5000*(-b))
			y2 = int(y0 - 5000*(a))
			slope = (y2 - y1) / (x2 - x1)
			slopes.append(slope)
			
			cv2.line(image,(x1,y1),(x2,y2),(0,255,0), 2)

	return slopes

# Different weights are added to the image to give a feeling of blending
def blend_images(image, final_image, alpha=0.7, beta=1., gamma=0.):
	return cv2.addWeighted(final_image, alpha, image, beta,gamma)

def median(array):
	n = len(array)
	array.sort()
	
	if n % 2 == 0:
		median1 = array[n//2]
		median2 = array[n//2 - 1]
		return (median1 + median2)/2
	else:
		return array[n//2]

image = cv2.imread("DSC_0390.jpg") # load image in grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
blurredImage = cv2.GaussianBlur(gray_image, (5, 5), 0)
edgeImage = cv2.Canny(blurredImage, 120, 200)

fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)

ax1.imshow(edgeImage, cmap='gray')
ax1.set_title('Edge Image')
ax1.axis('off')

ax2.imshow(image, cmap='gray')
ax2.set_title('Edge Image')
ax2.axis('off')

plt.show()

# Detect points that form a line
dis_reso = 1 # Distance resolution in pixels of the Hough grid
theta = pi /180 # Angular resolution in radians of the Hough grid
threshold = 10# minimum no of votes

houghLines = cv2.HoughLines(edgeImage, dis_reso, theta, threshold)

houghLinesImage = np.zeros_like(image) # create and empty image

slopes = drawhoughLinesOnImage(houghLines) # draw the lines on the empty image
orginalImageWithHoughLines = blend_images(houghLinesImage,image) # add two images together, using image blending

slope_mean = sum(slopes)/ len(slopes)

m1 = []
m2 = []
for slope in slopes:
	if (slope < slope_mean):
		m2.append(slope)
	else:
		m1.append(slope)

print(str(len(m1))+" of slopes m1:")
# print(m1)
print(str(len(m2))+" of slopes m2:")
# print(m2)

# m1_median = np.median(m1)
# m2_median = np.median(m2)
m1_median = median(m1)
m2_median = median(m2)

# angle = math.degrees(math.atan(abs((m1_median-m2_median)/(1+m1_median*m2_median))))
angle = degrees(atan(abs((m1_median-m2_median)/(1+m1_median*m2_median))))

if (short == "down"):
	print("face E(angle):")
else:
	print("face W(angle):")
print(angle)

print("Suggestion:")
if (short == "down"):
	print("Rotate to W(angle):")
else:
	print("Rotate to E(angle):")
print(angle)

total_roll = 0
total_teeth = angle/(0.327)
if (total_teeth >= 7):
	total_roll = total_teeth//7
	total_teeth = total_teeth%7
	print(str(total_roll)+ "rolls")
print(str(total_teeth)+ "teeths")





fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(50, 50))

val = 0. # this is the value where you want the data to appear on the y-axis.
import pandas as pd
df = pd.DataFrame({'slope': slopes,
					'count': np.ones_like(slopes)})
print(df.groupby('slope').sum())

ax1.plot(df.groupby('slope').sum(), color='r')
ax1.axvline(x=m1_median, color='w')
ax1.axvline(x=m2_median, color='w')

ax2.imshow(edgeImage, cmap='gray')
ax2.set_title('Edge Image')
ax2.axis('off')

ax3.imshow(orginalImageWithHoughLines, cmap='gray')
ax3.set_title("Original Image with Hough lines")
ax3.axis('off')

plt.show()