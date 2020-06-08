import matplotlib.pyplot as plt
import matplotlib.image as mpimg# reading in an image
import os
import cv2
import numpy as np

folder = os.path.abspath(os.getcwd())
file = "/paper/img078.jpg"

image = mpimg.imread(folder+file)# printing out some stats and plotting the imageprint('This image is:', type(image), 'with dimensions:', image.shape)

y = 340
h = 3360
x = 130
w = 5230

crop_img = image[x:x+w, y:y+h]
output = crop_img.copy()

gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)

# detect circles in the image
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, minDist=500, minRadius=500)
# ensure at least some circles were found

def draw_circles(circles, image):
	if circles is not None:
		# convert the (x, y) coordinates and radius of the circles to integers
		circles = np.round(circles[0, :]).astype("int")
		# loop over the (x, y) coordinates and radius of the circles
		print(len(circles))
		for (x, y, r) in circles:
			# draw the circle in the output image, then draw a rectangle
			# corresponding to the center of the circle
			cv2.circle(image, (x, y), r, (0, 255, 0), 4)
			cv2.rectangle(image, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

			return (x, y, r)

def draw_lines(img, center, points, color=[255, 0, 0], thickness=3):
	for point in points:
		cv2.line(img, center, point, color, thickness)

(x, y, _) = draw_circles(circles, output)

max_left = (2134, 2945)
offset = (2226, 3044)
roll1 = (2258, 3086)
roll05 = (2269, 3101)
max_right = (2303, 3151)

points = [max_left, offset, roll1, roll05, max_right]

draw_lines(output, (x, y), points)

import math
 
def angle3pt(a, b, c):
	"""Counterclockwise angle in degrees by turning from a to c around b
		Returns a float between 0.0 and 360.0"""
	ang = math.degrees(
		math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
	return ang

print("7 roll:")
angle_7roll = angle3pt(max_left, (x, y), max_right)
print(angle_7roll)
print("1 roll *7:")
angle_1roll = angle3pt(offset, (x, y), roll1)
print(angle_1roll *7)
print("0.5 roll *14:")
angle_05roll = angle3pt(roll1, (x, y), roll05)
print(angle_05roll *14)

print("1 teeth:")
angle_1teeth = (angle_7roll /7) /7
print(angle_1teeth)

print("orignal:")
angle_orignal = angle3pt((1152, 1102), (1036, 1078), (1251, 1078))
print(angle_orignal)

print("number of roll:")
N_roll = (angle_orignal/angle_05roll) *0.5
print(N_roll)

fig, (ax2, ax3) = plt.subplots(nrows=1, ncols=2, figsize=(50, 50))

ax2.imshow(crop_img, cmap='gray')
ax2.set_title('Edge Image')
ax2.axis('off')

ax3.imshow(output, cmap='gray')
ax3.set_title("Hough circles")
ax3.axis('off')

plt.show()