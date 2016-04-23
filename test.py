import cv2
import numpy as np

filename = "samples/BlobTest.jpg"
img = cv2.imread(filename)
img_resize = cv2.resize(img, (600, 400))

gray = cv2.cvtColor(img_resize, cv2.COLOR_RGB2GRAY)
# mask
params = cv2.SimpleBlobDetector_Params()

# Change thresholds
params.minThreshold = 10
params.maxThreshold = 200

# Filter by Area.
params.filterByArea = True
params.minArea = 500

# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.1

# Filter by Convexity
params.filterByConvexity = True
params.minConvexity = 0.5

# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.01

# Create a detector with the parameters
ver = cv2.__version__.split('.')
if int(ver[0]) < 3:
    detector = cv2.SimpleBlobDetector_Params()
else:
    detector = cv2.SimpleBlobDetector_create(params)

keypoint = detector.detect(gray)
# show
im_with_keypoint = cv2.drawKeypoints(gray, keypoint,np.array([]),(0,0,255),cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

cv2.imshow("original", im_with_keypoint)

cv2.waitKey(0)
cv2.destroyAllWindows()
