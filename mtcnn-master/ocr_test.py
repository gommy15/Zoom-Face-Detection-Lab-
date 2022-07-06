import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('image/real_test.png',0)

#ret, th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
#img_h, img_w


th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,3, 12)
contours, hierarchy = cv2.findContours(th2, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
if len(contours) > 0:
	for i in range(len(contours)) :
		x, y, w, h = cv2.boundingRect(contours[i])
		#if (h > 100) & (w > 500) :


th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,3,12)
contours, hierarchy = cv2.findContours(th3, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
th3 = cv2.drawContours(th2, contours, -1, (0,255,0), 5, cv2.LINE_8)


titles = ['Original','Mean','Gaussian']

images = [img,th2,th3]

for i in range(3):
	plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
	plt.title(titles[i])
	plt.xticks([]),plt.yticks([])

plt.show()