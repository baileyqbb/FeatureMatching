"""Provides utilities to detect markers from images.

The preprocessing steps for marker detection is as follows:

  1. Detecting circles using HoughCircles
  2. Detecting triangles within the detected circles
  3. Detecting the I marker within the triangles
"""

import cv2
import cPickle
import numpy as np


def preprocessing(image, kresize=2, kGblur=9):
    """
    :param image: 3D or 2D array. input image
    :param kresize: positive integer. resize kernel size.
    :param kGblur: positive integer. Gaussion kernel size.
    :return: 2D array. resized and deblurred grayscale image
    """
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (img.shape[1]/kresize, img.shape[0]/kresize))
    img = cv2.GaussianBlur(img, (kGblur, kGblur), 2)
    return img


def circleDetection(image):
    """
    :param image: 2D array. Gray image
    :return: list of 3D vectors. [centerx, centery, radius]
    """
    return cv2.HoughCircles(image, cv2.cv.CV_HOUGH_GRADIENT, 1, image.shape[0]/2, 200, 100)


def shapeDetection(image, threshvalue, param1=0.03):
    shapeCountors = {}
    ret, thresh = cv2.threshold(image, threshvalue, 255, 1)
    contours, h = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    tmp = cPickle.dumps(contours)
    contours = cPickle.loads(tmp)
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, param1 * cv2.arcLength(cnt, True), True)
        if len(approx) == 3:
            print "triangles detected"
            #cv2.drawContours(image, [cnt], 0, (0, 255, 0), -1)
            shapeCountors['triangle'].append(cnt)
        if len(approx) == 4:
            print "rectangles detected"
            #cv2.drawContours(image, [cnt], 0, (0, 255, 0), -1)
            shapeCountors['rectangles'].append(cnt)
