import matplotlib.pyplot as plt
import matplotlib.image as mpimg# reading in an image
import os
import cv2
import numpy as np

folder = os.path.abspath(os.getcwd())
file = "/DSC_0390_painted.jpg"

image = mpimg.imread(folder+file)# printing out some stats and plotting the imageprint('This image is:', type(image), 'with dimensions:', image.shape)

y = 340
h = 3360
x = 130
w = 5230

output = image.copy()

def draw_lines(img, points, color=[255, 0, 0], thickness=3):
	for (point1, point2) in points:
		cv2.line(img, point1, point2, color, thickness)

# points = []

# point1 = (2134, 2945)
# point2 = (2226, 3044)

# points.append((point1, point2))

# point1 = ()
# point2 = ()

# points.append((point1, point2))

# draw_lines(output, points)

# import math
 
# def angle3pt(a, b, c):
# 	"""Counterclockwise angle in degrees by turning from a to c around b
# 		Returns a float between 0.0 and 360.0"""
# 	ang = math.degrees(
# 		math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
# 	return ang

# print("7 roll:")
# angle_7roll = angle3pt(max_left, (x, y), max_right)
# print(angle_7roll)
# print("1 roll *7:")
# angle_1roll = angle3pt(offset, (x, y), roll1)
# print(angle_1roll *7)
# print("0.5 roll *14:")
# angle_05roll = angle3pt(roll1, (x, y), roll05)
# print(angle_05roll *14)

# print("1 teeth:")
# angle_1teeth = (angle_7roll /7) /7
# print(angle_1teeth)

# print("orignal:")
# angle_orignal = angle3pt((1152, 1102), (1036, 1078), (1251, 1078))
# print(angle_orignal)

# print("number of roll:")
# N_roll = (angle_orignal/angle_05roll) *0.5
# print(N_roll)

# fig, (ax2, ax3) = plt.subplots(nrows=1, ncols=2, figsize=(50, 50))

# ax2.imshow(image, cmap='gray')
# ax2.set_title('Edge Image')
# ax2.axis('off')

# ax3.imshow(output, cmap='gray')
# ax3.set_title("Hough circles")
# ax3.axis('off')

# plt.show()

plt.imshow(image, cmap='gray')
plt.axis('off')

plt.show()
