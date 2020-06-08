import numpy as np

from skimage.transform import (hough_line, hough_line_peaks,
                               probabilistic_hough_line)
from skimage.feature import canny
from skimage import data

# from pylab import imread, imshow, gray, mean

import matplotlib.pyplot as plt
from matplotlib import cm

import cv2

image = cv2.imread("tmp.jpg")
gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
blurredImage = cv2.GaussianBlur(gray_image, (5, 5), 0)
edgeImage = cv2.Canny(blurredImage, 120, 200)
# edgeImage = np.mean(edgeImage,axis=2)
# edgeImage = (edgeImage > 128)*255

h, theta, d = hough_line(edgeImage)

fig, axes = plt.subplots(1, 2, figsize=(15, 6))
ax = axes.ravel()

ax[0].imshow(image, cmap=cm.gray)
ax[0].set_title('Input image')
ax[0].set_axis_off()

ax[1].imshow(edgeImage, cmap=cm.gray)
for _, angle, dist in zip(*hough_line_peaks(h, theta, d)):
    y0 = (dist - 0 * np.cos(angle)) / np.sin(angle)
    y1 = (dist - edgeImage.shape[1] * np.cos(angle)) / np.sin(angle)
    ax[1].plot((0, edgeImage.shape[1]), (y0, y1), '-r')
ax[1].set_xlim((0, edgeImage.shape[1]))
ax[1].set_ylim((edgeImage.shape[0], 0))
ax[1].set_axis_off()
ax[1].set_title('Detected lines')

plt.tight_layout()
plt.show()