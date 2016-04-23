import cv2
import numpy as np
import math

def resize(frame, width, height):
    frame = cv2.resize(frame, (width, height))
    return frame

def addText(frame, text, size, x, y):
    font = cv2.FONT_HERSHEY_PLAIN
    cv2.putText(frame, "{0}".format(text), (x, y), font, size, (255, 255, 0), 1)

def convBGR2RGB(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame

def convRGB2GRAY(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    return frame

def convRGB2HSV(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    return frame

def initBackgrounSubtraction(real_time, start_time, alpha):
    if real_time < start_time + alpha:
        # print "initiation background subtraction"
        return False
    else:
        # print "background subtraction found"
        return True

def morfOpening(bin_frame, kernel, iteration):
    for iteration in range(1, iteration):
        bin_frame = cv2.erode(bin_frame, kernel)
        bin_frame = cv2.dilate(bin_frame, kernel)
    return bin_frame

def morfClosing(bin_frame, kernel, iteration):
    for iteration in range(1, iteration):
        bin_frame = cv2.dilate(bin_frame, kernel)
        bin_frame = cv2.erode(bin_frame, kernel)
    return bin_frame

def kernel():
    kernel = np.array([
        [0, 0, 0],
        [1, 1, 1],
        [0, 0, 0]], dtype=np.uint8)
    return kernel

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
    estimationVehicleHigh = 0

    delta1 = math.atan((x1 - W) / 2 * f)
    delta2 = math.atan((x2 - W) / 2 * f)

    if x1 >= W/2:
        Lx1 = H * math.tan(theta + delta1)
    else:
        Lx1 = H * math.tan(theta - delta1)

    if x2 >= W/2:
        Lx2 = H * math.tan(theta + delta2)
        X2G = estimationVehicleHigh * math.tan(theta + delta2)
    else:
        Lx2 = H * math.tan(theta - delta2)
        X2G = estimationVehicleHigh * math.tan(theta + delta2)

    Lv = Lx1 - (Lx2 + X2G)
    return Lv
