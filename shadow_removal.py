import cv2
import numpy as np

def hsvPassShadowRemoval(src, shadowThreshold):
    blurLevel = 3
    height, width = src.shape[:2]
    imgHSV = cv2.cvtColor(src, cv2.COLOR_RGB2HSV)
    gaussianBlur = cv2.GaussianBlur(imgHSV, (blurLevel, blurLevel), 0)
    hueImg, satImg, valImg = cv2.split(gaussianBlur)

    NSVDI = np.zeros((height, width, 1), np.uint8)
    count = height * width
    with np.errstate(divide='ignore'):
        # for i in range(0, height):
        #    for j in range(0, width):
        #       sat = int(satImg[i, j])
        #       val = int(valImg[i, j])
        #       NSVDI[i, j] = (satImg[i, j] - valImg[i, j]) / ((satImg[i, j] + valImg[i, j]) * 1.0)
        NSVDI = (satImg + valImg) / ((satImg - valImg) * 1)
    thresh = np.sum(NSVDI)
    avg = thresh / (count * 1.0)

    # for i in range(0, height):
    #    for j in range(0, width):
    #       if NSVDI[i, j] >= 0.25:
    #           hueImg[i, j] = 255
    #           satImg[i, j] = 255
    #           valImg[i, j] = 255
    #       else:
    #           hueImg[i, j] = 0
    #           satImg[i, j] = 0
    #           valImg[i, j] = 0

    if shadowThreshold is None:
        avg = avg
    else:
        avg = shadowThreshold

    np.where(NSVDI > avg, 255, 0)
    _, threshold = cv2.threshold(NSVDI, avg, 255, cv2.THRESH_BINARY_INV)

    output = threshold
    return output

def yuvPassShadowRemoval(src, shadowThreshold):
    height, width = src.shape[:2]
    imgYUV = cv2.cvtColor(src, cv2.COLOR_RGB2YUV)
    yImg, uImg, vImg = cv2.split(imgYUV)

    # for i in range(0, height):
    #   for j in range(0, width):
    #       yImg[i, j] = 0
    yImg = np.zeros((height, width, 1), np.uint8)
    imgYUV = cv2.merge([yImg, uImg, vImg])

    rgbImg = cv2.cvtColor(imgYUV, cv2.COLOR_YUV2RGB)
    rImg, gImg, bImg = cv2.split(rgbImg)

    count = width * height
    avg = np.sum(bImg)
    avg /= count * 1.0
    # for i in range(0, height):
    #    for j in range(0, width):
    #        if bImg[i, j] > ave:
    #           rImg[i, j] = 255
    #           gImg[i, j] = 255
    #           bImg[i, j] = 255
    #        else:
    #           rImg[i, j] = 0
    #           gImg[i, j] = 0
    #           bImg[i, j] = 0

    if shadowThreshold is None:
        avg = avg
    else:
        avg = shadowThreshold

    np.where(bImg > avg, 255, 0)
    _, threshold = cv2.threshold(bImg, avg, 255, cv2.THRESH_BINARY)

    output = threshold
    return output