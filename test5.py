import cv2
import numpy as np
import _vehicle_init as vehicleInit
import math_operation as mo
from munkres import Munkres

listVehicleDetected = []
templist = []
file_mask = "samples/background2.jpg"
file_foreground = "samples/frameori2.jpg"
file_mog = "samples/test_mog.jpg"

img_back = cv2.imread(file_mask)
img_fore = cv2.imread(file_foreground)
img_mog = cv2.imread(file_mog)
img_back = cv2.resize(img_back, (1120,630))
img_fore = cv2.resize(img_fore, (1120,630))

kernel = np.ones((5,5),np.float32)/25
hsv_background = cv2.cvtColor(img_back, cv2.COLOR_RGB2HSV)
hsv_foreground = cv2.cvtColor(img_fore, cv2.COLOR_RGB2HSV)
gray_background = cv2.cvtColor(img_back, cv2.COLOR_RGB2GRAY)
gray_foreground = cv2.cvtColor(img_fore, cv2.COLOR_RGB2GRAY)
lab_background = cv2.cvtColor(img_back,cv2.COLOR_RGB2HLS)
lab_foreground = cv2.cvtColor(img_fore,cv2.COLOR_RGB2HLS)

lback, aback, bback = cv2.split(lab_background)
lfore, afore, bfore = cv2.split(lab_foreground)

hue, saturation, value = cv2.split(hsv_foreground)
hueBack, satBack, valBack = cv2.split(hsv_background)
#cv2.imwrite("samples/grayforeground.jpg", gray_foreground)

#gray_foreground = cv2.blur(gray_foreground, (5,5))
#gray_background = cv2.blur(gray_background,(5,5))
# Background subtraction
abssub = (gray_background*2)-(gray_foreground*2)
subtracRGB = cv2.absdiff(gray_foreground,gray_background)
subtraction = cv2.absdiff(value,valBack)
subtractionLAB = cv2.absdiff(afore, aback)
comHSVRGB = cv2.bitwise_or(subtractionLAB, subtracRGB)
comALL = cv2.bitwise_or(subtraction, subtractionLAB)
# Threshold
_,thresholdRGB = cv2.threshold(comHSVRGB, 50,255,cv2.THRESH_BINARY)
_,threshold = cv2.threshold(comALL, 100,255,cv2.THRESH_OTSU)

im_floodfill = thresholdRGB.copy()
im_floodfillHSV = threshold.copy()
h, w = subtraction.shape[:2]
mask = np.zeros((h+2, w+2), np.uint8)

# Shadow Removal


# Filing hole
# Inverse Binary
cv2.floodFill(threshold,mask, (0,0),255)
im_floodfill_inv = cv2.bitwise_not(im_floodfill)
temp_floodfill = im_floodfill
# Build RoI
img_zero = np.zeros((630, 1120), np.uint8)
pts = np.array([[385,220],[50,465],[1040,465],[705,220]])

#cv2.polylines(temp_floodfill,[pts],True,(255,255,0),thickness=1)
cv2.fillPoly(img_zero,[pts],(255,255,0))
# Morphology
kernel = np.ones((3,3),np.uint8)
kernel1 = np.array([
    [0, 0, 0, 0],
    [0, 1, 1, 0],
    [0, 1, 1, 0],
    [0, 0, 0, 0]], dtype=np.uint8)
kernel2 = np.array([
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]], dtype=np.uint8)

morp_erosi1 = cv2.erode(im_floodfill,None,iterations=1)
morp_dilasi1 = cv2.dilate(morp_erosi1, kernel, iterations=1)
#morp_erosi2 = cv2.erode(morp_dilasi1,kernel,iterations=1)
morp_dilasi2 = cv2.dilate(morp_dilasi1, kernel, iterations=1)
morp_dilasi3 = cv2.dilate(morp_dilasi2, kernel, iterations=1)
morp_dilasi4 = cv2.dilate(morp_dilasi3, kernel, iterations=1)

combine = cv2.bitwise_and(img_zero,im_floodfill)
bit_and = cv2.bitwise_not(combine,gray_foreground)


com_edge_bin = cv2.bitwise_and(bit_and,subtraction)
chanel3bin = cv2.cvtColor(im_floodfill,cv2.COLOR_GRAY2RGB)
mask = cv2.bitwise_and(img_fore,chanel3bin)
edge_canny = cv2.Canny(mask, 240,255)

im2, contours, hierarchy = cv2.findContours(morp_dilasi4, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#draw = cv2.drawContours(img_fore, contours, -1, (0,255,0), 3)
contoursList = len(contours)
vehicle = vehicleInit.vehicle
for i in range(0, contoursList):
    cnt = contours[i]
    M = cv2.moments(cnt)
    area = cv2.contourArea(cnt)

    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])

    area = cv2.contourArea(cnt)

    x,y,w,h = cv2.boundingRect(cnt)
    font = cv2.FONT_HERSHEY_PLAIN
    #cv2.putText(img_fore, "{0}".format(i+1), (x+2, y-4), font, 1, (255, 255, 0), 2)

    cv2.rectangle(img_fore,(x,y),(x+w,y+h),(255,255,0),2)
    cv2.circle(img_fore,(cx,cy),3,255,-1)
    listVehicleDetected.append(vehicle(i, cx, cy, None, None, None,  None, None, None, None, True))

templist = listVehicleDetected

#dist = [[0 for i in range(templist.__len__())] for j in range(listVehicleDetected.__len__())]
#if templist.__len__() != listVehicleDetected.__len__()

dist = np.zeros((templist.__len__(), listVehicleDetected.__len__()))

for i in range(templist.__len__()):
    x1 = templist[i].xCoordinate
    y1 = templist[i].yCoordinate
    for j in range(listVehicleDetected.__len__()):
        x2 = listVehicleDetected[j].xCoordinate
        y2 = listVehicleDetected[j].yCoordinate
        dist[i][j] = mo.distancetwoPoint(x1, y1, x2, y2)
    cv2.putText(img_fore, "{0}".format(templist[i].vehicleID + 1), (x1 + 2, y1 - 4), font, 1, (255, 255, 0), 2)

hungarian = Munkres()
indexes = hungarian.compute(dist)
total = 0
for row, column in indexes:
    value = dist[row][column]
    total += value
    listVehicleDetected[row].vehicleID = templist[column].vehicleID
    print '(%d, %d) -> %d' % (row, column, value)
print 'total cost: %d' % total

for i in range(listVehicleDetected.__len__()):
    x1 = listVehicleDetected[i].xCoordinate
    y1 = listVehicleDetected[i].yCoordinate
    cv2.putText(img_fore, "{0}".format(listVehicleDetected[i].vehicleID + 1), (x1 + 10, y1 - 20), font, 1, (255, 255, 0),2)

cv2.imshow("edge", img_fore)
cv2.waitKey(0)
cv2.destroyAllWindows()

