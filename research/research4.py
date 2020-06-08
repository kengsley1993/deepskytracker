# Necessary imports
import matplotlib.pyplot as plt
import numpy as np
import cv2
import math

# Draw the lines represented in the hough accumulator on the original image
def drawhoughLinesOnImage(image, houghLines):
	slopes = []

	for line in houghLines:
		for rho,theta in line:
			a = np.cos(theta)
			b = np.sin(theta)
			x0 = a*rho
			y0 = b*rho
			print("start point:")
			print(x0, y0)
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

image = cv2.imread("DSC_0385.NEF") # load image in grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
blurredImage = cv2.GaussianBlur(gray_image, (5, 5), 0)
edgeImage = cv2.Canny(blurredImage, 120, 240)

minLineLength = 500
maxLineGap = 0
lines = cv2.HoughLinesP(edgeImage,1,np.pi/180,100,minLineLength,maxLineGap)
# lines = cv2.HoughLines(edgeImage, 1, np.pi/180, 100)
slopes = []
print(len(lines))
print(len(lines[0]))
for line in lines:
	for x1,y1,x2,y2 in line:
		cv2.line(image,(x1,y1),(x2,y2),(255,0,0),2)
		slope = float((y2 - y1) / (x2 - x1))
		slopes.append(slope)

print(len(slopes))
houghLinesImage = np.zeros_like(image) # create and empty image

slopes = drawhoughLinesOnImage(houghLinesImage, houghLines) # draw the lines on the empty image
orginalImageWithHoughLines = blend_images(houghLinesImage,image) # add two images together, using image blending

slope_mean = sum(slopes)/ len(slopes)
slope_max = max(slopes)
slope_min = min(slopes)

error = max(abs(slope_max-slope_mean)/abs(slope_max), abs(slope_min-slope_mean)/abs(slope_min))
error_final = min(error, 0.1)

print("error:")
print(error)

m1 = []
m2 = []
for slope in slopes:
	if (slope_max - slope <= error_final):
		m2.append(slope)
	elif (slope - slope_min <= error_final):
		m1.append(slope)

print(str(len(m1))+" of slopes m1:")
# print(m1)
print(str(len(m2))+" of slopes m2:")
# print(m2)

m1_mean = sum(m1)/len(m1)
m2_mean = sum(m2)/len(m2)

angle = math.degrees(math.atan(abs((m1_mean-m2_mean)/(1+m1_mean*m2_mean))))

print("angle:")
print(angle)

fig, (ax2, ax3) = plt.subplots(nrows=1, ncols=2, figsize=(50, 50))
# ax1.imshow(image)
# ax1.set_title('Original Image')
# ax1.axis('off')

ax2.imshow(edgeImage, cmap='gray')
ax2.set_title('Edge Image')
ax2.axis('off')

ax3.imshow(image, cmap='gray')
ax3.set_title("Original Image with Hough lines")
ax3.axis('off')

plt.show()