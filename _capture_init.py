import cv2
import numpy as np
import image_processing as improc
import math_operation as mo
import time
import datetime
import os

from PyQt4 import QtGui, QtCore
from PyQt4 import uic
from cv2 import ocl

ocl.setUseOpenCL(False)  # set flag OCL to False if you build OPENCV -D WITH_OPENCL=ON

# Global variable
video_frame = uic.loadUiType("gtk/video_frame.ui")[0]

# init variable
start_time = None
width_frame = 960  # pixel
height_frame = 540  # pixel
init_time = 12  # second /fps (fps 30) -> 24/30 = 0.8 -> 8 second
mask_status = False
mask_frame = None
frame = 0
total_LV = 0
total_HV = 0
initMOG2 = cv2.createBackgroundSubtractorMOG2()  # Mixture of Gaussian initialization
initMOG = cv2.bgsegm.createBackgroundSubtractorMOG()

class QtCapture(QtGui.QFrame, video_frame):
    def setVideoMode(self, video_mode):
        self.video_mode = video_mode

    def getVideoMode(self):
        return self.video_mode

    def setBackgroundSubtraction(self, backgroundSubtraction):
        self.backgroundSubtracion = backgroundSubtraction

    def getBackgroundSubtraction(self):
        return self.backgroundSubtracion

    def setBoundary(self, boundary):
        self.boundary = boundary

    def getBoundary(self):
        return self.boundary

    def setROI(self, roi):
        self.roi = roi

    def getROI(self):
        return self.roi

    def setFPS(self, fps):
        self.fps = fps

    def getFPS(self):
        return self.fps

    def setAlt(self, alt):
        self.alt = alt

    def getAlt(self):
        return self.alt

    def setElevated(self, elevated):
        self.elevated = elevated

    def getElevated(self):
        return self.elevated

    def setFocal(self, focal):
        self.focal = focal

    def getFocal(self):
        return self.focal

    def setFOV(self, fov):
        self.fov = fov

    def getFOV(self):
        return self.fov

    def setLengthLV(self, lenghtLV):
        self.lengthLV = lenghtLV

    def getLengthLV(self):
        return self.lengthLV

    def setWidthLV(self, widthLV):
        self.widthLV = widthLV

    def getWidthLV(self):
        return self.widthLV

    def setHighLV(self, highLV):
        self.highLV = highLV

    def getHighLV(self):
        return self.highLV

    def setLengthHV(self, lenghtHV):
        self.lengthHV = lenghtHV

    def getLengthHV(self):
        return self.lengthHV

    def setWidthHV(self, widthHV):
        self.widthHV = widthHV

    def getWidthHV(self):
        return self.widthHV

    def setHighHV(self, highHV):
        self.highHV = highHV

    def getHighHV(self):
        return self.highHV

    def setDetectionLine(self, x1, y1, x2, y2):
        self.detectX1 = int(x1)
        self.detectY1 = int(y1)
        self.detectX2 = int(x2)
        self.detectY2 = int(y2)

    def getDetectionLine(self):
        return self.detectX1, self.detectY1, self.detectX2, self.detectY2

    def setRegistrationLine(self, x1, y1, x2, y2):
        self.registX1 = int(x1)
        self.registY1 = int(y1)
        self.registX2 = int(x2)
        self.registY2 = int(y2)

    def getRegistrationLine(self):
        return self.registX1, self.registY1, self.registX2, self.registY2

    def __init__(self, filename):
        global avg
        super(QtGui.QFrame, self).__init__()
        self.setupUi(self)

        # Start Capture Video
        self.cap = cv2.VideoCapture(filename)

        # Initiation file
        now = datetime.datetime.now()
        formatDate = now.strftime("%d-%m-%Y %H-%M")
        self.file = open("output/{0}.csv".format(formatDate), "a")
        if os.stat("output/{0}.csv".format(formatDate)).st_size == 0:
            self.file.write("No,Waktu,Jenis Kendaraan,Panjang,Lebar, Gambar\n")

        # Initiation folder
        path = "output"
        self.formatFolder = now.strftime("{0}/%d-%m-%Y %H-%M").format(path)
        if not os.path.isdir(self.formatFolder):
            os.makedirs(self.formatFolder)

        # Initiation to moving average
        _, PrimImg_frame = self.cap.read()
        PrimImg_frame = improc.cvtBGR2RGB(PrimImg_frame)
        PrimImg_frame = cv2.resize(PrimImg_frame, (width_frame, height_frame))
        avg = np.float32(PrimImg_frame)

    def start(self):
        global start_time
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.nextFrame)
        self.timer.start(1000. / self.getFPS())
        start_time = time.time()

        return start_time

    def stop(self):
        self.timer.stop()

    def deleteLater(self):
        global frame, total_HV, total_LV
        frame = 0
        # Stop capture
        self.cap.release()

        # Close opening file
        self.file.write("FOV:" + "," + str(self.getFOV()) + "\n" +
                        "Focal:" + "," + str(self.getFocal()) + "\n" +
                        "Angle:" + "," + str(self.getElevated()) + "\n" +
                        "Altitude:" + "," + str(self.getAlt()) + "\n" +
                        "Total LV:" + "," + str(total_LV) + "\n" +
                        "Total HV:" + "," + str(total_HV) + "\n" +
                        "Total Vehicle:" + "," + str(total_HV + total_LV) + "\n")
        self.file.flush()
        self.file.close()

        total_HV = 0
        total_LV = 0

        super(QtGui.QFrame, self).deleteLater()

    def nextFrame(self):
        global mask_status, mask_frame, frame, total_HV, total_LV
        real_time = time.time()
        ret, PrimImg_frame = self.cap.read()
        frame += 1

        # ----------- Do not disturb this source code ---------- #
        # Default color model is BGR format
        PrimResize_frame = cv2.resize(PrimImg_frame, (width_frame, height_frame))
        PrimRGB_frame = improc.cvtBGR2RGB(PrimResize_frame)

        # ------ [1] Initiation background subtraction ----------#
        # Initial State (IS)   : RGB - primary frame
        # Final State (FS)     : Binary - foreground frame
        if self.getBackgroundSubtraction() == "MA":  # if choose Moving Average

            # Moving Average subtraction
            cvtScaleAbs = improc.backgroundSubtractionAverage(PrimRGB_frame, avg, 0.01)
            movingAverage_frame = cvtScaleAbs
            initBackground = improc.initBackgrounSubtraction(real_time, start_time, init_time)

            if not mask_status:
                if not initBackground:
                    subtract_frame = movingAverage_frame
                else:
                    mask_frame = movingAverage_frame
                    mask_status = True
            else:
                subtract_frame = mask_frame

        else:  # If choose Mixture of Gaussian
            # Mixture of Gaussian Model Background Subtraction
            MOG_frame = initMOG.apply(PrimRGB_frame)

        # --- [x] Convert to Different Color Space ----------------#
        # IS    :
        # FS    :
        if self.getBackgroundSubtraction() == "MA":
            PrimGray_frame = improc.cvtRGB2GRAY(PrimRGB_frame)
            BackgroundGray_frame = improc.cvtRGB2GRAY(movingAverage_frame)

            PrimHSV_frame = cv2.cvtColor(PrimRGB_frame, cv2.COLOR_RGB2HSV)
            BackgroundHSV_frame = cv2.cvtColor(movingAverage_frame, cv2.COLOR_RGB2HSV)

            PrimLAB_frame = cv2.cvtColor(PrimRGB_frame, cv2.COLOR_RGB2LAB)
            BackgroundLAB_frame = cv2.cvtColor(movingAverage_frame, cv2.COLOR_RGB2LAB)

            PrimHue, PrimSat, PrimVal = cv2.split(PrimHSV_frame)
            BackHue, BackSat, BackVal = cv2.split(BackgroundHSV_frame)

            PrimLight, PrimA, PrimB = cv2.split(PrimLAB_frame)
            BackLight, BackA, BackB = cv2.split(BackgroundLAB_frame)

        # -- [x] Background Extraction ---------------------------#
        # IS    :
        # FS
        if self.getBackgroundSubtraction() == "MA":
            ImgDiffRGB = cv2.absdiff(PrimGray_frame, BackgroundGray_frame)
            ImgDiffHSV = cv2.absdiff(PrimVal, BackVal)
            ImgDiffLAB = cv2.absdiff(PrimLight, BackLight)

            combineRGBHSV = cv2.bitwise_or(ImgDiffRGB, ImgDiffHSV)
            combineLABHSV = cv2.bitwise_or(ImgDiffLAB, ImgDiffHSV)

            # -- [x] Smoothing and Noise Reduction --------------------#
            # IS    :
            # FS    :
            blurLevel = 21
            gaussianBlur_frame = cv2.GaussianBlur(combineRGBHSV, (blurLevel, blurLevel), 0)

            # -- [x] Thresholds to Binary ----------------------------#
            # IS    :
            # FS    :
            thresholdLevel = 30
            #_, threshold = cv2.threshold(combineRGBHSV, thresholdLevel, 255, cv2.THRESH_OTSU)
            _, threshold = cv2.threshold(gaussianBlur_frame, thresholdLevel, 255, cv2.THRESH_BINARY)
        else:  # Mixture of Gaussian
            _, threshold = cv2.threshold(MOG_frame, 100, 255, cv2.THRESH_OTSU)

        bin_frame = threshold.copy()
        # -- [x] Draw Detection and RegistrationLine -------------#
        # IS    :
        # FS    :
        thick = 2
        detectLine_color = (255, 0, 0)
        registLine_color = (0, 0, 255)

        detectX1, detectY1, detectX2, detectY2 = self.getDetectionLine()
        registX1, registY1, registX2, registY2 = self.getRegistrationLine()

        if self.getROI():
            cv2.line(PrimRGB_frame, (detectX1, detectY1), (detectX2, detectY2), detectLine_color, thick)
            cv2.line(PrimRGB_frame, (registX1, registY1), (registX2, registY2), registLine_color, thick)

        # -- [x] Draw information text ---------------------------#
        # IS    :
        # FS    :
        size = 0.6
        font = cv2.FONT_HERSHEY_DUPLEX
        LV_color = (255, 0, 0)
        Hv_color = (0, 0, 255)
        Frame_color = (255, 255, 255)

        cv2.putText(PrimRGB_frame, "Frame : {0}".format(frame), (800, 20), font, 0.5, Frame_color, 1)
        cv2.putText(PrimRGB_frame, "Light Vehicle  : {0}".format(total_LV), (10, 500), font, size, LV_color, 1)
        cv2.putText(PrimRGB_frame, "Heavy Vehicle : {0}".format(total_HV), (10, 520), font, size, Hv_color, 1)

        # -- [x] Morphological Operation -------------------------#
        # IS    : ~
        # FS    : ~
        kernel = np.array([
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0]], dtype=np.uint8)

        morph_frame = cv2.erode(bin_frame, kernel, iterations=1)
        morph_frame = cv2.dilate(morph_frame, kernel, iterations=2)
        morph_frame = cv2.erode(morph_frame, kernel, iterations=2)

        kernel = np.array([
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1]], dtype=np.uint8)

        morph_frame = cv2.erode(morph_frame, kernel, iterations=2)
        morph_frame = cv2.dilate(morph_frame, kernel, iterations=2)
        morph_frame = cv2.erode(morph_frame, kernel, iterations=1)
        morph_frame = cv2.dilate(morph_frame, kernel, iterations=2)

        # -- [x] Mask Boundary ROI ------------------------------#
        # IS    : ~
        # FS    : ~
        color = (255, 255, 0)
        roiThreshold = 10

        ImgZero_frame = np.zeros((height_frame, width_frame), np.uint8)
        x1ROI = mo.funcX_line(detectX1, detectY1, registX1, registY1, 0)
        x2ROI = mo.funcX_line(detectX2, detectY2, registX2, registY2, 0)
        x3ROI = mo.funcX_line(detectX1, detectY1, registX1, registY1, height_frame)
        x4ROI = mo.funcX_line(detectX2, detectY2, registX2, registY2, height_frame)

        pts = np.array([
            [x1ROI - roiThreshold, 0], [x2ROI + roiThreshold, 0],
            [x4ROI + roiThreshold, height_frame], [x3ROI - roiThreshold, height_frame]])

        cv2.fillPoly(ImgZero_frame, [pts], color)

        roiBinary_frame = cv2.bitwise_and(ImgZero_frame, bin_frame)

        # -- [x] Mask RGB Frame and Binary Frame ----------------#
        # IS    : ~
        # FS    : ~
        ThreeChanelBinary_frame = improc.cvtGRAY2RGB(threshold)
        maskRGBandBin_frame = cv2.bitwise_and(PrimRGB_frame, ThreeChanelBinary_frame)
        Canny_EdgeDetection = cv2.Canny(maskRGBandBin_frame, 100, 150)

        # -- [x] Contour Detection ------------------------------#
        # IS    :
        # FS    :

        image, contours, hierarchy = cv2.findContours(roiBinary_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        contoursList = len(contours)

        for i in range(0, contoursList):
            cnt = contours[i]
            areaContours = cv2.contourArea(cnt)
            xContour, yContour, widthContour, highContour = cv2.boundingRect(cnt)
            # Point A : (xContour, yContour)
            # Point B : (xContour + widthContour, yContour)
            # Point C : (xContour + widthContour, yContour + highContour)
            # Point D : (xContour, yContour + highContour)
            areaBoundary = widthContour * highContour

            # -- [x] Pin Hole Model -------------------------#
            # IS    :
            # FS    :
            fov = self.getFOV()
            focal = self.getFocal() * 3.779527559055
            theta = self.getElevated()
            altitude = self.getAlt()
            maxHighLV = self.getHighLV()
            maxHighHV = self.getHighHV()
            maxLengthLV = self.getLengthLV()
            maxLengthHV = self.getLengthHV()
            maxWidthHV = self.getWidthHV()

            x1Vehicle = (yContour + highContour)
            x2Vehicle = yContour

            if self.getFocal() == 0.0:
                horizontalFOV, verticalFOV = mo.transformDiagonalFOV(fov)
                focal = mo.getFocalfromFOV(height_frame, verticalFOV)

            lengthVehicle = mo.vertikalPinHoleModel(height_frame, focal, altitude, theta, x1Vehicle, x2Vehicle,
                                                    maxHighLV, maxHighHV, maxLengthLV)
            centerVehicle = mo.centeroidPinHoleMode(height_frame, focal, altitude, theta, (yContour + highContour))

            if self.getFocal() == 0.0:
                focal = mo.getFocalfromFOV(width_frame, horizontalFOV)

            widthVehicle = mo.horizontalPinHoleModel(width_frame, focal, altitude, xContour, (xContour + widthContour), centerVehicle)

            # -- [x] Vehicle Classification -------------#
            # IS    :
            # FS    :
            if lengthVehicle <= maxLengthLV:
                classification = "LV"
            else:
                classification = "HV"

            # -- [x] Draw Boundary --------------------------#
            # IS    :
            # FS    :
            colorLV = (0, 255, 0)
            colorHV = (0, 0, 255)
            thick = 3
            size = 2
            areaThreshold = 40

            if (widthVehicle >= 2.0) and (widthVehicle <= 10.0) and \
                    (lengthVehicle >= 1.5) and (lengthVehicle < maxLengthHV) and \
                    (areaContours >= (float(areaBoundary) * (float(areaThreshold) / 100))):
                # Get moment for centroid
                Moment = cv2.moments(cnt)
                xCentroid = int(Moment['m10'] / Moment['m00'])
                yCentroid = int(Moment['m01'] / Moment['m00'])

                if classification == "LV":
                    color = colorLV
                else:
                    color = colorHV

                if self.getBoundary():
                    cv2.rectangle(PrimRGB_frame, (xContour + widthContour, yContour + highContour),
                                  (xContour, yContour), color, thick)
                    cv2.circle(PrimRGB_frame, (xCentroid, yCentroid), size, (0, 0, 255), thick)
                    improc.addText(PrimRGB_frame, lengthVehicle, size, xContour, (yContour - 3))

                # -- [x] Counting Detection -----------------#
                # IS    :
                # FS    :
                stopGap = 20
                changeRegistLine_color = (255, 255, 255)
                changeThick = 4

                yPredict = mo.funcY_line(registX1, registY1, registX2, registY2, xCentroid)
                countClass = improc.initCounting(registX1, registY1, registX2, registX2, xCentroid, yPredict,
                                                 classification)

                if (yCentroid >= yPredict) and (yCentroid < yPredict + stopGap) and (xCentroid >= registX1) and (xCentroid <= registX2):
                    if countClass == "LV":
                        total_LV += 1
                    elif countClass == "HV":
                        total_HV += 1

                    cv2.line(PrimRGB_frame, (registX1, registY1), (registX2, registY2), changeRegistLine_color, changeThick)
                    print "Total LV: {0} | Total HV: {1} | class: {2} length: {3} width: {4}".format(total_LV, total_HV, countClass, lengthVehicle, widthVehicle)

                    # -- [x] Crop Image -------------------------#
                    # IS    :
                    # FS    :
                    now = datetime.datetime.now()
                    formatDate = now.strftime("%d%m%Y_%H%M%S")

                    formatFileName = "{0}/{1}_{2:03}_{3}.jpg".format(self.formatFolder, countClass, (total_LV + total_HV), formatDate)
                    cropping_frame = PrimResize_frame[yContour:yContour + highContour, xContour:xContour + widthContour]
                    cv2.imwrite(formatFileName, cropping_frame)

                    # -- [x] Save Filename to Text --------------#
                    # IS    :
                    # FS    :
                    formatDate = now.strftime("%d:%m:%Y %H:%M:%S")
                    self.file.write(str(total_LV + total_HV) + "," +
                                    str(formatDate) + "," +
                                    str(countClass) + "," +
                                    str(lengthVehicle) + "," +
                                    str(widthVehicle) + "," +
                                    str(formatFileName) + "\n")
                    self.file.flush()

        # ---------- Do not disturb this source code ----------- #
        if self.getVideoMode() == "RGB":
            show_frame = PrimRGB_frame
            img = QtGui.QImage(show_frame, show_frame.shape[1], show_frame.shape[0], QtGui.QImage.Format_RGB888)
            # RGB image - Format_RGB888
        else:
            show_frame = bin_frame
            img = QtGui.QImage(show_frame, show_frame.shape[1], show_frame.shape[0], QtGui.QImage.Format_Indexed8)
            # Gray scale, binary image - Format_Indexed8

        pix = QtGui.QPixmap.fromImage(img)
        self.video_frame.setPixmap(pix)
