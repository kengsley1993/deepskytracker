import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import math

image = mpimg.imread('tmp.jpg')
image = np.array((image > 150) *255, dtype='uint8')
gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
cannyed_image = cv2.Canny(gray_image, 200, 300)

lines = cv2.HoughLinesP(
	cannyed_image,
	rho=6,
	theta=np.pi / 60,
	threshold=160,
	lines=np.array([]),
	minLineLength=200,
	maxLineGap=75
)

print(len(lines))


slopes = []
distances = []

for line in lines:
	for x1, y1, x2, y2 in line:
		slope = (y2-y1)/(x2-x1)
		distance = math.sqrt(abs(((x2-x1)^2)+((y2-y1)^2)))
		slopes.append(slope)
		distances.append(distance)

slopes_orignal = []
slopes_tracker = []

distance_middle = (max(distances)+min(distances))/2

for i, _ in enumerate(slopes):
	if (distances[i] > distance_middle):
		slopes_tracker.append(slopes[i])
	elif (distances[i] < distance_middle):
		slopes_orignal.append(slopes[i])

print(str(len(slopes_orignal))+" of slopes slopes_orignal:")
print(slopes_orignal)
print(str(len(slopes_tracker))+" of slopes slopes_tracker:")
print(slopes_tracker)

# slopes = []
# for line in lines:
# 	for x1, y1, x2, y2 in line:
# 		slope = (y2 - y1) / (x2 - x1)
# 		slopes.append(slope)

# slope_mean = sum(slopes)/ len(slopes)
# slope_max = max(slopes)
# slope_min = min(slopes)

# error = max(abs(slope_max-slope_mean)/abs(slope_max), abs(slope_min-slope_mean)/abs(slope_min))
# error_final = min(error, 0.1)

# print("error:")
# print(error)

# m1 = []
# m2 = []
# for slope in slopes:
# 	if (slope_max - slope <= error_final):
# 		m2.append(slope)
# 	elif (slope - slope_min <= error_final):
# 		m1.append(slope)

# print(str(len(m1))+" of slopes m1:")
# print(m1)
# print(str(len(m2))+" of slopes m2:")
# print(m2)

def draw_lines(img, lines, color=[255, 0, 0], thickness=3):
	# If there are no lines to draw, exit.
	if lines is None:
		return    # Make a copy of the original image.
	img = np.copy(img)    # Create a blank image that matches the original in size.
	line_img = np.zeros(
		(
			img.shape[0],
			img.shape[1],
			3
		),
		dtype=np.uint8,
	)    # Loop over all lines and draw them on the blank image.
	for line in lines:
		for x1, y1, x2, y2 in line:
			cv2.line(line_img, (x1, y1), (x2, y2), color, thickness)    # Merge the image with the lines onto the original.
	img = cv2.addWeighted(img, 0.8, line_img, 1.0, 0.0)    # Return the modified image.
	return img

# orignal_line_x = []
# orignal_line_y = []
# stracker_line_x = []
# stracker_line_y = []
# for line in lines:
# 	for x1, y1, x2, y2 in line:
# 		slope = (y2 - y1) / (x2 - x1) # <-- Calculating the slope.
# 		if slope <= 0: # <-- If the slope is negative, left group.
# 			left_line_x.extend([x1, x2])
# 			left_line_y.extend([y1, y2])
# 		else: # <-- Otherwise, right group.
# 			right_line_x.extend([x1, x2])
# 			right_line_y.extend([y1, y2])

fig, (ax2, ax3) = plt.subplots(nrows=1, ncols=2, figsize=(50, 50))

ax2.imshow(cannyed_image, cmap='gray')
ax2.set_title('Edge Image')
ax2.axis('off')

line_image = draw_lines(image, lines)
ax3.imshow(line_image, cmap='gray')
ax3.set_title("Original Image with Hough lines")
ax3.axis('off')

plt.show()