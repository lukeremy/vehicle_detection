import cv2
import numpy as np
import math

def resize(frame, width, height):
    frame = cv2.resize(frame, (width, height))
    return frame

def addText(frame, text, size, x, y):
    font = cv2.FONT_HERSHEY_PLAIN
    cv2.putText(frame, "{0}".format(text), (x, y), font, size, (255, 255, 0), 1)

def cvtBGR2RGB(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame

def cvtRGB2GRAY(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    return frame

def cvtRGB2HSV(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    return frame

def cvtGRAY2RGB(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
    return frame

def initBackgrounSubtraction(real_time, start_time, init_time):
    if real_time < start_time + init_time:
        # print "initiation background subtraction"
        return False
    else:
        # print "background subtraction found"
        return True

def morphOpening(bin_frame, kernel, iteration):
    for iteration in range(0, iteration):
        bin_frame = cv2.erode(bin_frame, kernel)
        bin_frame = cv2.dilate(bin_frame, kernel)
    return bin_frame

def morphClosing(bin_frame, kernel, iteration):
    for iteration in range(1, iteration):
        bin_frame = cv2.dilate(bin_frame, kernel)
        bin_frame = cv2.erode(bin_frame, kernel)
    return bin_frame

def pinholeModel(W, f, H, theta, x1, x2):
    # W : jumlah baris (piksel)
    # f -> |A'B| : focal length (piksel)
    # H -> |O'O| : tinggi kamera (m)
    # theta : sudut kemiringan kamera (derajat)
    # x1' : indeks piksel terdepan kendaraan
    # x2' : indeks piksel terbelakang kendaraan
    # Lx1 -> |O'X1| : jarak titik terdepan kendaraan dengan kamera (m)
    # Lx2 -> |O'X2| : jarak titik blindspot belakang kendaraan (m)
    # X2G -> |X2G| : jarak belakang kendaraan dengan titik blindspot belakang kendaraan (m)
    maxhighLV = 1.6
    maxhighHV = 4.0
    maxlengthLV = 6.0

    delta1 = math.degrees(math.atan(math.fabs(x1 - (W / 2)) / f))
    delta2 = math.degrees(math.atan(math.fabs(x2 - (W / 2)) / f))

    if x1 >= W / 2:
        Lx1 = H * math.tan(math.radians(theta + delta1))
    else:
        Lx1 = H * math.tan(math.radians(theta - delta1))

    if x2 >= W / 2:
        Lx2 = H * math.tan(math.radians(theta + delta2))
    else:
        Lx2 = H * math.tan(math.radians(theta - delta2))

    Lv = Lx1 - Lx2

    if Lv <= maxlengthLV:
        estimationVehicleHigh = maxhighLV
    else:
        estimationVehicleHigh = maxhighHV

    if x2 >= W / 2:
        X2G = estimationVehicleHigh * math.tan(math.radians(theta + delta2))
    else:
        X2G = estimationVehicleHigh * math.tan(math.radians(theta - delta2))

    Lv = Lx1 - (Lx2 + X2G)
    delta1 = round(delta1, 3)
    delta2 = round(delta2, 3)
    Lx1 = round(Lx1, 4)
    Lx2 = round(Lx2, 4)
    X2G = round(X2G, 4)

    Lv = round(Lv, 2)
    # print "delta1: {0} | delta2: {1} | Lx1: {2} | Lx2: {3} | X2G: {4} | Lv: {5}".format(delta1, delta2, Lx1, Lx2, X2G, Lv)
    return Lv

def shadowRemoval(RGB_frame, Bin_frame):
    x = 5

def contourDetection(PrimRGB_frame, Binary_frame):
    color = (0, 255, 0)
    thick = 3
    height = 540
    high = 7
    width = 960
    fov_w = 90
    theta = 20
    focal = ((width / 2) / math.tan(math.radians(fov_w / 2)))
    fov_h = math.degrees(math.atan((height / 2) / focal))

    im2, contours, hierarchy = cv2.findContours(Binary_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # draw = cv2.drawContours(PrimRGB_frame, contours, -1, color, thick)

    contourList = len(contours)

    for i in range(0, contourList):
        cnt = contours[i]
        M = cv2.moments(cnt)
        # print M

        #cx = int(M['m10'] / M['m00'])
        #cy = int(M['m01'] / M['m00'])

        x, y, w, h = cv2.boundingRect(cnt)
        centeroidX = (x + (x + w)) / 2
        centeroidY = (y + (y + h)) / 2
        lengthVehicle = pinholeModel(height, focal, high, theta, (y+h), y)
        if (w >= 100) & (w < 200):

            cv2.rectangle(PrimRGB_frame, (x + w, y + h), (x, y), color, thick)
            cv2.line(PrimRGB_frame, (centeroidX, centeroidY), (centeroidX, centeroidY), (0, 0, 255), thick)
            addText(PrimRGB_frame, lengthVehicle, 1, x, (y-3))
            #x, y, w, h = 0
    return PrimRGB_frame

def initCounting(registX1, registY1, registX2, registY2, centeroidX, centeroidY, clasification):
    if ((centeroidX >= registX1) & (centeroidX <= registX2)) & ((centeroidY >= registY1) & (centeroidY <= registY2)):
        return clasification

def backgroundSubtractionAverage(frame_ori, avg, alpha):
    accuWeight = cv2.accumulateWeighted(frame_ori, avg, alpha)
    cvtScaleAbs = cv2.convertScaleAbs(accuWeight)
    return cvtScaleAbs

def croppingImage(frame, x1, y1, x2, y2, filename):
    crop = frame[y1:y2, x1:x2]  #y1:y+h, x:x+w
    cv2.imwrite("{0}.jpg".format(filename), crop)

def backgroundSubtractionMoG(frame):
    initMOG2 = cv2.createBackgroundSubtractorMOG2()
    MOG2_frame = initMOG2.apply(frame)
    return MOG2_frame

def funcY_line(x1, y1, x2, y2, centeroidX):
    m = (y1 -y2) / (x1 - x2)
    y = ((m * centeroidX) - (m * x1)) + y1
    y = round(y)
    return y
