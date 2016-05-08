import cv2
import numpy as np
import vehicle_tracking as proc
import _main_init as mi
import time

from PyQt4 import QtGui, QtCore
from PyQt4 import uic
from cv2 import ocl
ocl.setUseOpenCL(False)         # set flag OCL to False if you build OPENCV -D WITH_OPENCL=ON


# Global variable
video_frame = uic.loadUiType("gtk/video_frame.ui")[0]
# init variable
start_time = None
width = 960     # pixel
height = 540    # pixel
init_time = 3      # second /fps (fps 30) -> 24/30 = 0.8 -> 8 second
mask_status = False
mask_frame = None
frame = 0
initMOG2 = cv2.createBackgroundSubtractorMOG2()      # Mixture of Gaussian initialization
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

    def getLabelFPS(self):
        return 10

    def getLabelLV(self):
        return 80

    def getLabelHV(self):
        return 190

    def __init__(self, filename):
        global avg
        super(QtGui.QFrame, self).__init__()
        self.setupUi(self)

        # Start Capture Video
        self.cap = cv2.VideoCapture(filename)

        # Initiation to moving average
        _, PrimImg_frame = self.cap.read()
        PrimImg_frame = proc.cvtBGR2RGB(PrimImg_frame)
        PrimImg_frame = cv2.resize(PrimImg_frame, (width, height))
        avg = np.float32(PrimImg_frame)

    def initSetting(self):
        print "load Setting"

    def start(self):
        global start_time
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.nextFrame)
        self.timer.start(1000. / self.getFPS())
        start_time = time.time()

        #print format(start_time)
        #print format(self.alt)
        #print format(self.focal)
        #print format(self.elevated)
        #print format(self.fps)

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
        PrimResize_frame = cv2.resize(PrimImg_frame, (width, height))
        PrimRGB_frame = proc.cvtBGR2RGB(PrimResize_frame)

        # ------ [1] Initiation background subtraction ----------#
        # IS    : RGB - primary frame
        # FS    : Binary - foreground frame
        if self.getBackgroundSubtraction() == "MA":  # if choose Moving Average

            # Moving Average subtraction
            cvtScaleAbs = proc.backgroundSubtractionAverage(PrimRGB_frame, avg, 0.01)
            movingAverage_frame = cvtScaleAbs

            initBackground = proc.initBackgrounSubtraction(real_time, start_time, init_time)
            if not mask_status:
                if not initBackground:
                    print "initiation background subtraction"
                else:
                    print "mask found"
                    mask_frame = cvtScaleAbs
                    mask_status = True
                subtract_frame = cvtScaleAbs
            else:
                print "mask frame"
                subtract_frame = mask_frame

            # Convert RGB to Grayscale
            PrimGray_frame = proc.cvtRGB2GRAY(PrimRGB_frame)
            BackgroundGray_frame = proc.cvtRGB2GRAY(movingAverage_frame)

            # Background Extraction
            ImgDiff = cv2.absdiff(PrimGray_frame, BackgroundGray_frame)

            # Threshold
            _, threshold = cv2.threshold(ImgDiff, 100, 255, cv2.THRESH_OTSU)
        else:  # If choose Mixture of Gaussian
            # Mixture of Gaussian Model Background Subtraction
            MOG_frame = initMOG.apply(PrimRGB_frame)
            _, threshold = cv2.threshold(MOG_frame, 100, 255, cv2.THRESH_OTSU)

        # ------------- [2] Morphological Operation -------------#
        # IS    : ~
        # FS    : ~
        kernel = np.array([
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1]], dtype=np.uint8)

        bin_frame = proc.morphClosing(threshold, kernel, 2)
        #bin_frame = cv2.erode(threshold, kernel)
        #bin_frame = cv2.dilate(bin_frame, kernel)

        # -------- [x] Mask RGB Frame and Binary Frame ----------#
        # IS    : ~
        # FS    : ~
        ThreeChanelBinary_frame = proc.cvtGRAY2RGB(threshold)
        maskRGBandBin_frame = cv2.bitwise_and(PrimRGB_frame, ThreeChanelBinary_frame)
        Canny_EdgeDetection = cv2.Canny(maskRGBandBin_frame, 100, 150)

        # ----------- [x] Shadow Detection and Removal ----------#
        # IS    : ~
        # FS    : ~

        # ---- [x] Draw Detection and RegistrationLine ----------#
        # IS    :
        # FS    :
        thick = 2
        detectLine_color = (255, 255, 255)
        registLine_color = (255, 0, 255)

        detectX1, detectY1, detectX2, detectY2 = self.getDetectionLine()
        registX1, registY1, registX2, registY2 = self.getRegistrationLine()

        cv2.line(PrimRGB_frame, (detectX1, detectY1), (detectX2, detectY2), detectLine_color, thick)
        cv2.line(PrimRGB_frame, (registX1, registY1), (registX2, registY2), registLine_color, thick)

        # ------------- [x] Contour Detection -------------------#
        # IS    :
        # FS    :

        PrimRGB_frame = proc.contourDetection(PrimRGB_frame, bin_frame)

        # ---------- Do not disturb this source code ----------- #
        if self.getVideoMode() == "RGB":
            show_frame = maskRGBandBin_frame
            img = QtGui.QImage(show_frame, show_frame.shape[1], show_frame.shape[0], QtGui.QImage.Format_RGB888)
            # RGB image - Format_RGB888
        else:
            show_frame = Canny_EdgeDetection
            img = QtGui.QImage(show_frame, show_frame.shape[1], show_frame.shape[0], QtGui.QImage.Format_Indexed8)
            # Gray scale, binary image - Format_Indexed8

        pix = QtGui.QPixmap.fromImage(img)
        self.video_frame.setPixmap(pix)