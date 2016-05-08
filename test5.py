import cv2
import numpy as np

file_mask = "samples/background2.jpg"
file_foreground = "samples/frameori2.jpg"
file_mog = "samples/test_mog.jpg"

img_back = cv2.imread(file_mask)
img_fore = cv2.imread(file_foreground)
img_mog = cv2.imread(file_mog)
img_back = cv2.resize(img_back, (960,540))
img_fore = cv2.resize(img_fore, (960,540))

kernel = np.ones((5,5),np.float32)/25

gray_background = cv2.cvtColor(img_back, cv2.COLOR_RGB2GRAY)
gray_foreground = cv2.cvtColor(img_fore, cv2.COLOR_RGB2GRAY)


#cv2.imwrite("samples/grayforeground.jpg", gray_foreground)

#gray_foreground = cv2.blur(gray_foreground, (5,5))
#gray_background = cv2.blur(gray_background,(5,5))
# Background subtraction
abssub = (gray_background*2)-(gray_foreground*2)
subtraction = cv2.absdiff(gray_foreground,gray_background)

# Threshold
_,threshold = cv2.threshold(subtraction, 100,255,cv2.THRESH_OTSU)

# Filing hole
im_floodfill = threshold.copy()
h, w = subtraction.shape[:2]
mask = np.zeros((h+2, w+2), np.uint8)

# Shadow Removal


# Inverse Binary
cv2.floodFill(threshold,mask, (0,0),255)
im_floodfill_inv = cv2.bitwise_not(im_floodfill)
temp_floodfill = im_floodfill
# Build RoI
img_zero = np.zeros((540, 960), np.uint8)
pts = np.array([[385,220],[50,465],[1040,465],[705,220]])

#cv2.polylines(temp_floodfill,[pts],True,(255,255,0),thickness=1)
cv2.fillPoly(img_zero,[pts],(255,255,0))
# Morphology
kernel = np.ones((3,3),np.uint8)

morp_erosi = cv2.erode(im_floodfill,kernel,iterations=1)
morp_dilasi = cv2.dilate(morp_erosi, kernel, iterations=1)
morp_erosi = cv2.erode(morp_dilasi,kernel,iterations=1)
morp_dilasi = cv2.dilate(morp_erosi, kernel, iterations=1)
morp_dilasi = cv2.dilate(morp_dilasi, kernel, iterations=1)
morp_dilasi = cv2.dilate(morp_dilasi, kernel, iterations=1)

combine = cv2.bitwise_and(img_zero,im_floodfill)
bit_and = cv2.bitwise_not(combine,gray_foreground)


com_edge_bin = cv2.bitwise_and(bit_and,subtraction)
chanel3bin = cv2.cvtColor(im_floodfill,cv2.COLOR_GRAY2RGB)
mask = cv2.bitwise_and(img_fore,chanel3bin)
edge_canny = cv2.Canny(mask, 100,150)

im2, contours, hierarchy = cv2.findContours(morp_dilasi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
draw = cv2.drawContours(img_fore, contours, -1, (0,255,0), 3)

cnt = contours[0]
M = cv2.moments(cnt)

print M
cx = int(M['m10']/M['m00'])
cy = int(M['m01']/M['m00'])

print cx
print cy

#areas = [cv2.contourArea(c) for c in contours]
#max_index = np.argmax(areas)
#cnt=contours[max_index]

x,y,w,h = cv2.boundingRect(cnt)
cv2.rectangle(img_fore,(x,y),(x+w,y+h),(255,255,0),2)


#print M
#x,y,w,h = cv2.boundingRect(contours)
#cv2.rectangle(img_fore,(x,y),(x+w,y+h),(0,255,0),2)

cv2.imshow("edge", img_fore)
#cv2.imshow("binary", morp_dilasi)

cv2.waitKey(0)
cv2.destroyAllWindows()

