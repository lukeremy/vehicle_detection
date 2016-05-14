import cv2
import numpy as np
import image_processing as improc
import math_operation as mo
import _main_init as mi
import time
import math

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
        self.boudary = boundary

    def getBoundary(self):
        return self.boudary

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
        return self.getWidthHV()

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

        # Initiation to moving average
        _, PrimImg_frame = self.cap.read()
        PrimImg_frame = improc.cvtBGR2RGB(PrimImg_frame)
        PrimImg_frame = cv2.resize(PrimImg_frame, (width_frame, height_frame))
        avg = np.float32(PrimImg_frame)

    def initSetting(self):
        print "load Setting"

    def start(self):
        global start_time, label_fps
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.nextFrame)
        self.timer.start(1000. / self.getFPS())
        start_time = time.time()

        return start_time

    def stop(self):
        self.timer.stop()

    def deleteLater(self):
        global frame
        frame = 0

        self.cap.release()
        super(QtGui.QFrame, self).deleteLater()

    def nextFrame(self):
        global mask_status, mask_frame, frame
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
                    #print "mask found"
            else:
                subtract_frame = mask_frame
                #print "get background"

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

        # -- [x] Smoothing and Noise Reduction --------------------#
        # IS    :
        # FS    :

        # -- [x] Background Extraction ---------------------------#
        # IS    :
        # FS
        if self.getBackgroundSubtraction() == "MA":
            ImgDiffRGB = cv2.absdiff(PrimGray_frame, BackgroundGray_frame)
            ImgDiffHSV = cv2.absdiff(PrimVal, BackVal)
            ImgDiffLAB = cv2.absdiff(PrimLight, BackLight)

            combineRGBHSV = cv2.bitwise_or(ImgDiffRGB, ImgDiffHSV)
            combineLABHSV = cv2.bitwise_or(ImgDiffLAB, ImgDiffHSV)

        # -- [x] Thresholds to Binary ----------------------------#
        # IS    :
        # FS    :
        if self.getBackgroundSubtraction() == 'MA':  # Moving Averages
            _, threshold = cv2.threshold(combineRGBHSV, 100, 255, cv2.THRESH_OTSU)
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
        total_LV = 0
        total_HV = 0

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

        ImgZero_frame = np.zeros((height_frame, width_frame), np.uint8)
        x1ROI = mo.funcX_line(detectX1, detectY1, registX1, registY1, 0)
        x2ROI = mo.funcX_line(detectX2, detectY2, registX2, registY2, 0)
        x3ROI = mo.funcX_line(detectX1, detectY1, registX1, registY1, height_frame)
        x4ROI = mo.funcX_line(detectX2, detectY2, registX2, registY2, height_frame)

        pts = np.array([
            [x1ROI - 10, 0], [x2ROI + 10, 0],
            [x4ROI + 10, height_frame], [x3ROI - 10, height_frame]])

        cv2.fillPoly(ImgZero_frame, [pts], color)

        roiBinary_frame = cv2.bitwise_and(ImgZero_frame, bin_frame)

        # -- [x] Mask RGB Frame and Binary Frame ----------------#
        # IS    : ~
        # FS    : ~
        ThreeChanelBinary_frame = improc.cvtGRAY2RGB(threshold)
        maskRGBandBin_frame = cv2.bitwise_and(PrimRGB_frame, ThreeChanelBinary_frame)
        Canny_EdgeDetection = cv2.Canny(maskRGBandBin_frame, 100, 150)

        # -- [x] Shadow Detection and Removal -------------------#
        # IS    : ~
        # FS    : ~

        # -- [x] Contour Detection ------------------------------#
        # IS    :
        # FS    :

        if self.getBoundary():
            image, contours, hierarchy = cv2.findContours(roiBinary_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            contoursList = len(contours)

            for i in range(0, contoursList):
                cnt = contours[i]

                xContour, yContour, widthContour, highContour = cv2.boundingRect(cnt)
                xCenteroid = (xContour + (xContour + widthContour)) / 2
                yCenteroid = (yContour + (yContour + highContour)) / 2

                # -- [x] Pin Hole Model -------------------------#
                # IS    :
                # FS    :
                fov_w = self.getFOV()
                focal = self.getFocal()
                theta = self.getElevated()
                altitude = self.getAlt()
                maxHighLV = self.getHighLV()
                maxHighHV = self.getHighHV()
                maxLengthLV = self.getLengthLV()

                x1Vehicle = (yContour + highContour)
                x2Vehicle = yContour

                if focal == 0:
                    focal = mo.getFocalfromFOV(width_frame, fov_w)
                    fov_h = math.degrees(math.atan((height_frame / 2) / focal))

                lengthVehicle = mo.vertikalPinHoleModel(height_frame, focal, altitude, theta, x1Vehicle, x2Vehicle,
                                                        maxHighLV, maxHighHV, maxLengthLV)

                # -- [x] Draw Boundary --------------------------#
                # IS    :
                # FS    :
                color = (0, 255, 0)
                thick = 3
                size = 2

                if (widthContour >= 100) & (widthContour < 200):
                    cv2.rectangle(PrimRGB_frame, (xContour + widthContour, yContour + highContour),
                                  (xContour, yContour), color, thick)
                    cv2.line(PrimRGB_frame, (xCenteroid, yCenteroid), (xCenteroid, yCenteroid), (0, 0, 255), thick)
                    improc.addText(PrimRGB_frame, lengthVehicle, size, xContour, (yContour - 3))
                    # -- [x] Vehicle Classification -------------#
                    # IS    :
                    # FS    :
                    if lengthVehicle <= maxLengthLV:
                        classification = "LV"
                    else:
                        classification = "HV"
                    # -- [x] Counting Detection -----------------#
                    # IS    :
                    # FS    :
                    # LV_count = self.getLabelLV()
                    # HV_count = self.getLabelHV()
                    yPredict = mo.funcY_line(registX1, registY1, registX2, registY2, xCenteroid)
                    countClass = improc.initCounting(registX1, registY1, registX2, registX2, xCenteroid, yPredict,
                                                     classification)

                    # -- [x] Crop Image -------------------------#
                    # IS    :
                    # FS    :

                    #filename = "test{0}.jpg".format(i)
                    #cropping_frame = PrimRGB_frame[yContour:yContour + highContour, xContour:xContour + widthContour]
                    #cv2.imwrite(filename, cropping_frame)

        # ---------- Do not disturb this source code ----------- #
        if self.getVideoMode() == "RGB":
            show_frame = PrimRGB_frame
            img = QtGui.QImage(show_frame, show_frame.shape[1], show_frame.shape[0], QtGui.QImage.Format_RGB888)
            # RGB image - Format_RGB888
        else:
            show_frame = roiBinary_frame
            img = QtGui.QImage(show_frame, show_frame.shape[1], show_frame.shape[0], QtGui.QImage.Format_Indexed8)
            # Gray scale, binary image - Format_Indexed8

        pix = QtGui.QPixmap.fromImage(img)
        self.video_frame.setPixmap(pix)
