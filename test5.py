import ShadowRemoval
import cv2
import numpy
import os

img_path = raw_input("Please Enter Image Path: ")
assert os.path.exists(img_path), "img_path does not exists"

filename = "samples/LV1.jpg"
img = cv2.imread(img_path)
# Processing Image
res, val = ShadowRemoval.process(img)
print "{0}% of this image is shaded".format(int(100*val))
# Display Images
ShadowRemoval.scripts.display("img", img)
ShadowRemoval.scripts.display("res", res)
cv2.waitKey(0)

