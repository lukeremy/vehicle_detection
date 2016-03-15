import cv2

img1 = cv2.imread("samples/enigma1.jpg")
img2 = cv2.imread("samples/enigma2.jpg")
img3 = cv2.imread("samples/enigma3.jpg")
img4 = cv2.imread("samples/enigma4.jpg")

# mask
mask1 = (img1/2 + img2/2)
mask2 = (mask1/2 + img3/2)
mask3 = (mask2/2 + img4/2)

mk1 = (img1 + img2)/2
mk2 = (mk1 + img3)/2
mk3 = (mk2 + img4)/2
#img2=cv2.imread(pict1,2)
#gray1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
img3 = (img1/2 + img4/2)

gray1= cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
gray2= cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
subtrack = gray2 - gray1

m1 = cv2.addWeighted(img1,0.5,img2,0.5,0)
m2 = cv2.addWeighted(m1, 0.5, img3, 0.5,0)
m3 = cv2.addWeighted(m2, 0.5, img4, 0.5,0)

frame = cv2.resize(m3, (600, 400))
fram2 = cv2.resize(subtrack, (600, 400))
cv2.imshow('frame',subtrack)
#cv2.imshow('frame2',fram2)


cv2.waitKey(0)

cv2.destroyAllWindows()
