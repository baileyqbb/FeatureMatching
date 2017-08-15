import numpy as np
import cv2
import markerDetector
import cPickle
print cv2.__version__
cap = cv2.VideoCapture('Video/YDXJ0018.mp4')
indx = 0
while(cap.isOpened()):
    ret, frame = cap.read()
    img = markerDetector.preprocessing(frame, kGblur=3)
    img_copy = img.copy()
    circles = markerDetector.circleDetection(img)

    #print circles
    if circles is not None:
        #circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            #print circle
            centerx = circle[0]
            centery = circle[1]
            radius = circle[2]
            cv2.circle(img, (centerx, centery), 3, (0,255,0), -1)
            cv2.circle(img, (centerx, centery), radius, (0,0,255), 3)

            bdl_x = int(centerx - radius) - 10 if centerx - radius - 10 > 0 else 0
            bdl_y = int(centery - radius) - 10 if centery - radius - 10 > 0 else 0
            bdr_x = int(centerx + radius) + 10 if centerx + radius + 10 < img.shape[1] else img.shape[1] - 1
            bdr_y = int(centery + radius) + 10 if centery + radius + 10 < img.shape[0] else img.shape[0] - 1

            # print bdl_x, bdl_y, bdr_x, bdr_y
            clip_image = img_copy[bdl_y:bdr_y, bdl_x:bdr_x]

            ret, thresh = cv2.threshold(clip_image, 200, 255, 1)
            contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            tmp = cPickle.dumps(contours)
            contours = cPickle.loads(tmp)
            if contours is not None:
              for cnt in contours:
                  print cnt.shape
                  approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
                  if len(approx) == 3:
                      print "triangle"
                      cv2.drawContours(clip_image, [approx], -1, (0, 255, 0), 3)
                  if len(approx) == 4:
                      print "rectangle"
                      rect = cv2.minAreaRect(cnt)
                      box = np.int0(cv2.cv.BoxPoints(rect))
                      cv2.drawContours(clip_image, [box], -1, (0, 255, 0), 3)
                  if len(approx) == 12:
                      print "I-shape"
                      rect = cv2.minAreaRect(cnt)
                      box = np.int0(cv2.cv.BoxPoints(rect))
                      cv2.drawContours(clip_image, [box], -1, (200,0,0), 3)

            cv2.imshow('clip image', clip_image)

    cv2.imshow('frame', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
      break



cap.release()
cv2.destroyAllWindows()