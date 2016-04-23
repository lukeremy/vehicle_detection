import cv2
import numpy as np
import vehicle_tracking as proc
import time

from PyQt4 import QtGui, QtCore
from PyQt4 import uic
from cv2 import ocl
ocl.setUseOpenCL(False)
# set flag OCL to False if you build OPENCV -D WITH_OPENCL=ON


# Global variable
video_frame = uic.loadUiType("gtk/video_frame.ui")[0]

# init variable
start_time = None
width = 960     # pixel
height = 540    # pixel
alpha = 20      # second /fps (fps 30) -> 24/30 = 0.8 -> 8 second
mask_status = False
mask_frame = None
frame = 0

# background subtraction
# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
initMog = cv2.createBackgroundSubtractorMOG2()

class QtCapture(QtGui.QFrame, video_frame):
    def __init__(self, fps, filename):
        global avg
        super(QtGui.QFrame, self).__init__()

        self.fps = fps
        self.setupUi(self)

        # Start Capture Video
        self.cap = cv2.VideoCapture(filename)

        # Initiation to moving average
        _, frame = self.cap.read()
        frame = proc.convBGR2RGB(frame)
        frame = cv2.resize(frame, (width, height))
        avg = np.float32(frame)

    def setFPS(self, fps):
        self.fps = fps

    def initSetting(self):
        print "load Setting"

    def start(self):
        global start_time
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.nextFrame)
        self.timer.start(1000. / self.fps)
        start_time = time.time()
        print format(start_time)
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
        ret, frame_ori = self.cap.read()
        frame += 1

        # ---------- Do not disturb this source code ---------- #
        # Default color model is BGR format
        frame_resize = cv2.resize(frame_ori, (width, height))
        rgb_frame = proc.convBGR2RGB(frame_resize)
        # ----------------------------------------------------- #

        # Initiation background subtraction
        # ------------------------------------------------------#

        # Moving Average subtraction
        acuWeight = cv2.accumulateWeighted(rgb_frame, avg, 0.01)
        initSubtrack = cv2.convertScaleAbs(acuWeight)               # return rgb color for background subtraction
        initBackground = proc.initBackgrounSubtraction(real_time, start_time, alpha)
        if not mask_status:
            if not initBackground:
                print "initiation background subtraction"
            else:
                print "mask found"
                mask_frame = initSubtrack
                mask_status = True
            subtract_frame = initSubtrack
            cv2.imwrite("samples/foreground.jpg", frame_ori)
        else:
            print "mask frame"
            subtract_frame = mask_frame

        # Mixture of Gaussian subtraction
        mog_frame = initMog.apply(rgb_frame)

        # Mask
        #bs_mask = cv2.morphologyEx(mog_frame, cv2.MORPH_OPEN, proc.kernel())

        # ------------------------------------------------------#
        # Image processing
        #gray_frame = proc.convRGB2GRAY(subtract_frame)

        # Add frame rate text
        #proc.addText(gray_frame, "frame: {0}".format(frame), 1, 850, 525)

        # Last variable to show must 'show_frame'
        show_frame = initSubtrack

        colorSpace = True
        # True for RGB, HSV, LAB, and other 3 channel color space
        # False for Grayscale and binary

        # ---------- Do not disturb this source code ----------- #
        # Gray scale, binary image - Format_Indexed8
        # RGB image - Format_RGB888
        if colorSpace:
            img = QtGui.QImage(show_frame, show_frame.shape[1], show_frame.shape[0], QtGui.QImage.Format_RGB888)
        else:
            img = QtGui.QImage(show_frame, show_frame.shape[1], show_frame.shape[0], QtGui.QImage.Format_Indexed8)
        pix = QtGui.QPixmap.fromImage(img)
        self.video_frame.setPixmap(pix)
        # ------------------------------------------------------ #
