import cv2
import shadow_removal

fileori = "ori.jpg"
filehsv = "hsvframe.jpg"
# 1. HSV
ori = cv2.imread(fileori)
hsv = cv2.cvtColor(ori, cv2.COLOR_RGB2HSV)

hue, sat, val = cv2.split(hsv)
shadow = shadow_removal.hsvPassShadowRemoval(ori, 0.6)

cv2.imshow("hsv", shadow)
cv2.imwrite("shadow.jpg", shadow)

cv2.waitKey(0)
cv2.destroyAllWindows()